"""Build an atomic Pages site from published, hash-verified release assets."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[2]
REPO = 'xunyu5800-alt/OpenGD77-DIGIALL-Testing'
PROJECT = 'opengd77-digiall'
SITE = 'https://opengd77-digiall.pages.dev'
TAG = re.compile(r'v\d+\.\d+\.\d+(?:-[A-Za-z0-9.]+)?\Z')
SHA = re.compile(r'[0-9a-f]{64}\Z')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def get(url, *, token=None):
    headers = {'User-Agent': 'DIGIALL-Pages-release-sync'}
    if token:
        headers['Authorization'] = 'Bearer ' + token
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60) as response:
                data = response.read(32 * 1024 * 1024 + 1)
                require(len(data) <= 32 * 1024 * 1024, 'Download exceeds size limit')
                return data
        except (OSError, TimeoutError):
            if attempt == 2:
                raise
            time.sleep(2 * (attempt + 1))


def github(path):
    return json.loads(get('https://api.github.com/repos/' + REPO + path,
                          token=os.environ.get('GH_TOKEN')))


def release(tag=''):
    if tag:
        require(TAG.fullmatch(tag), 'Invalid firmware tag')
        result = github('/releases/tags/' + tag)
    else:
        # /releases/latest excludes prereleases: public tests must include rc tags.
        candidates = []
        page = 1
        while True:
            batch = github(f'/releases?per_page=100&page={page}')
            candidates.extend(r for r in batch if not r['draft'] and TAG.fullmatch(r['tag_name'])
                              and any(a['name'] == 'release_manifest.json' for a in r['assets']))
            if len(batch) < 100:
                break
            page += 1
        require(candidates, 'No published firmware release with manifest')
        result = max(candidates, key=lambda r: r['published_at'])
    require(not result['draft'] and TAG.fullmatch(result['tag_name']), 'Release is not published firmware')
    return result


def filename(name):
    require(isinstance(name, str) and re.fullmatch(r'[A-Za-z0-9_.-]+', name)
            and name not in ('.', '..'), 'Unsafe filename')
    return name


def checked(data, sha, label):
    require(isinstance(sha, str) and SHA.fullmatch(sha), 'Invalid SHA-256: ' + label)
    require(hashlib.sha256(data).hexdigest() == sha, 'SHA-256 mismatch: ' + label)
    return data


def archive(data):
    z = zipfile.ZipFile(io.BytesIO(data))
    names = z.namelist()
    require(len(names) == len(set(names)), 'Duplicate ZIP entries')
    require(sum(i.file_size for i in z.infolist()) < 64 * 1024 * 1024, 'ZIP exceeds expansion limit')
    require(z.testzip() is None, 'Corrupt ZIP')
    return z


def native_zip(data, package, source):
    with archive(data) as z:
        require(json.loads(z.read('profile.json'))['firmware_source_commit'] == source,
                'Package has different firmware source')
        require([s['kind'] for s in package['stages']] == ['font', 'pinyin', 'main'], 'Missing firmware stage')
        for stage in package['stages']:
            name = filename(stage['filename'])
            image = checked(z.read(name), stage['sha256'], name)
            require(len(image) == stage['bytes'] and len(image) >= 0xB1F2C, 'Firmware size mismatch')
            require(image[0x6937C:0xB1F2C] == b'\xff' * (0xB1F2C - 0x6937C),
                    'Firmware contains non-empty donor area')


def upstream_zip(data, package):
    with archive(data) as outer:
        inner = checked(outer.read(package['inner']), package['innerSha256'], package['inner'])
    with archive(inner) as z:
        checked(z.read(package['firmware']), package['firmwareSha256'], package['firmware'])


def build(info, docs, output, fetch=get):
    tag = info['tag_name']
    require(not info['draft'] and TAG.fullmatch(tag), 'Invalid published release')
    assets = {filename(a['name']): a for a in info['assets']}
    require(len(assets) == len(info['assets']), 'Duplicate release asset names')
    prefix = f'https://github.com/{REPO}/releases/download/{tag}/'

    def download(name):
        url = assets[filename(name)]['browser_download_url']
        require(url == prefix + name, 'Unexpected release asset URL')
        print('Verifying release asset: ' + name, flush=True)
        return fetch(url)

    sums = {}
    for line in download('SHA256SUMS.txt').decode().splitlines():
        sha, name = line.split('  ', 1)
        filename(name)
        require(SHA.fullmatch(sha) and name not in sums, 'Invalid checksum list')
        sums[name] = sha
    manifest_bytes = checked(download('release_manifest.json'), sums['release_manifest.json'], 'manifest')
    manifest = json.loads(manifest_bytes)
    require(manifest['tag'] == tag and re.fullmatch(r'[0-9a-f]{40}', manifest['source_commit']), 'Manifest provenance mismatch')
    packages = manifest['packages']
    require(len(packages) == 6 and len({p['board'] for p in packages}) == 6, 'Expected six distinct native boards')
    artifacts = {a['filename']: a for a in manifest['artifacts']}
    catalog = json.loads((docs / 'site-assets/catalog.json').read_bytes())
    entries = []
    blobs = {}
    for package in packages:
        name = filename(package['filename'])
        require(package['origin'] == 'DIGIALL' and package['version'] == tag
                and package['firmware_source_commit'] == manifest['source_commit'], 'Package provenance mismatch')
        require(artifacts[name]['sha256'] == sums[name], 'Manifest/checksum disagreement')
        data = checked(download(name), sums[name], name)
        require(len(data) == artifacts[name]['bytes'], 'Package size mismatch')
        native_zip(data, package, manifest['source_commit'])
        path = f'downloads/{tag}/{name}'
        blobs[path] = data
        entries.append(dict(model=package['model'], origin='DIGIALL', version=tag, filename=name,
                            sha256=sums[name], url=path, board=package['board'], platform='STM32',
                            stages=[{k: s[k] for k in ('filename', 'sha256', 'bytes')} for s in package['stages']],
                            c4fmTx=package['stages'][-1]['c4fm_tx']))
    for original in catalog['packages']:
        if original['origin'] == 'DIGIALL':
            continue
        entry = dict(original)
        name = filename(entry['filename'])
        url = entry['url']
        match = re.fullmatch(r'https://github.com/' + re.escape(REPO) + r'/releases/download/([^/]+)/' + re.escape(name), url)
        require(match and TAG.fullmatch(match[1]), 'Upstream package needs pinned GitHub release URL')
        print('Verifying pinned reference: ' + name, flush=True)
        data = checked(fetch(url), entry['sha256'], name)
        upstream_zip(data, entry)
        path = f'downloads/{match[1]}/{name}'
        blobs[path] = data
        entry['url'] = path
        entries.append(entry)
    # Construct in a new directory only after every download has passed validation.
    require(not output.exists(), 'Build output already exists; choose a fresh directory')
    require(output.resolve() != docs.resolve() and docs.resolve() not in output.resolve().parents,
            'Output cannot overwrite source docs')
    shutil.copytree(docs, output)
    for path, data in blobs.items():
        target = output / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    catalog = dict(tag=tag, packages=entries)
    (output / 'site-assets/catalog.json').write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
    index = output / 'index.html'
    html = index.read_text(encoding='utf8')
    # Only update the current firmware badge/link; keep explicitly older manuals and tools pinned.
    html = re.sub(r'(<p class="version"><span></span> )v[\w.-]+', lambda m: m[1] + tag, html)
    html = re.sub(r'(releases/tag/)v[\w.-]+(?=">GitHub 发布页)', lambda m: m[1] + tag, html)
    index.write_text(html, encoding='utf8')
    receipt = dict(tag=tag, release_url=info['html_url'], firmware_source_commit=manifest['source_commit'],
                   documentation_commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                   catalog_sha256=hashlib.sha256((output / 'site-assets/catalog.json').read_bytes()).hexdigest(),
                   packages=[dict(path=p, sha256=hashlib.sha256(b).hexdigest(), bytes=len(b)) for p, b in blobs.items()])
    (output / 'deployment-version.json').write_text(json.dumps(receipt, indent=2) + '\n')
    (output / '_headers').write_text('/\n  Cache-Control: no-cache\n/index.html\n  Cache-Control: no-cache\n'
        '/site-assets/*\n  Cache-Control: no-cache\n/deployment-version.json\n  Cache-Control: no-cache\n'
        '/downloads/*\n  Cache-Control: public, max-age=31536000, immutable\n')
    return receipt


def project():
    account = os.environ.get('CLOUDFLARE_ACCOUNT_ID', '')
    token = os.environ.get('CLOUDFLARE_API_TOKEN', '')
    require(account, 'CLOUDFLARE_ACCOUNT_ID is missing; add it as a repository Actions secret')
    require(re.fullmatch(r'[0-9a-f]{32}', account),
            'CLOUDFLARE_ACCOUNT_ID must be the 32-character account ID without whitespace')
    require(token, 'CLOUDFLARE_API_TOKEN is missing; add it as a repository Actions secret')
    require(token == token.strip() and not any(c.isspace() for c in token),
            'CLOUDFLARE_API_TOKEN contains whitespace; paste only the token value')
    try:
        result = json.loads(get(f'https://api.cloudflare.com/client/v4/accounts/{account}/pages/projects/{PROJECT}', token=token))
    except urllib.error.HTTPError as error:
        codes = []
        try:
            body = json.loads(error.read())
            codes = [entry['code'] for entry in body.get('errors', []) if isinstance(entry.get('code'), int)]
        except (ValueError, KeyError):
            pass
        raise ValueError(f'Cloudflare Pages project lookup returned HTTP {error.code}; error codes {codes}. '
                         'Check the token account and Account / Cloudflare Pages / Edit permission') from None
    require(result.get('success'), 'Cannot read the existing Cloudflare Pages project')
    require(result['result']['subdomain'] == PROJECT + '.pages.dev', 'Unexpected Cloudflare project')
    branch = result['result']['production_branch']
    require(re.fullmatch(r'[A-Za-z0-9_./-]+', branch or ''), 'Unsupported production branch name')
    with open(os.environ['GITHUB_OUTPUT'], 'a') as stream:
        stream.write('branch=' + branch + '\n')
    print('Verified existing Pages project and production branch')


def verify(output):
    expected = json.loads((output / 'deployment-version.json').read_bytes())
    # Deployment propagation is bounded; never report success from Wrangler exit status alone.
    for attempt in range(12):
        stamp = str(time.time_ns())
        try:
            actual = json.loads(get(SITE + '/deployment-version.json?verify=' + stamp))
        except (OSError, ValueError):
            actual = None
        if actual == expected:
            break
        if attempt == 11:
            raise ValueError('Production has not switched to the expected deployment')
        time.sleep(5)
    checked(get(SITE + '/site-assets/catalog.json?verify=' + stamp), expected['catalog_sha256'], 'live catalog')
    for package in expected['packages']:
        data = checked(get(SITE + '/' + package['path'] + '?verify=' + stamp), package['sha256'], package['path'])
        require(len(data) == package['bytes'], 'Live package size mismatch')
    print('Verified production catalog and all package bytes for ' + expected['tag'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['build', 'project', 'verify'])
    parser.add_argument('--tag', default='')
    parser.add_argument('--output', type=Path, default=ROOT / '.site-build')
    args = parser.parse_args()
    if args.command == 'build':
        result = build(release(args.tag), ROOT / 'docs', args.output)
        print('Prepared ' + result['tag'] + ': ' + str(len(result['packages'])) + ' verified packages')
    elif args.command == 'project':
        try:
            project()
        except ValueError as error:
            print('::error::' + str(error), flush=True)
            raise SystemExit(1)
    else:
        verify(args.output)
