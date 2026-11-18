# 多机型刷机与公测

**发布署名 / Release credit · VRWZI / BIAOQ**

[公测下载 v1.2.0-rc.16](https://github.com/xunyu5800-alt/OpenGD77-DIGIALL-Testing/releases/tag/v1.2.0-rc.16) · [浏览器选包与校验](https://xunyu5800-alt.github.io/OpenGD77-DIGIALL-Testing/#install) · [机型验收表](TEST_MATRIX.md) · [反馈](https://github.com/xunyu5800-alt/OpenGD77-DIGIALL-Testing/issues/new?template=firmware-test.yml)

先看机背，再按同一行选包。每个机型单独提供 ZIP，总包也包含所有机型的独立 ZIP。不要按外壳相似、名称相近或接头相同选包。

## DIGIALL rc.16 公测包

| 机身型号或实际板型 | ZIP 名称后缀 | 功能与测试重点 |
| --- | --- | --- |
| TYT 双段 MD-UV380／390，普通 5W＋GPS | `TYT_MD-UV380-390_5W_GPS` | FM／DMR、C4FM DN 收发和 +300 Hz 预置 |
| TYT 双段 MD-UV380／390 Plus 10W，PD8 背光 | `TYT_MD-UV380-390_PLUS_10W_PD8` | C4FM DN 收发及该板型背光／功率 |
| TYT 双段 MD-UV380／390 Plus 10W，PC6 背光 | `TYT_MD-UV380-390_PLUS_10W_PC6` | C4FM DN 收发及该板型背光／功率 |
| Retevis RT-3S，已确认使用 OpenMDUV380 兼容板 | `RETEVIS_RT-3S` | 新增公测目标，先确认背光、FM／DMR 后再测 C4FM DN 收发。GPS 取决于实机是否装模块 |
| Baofeng DM-1701，带 STM32F405 兼容板的版本 | `BAOFENG_DM-1701` | 新增目标，先测屏幕、键盘、FM／DMR。C4FM 接收待测，C4FM 发射关闭 |
| Retevis RT-84 | `RETEVIS_RT-84` | 单独的屏幕配置。先测背光、键盘、FM／DMR。C4FM 接收待测，C4FM 发射关闭 |

本次的板型和 RF 功能以公测反馈为准。DM-1701B 若已确认可以运行原版 OpenDM1701，合集有同系列上游对照包，供该机型按上游说明测试。不同版号的 DM-1701、DM-1701A 和 DM-1701B 先核对芯片及已验证固件，不能仅由字母后缀确定兼容性。 [上游机型分组与下载](https://www.opengd77.com/archive/viewforum218b.html?f=19)

### 安装步骤

1. 备份原有码表、校准和需要保留的记录。首次迁移原厂固件前，另保存可恢复的原厂版本，并按上游方式备份本机 Flash。确认板型和下载文件 SHA-256。 [上游安装与备份](https://www.opengd77.com/archive/viewtopic6560.html?t=2380)
2. 解压本机型 ZIP。已经装好兼容的 DIGIALL 中文字库和拼音时，使用本机型的 `03`。首次安装按 `01 字库 → 02 拼音 → 03 主固件`。同一次安装全程用同一个 ZIP 的 BIN。
3. 用 **OpenGD77 CPS → Extras → Firmware Loader** 选择实际电台型号。TYT／RT-3S 用 MD-UV380 同系列入口。DM-1701 和 RT-84 选择 CPS 所列的对应机型。按照上游说明进入各机型的 DFU，加载本步骤的 BIN。需要数字语音时，用 CPS 合入自己有权使用的 **MD9600 V26.45 CSV donor**。
4. 刷 `01` 后正常开机运行 `CHINESE FONT WRITER`。看到 `COMPLETE - VERIFIED`，等背光熄灭，再把电源旋钮转到关。按住 **SK1＋PTT** 开机重新进 DFU，用 CPS 刷 `02`。正常开机运行 `CHINESE PINYIN WRITER`，等同样的成功提示和背光熄灭，再关机。任一写入器显示 `FAILED` 时，先停在当前阶段。
5. 再按 **SK1＋PTT** 开机进 DFU，用 CPS 刷 `03`。松开按键后正常开机，确认版本显示、背光、键盘和主屏。`01` 和 `02` 是临时固件，普通开机仍会运行上一次刷入的写入器。要切换阶段，需重新进 DFU 并在 CPS 中选下一份 BIN。
6. 先验 FM 接收和最低合适功率的 FM／DMR 短通联。再验中文名称输入、APRS 或 C4FM。此前发布的 Windows 一次刷机向导 **v0.2.0** 对应 rc.15 的 UV380／390，此次 rc.16 多机型包使用 CPS。

## 随合集提供的上游 OpenGD77 R20260131

这些是上游原件及对应装机说明。机型适配以各家上游说明为准，语言、APRS、C4FM 等能力按上游版本使用。

| 设备 | 内层上游 ZIP | 安装区别 |
| --- | --- | --- |
| Radioddity GD-77 | `OpenGD77.zip` | 在 CPS 选择 GD-77，对应 MK22 donor |
| Radioddity GD-77S | `OpenGD77S.zip` | 在 CPS 选择 GD-77S，对应 MK22 donor |
| Baofeng DM-1801，受支持的 MK22 旧硬件 | `OpenDM1801.zip` | 核对硬件版本，在 CPS 选 DM-1801 |
| Baofeng DM-1801A，受支持的 MK22 硬件 | `OpenDM1801A.zip` | 在 CPS 选 DM-1801A |
| Baofeng RD-5R／受支持的 DM-5R Mk2（Tier 2） | `OpenRD5R.zip` | 核对 Tier 2 及实际硬件，使用 CPS 指定入口 |
| TYT MD-9600／Retevis RT-90 | `MD9600_firmware_HW_V1/V2/V4/V5.zip` | 四个板型分别打包。按 PCB 及已验证记录选择。上游说明部分 4A 使用 V5 |
| TYT MD-2017／Retevis RT-82 | `OpenMD2017.zip` | 用对应 STM32 CPS 入口，使用对应 donor |
| Baofeng DM-1701 系列的上游对照 | `OpenDM1701.zip` | 供已经确认兼容上游 OpenDM1701 的板卡使用 |

MK22 使用上游所列的 GD-77 donor，不与 STM32 的 MD9600 donor 混用。每个上游包都有准确来源和原许可证。 [MK22 下载](https://www.opengd77.com/downloads/releases/MK22/R20260131/firmware/) · [MD-9600 板型](https://www.opengd77.com/downloads/releases/MD9600/R20260131/firmware/) · [MD-2017 下载](https://www.opengd77.com/downloads/releases/MD2017/R20260131/firmware/) · [上游 CPS 用户指南](https://github.com/LibreDMR/OpenGD77_UserGuide/blob/master/OpenGD77_User_Guide.md)

## C4FM +300 Hz 预置怎么用

进 **C4FM 主屏 → SK2＋短按绿键 → 发射频率**。在显示 `SK1` 的微调项目上短按 **SK1**，在 `0 Hz` 和 `+300 Hz` 间切换。旋钮仍能按 50 Hz 步进微调。按下页面的保存键组合才生效，红键取消。要回到零偏移，可从 +300 短按一次 SK1 再保存。

+300 Hz 是已有手台与热点组合的测试预置。最低误码点变好说明上行信号与热点解调中心更接近。误差来源可能是手台参考、热点参考或两者的校准差，需独立频率基准才能区分。热点的 `RXOffset` 会加到其共用接收频率。测试时先保持 DMR 正常使用的热点设置，再只改手台 C4FM 微调。预置仅作用于本机 C4FM 发射，默认仍是 0 Hz，升级保留用户已保存的值。 [MMDVM-Host 频率计算](https://github.com/g4klx/MMDVM-Host/blob/94d81993023fe26a56fd4960fd0f94f4c024b31b/Modem.cpp)

用同一频率、距离、功率和热点设置，分别对照 0 Hz 与 +300 Hz，各发三轮短语音。较优点附近每次只改 50 Hz，记录平均 BER 和按住 PTT 时是否掉锁。最后回到 DMR 检查发射。若不同热点的最佳点不同，记录各自测量条件和已保存值。

## 给测试者的提交格式

| 项目 | 需要记录 |
| --- | --- |
| 设备 | 机背完整型号、板型或硬件修订、GPS 情况 |
| 安装 | ZIP 完整文件名、CPS 版本、资源步骤和屏幕原文 |
| 基础 | 开机背光、菜单、旋钮、PTT、FM／DMR 的收发结果 |
| 进阶 | DN 语音是否可懂、APRS 收包、C4FM 频偏和 BER；上游包按上游功能范围测试 |
| 回退 | 备份路径在本机保留，反馈中仅写恢复结果 |

发布包适用于免费非商业测试，保留原作者与各组件许可。公开反馈前请去掉账号、密码、私人精确位置和无关录音。
