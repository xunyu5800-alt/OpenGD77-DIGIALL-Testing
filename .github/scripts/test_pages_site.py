"""Exercise release selection and fail-closed site preparation without the network."""
import hashlib
import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile
import urllib.error

import pages_site as site


def sha(data):
    return hashlib.sha256(data).hexdigest()


def zip_bytes(entries):
    out = io.BytesIO()
    with zipfile.ZipFile(out, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for name, data in entries.items():
            z.writestr(name, data)
    return out.getvalue()


class PagesTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.docs = self.root / 'docs'
        (self.docs / 'site-assets').mkdir(parents=True)
        (self.docs / 'index.html').write_text('<p class="version"><span></span> v1.0.0</p>'
            '<a href="https://github.com/' + site.REPO + '/releases/tag/v1.0.0">GitHub 发布页</a>', encoding='utf8')
        self.tag = 'v1.2.0-rc.18'
        self.source = '1' * 40
        self.files = {}
        packages = []
        artifacts = []
        for board in range(6):
            image = b'\xff' * 0xB1F2C
            stages = [dict(filename=f'{kind}{board}.bin', kind=kind, bytes=len(image), sha256=sha(image), c4fm_tx=kind == 'main')
                      for kind in ['font', 'pinyin', 'main']]
            package = dict(filename=f'board{board}.zip', model=f'Board {board}', origin='DIGIALL', version=self.tag,
                           board=str(board), stages=stages, firmware_source_commit=self.source)
            data = zip_bytes({**{s['filename']: image for s in stages},
                              'profile.json': json.dumps(dict(firmware_source_commit=self.source))})
            self.files[package['filename']] = data
            artifacts.append(dict(filename=package['filename'], bytes=len(data), sha256=sha(data)))
            packages.append(package)
        self.manifest = dict(tag=self.tag, source_commit=self.source, packages=packages, artifacts=artifacts)
        self.rehash()
        self.info = dict(tag_name=self.tag, draft=False, published_at='2026-11-20T00:00:00Z',
                         html_url='https://github.com/' + site.REPO + '/releases/tag/' + self.tag,
                         assets=[dict(name=n, browser_download_url=self.url(n)) for n in self.files])
        firmware = b'upstream'
        inner = zip_bytes({'fw.bin': firmware})
        outer = zip_bytes({'inner.zip': inner})
        self.upstream = dict(origin='OpenGD77', filename='reference.zip', inner='inner.zip', innerSha256=sha(inner),
                             firmware='fw.bin', firmwareSha256=sha(firmware), sha256=sha(outer),
                             url=f'https://github.com/{site.REPO}/releases/download/v1.2.0-rc.16/reference.zip')
        self.network = {self.url(n): b for n, b in self.files.items()}
        self.network[self.upstream['url']] = outer
        (self.docs / 'site-assets/catalog.json').write_text(json.dumps(dict(tag='v1.0.0', packages=[self.upstream])))

    def url(self, name):
        return f'https://github.com/{site.REPO}/releases/download/{self.tag}/{name}'

    def rehash(self):
        self.files['release_manifest.json'] = json.dumps(self.manifest).encode()
        self.files['SHA256SUMS.txt'] = ''.join(sha(b) + '  ' + n + '\n' for n, b in self.files.items()
                                              if n != 'SHA256SUMS.txt').encode()

    def build(self):
        return site.build(self.info, self.docs, self.root / 'output', self.network.__getitem__)

    def test_complete_native_and_upstream_site(self):
        receipt = self.build()
        self.assertEqual(len(receipt['packages']), 7)
        output = self.root / 'output'
        catalog = json.loads((output / 'site-assets/catalog.json').read_bytes())
        self.assertEqual(catalog['tag'], self.tag)
        for entry in catalog['packages']:
            self.assertEqual(sha((output / entry['url']).read_bytes()), entry['sha256'])
        self.assertIn(self.tag, (output / 'index.html').read_text(encoding='utf8'))
        self.assertIn('immutable', (output / '_headers').read_text())

    def test_corrupt_native_never_creates_output(self):
        self.network[self.url('board0.zip')] += b'corrupt'
        with self.assertRaisesRegex(ValueError, 'SHA-256 mismatch'):
            self.build()
        self.assertFalse((self.root / 'output').exists())

    def test_corrupt_upstream_never_creates_output(self):
        self.network[self.upstream['url']] += b'corrupt'
        with self.assertRaisesRegex(ValueError, 'SHA-256 mismatch'):
            self.build()
        self.assertFalse((self.root / 'output').exists())

    def test_missing_native_asset_fails(self):
        self.info['assets'] = [a for a in self.info['assets'] if a['name'] != 'board1.zip']
        with self.assertRaises(KeyError):
            self.build()

    def test_existing_output_is_preserved(self):
        output = self.root / 'output'
        output.mkdir()
        (output / 'original').write_text('keep')
        with self.assertRaisesRegex(ValueError, 'already exists'):
            self.build()
        self.assertEqual((output / 'original').read_text(), 'keep')

    def test_bad_inner_firmware_even_with_valid_zip_hash(self):
        package = self.manifest['packages'][0]
        bad = b'\0' * 0xB1F2C
        package['stages'][0]['sha256'] = sha(bad)
        entries = {'profile.json': json.dumps(dict(firmware_source_commit=self.source))}
        for stage in package['stages']:
            entries[stage['filename']] = bad if stage['kind'] == 'font' else b'\xff' * 0xB1F2C
        data = zip_bytes(entries)
        self.files['board0.zip'] = data
        self.manifest['artifacts'][0].update(bytes=len(data), sha256=sha(data))
        self.rehash()
        self.network.update({self.url(n): b for n, b in self.files.items()})
        with self.assertRaisesRegex(ValueError, 'donor area'):
            self.build()

    def test_wrong_package_provenance_fails(self):
        self.manifest['packages'][0]['firmware_source_commit'] = '2' * 40
        self.rehash()
        self.network.update({self.url(n): b for n, b in self.files.items()})
        with self.assertRaisesRegex(ValueError, 'provenance mismatch'):
            self.build()

    def test_newest_includes_rc_and_excludes_tool_and_draft(self):
        stable = dict(self.info, tag_name='v1.1.0', published_at='2026-11-19T00:00:00Z')
        tool = dict(self.info, tag_name='flash-wizard-v9.0.0', published_at='2026-11-21T00:00:00Z')
        draft = dict(self.info, tag_name='v9.0.0', draft=True, published_at='2026-11-21T00:00:00Z')
        with patch.object(site, 'github', return_value=[stable, self.info, tool, draft]):
            self.assertEqual(site.release()['tag_name'], self.tag)

    def test_explicit_rollback_supported_but_draft_rejected(self):
        with patch.object(site, 'github', return_value=self.info):
            self.assertEqual(site.release(self.tag)['tag_name'], self.tag)
        with patch.object(site, 'github', return_value=dict(self.info, draft=True)):
            with self.assertRaisesRegex(ValueError, 'not published'):
                site.release(self.tag)

    def test_external_asset_url_rejected(self):
        self.info['assets'][0]['browser_download_url'] = 'https://example.org/board0.zip'
        with self.assertRaisesRegex(ValueError, 'Unexpected release asset URL'):
            self.build()

    def test_missing_credentials_identify_the_missing_secret(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(ValueError, 'CLOUDFLARE_ACCOUNT_ID is missing'):
                site.project()
        with patch.dict(os.environ, {'CLOUDFLARE_ACCOUNT_ID': 'a' * 32}, clear=True):
            with self.assertRaisesRegex(ValueError, 'CLOUDFLARE_API_TOKEN is missing'):
                site.project()

    def test_cloudflare_error_reports_code_without_reflected_secrets(self):
        token = 'private-test-token-sentinel'
        error = urllib.error.HTTPError('https://api.cloudflare.com/', 403, 'Forbidden', {},
            io.BytesIO(json.dumps({'errors': [{'code': 10000, 'message': token}]}).encode()))
        with patch.dict(os.environ, {'CLOUDFLARE_ACCOUNT_ID': 'a' * 32, 'CLOUDFLARE_API_TOKEN': token}, clear=True):
            with patch.object(site, 'get', side_effect=error):
                with self.assertRaises(ValueError) as caught:
                    site.project()
        self.assertIn('HTTP 403; error codes [10000]', str(caught.exception))
        self.assertNotIn(token, str(caught.exception))

    def test_project_emits_only_the_verified_production_branch(self):
        output = self.root / 'github-output'
        env = dict(CLOUDFLARE_ACCOUNT_ID='a' * 32, CLOUDFLARE_API_TOKEN='private-test-token', GITHUB_OUTPUT=str(output))
        response = dict(success=True, result=dict(subdomain='opengd77-digiall.pages.dev', production_branch='production'))
        with patch.dict(os.environ, env, clear=True), patch.object(site, 'get', return_value=json.dumps(response).encode()):
            site.project()
        self.assertEqual(output.read_text(), 'branch=production\n')

    def test_surrounding_secret_whitespace_is_normalized_for_wrangler(self):
        output = self.root / 'github-output'
        environment = self.root / 'github-env'
        token = 'private-test-token'
        env = dict(CLOUDFLARE_ACCOUNT_ID=' ' + 'a' * 32 + '\n', CLOUDFLARE_API_TOKEN='\r\n' + token + ' ',
                   GITHUB_OUTPUT=str(output), GITHUB_ENV=str(environment), GITHUB_ACTIONS='true')
        response = dict(success=True, result=dict(subdomain='opengd77-digiall.pages.dev', production_branch='main'))
        captured = io.StringIO()
        with patch.dict(os.environ, env, clear=True), patch.object(site, 'get', return_value=json.dumps(response).encode()) as get:
            with contextlib.redirect_stdout(captured):
                site.project()
            self.assertEqual(get.call_args.kwargs['token'], token)
        self.assertIn('PAGES_API_TOKEN=' + token + '\n', environment.read_text())
        self.assertIn('::add-mask::' + token, captured.getvalue())

    def test_internal_token_whitespace_needs_a_correct_secret(self):
        env = dict(CLOUDFLARE_ACCOUNT_ID='a' * 32, CLOUDFLARE_API_TOKEN='two words')
        with patch.dict(os.environ, env, clear=True), patch.object(site, 'get') as get:
            with self.assertRaisesRegex(ValueError, 'whitespace inside'):
                site.project()
            get.assert_not_called()


if __name__ == '__main__':
    unittest.main()
