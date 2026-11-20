const maxBytes = 16 * 1024 * 1024;
const decoder = new TextDecoder();

async function verify(bytes, expected, label) {
  if (!globalThis.crypto?.subtle) {
    throw new Error('浏览器需要 HTTPS 才能校验 SHA-256。请打开公测网站。');
  }
  const digest = new Uint8Array(await crypto.subtle.digest('SHA-256', bytes));
  const hex = Array.from(digest, value => value.toString(16).padStart(2, '0')).join('');
  if (hex !== expected) {
    throw new Error(`${label} 的 SHA-256 不符。请确认板型并重新下载该机型的 ZIP。`);
  }
}

// Parse only the release's pinned ZIP, after its SHA-256 matches. Released
// archives use ordinary ZIP32 entries with the stored or raw deflate method.
async function extract(zip, name, expectedBytes) {
  const view = new DataView(zip.buffer, zip.byteOffset, zip.byteLength);
  let end = view.byteLength - 22;
  while (end >= Math.max(0, view.byteLength - 65557)) {
    if (view.getUint32(end, true) === 0x06054b50 && end + 22 + view.getUint16(end + 20, true) === view.byteLength) break;
    end--;
  }
  if (end < Math.max(0, view.byteLength - 65557)) throw new Error('ZIP 目录不完整。');
  const entries = view.getUint16(end + 10, true);
  let offset = view.getUint32(end + 16, true);
  for (let entry = 0; entry < entries; entry++) {
    if (offset + 46 > end || view.getUint32(offset, true) !== 0x02014b50) throw new Error('ZIP 目录格式不支持。');
    const nameSize = view.getUint16(offset + 28, true);
    const entryName = decoder.decode(zip.subarray(offset + 46, offset + 46 + nameSize));
    if (entryName !== name) {
      offset += 46 + nameSize + view.getUint16(offset + 30, true) + view.getUint16(offset + 32, true);
      continue;
    }
    const size = view.getUint32(offset + 24, true);
    const stored = view.getUint32(offset + 20, true);
    const method = view.getUint16(offset + 10, true);
    const local = view.getUint32(offset + 42, true);
    if (local + 30 > offset || view.getUint32(local, true) !== 0x04034b50 || size > maxBytes ||
        (expectedBytes !== undefined && size !== expectedBytes)) throw new Error(`${name} 的 ZIP 条目无效。`);
    const start = local + 30 + view.getUint16(local + 26, true) + view.getUint16(local + 28, true);
    if (start + stored > offset) throw new Error(`${name} 的 ZIP 数据不完整。`);
    const compressed = zip.subarray(start, start + stored);
    if (method === 0 && stored === size) return compressed;
    if (method !== 8) throw new Error('ZIP 压缩格式不支持。');
    let stream;
    try {
      stream = new DecompressionStream('deflate-raw');
    } catch {
      throw new Error('此浏览器无法提取 ZIP，请用新版 Chrome 或 Edge，或在电脑上手动解压。');
    }
    const bytes = new Uint8Array(await new Response(new Blob([compressed]).stream().pipeThrough(stream)).arrayBuffer());
    if (bytes.length !== size) throw new Error(`${name} 解压后的大小不符。`);
    return bytes;
  }
  throw new Error(`ZIP 中找不到 ${name}。`);
}

export async function prepareFirmware(file, selected) {
  if (!file.size || file.size > maxBytes) throw new Error('请选择单一机型 ZIP，合集请先解压。');
  const zip = new Uint8Array(await file.arrayBuffer());
  await verify(zip, selected.sha256, '机型 ZIP');
  if (selected.stages) {
    const prefixes = ['01_font_', '02_pinyin_', '03_main_'];
    if (selected.stages.length !== 3 || selected.stages.some((stage, index) =>
      !stage.filename?.startsWith(prefixes[index]) || !stage.filename.toLowerCase().endsWith('.bin'))) {
      throw new Error('DIGIALL 包必须包含顺序正确的 01 字库、02 拼音、03 主固件 BIN。请从发布页重新下载。');
    }
    return Promise.all(selected.stages.map(async stage => {
      const bytes = await extract(zip, stage.filename, stage.bytes);
      await verify(bytes, stage.sha256, stage.filename);
      if (bytes[0] === 0x50 && bytes[1] === 0x4b) throw new Error('提取结果仍是 ZIP，已停止。刷机只能选择解压后的 BIN。');
      return {filename: stage.filename, bytes};
    }));
  }
  const inner = await extract(zip, selected.inner);
  await verify(inner, selected.innerSha256, '上游原版 ZIP');
  const bytes = await extract(inner, selected.firmware);
  await verify(bytes, selected.firmwareSha256, selected.firmware);
  if (!selected.firmware.toLowerCase().endsWith('.bin') || (bytes[0] === 0x50 && bytes[1] === 0x4b)) {
    throw new Error('提取结果不是可用的 BIN，已停止。请按机型安装指南操作。');
  }
  return [{filename: selected.firmware, bytes}];
}

export async function inspectDfu(usb) {
  let device;
  try {
    device = await usb.requestDevice({filters: [{vendorId: 0x0483, productId: 0xdf11}]});
  } catch (error) {
    return {state: error.name === 'NotFoundError' ? 'no-selection' : 'chooser-error', error};
  }
  try {
    await device.open();
  } catch (error) {
    const denied = error.name === 'SecurityError' || error.name === 'NotAllowedError' || /access denied|permission denied/i.test(error.message);
    return {state: denied ? 'access-denied' : 'open-error', error};
  }
  try {
    const valid = device.configurations.some(config =>
      config.interfaces.some(iface => iface.alternates.some(alt =>
        alt.interfaceClass === 0xfe && alt.interfaceSubclass === 1
      ))
    );
    return {state: valid ? 'ready' : 'invalid-interface'};
  } finally {
    if (device.opened) await device.close();
  }
}
