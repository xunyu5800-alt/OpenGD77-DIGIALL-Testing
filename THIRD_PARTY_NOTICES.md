> Public binary/documentation mirror: source-path references identify the original notices in the private development tree, not downloadable source.
> 本仓库仅发布固件和文档；源码路径用于说明原署名出处，不提供源码下载。

# 第三方许可索引 / Third-party notices

本索引用于说明来源与随包材料，不是把第三方作品统一改为一种许可证，也不是完整的权利清查结论。源码内每个文件的适用条款仍需保留；发布声明与致谢不能代替许可。

This index identifies components and included notices. It does not relicense third-party works or certify a complete rights audit. File-level terms continue to apply; credits and distribution statements do not replace licences.

| 组件 / Component | 适用材料 / Applicable material | 独立 ZIP 中的副本 / Copy in each stage ZIP |
| --- | --- | --- |
| OpenGD77 与沿用其条款的修改 / code using its terms | [原许可](https://github.com/xunyu5800-alt/OpenGD77-DIGIALL-Testing/blob/main/licenses/OpenGD77.txt)，含非商业限制 / includes non-commercial restriction | `license.txt` |
| Fusion Pixel 与上游字体 / fonts | OFL 与来源，各上游通知分别保留 / upstream notices retained separately | `font-licenses/` |
| pypinyin 与 pinyin-data | pypinyin MIT、数据 MIT | `pinyin-licenses/` |
| Arm CMSIS | Apache-2.0 | `third-party-licenses/CMSIS/LICENSE.txt` |
| STM32F4 CMSIS Device | 本地 Apache-2.0 指引，附 CMSIS 内完整 Apache 文本 / full Apache text also included | `third-party-licenses/STM32F4-Device/LICENSE.txt` |
| STM32F4 HAL | 本地 BSD-3-Clause 回退指引；[ST 原版全文](https://github.com/xunyu5800-alt/OpenGD77-DIGIALL-Testing/blob/main/third-party-licenses/ST-BSD-3-Clause.txt) | `third-party-licenses/STM32F4-HAL/LICENSE.txt` 与 `ST-BSD-3-Clause.txt` |
| ST USB Device Library | 本地 SLA0044 Rev5 全文，包括 ST 器件使用范围等条件 / includes ST-device restriction | `third-party-licenses/ST-USB-Device/LICENSE.txt` |
| FreeRTOS | 本地 MIT 及 Amazon 版权 | `third-party-licenses/FreeRTOS/LICENSE` |

`third-party-licenses/SOURCE_COPYRIGHTS.txt` 随包保留本仓库 Drivers／Middlewares 源文件中的版权行及路径，作为上述完整许可证的补充；它涵盖源码树，不表示每个文件都编入每种固件。ST BSD 全文复制自[ST 官方仓库](https://github.com/STMicroelectronics/stm32f4xx-hal-driver/blob/master/LICENSE.md)，没有修改本仓库原许可指引或版权头。

`SOURCE_COPYRIGHTS.txt` supplements the complete licences with copyright lines and paths from Drivers/Middlewares. Its source-tree scope does not imply every file is compiled into every profile. The ST BSD text is copied from the official repository; original local notices are unchanged.

## 协议参考与声码器 / Protocol references and codec

本分支 YSF 协议代码与电脑参考测试的分离方式见协议验证记录。MMDVM、YSFClients、DigiHAM 等参考项目保持其自身许可；不得仅凭致谢将参考实现复制入非商业固件。测试辅助工具、生成数据与固件应分别核对来源；本索引不声明已完成代码相似性或专利审计。

YSF reference implementations retain their own licences. Documented separation of host references from firmware does not grant permission to copy their implementation or certify copyright/patent clearance. Host tools, generated fixtures and firmware require their own provenance checks.

公开包不分发 AMBE 专有实现、donor 或合入产物。DVSI、厂商及其他权利人的权利不因本项目免费发布而转让；用户须取得适用授权。人名、呼号、厂商和协议名称仅用于来源、致谢及兼容性说明，不代表官方背书。

Public packages exclude proprietary AMBE implementations, donors and merged firmware. Free distribution transfers no DVSI/manufacturer/other third-party rights. Names and callsigns identify provenance, contribution or compatibility without endorsement.
