import {inspectDfu, prepareFirmware} from './firmware.mjs';

const element = id => document.getElementById(id);
const select = element('model');
const fileInput = element('zip');
const fileStatus = element('zip-status');
const defaultFileStatus = fileStatus.textContent;
const files = element('files');
const boardNote = element('board-note');
const instructionList = element('instructions');
const online = element('online');
const cps = element('cps');
const usb = element('usb');
const usbStatus = element('usb-status');
const usbHelp = element('usb-help');
const catalog = new Map();
const objectUrls = [];
let selection;
let verification = 0;
let usbChecking = false;

const usbResultText = {
  'ready': '浏览器已打开 STM32 DFU 并读取升级接口。下一步请用下方对应的刷机工具写入。',
  'access-denied': '浏览器已找到 STM32 DFU，但系统拒绝打开设备（Access denied）。请检查下方的 USB 占用与 WinUSB 驱动步骤。',
  'open-error': '浏览器已找到 STM32 DFU，但打开设备失败。请重新连接、进入 DFU 后再试。',
  'no-selection': '未选中 DFU 设备。如果列表为空，请确认数据线和升级模式，再重新检测。',
  'chooser-error': '浏览器无法打开 USB 选择框。请用桌面 Chrome 或 Edge 通过 HTTPS 直接打开本页，检查浏览器 USB 权限后重试。',
  'invalid-interface': '已打开 USB 设备，但未读到正确的 DFU 升级接口。请检查电台是否处在升级模式。',
  'unsupported': '当前浏览器无法使用 WebUSB。请用桌面 Chrome 或 Edge 通过 HTTPS 打开；已有可用 CPS 时也可直接去第 4 步。',
};

function showUsbResult(state, error) {
  usbStatus.dataset.result = state;
  usbStatus.textContent = usbResultText[state] ?? '';
  if (error?.message && ['open-error', 'chooser-error'].includes(state)) {
    usbStatus.textContent += `（${error.message}）`;
  }
  usbHelp.hidden = !['access-denied', 'open-error'].includes(state);
}

function instructionsFor(entry) {
  if (entry.origin === 'DIGIALL') {
    return [
      '在桌面 OpenGD77 CPS 打开 Extras → Firmware Loader，选择本机型号。需要数字语音时，用 Select official firmware 选择自己有权使用的 MD9600 V26.45 CSV donor。',
      '首次安装，在 DFU 中用 Select Open firmware file & update 刷 01_font。随后正常开机运行 CHINESE FONT WRITER，看到 COMPLETE - VERIFIED 并等背光熄灭后，把电源旋钮转到关。显示 FAILED 时停止。',
      '刷 02_pinyin 时，按住 SK1＋PTT 开机进入 DFU，在 CPS 选 02_pinyin 写入。再正常开机运行 CHINESE PINYIN WRITER，看到 COMPLETE - VERIFIED 并等背光熄灭后关机。',
      '再次按 SK1＋PTT 开机进 DFU，用 CPS 刷 03_main，完成后松开按键正常开机进主屏。已有兼容字库与拼音的升级可直接刷 03_main。',
      '01 和 02 是临时写入器。它们黑屏后再普通开机会重复同一阶段；进入下一阶段必须先进入 DFU，并在 CPS 里选择下一份 BIN。',
    ];
  }
  return [
    `在第三方 Web CPS 打开 Firmware Update → ${entry.platform} Radio Firmware → Custom File，确认列表有本机型号。也可用桌面 OpenGD77 CPS 的 Firmware Loader。`,
    '选择实际机型、校验后的上游原版 BIN。数字语音按上游说明选用对应平台的自有 donor。',
    '在 Web CPS 点 Upload Firmware 并选择 USB 设备，或在桌面 CPS 点 Select Open firmware file & update。等待工具报告完成。',
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
  showUsbResult('idle');
  const pack = element('package');
  pack.replaceChildren();
  boardNote.hidden = !selection;
  element('usb-section').hidden = selection?.platform !== 'STM32';
  element('wizard').hidden = !selection?.board.startsWith('TYT_MD-UV380-390');
  online.hidden = selection?.origin !== 'OpenGD77';
  cps.hidden = !selection;
  if (!selection) {
    element('boot-mode').textContent = '选好机型后，这里会显示对应的升级按键。';
    element('path-intro').textContent = '选择机型后，这里会给出对应的刷写入口和顺序。';
    instructionList.replaceChildren();
    return;
  }

  const native = selection.origin === 'DIGIALL';
  element('boot-mode').textContent = selection.platform === 'MK22'
    ? '关机并连接数据线。按住两个侧键 SK1＋SK2 开机进入升级模式，具体按键以对应机型的上游说明为准。'
    : '关机并连接数据线。按住上侧键 SK1＋PTT 开机进入 DFU，再松开按键。升级模式下屏幕可能保持黑屏。';
  element('path-intro').textContent = native
    ? 'DIGIALL rc.16 由桌面 OpenGD77 CPS 写入。浏览器 USB 检测失败时，若 CPS 能识别电台，仍可继续。'
    : '这是上游原版包。用 Web CPS 或桌面 CPS 刷写前，先确认工具支持你的机型。';
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

element('start-flash').addEventListener('click', () => {
  requestAnimationFrame(() => select.focus({preventScroll: true}));
});
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
  if (!navigator.usb) return showUsbResult('unsupported');
  const checkedSelection = selection;
  usbChecking = usb.disabled = true;
  showUsbResult('checking');
  usbStatus.textContent = '请在浏览器的设备列表中选择 DFU。';
  try {
    const {state, error} = await inspectDfu(navigator.usb);
    if (checkedSelection === selection) showUsbResult(state, error);
  } catch (error) {
    if (checkedSelection === selection) showUsbResult('open-error', error);
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
