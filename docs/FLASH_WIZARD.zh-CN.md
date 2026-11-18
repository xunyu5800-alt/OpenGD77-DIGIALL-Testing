# OpenGD77-DIGIALL 刷机教程与 Windows 向导

适用 **TYT MD-UV380／MD-UV390 双段机**，对应固件 **v1.2.0-rc.15**。发布署名 **VRWZI／BIAOQ**。

- [Windows x64 刷机向导公测下载](https://github.com/xunyu5800-alt/OpenGD77-DIGIALL-Testing/releases/tag/flash-wizard-v0.2.0)
- [手动刷机固件下载](https://github.com/xunyu5800-alt/OpenGD77-DIGIALL-Testing/releases/tag/v1.2.0-rc.15)
- [刷完后第一次接收与通联](MANUAL.zh-CN.md#start-01)

向导会下载、校验固件并处理本地 donor。**首次安装只需进入一次 DFU 写主固件**，随后通过正常开机的 OpenGD77 USB 串口自动补装字库和拼音。若 DFU 没有自行退出，保持 USB 连接，松开侧键后正常开机一次即可。自动 DFU 和串口写入已完成模拟验证，尚待真机验收。CPS 手动流程仍可独立使用。

## 1　确认板型，备份这台电台

在机背和已验证的板卡记录核对 **MD-UV380／MD-UV390** 以及 5W 或 Plus 10W。单段 MD-380／MD-390 不能用本页固件。同一采购型号的 10W 可能使用不同的背光引脚，不能凭电台外观或 USB 设备名代选。

| 实际板型 | 应选固件 |
| --- | --- |
| 普通双段 5W＋GPS，PD8 背光 | `5W_GPS` |
| Plus 10W，已确认 PD8 背光 | `PLUS_10W_PD8_GPS` |
| Plus 10W，已确认 PC6 背光 | `PLUS_10W_PC6_GPS` |

1. 准备有数据功能的写频线、充足的电池、Windows 电脑。使用 **OpenGD77 CPS**。已有目标项目的字库和拼音且使用正常，只需要刷 `03`。第一次装本项目资源、缺资源或仍用 R250326 资源时选 `01 → 02 → 03`。
2. 电台正常开机并连接电脑，在对应 CPS 用「从电台读取」备份码表并另存文件。备份本机校准及需要保留的录音、日志，同时保留已经验证能启动的固件。记下机型和板型，恢复时只使用本机备份。
3. 从原厂迁移时先在原厂 CPS 备份原厂码表与校准并保存原厂固件。按上游迁移方法，在兼容的 OpenGD77 正常启动后、写新码表和本项目字库之前，使用 OpenGD77 CPS 的 **Extras → OpenGD77 Support → Backup Flash** 做完整 Flash 备份。保留原厂码表文件，日常使用准备 OpenGD77 格式码表。 [上游 MD-UV380／MD-UV390 安装与备份](https://www.opengd77.com/archive/viewtopic6560.html?t=2380)

## 2　准备 OpenGD77 CPS 和 donor

donor 是数字声码器的来源。上游给出的兼容文件是 `MD9600-CSV(2571V5)-V26.45.bin`。从上游安装说明获取自己有权使用的文件，解压后留在电脑上。CPS 或向导会在本机合入。主固件发布包和向导 ZIP 都不带 donor。 [上游安装说明与 donor 文件名](https://www.opengd77.com/archive/viewtopic6560.html?t=2380)

用新的 Windows 电脑时，CPS 的 DFU 驱动和正常开机后的码表串口是两个用途。若按升级组合键后 CPS 找不到电台，在设备管理器查看 **STM DFU** 设备，再按上游说明装匹配驱动。Windows 标准 libusb 后端使用兼容的 DFU 驱动，例如 WinUSB。向导不自动修改驱动。如果现有 CPS 可用，保留它的驱动即可走手动流程。 [上游 DFU 驱动说明](https://www.opengd77.com/archive/viewtopic6560.html?t=2380) · [libusb Windows 驱动说明](https://github.com/libusb/libusb/wiki/Windows)

## 3　向导一次刷机

1. 整包解压 Windows ZIP，双击 `Demo.cmd` 演练。正式安装时打开 `OpenGD77-DIGIALL-Flasher.exe`，选择实际板型和安装方式，再选择本地 donor。备份完成后点「准备并校验」。首次安装选择「一次 DFU，自动补装字库和拼音」；已有资源的更新选择「仅更新主固件」。
2. 关闭 CPS 和热点程序，只连接这台手台。关机，按住 **SK1＋PTT** 开机进 DFU，随后松开按键。点「开始安装」并确认。向导会在写入前检查 DFU。
3. 向导写入主固件，尝试让手台正常启动。屏幕仍黑、顶灯仍闪时，保持 USB 连接，**松开侧键，关机再正常开机一次**。无需再次进入 DFU。
4. 手台出现主屏后，向导自动发现正常串口，核对手台运行的是匹配板型的本次主固件，再把字库与拼音写到各自的外部 Flash 保留区。两份资源分别经过全量回读，匹配的资源会直接跳过。
5. 向导请求手台重启加载资源。看到「安装结束」后，检查手台主屏，并在支持的名称编辑页按 **SK2＋`#`**，确认出现拼音候选。若电台没有自动回到主屏，正常关机再开机。

有下载包时，可以在「本地 ZIP 目录」选择装有对应编号 ZIP 的文件夹。走首次安装时，向导也会校验同板型的 `01` 和 `02`，便于需要时点「导出给 CPS」走三阶段手动恢复。正式流程只用 DFU 写 `03`。字库、拼音随向导提供，donor 文件和合入后的主固件始终在本机处理。

**中断时从资源阶段继续。** 若主固件已经写入而串口阶段超时，先确认手台正常开机、USB 串口可见，且没有另一软件占用。保持连接，点「重试中文资源」。已回读匹配的资源跳过，未正确写完的资源重新安装。向导在两份资源均通过校验后才请求重启。

## 4　用 OpenGD77 CPS 手动刷机

1. 从固件发布页下载对应板型的各阶段 ZIP，核对 `SHA256SUMS.txt` 并分别解压。全新安装先选 `01` 中的 BIN，已有正确资源的升级直接选择 `03`。全程使用同一板型。
2. 关闭电台，接写频线。同时按住 **SK1＋PTT**，转动电源旋钮。电脑识别出 DFU、屏幕通常黑，即可松开按键。
3. 在 OpenGD77 CPS 选 **MD9600／MD-UV380** 对应加载器，打开 **Extras → Firmware Loader**，确认加载器里的电台类型为 **MD-UV380** 系列。首次使用点 `Select official firmware (donor) file` 选 donor，接受该用法的 CPS 可能在标题显示 `[+DMR]`。
4. 点 `Select Open firmware file & update`，选择本步骤的 **项目 BIN**。等 CPS 提示完成。序号代表装机步骤；不能把 donor 或 ZIP 里的说明文件选为主固件。
5. 刷 `01`、`02` 后各正常开机一次，等 **COMPLETE - VERIFIED** 与背光熄灭，再关机。每次刷下一个 BIN 前，关机并再次按 **SK1＋PTT** 进入 DFU。刷完 `03` 后松开按键正常开机。
6. 用正常开机模式在 CPS 写入或恢复适用的 OpenGD77 码表。用手台菜单查看「固件信息」版本，测试背光和已有 FM 信道。打开姓名编辑页，用 SK2＋`#` 看是否出现拼音候选。最后再用已知参数的 DMR／C4FM 对端验收数字语音。

可以用 PowerShell 检查单个下载文件：

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath ".\下载的固件文件.zip"
```

将结果与发布页 `SHA256SUMS.txt` 中同名行比对。 [公开发行包](https://github.com/xunyu5800-alt/OpenGD77-DIGIALL-Testing/releases/tag/v1.2.0-rc.15)

## 5　卡在哪一步就查哪一步

| 现象 | 下一步 |
| --- | --- |
| 进入升级模式时屏幕全黑 | 看顶灯和电脑是否检测到 DFU。正常开机也始终黑时，用外光查看是否有文字，并核对板型和背光 |
| 正常开机后一直等待串口 | 关闭 CPS 和热点软件。检查设备管理器是否出现 OpenGD77 串口，再点「重试中文资源」 |
| 向导检测不到或不认可 DFU | 检查 SK1＋PTT、数据线、只连接一台手台、关闭 CPS。若设备原厂驱动可被 CPS 识别，使用 CPS 手动刷机 |
| `FAILED - DO NOT CONTINUE` | 停在当前资源步骤。先核对该阶段的板型、顺序和供电，再重新执行 |
| 主固件进了主屏，但无信道 | 用正常开机模式在 CPS 写入适配码表。检查信道已加入分区，再到手台选该分区 |
| FM 可用，DMR 或 C4FM 无语音 | 检查 donor 是否确实合入主固件，再检查频率、模式、组号及对端。仅写码表不会合入声码器 |
| 拼音提示缺资源 | 依次校验 `01`、`02` 的屏幕提示，三阶段都要用同一板型。需要检查旧日志索引时先备份，再按手册操作 |
| 需要回退原厂固件 | 用本机原厂固件和备份走上游恢复流程，完整 Flash 备份和原厂码表分别保留 |

上机反馈请注明板型、完整固件文件名、CPS 版本、使用向导或手动、失败阶段以及屏幕原文。 [公测反馈](https://github.com/xunyu5800-alt/OpenGD77-DIGIALL-Testing/issues/new/choose)
