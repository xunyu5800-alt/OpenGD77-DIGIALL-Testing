"""Publish verified binary-only rc.19 assets; retain private-source provenance."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

TAG = 'v1.2.0-rc.19'
ROOT = Path(__file__).resolve().parents[2]
REF = 'refs/notes/releases-' + TAG


def run(*args):
    return subprocess.check_output(args,cwd=ROOT,text=True).strip()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def state():
    url=json.loads(run('gh','release','view',TAG,'--json','apiUrl'))['apiUrl']
    return json.loads(run('gh','api',url))


def publish():
    folder=ROOT/'_release'/TAG
    assets=sorted(folder.iterdir(),key=lambda p:p.name)
    assert len(assets)==10 and all(p.is_file() for p in assets)
    expected={}
    for line in (folder/'SHA256SUMS.txt').read_text().splitlines():
        value,name=line.split('  ',1)
        assert Path(name).name==name and name not in expected
        expected[name]=value
        assert digest(folder/name)==value,name
    assert sorted(expected)==sorted(p.name for p in assets if p.name!='SHA256SUMS.txt')
    manifest=json.loads((folder/'release_manifest.json').read_bytes())
    assert manifest['tag']==TAG and len(manifest['packages'])==6
    assert {p['target'] for p in manifest['packages']}=={'5w','10w-pd8','10w','rt3s','dm1701','rt84'}
    for package in manifest['packages']:
        assert [s['kind'] for s in package['stages']]==['font','pinyin','main']
        assert [s['c4fm_tx'] for s in package['stages']]==[False,False,True],package['board']
    for asset in manifest['artifacts']:
        assert digest(folder/asset['filename'])==asset['sha256']
    for path in assets:
        if path.suffix!='.zip':continue
        with zipfile.ZipFile(path) as z:
            assert z.testzip() is None
            for line in z.read('SHA256SUMS.txt').decode().splitlines():
                value,name=line.split('  ',1)
                assert hashlib.sha256(z.read(name)).hexdigest()==value,(path.name,name)
            if 'profile.json' in z.namelist():
                profile=json.loads(z.read('profile.json'))
                assert profile['firmware_source_commit']==manifest['source_commit']
                assert profile['stages'][-1]['c4fm_tx'] is True
    commit=os.environ['GITHUB_SHA']
    notes=ROOT/'docs/releases'/(TAG+'.md')
    title=notes.read_text(encoding='utf8').splitlines()[0].removeprefix('# ')
    existing=subprocess.run(['gh','release','view',TAG,'--json','apiUrl'],text=True,capture_output=True)
    if existing.returncode==0:
        release=state()
        assert release['draft'],'Published releases are immutable'
        old=run('git','ls-remote','origin','refs/tags/'+TAG)
        assert not old or old.split()[0]==commit,'Existing tag cannot move'
        run('gh','release','edit',TAG,'--target',commit,'--title',title,'--notes-file',str(notes),'--prerelease')
        run('gh','release','upload',TAG,'--clobber',*map(str,assets))
    else:
        assert '404' in existing.stderr or 'release not found' in existing.stderr.lower(),existing.stderr
        run('gh','release','create',TAG,'--target',commit,'--title',title,'--notes-file',str(notes),'--draft','--prerelease',*map(str,assets))
    release=state()
    assert release['draft'] and release['target_commitish']==commit
    assert sorted(a['name'] for a in release['assets'])==[p.name for p in assets]
    with tempfile.TemporaryDirectory() as destination:
        run('gh','release','download',TAG,'--dir',destination)
        for p in assets:assert digest(p)==digest(Path(destination)/p.name),p.name
    head=run('git','ls-remote','origin','refs/heads/codex/publish-'+TAG)
    assert head and head.split()[0]==commit,'A newer source superseded this run'
    run('gh','release','edit',TAG,'--draft=false','--prerelease','--latest=false')
    release=state()
    assert not release['draft'] and release['prerelease'] and release['target_commitish']==commit
    receipt=dict(status='success',tag=TAG,url=release['html_url'],documentation_commit=commit,
                 firmware_source_commit=manifest['source_commit'],
                 assets=[dict(name=p.name,bytes=p.stat().st_size,sha256=digest(p)) for p in assets])
    (ROOT/'published-rc19.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(receipt['url'])


def status():
    commit=os.environ['GITHUB_SHA']
    receipt=dict(status=os.environ.get('JOB_STATUS','failure'),source_commit=commit,tag=TAG,
                 run_url=f'https://github.com/{os.environ["GITHUB_REPOSITORY"]}/actions/runs/{os.environ["GITHUB_RUN_ID"]}')
    file=ROOT/'published-rc19.json'
    if file.is_file():receipt['release']=json.loads(file.read_text())
    log=ROOT/'publish-rc19.log'
    if receipt['status']!='success' and log.is_file():receipt['log_tail']=log.read_text(errors='replace').splitlines()[-30:]
    old=run('git','ls-remote','origin',REF)
    if old:run('git','fetch','origin',REF+':'+REF)
    with tempfile.TemporaryDirectory() as directory:
        path=Path(directory)/'receipt.json';path.write_text(json.dumps(receipt,indent=2)+'\n')
        run('git','-c','user.name=github-actions[bot]','-c','user.email=41898282+github-actions[bot]@users.noreply.github.com',
            'notes','--ref='+REF,'add','-f','-F',str(path),commit)
    run('git','push','origin',REF)
    print(json.dumps(receipt))


if __name__=='__main__':
    if sys.argv[1:]==['publish']:publish()
    elif sys.argv[1:]==['status']:status()
    else:raise SystemExit('publish_rc19.py publish|status')
