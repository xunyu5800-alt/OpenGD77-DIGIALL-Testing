import {inspectDfu, prepareFirmware} from './firmware.mjs';

const element = id => document.getElementById(id);
const select = element('model');
const fileInput = element('zip');
const fileStatus = element('zip-status');
const defaultFileStatus = fileStatus.textContent;
const files = element('files');
const boardNote = element('board-note');
const instructionList = element('instructions');
const initialInstructions = instructionList.innerHTML;
const online = element('online');
const usb = element('usb');
const usbStatus = element('usb-status');
const catalog = new Map();
const objectUrls = [];
let selection;
let verification = 0;
let usbChecking = false;

function instructionsFor(entry) {
  const bootKeys = entry.platform === 'MK22' ? '按住两个侧键开机' : '按住 SK1＋PTT 开机';
  if (entry.origin === 'DIGIALL') {
    return [
      '使用 OpenGD77 CPS → Extras → Firmware Loader，选对应电台型号。数字语音使用自己有权使用的 MD9600 V26.45 CSV donor。',
      `进入 DFU 时${bootKeys}。首次安装按 01 字库 → 02 拼音 → 03 主固件，已有兼容资源则直接加载 03。`,
      '刷 01 和 02 后分别正常开机，等待 COMPLETE - VERIFIED 和背光熄灭，再关机进入下一步。刷完 03 后正常开机验收。',
    ];
  }
  return [
    `备份后，按上游说明进入 ${entry.platform} 升级模式（通常${bootKeys}）。按实际板型选择 CPS 的机型入口。`,
    '使用桌面 OpenGD77 CPS，或在第三方 Web CPS 的 Firmware Update 中确认有该机型后，选择对应平台和 Custom File，再选校验后的上游原版 BIN。',
    '数字语音按上游说明选择对应平台的自有 donor。刷完后正常开机，核对版本、背光、按键和 FM／DMR。',
  ];
}

function clearFiles() {
  while (objectUrls.length) URL.revokeObjectURL(objectUrls.pop());
  files.replaceChildren();
}

function renderSelection() {
  selection = catalog.get(select.value);
  verification++;
  clearFiles();
  fileInput.value = '';
  fileInput.disabled = !selection;
  fileStatus.textContent = defaultFileStatus;
  usbStatus.textContent = '';
  const pack = element('package');
  pack.replaceChildren();
  boardNote.hidden = !selection;
  element('usb-section').hidden = selection?.platform !== 'STM32';
  element('wizard').hidden = !selection?.board.startsWith('TYT_MD-UV380-390');
  online.hidden = selection?.origin !== 'OpenGD77';
  if (!selection) {
    instructionList.innerHTML = initialInstructions;
    return;
  }

  const native = selection.origin === 'DIGIALL';
  boardNote.textContent = native
    ? selection.c4fmTx
      ? 'DIGIALL · C4FM DN 收发已编入，射频表现按板型实测。'
      : 'DIGIALL · C4FM DN 接收待验，C4FM 发射关闭。'
    : 'OpenGD77 上游原版对照 · 功能与适配范围按上游说明。';
  if (selection.board.includes('PLUS_10W')) {
    const pin = selection.board.endsWith('PD8') ? 'PD8' : 'PC6';
    boardNote.textContent += ` 本包用于 ${pin} 背光板。`;
  }
  pack.append(element('package-template').content.cloneNode(true));
  element('package-name').textContent = selection.filename;
  element('sha').textContent = selection.sha256;
  element('download-zip').href = selection.url;
  instructionList.replaceChildren(...instructionsFor(selection).map(text => {
    const li = document.createElement('li');
    li.textContent = text;
    return li;
  }));
}

select.addEventListener('change', renderSelection);
fileInput.addEventListener('change', async () => {
  clearFiles();
  const request = ++verification;
  const [file] = fileInput.files;
  if (!file || !selection) {
    fileStatus.textContent = defaultFileStatus;
    return;
  }
  fileStatus.textContent = '正在校验 ZIP 和固件文件…';
  try {
    const results = await prepareFirmware(file, selection);
    if (request !== verification) return;
    fileStatus.textContent = 'SHA-256 校验通过。保存对应文件，用刷机工具加载。';
    results.forEach(({bytes, filename}, index) => {
      const link = document.createElement('a');
      link.download = filename;
      link.href = URL.createObjectURL(new Blob([bytes], {type: 'application/octet-stream'}));
      objectUrls.push(link.href);
      link.title = filename;
      link.textContent = results.length === 1 ? '保存原版 BIN' : ['保存 01 字库', '保存 02 拼音', '保存 03 主固件'][index];
      files.append(link);
    });
  } catch (error) {
    if (request === verification) fileStatus.textContent = error.message;
  }
});

usb.addEventListener('click', async () => {
  if (usbChecking) return;
  if (!navigator.usb) {
    usbStatus.textContent = '浏览器没有开放 WebUSB。可用电脑 Chrome／Edge，或直接用 CPS。';
    return;
  }
  const checkedSelection = selection;
  usbChecking = usb.disabled = true;
  usbStatus.textContent = '请在浏览器的设备列表中选择 DFU。';
  try {
    await inspectDfu(navigator.usb);
    if (checkedSelection === selection) usbStatus.textContent = '已检测到 STM32 DFU。请仍按机背和板卡记录核对板型。';
  } catch (error) {
    if (checkedSelection === selection) {
      usbStatus.textContent = error.name === 'NotFoundError'
        ? '没有选择 DFU。请检查升级模式、数据线和驱动，再试一次。'
        : `无法读取 DFU。请检查 WinUSB 和设备占用。${error.message}`;
    }
  } finally {
    usbChecking = usb.disabled = false;
  }
});

try {
  const response = await fetch(new URL('./catalog.json', import.meta.url));
  if (!response.ok) throw new Error('catalog unavailable');
  const release = await response.json();
  for (const origin of ['DIGIALL', 'OpenGD77']) {
    const group = document.createElement('optgroup');
    group.label = origin === 'DIGIALL' ? 'DIGIALL 公测' : '上游 OpenGD77 原版';
    for (const entry of release.packages.filter(item => item.origin === origin)) {
      catalog.set(entry.filename, entry);
      group.append(new Option(entry.model, entry.filename));
    }
    select.append(group);
  }
  select.disabled = false;
  renderSelection();
} catch {
  element('catalog-status').textContent = '暂时无法读取机型列表。请刷新页面或从 GitHub 发布页查看安装指南。';
}
