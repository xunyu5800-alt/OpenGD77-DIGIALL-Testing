"""Publish the verified DM1701-only test package, without private sources."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

TAG = 'v1.2.0-rc.21-test'
SOURCE = '3fe0438ab43a1eac4301dfdf5cc81db1872337a7'
ROOT = Path(__file__).resolve().parents[2]
REF = 'refs/notes/releases-' + TAG


def run(*args):
    return subprocess.check_output(args, cwd=ROOT, text=True).strip()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def state():
    url = json.loads(run('gh', 'release', 'view', TAG, '--json', 'apiUrl'))['apiUrl']
    return json.loads(run('gh', 'api', url))


def verify():
    folder = ROOT / '_release' / TAG
    assets = sorted(folder.iterdir(), key=lambda p: p.name)
    assert len(assets) == 4 and all(p.is_file() for p in assets)
    expected = {}
    for line in (folder / 'SHA256SUMS.txt').read_text().splitlines():
        value, name = line.split('  ', 1)
        assert Path(name).name == name and name not in expected
        expected[name] = value
        assert sha((folder / name).read_bytes()) == value, name
    assert sorted(expected) == sorted(p.name for p in assets if p.name != 'SHA256SUMS.txt')
    # Dedicated manifest name keeps this one-board test out of the six-board
    # production catalog selector, which requires release_manifest.json.
    manifest = json.loads((folder / 'test_release_manifest.json').read_bytes())
    assert manifest['tag'] == TAG and manifest['source_commit'] == SOURCE
    assert manifest['scope'] == 'dm1701-main-upgrade-test' and manifest['target'] == 'dm1701'
    assert manifest['hardware_verified'] is False
    assert manifest['firmware_sha256'] == '84e0a3d636b07491ac32dea0c502ce5ab811675316cc2091f5cb8e630b586312'
    for asset in manifest['artifacts']:
        assert sha((folder / asset['filename']).read_bytes()) == asset['sha256']
    archive = folder / manifest['package']
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for line in z.read('SHA256SUMS.txt').decode().splitlines():
            value, name = line.split('  ', 1)
            assert sha(z.read(name)) == value, name
        bins = [n for n in z.namelist() if n.lower().endswith('.bin')]
        assert bins == [manifest['firmware']]
        assert all(Path(n).suffix.lower() not in ('.c', '.h', '.a', '.elf') for n in z.namelist())
        data = z.read(bins[0])
        metadata = json.loads(z.read('build-metadata.json'))
        checks = json.loads(z.read('validation.json'))
        assert metadata['target'] == 'dm1701' and metadata['source_commit'] == SOURCE
        assert metadata['source_dirty'] is False and metadata['version'] == TAG[1:]
        assert len(data) == metadata['size'] and sha(data) == metadata['sha256'] == manifest['firmware_sha256']
        start, size = metadata['codec_offset'], metadata['codec_size']
        assert data[start:start + size] == b'\xff' * size
        assert checks['source_commit'] == checks['sk1_followup_tests_source_commit'] == SOURCE
        assert checks['hardware_verified'] is False and checks['host_tests_exit_code'] == 0
        assert all(code == 0 for code in checks['sk1_followup_tests'].values())
        assert all(code == 0 for code in checks['build_exit_codes'].values())
    return assets, manifest


def publish():
    assert os.environ.get('GITHUB_ACTIONS') == 'true'
    assert os.environ['GH_REPO'] == 'xunyu5800-alt/OpenGD77-DIGIALL-Testing'
    assets, manifest = verify()
    commit = os.environ['GITHUB_SHA']
    notes = ROOT / 'docs/releases' / (TAG + '.txt')
    title = notes.read_text(encoding='utf8').splitlines()[0]
    existing = subprocess.run(['gh', 'release', 'view', TAG, '--json', 'apiUrl'], text=True, capture_output=True)
    if existing.returncode == 0:
        release = state()
        assert release['draft'], 'Published releases are immutable'
        old = run('git', 'ls-remote', 'origin', 'refs/tags/' + TAG)
        assert not old or old.split()[0] == commit, 'Existing tag cannot move'
        run('gh', 'release', 'edit', TAG, '--target', commit, '--title', title, '--notes-file', str(notes), '--prerelease')
        run('gh', 'release', 'upload', TAG, '--clobber', *map(str, assets))
    else:
        assert '404' in existing.stderr or 'release not found' in existing.stderr.lower(), existing.stderr
        run('gh', 'release', 'create', TAG, '--target', commit, '--title', title, '--notes-file', str(notes), '--draft', '--prerelease', *map(str, assets))
    release = state()
    assert release['draft'] and release['target_commitish'] == commit
    assert sorted(a['name'] for a in release['assets']) == [p.name for p in assets]
    with tempfile.TemporaryDirectory() as directory:
        run('gh', 'release', 'download', TAG, '--dir', directory)
        for p in assets:
            assert sha(p.read_bytes()) == sha((Path(directory) / p.name).read_bytes()), p.name
    head = run('git', 'ls-remote', 'origin', 'refs/heads/codex/publish-' + TAG)
    assert head and head.split()[0] == commit, 'A newer package superseded this run'
    run('gh', 'release', 'edit', TAG, '--draft=false', '--prerelease', '--latest=false')
    release = state()
    assert not release['draft'] and release['prerelease'] and release['target_commitish'] == commit
    receipt = dict(status='success', tag=TAG, url=release['html_url'], public_commit=commit,
                   firmware_source_commit=manifest['source_commit'],
                   assets=[dict(name=p.name, bytes=p.stat().st_size, sha256=sha(p.read_bytes())) for p in assets])
    (ROOT / 'published-rc21-test.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(receipt['url'])


def status():
    commit = os.environ['GITHUB_SHA']
    receipt = dict(status=os.environ.get('JOB_STATUS', 'failure'), source_commit=commit, tag=TAG,
                   run_url=f'https://github.com/{os.environ["GITHUB_REPOSITORY"]}/actions/runs/{os.environ["GITHUB_RUN_ID"]}')
    file = ROOT / 'published-rc21-test.json'
    if file.is_file():
        receipt['release'] = json.loads(file.read_text())
    log = ROOT / 'publish-rc21-test.log'
    if receipt['status'] != 'success' and log.is_file():
        receipt['log_tail'] = log.read_text(errors='replace').splitlines()[-30:]
    old = run('git', 'ls-remote', 'origin', REF)
    if old:
        run('git', 'fetch', 'origin', REF + ':' + REF)
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / 'receipt.json'
        path.write_text(json.dumps(receipt, indent=2) + '\n')
        run('git', '-c', 'user.name=github-actions[bot]', '-c', 'user.email=41898282+github-actions[bot]@users.noreply.github.com',
            'notes', '--ref=' + REF, 'add', '-f', '-F', str(path), commit)
    run('git', 'push', 'origin', REF)
    print(json.dumps(receipt))


if __name__ == '__main__':
    if sys.argv[1:] == ['verify']:
        assets, manifest = verify()
        print('Verified DM1701 test package, firmware provenance and all asset hashes')
    elif sys.argv[1:] == ['publish']:
        publish()
    elif sys.argv[1:] == ['status']:
        status()
    else:
        raise SystemExit('publish_rc21_test.py verify|publish|status')
