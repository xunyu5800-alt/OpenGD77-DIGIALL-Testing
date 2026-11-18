# 一次刷机向导 v0.2.0 / One-pass flash wizard v0.2.0

**发布署名 / Release credit · VRWZI / BIAOQ**

适用双段 TYT MD-UV380／MD-UV390 的 **v1.2.0-rc.15**。本版首次安装只需一次 DFU 写主固件。电台正常开机后，向导自动切到 OpenGD77 USB 串口，安装并回读核对字库、拼音，然后请求重启。

- 下载 Windows x64 ZIP，整包解压。双击 `Demo.cmd` 即可演练一次 DFU 和正常串口交接。
- 实际安装请先备份并确认板型，选择自己有权使用的本地 donor。按 SK1＋PTT 进入 DFU 后只写入主固件。如果手台仍停在 DFU，保持 USB 连接，松开侧键后正常开机一次，向导会继续。
- 串口阶段中断时可重试资源，已回读一致的资源会跳过。可导出已校验的三阶段 BIN 用于 CPS 手动安装。
- Windows 启动、模拟交接、写入边界、回读失败时延迟提交均已验证。DFU 自动启动、真实 USB 写入及不同板型的端到端行为仍待真机验证。

[完整教程及 CPS 手动流程](https://github.com/xunyu5800-alt/OpenGD77-DIGIALL-Testing/blob/main/docs/FLASH_WIZARD.zh-CN.md)

This Windows x64 beta uses one DFU pass for the v1.2.0-rc.15 main image, then installs the font and pinyin banks using the radio's normal OpenGD77 CPS port. If DFU does not exit automatically, leave USB connected and boot the radio normally. The wizard checks the running image and verifies both banks before requesting a reboot. Real radio testing is still pending.
