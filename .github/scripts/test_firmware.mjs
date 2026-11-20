import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {prepareFirmware} from '../../docs/site-assets/firmware.mjs';

const sha = bytes => createHash('sha256').update(bytes).digest('hex');
function crc32(bytes) {
  let crc = 0xffffffff;
  for (const byte of bytes) {
    crc ^= byte;
    for (let bit = 0; bit < 8; bit++) crc = (crc >>> 1) ^ ((crc & 1) ? 0xedb88320 : 0);
  }
  return (crc ^ 0xffffffff) >>> 0;
}
function zip(entries) {
  const locals = [], central = [];
  let offset = 0;
  for (const [filename, bytes] of entries) {
    const name = Buffer.from(filename), local = Buffer.alloc(30), directory = Buffer.alloc(46);
    local.writeUInt32LE(0x04034b50); local.writeUInt16LE(20, 4);
    local.writeUInt32LE(crc32(bytes), 14);
    local.writeUInt32LE(bytes.length, 18); local.writeUInt32LE(bytes.length, 22); local.writeUInt16LE(name.length, 26);
    directory.writeUInt32LE(0x02014b50); directory.writeUInt16LE(20, 4); directory.writeUInt16LE(20, 6);
    directory.writeUInt32LE(crc32(bytes), 16);
    directory.writeUInt32LE(bytes.length, 20); directory.writeUInt32LE(bytes.length, 24);
    directory.writeUInt16LE(name.length, 28); directory.writeUInt32LE(offset, 42);
    locals.push(local, name, bytes); central.push(directory, name);
    offset += local.length + name.length + bytes.length;
  }
  const body = Buffer.concat(locals), table = Buffer.concat(central), end = Buffer.alloc(22);
  end.writeUInt32LE(0x06054b50); end.writeUInt16LE(entries.length, 8); end.writeUInt16LE(entries.length, 10);
  end.writeUInt32LE(table.length, 12); end.writeUInt32LE(body.length, 16);
  return Buffer.concat([body, table, end]);
}
function fixture(nested = false) {
  const entries = ['01_font_board.bin', '02_pinyin_board.bin', '03_main_board.bin'].map((name, i) =>
    [name, nested && i === 2 ? Buffer.from('PK\x03\x04nested archive') : Buffer.from([0, 0, 2, 32, i, 1, 2, 3])]);
  const bytes = zip(entries);
  return {file: new File([bytes], 'board.zip'), selection: {sha256: sha(bytes), stages: entries.map(([filename, data]) =>
    ({filename, bytes: data.length, sha256: sha(data)}))}, entries};
}
const good = fixture();
const prepared = await prepareFirmware(good.file, good.selection);
assert.equal(prepared.length, 3);
for (let i = 0; i < 3; i++) {
  assert.equal(prepared[i].filename, good.entries[i][0]);
  assert.deepEqual(Buffer.from(prepared[i].bytes), good.entries[i][1]);
  assert(!prepared[i].filename.endsWith('.zip'));
}
await assert.rejects(prepareFirmware(good.file, {...good.selection, stages: [...good.selection.stages].reverse()}), /01.*02.*03/);
await assert.rejects(prepareFirmware(good.file, {...good.selection, stages: good.selection.stages.slice(1)}), /01.*02.*03/);
await assert.rejects(prepareFirmware(new File(['corrupt'], 'board.zip'), good.selection), /SHA-256/);
const nested = fixture(true);
await assert.rejects(prepareFirmware(nested.file, nested.selection), /仍是 ZIP/);
console.log('PASS ZIP preparation: three ordered BIN outputs; missing/reversed stages, corrupt ZIP and nested ZIP payloads rejected');
