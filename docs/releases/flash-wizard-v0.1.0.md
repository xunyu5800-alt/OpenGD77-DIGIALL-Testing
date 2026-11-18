# 刷机向导 v0.1.0 / Windows flash wizard v0.1.0

**发布署名 / Release credit · VRWZI / BIAOQ**

适用双段 **TYT MD-UV380／MD-UV390** 的 **v1.2.0-rc.15** 固件。下载 Windows x64 ZIP 并整包解压。第一次建议先双击 `Demo.cmd`，走完一遍模拟流程，再运行 `OpenGD77-DIGIALL-Flasher.exe` 准备实际安装。

- 自动准备所选板型的 03，或按 01 字库 → 02 拼音 → 03 主固件运行。
- 自动校验 ZIP、BIN 和本地 donor，需要时合入数字声码器。包内附 `SHA256SUMS.txt`，发布页另附 ZIP 的摘要。
- 用户核对板型、备份码表及校准，按 SK1＋PTT 进 DFU。资源写入后正常开机，看到 `COMPLETE - VERIFIED` 后再进入下一步。
- 自动 DFU 写入为公测，已验证 Windows 启动、完整模拟流程和三板型包的校验，实际 USB 刷写仍待上机验证。设备或驱动识别失败时可导出原始 BIN，用 OpenGD77 CPS 安装。

[完整刷机教程，含 CPS 手动流程](https://github.com/xunyu5800-alt/OpenGD77-DIGIALL-Testing/blob/main/docs/FLASH_WIZARD.zh-CN.md)

For dual-band TYT MD-UV380/MD-UV390 and firmware v1.2.0-rc.15. Extract the full Windows x64 ZIP and run `Demo.cmd` for a no-radio rehearsal. The wizard verifies the release ZIPs, raw images and local donor, then guides each DFU write and normal-boot checkpoint. Automated USB writes await on-radio validation. The OpenGD77 CPS procedure remains available via the illustrated installation manual.
