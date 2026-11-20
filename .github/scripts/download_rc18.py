"""Fetch approved binary assets over HTTPS; the publisher verifies them again."""
import hashlib
import json
from pathlib import Path
import re
import time
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
TAG = 'v1.2.0-rc.18'
descriptor = json.loads((ROOT/'.github/release-inputs'/(TAG+'.json')).read_bytes())
base = urllib.parse.urlsplit(descriptor['base_url'])
assert base.scheme == 'https' and base.hostname.endswith('.opengd77-digiall.pages.dev')
assert not base.username and not base.password and not base.query and not base.fragment and base.path in ('','/')
assert descriptor['tag'] == TAG and len(descriptor['files']) == 10
directory = ROOT/'_release'/TAG
assert not directory.exists(), 'Use a fresh release download directory'
directory.mkdir(parents=True)
seen = set()
for entry in descriptor['files']:
    name = entry['filename']
    assert re.fullmatch(r'[A-Za-z0-9_.-]+',name) and name not in ('.','..') and name not in seen
    assert re.fullmatch(r'[0-9a-f]{64}',entry['sha256'])
    seen.add(name)
    for attempt in range(3):
        try:
            request = urllib.request.Request(descriptor['base_url'].rstrip('/')+'/'+name,
                                             headers={'User-Agent':'DIGIALL-release-publisher'})
            with urllib.request.urlopen(request,timeout=60) as response:
                data = response.read(16*1024*1024+1)
            break
        except OSError:
            if attempt == 2:
                raise
            time.sleep(3)
    assert len(data) == entry['bytes'] and hashlib.sha256(data).hexdigest() == entry['sha256'], name
    (directory/name).write_bytes(data)
    print('Verified HTTPS asset: '+name, flush=True)
manifest = json.loads((directory/'release_manifest.json').read_bytes())
assert manifest['tag'] == TAG and manifest['source_commit'] == descriptor['firmware_source_commit']
