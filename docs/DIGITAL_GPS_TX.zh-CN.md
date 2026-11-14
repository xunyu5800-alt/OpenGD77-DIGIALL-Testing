# 数字语音随 PTT 发送实时 GPS（rc.10 开发测试版）

DMR 和C4FM DN 可在语音通联中携带本机实时 GPS 坐标。它沿用当前数字频道、目标组和 PTT，不切换到 APRS FM 频率，不新增独立信标或自动发射。

## 开启方式

1. 开启 GPS，在 GPS 页等待有效定位。
2. **DMR**：进入频道详情，把实际使用时隙的“TA 发送 TS1／TS2”设为 **GPS** 或 **两者**。GPS 发送坐标，两者同时保留文字别名。直通 DMO 沿用两个时隙配置的合并规则。
3. **C4FM**：按住 SK2 短按绿键进入信道详情。上下键选「发送GPS」，右键开启，左键关闭。存储信道用 SK2＋绿键保存，VFO 用绿键保存。默认关闭。rc.7 已开启过 GPS TX 的信道，升级后请重新开启。
4. 返回主屏，按实体 PTT 正常讲话。建议持续约 2 秒，给接收端足够时间收到完整的嵌入式位置数据。松键仍按原收尾时限结束，不为位置包延长发射。

两种 10W 板卡均启用 C4FM DN 的 GPS 发送，真机互通待测试。GPS 关闭、无硬件或没有有效定位时，数字语音仍可使用。

## 坐标来源与有效期

每次按下 PTT 时截取一次实时定位，整次讲话使用这个坐标快照。必须是 GPS 已开启、最新有效 RMC 定位报文不超过 10 秒、经纬度有效。无效 RMC 会立即禁止下一次位置发送，不沿用屏幕的定位丢失宽限。

**不会把保存位置或上次通联坐标当作当前 GPS 发送。** 本次没有定位就省略坐标，保持普通语音和已启用的文字别名。坐标 `(0, 0)` 是有效位置，不因零值被拒绝。语音期间本机移动不会逐帧更新坐标；下次 PTT 重新取快照。

## 发送内容与网络转发

| 模式 | 实际发送内容 |
| --- | --- |
| DMR | 标准嵌入式 GPS Info LC（FLCO 8），GPS 与文字同时启用时先发 GPS，再保持完整别名顺序。精度字段使用“未知”，不把 HDOP 当作米级误差。 |
| C4FM DN | 短 GPS 数据分布于 DCH 的 FN6／FN7，保留语音位、DG-ID、呼号、原结束帧与故障保护。极点／180 度端点不发送不可表示的 YSF 坐标。 |

接收端是否显示坐标、是否送入 APRS-IS／aprs.fi，取决于接收机和数字网关支持、网关开关、呼号／DMR ID 及网络配置。FM AFSK 的 APRS 发送操作与数字语音位置携带仍是不同功能。

字段参考：[ETSI DMR TS 102 361-2](https://www.etsi.org/deliver/etsi_ts/102300_102399/10236102/02.05.01_60/ts_10236102v020501p.pdf)、[YSFGateway GPS 数据处理](https://github.com/g4klx/YSFClients/blob/master/YSFGateway/GPS.cpp)。本项目使用独立的有界编码实现，参考文件不参与链接。

## 上机复测

先用另一台支持数字定位的接收机或热点确认：GPS 开关关时只有语音；有效定位且开启时出现正确南北／东西坐标；无定位、GPS 关闭或报文过期后不重复发送旧位置；语音连续、松键正常。再检查网关是否按预期转发。软件波形与主机回归不替代空口、音质或 BER 验收。

## English

DMR and C4FM DN can attach a live GPS snapshot to normal physical-PTT speech. DMR: select GPS or Both in the active timeslot's TA TX setting. C4FM: enable GPS Tx in Channel Details. Hold SK2 and tap GREEN to save to a memory channel, or tap GREEN for VFO. The switch defaults to Off and must be re-enabled on channels configured in rc.7. Both 10W profiles now enable C4FM DN GPS TX for hardware testing.

A new PTT snapshots an enabled GPS receiver's valid RMC position, at most 10 seconds old. Invalid/no/stale fix suppresses location while retaining voice/text. Saved locations never substitute for live GPS. The snapshot stays fixed for that call; there is no standalone beacon, retune or extra RF tail. Allow about 2 seconds for complete embedded metadata.

DMR uses standard GPS Info LC with unknown accuracy and prioritises it before text. C4FM carries a short GPS message in DN DCH FN6/7 without changing speech, DG-ID or EOT timing. APRS network forwarding requires compatible gateways and configuration. Verify with another receiver/hotspot; on-radio interoperability and RF/audio acceptance remain pending.
