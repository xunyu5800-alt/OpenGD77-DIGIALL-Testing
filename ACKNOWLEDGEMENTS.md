> Public binary/documentation mirror: source-path references identify the original notices in the private development tree, not downloadable source.
> 本仓库仅发布固件和文档；源码路径用于说明原署名出处，不提供源码下载。

# 致谢 / Acknowledgements

感谢 OpenGD77、TA8BMO 及业余无线电社区长期积累的代码、硬件研究、协议资料和测试反馈，让本分支能够继续完善中文、DMR、C4FM、APRS 和界面功能。以下依据当前源码的版权头、注释及原有鸣谢页整理，**不改变原文件的版权归属与许可证，也不表示被致谢者参与、批准或担保本分支**。测试呼号、示例数据中的呼号不据此认定为贡献者。

Thank you to the OpenGD77, TA8BMO and wider amateur-radio communities for code, hardware research, protocol information and testing. These credits follow source headers/comments and existing acknowledgements. They do not change ownership/licences or imply involvement, endorsement or approval of this branch. Callsigns used only as test/example data are not treated as contributor identities.

## OpenGD77-DIGIALL 项目署名 / Project credit

**VRWZI／BIAOQ** — OpenGD77-DIGIALL 项目与本版发布署名。

**VRWZI / BIAOQ** — OpenGD77-DIGIALL project and release credit.

## 源码作者与分支贡献 / Recorded source authors

| 姓名／呼号 / Name and callsign | 来源举例 / Source evidence |
| --- | --- |
| Roger Clark — **VK3KYY / G4KYF** | applicationMain.h、trx.c 等原版权头 / original copyright headers |
| Daniel Caujolle-Bert — **F1RMB** | applicationMain.h、menuLastHeard.c 等原版权头 |
| Kai Ludwig — **DG4KLU** | calibration.c、codec.c 原版权头 |
| Colin Durbridge — **G4EML** | applicationMain.h、trx.c 原版权头 |
| Alex — **DL4LEX** | keyboard.c、buttons.c 原版权头 |
| **TA8BMO** | aprsDecode.c、voiceRecorder.c、menuUserManual.c 等分支版权头 / branch copyright headers |

## 资料与上游鸣谢 / Information and upstream credits

| 姓名／呼号 / Name and callsign | 源码记录的范围 / Recorded context |
| --- | --- |
| Jason — **VK7ZJA (SK)** | 原固件鸣谢页保留纪念；trx.c 注释亦致谢其 RSSI 数据 / remembered in upstream credits and acknowledged for RSSI data |
| **VK4JWT** | trx.c 中 RSSI 换算数据 / RSSI conversion data |
| Ian Wraith — **G7GHH**；Jonathan Naylor — **G4KLX** | hotspot.c 原注释中的低层 DMR 信息来源 / original low-level DMR reference acknowledgement |
| Andy — **CA6JAU** | uiHotspot.c 原注释中的 MMDVM_HS 信息来源 / original MMDVM_HS information acknowledgement |

同样保留 `hotspot.c` 对匿名 DSD、MBELib 作者的原鸣谢，以及 HX8353E_display.c 对 Jnmattern 绘图资料的鸣谢。MMDVM-Host、YSFClients 与 DigiHAM 等作为本分支协议研究／独立验证参考，具体版本与用途见测试资料；致谢不等于把它们的代码重新许可或声称其为本固件背书。

The original anonymous DSD/MBELib and Jnmattern drawing acknowledgements are retained. MMDVM-Host, YSFClients and DigiHAM are credited as protocol/independent-validation references where documented; this does not relicense their code or imply endorsement.

## 历史语言贡献 / Historical language contributors

当前发布只启用英文与简体中文。源码仍保留的其他语言文件及历史贡献应继续署名；下列人员不因此被标为本分支中文翻译作者。Current releases enable English and Simplified Chinese; retained historical language sources still deserve attribution, without attributing this branch's Chinese translation to those contributors.

| 源码语言文件 / Language source | 原署名呼号 / Recorded callsigns |
| --- | --- |
| catalan.h | EA3IGM、EA5SW、EB3AM、EA3BIL |
| spanish.h | EA3IGM、EA3BIL、EA5SW |
| german.h | DG3GSP、DL4LEX、HB9WCN |
| french.h | F1CXG、F1RMB |
| dutch.h | ON7LDS |
| italian.h | IU4LEG、IZ2EIB |
| portuguese.h | CT4TX、CT1HSN |
| portugues_brazil.h | PU4RON |
| japanese.h | JE4SMQ |
| czech.h | OK2HAD、OK2MOP |
| danish.h | OZ1MAX |
| swedish.h | Roger Caballero Jonsson — SM0LTV |
| polish.h | SQ7PTE |
| romanian.h | YO3IDG |
| russian.h | TA8BMO |

## 其他项目与测试 / Other projects and testing

感谢 TakWolf 与 Fusion Pixel Font 及其上游字体作者，mozillazg、闲耘及拼音数据贡献者，Arm、STMicroelectronics、FreeRTOS 及各自贡献者。其独立许可证见[第三方许可索引](THIRD_PARTY_NOTICES.md)。

感谢本分支维护者及参与真机、热点、SDR、中文输入和界面验证的用户。私人录音、IQ、位置和原始日志不随发布包公开；没有将私人测试身份补入名单。名单可能并不穷尽历史贡献，原文件署名仍应保留，欢迎凭来源提交补充或纠正。

Thanks also to the font/pinyin/platform projects and this branch's maintainers and testers. Private recordings, IQ, positions and raw logs are excluded from release packages; private test identities are not added here. This list may not exhaust historical contributions. Original notices remain authoritative; evidence-based corrections are welcome.
