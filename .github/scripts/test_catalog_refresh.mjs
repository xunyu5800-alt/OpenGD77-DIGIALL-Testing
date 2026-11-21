// Exercise the real page module as an already-open tab across a release.
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';

class Element {
  constructor() { this.children = []; this.events = {}; this.dataset = {}; this.value = ''; this.textContent = ''; this.content = {cloneNode: () => new Element()}; }
  addEventListener(name, callback) { this.events[name] = callback; }
  append(...children) { this.children.push(...children); }
  replaceChildren(...children) { this.children = children; }
}
const elements = new Map();
const element = id => {
  if (!elements.has(id)) elements.set(id, new Element());
  return elements.get(id);
};
const windowEvents = {}, documentEvents = {}, intervals = [];
globalThis.document = {
  getElementById: element, createElement: () => new Element(), visibilityState: 'visible',
  addEventListener: (name, fn) => { documentEvents[name] = fn; },
};
globalThis.window = {
  addEventListener: (name, fn) => { windowEvents[name] = fn; },
  setInterval: (fn, ms) => { intervals.push({fn, ms}); },
};
globalThis.Option = class extends Element {
  constructor(label, value) { super(); this.textContent = label; this.value = value; }
};
const release = version => ({tag: version, packages: [{
  filename: `DIGIALL_${version}_DM1701.zip`, model: 'Baofeng DM-1701', board: 'DM1701',
  origin: 'DIGIALL', platform: 'STM32', version, sha256: 'a'.repeat(64),
  c4fmTx: false,
  url: `downloads/${version}/DIGIALL_${version}_DM1701.zip`,
}]});
let incoming = release('v1.2.0-rc.17'), fail = false;
const requests = [];
globalThis.fetch = async (url, options) => {
  requests.push({url: String(url), options});
  if (fail) throw new Error('offline');
  return {ok: true, json: async () => incoming};
};
let source = await readFile(new URL('../../docs/site-assets/site.js', import.meta.url), 'utf8');
assert.ok(source.startsWith("import {inspectDfu, prepareFirmware} from './firmware.mjs';"));
source = source.replace(/^import .*?;\r?\n/, 'const inspectDfu = () => {}; const prepareFirmware = () => {};\n')
  .replaceAll('import.meta.url', "'https://digiall.iot-c.com/site-assets/site.js'");
await import('data:text/javascript;base64,' + Buffer.from(source).toString('base64'));
const model = element('model');
model.value = incoming.packages[0].filename;
model.events.change();
assert.match(element('download-zip').href, /rc\.17/);
assert.match(element('board-note').textContent, /FM／DMR 收发.*仅开放 C4FM DN 接收/);
element('files').append('previously prepared BIN');
element('zip').value = 'previous.zip';

incoming = release('v1.2.0-rc.18');
await windowEvents.focus();
assert.equal(model.value, incoming.packages[0].filename, 'preserve the radio across versions');
assert.match(element('download-zip').href, /rc\.18/);
assert.equal(element('firmware-version').textContent, incoming.tag);
assert.match(element('current-release-link').href, /rc\.18$/);
assert.equal(element('files').children.length, 0, 'discard files prepared for an older release');
assert.equal(element('zip').value, '');
assert.match(element('zip-status').textContent, /重新下载/);

element('files').append('current BIN');
element('zip').value = 'current.zip';
await windowEvents.pageshow();
assert.equal(element('files').children.length, 1, 'an unchanged check must preserve prepared files');
assert.equal(element('zip').value, 'current.zip');

incoming = release('v1.2.0-rc.17');
await element('check-release').events.click();
assert.match(element('download-zip').href, /rc\.18/, 'reject stale responses after a newer release');
assert.match(element('catalog-status').textContent, /收到旧目录/);
fail = true;
await documentEvents.visibilitychange();
assert.match(element('catalog-status').textContent, /检查失败.*rc\.18/);
assert.equal(element('check-release').disabled, false);
assert.equal(intervals[0].ms, 60000);
assert.ok(requests.every(r => r.options.cache === 'no-store'));
assert.ok(requests.slice(1).every(r => /catalog\.json\?check=\d+/.test(r.url)));
console.log('Catalog refresh passed: rc.17 → rc.18, preserved radio, cleared old BINs, ignored stale responses, retry enabled.');
