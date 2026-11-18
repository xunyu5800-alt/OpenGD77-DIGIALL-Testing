# OpenGD77-DIGIALL 中文操作手册

**双段 TYT MD-UV380／MD-UV390 · v1.2.0-rc.15**<br>
发布署名 **VRWZI／BIAOQ**

[在线查看 PDF](https://github.com/xunyu5800-alt/OpenGD77-DIGIALL-Testing/blob/main/docs/manual/OpenGD77_DIGIALL_Manual_ZH_CN_v1.2.0-rc.15.pdf) · [下载 PDF](https://github.com/xunyu5800-alt/OpenGD77-DIGIALL-Testing/releases/download/v1.2.0-rc.15/OpenGD77_DIGIALL_Manual_ZH_CN_v1.2.0-rc.15.pdf) · [公测下载](https://github.com/xunyu5800-alt/OpenGD77-DIGIALL-Testing/releases/tag/v1.2.0-rc.15)

本手册覆盖普通 5W＋GPS、Plus 10W PD8 和 Plus 10W PC6。按板型选包，再按章节设置 FM、DMR、C4FM、APRS 和双守候。图例由固件界面与字库重建，使用示例呼号和频率。双守分路发射及两种 10W 的 C4FM 收发仍待上机确认。

|   |   |   |
| --- | --- | --- |
| <img src="manual/images/dual-rx.png" alt="双守候 B 路接收" width="220"><br>双守候 B 路接收 | <img src="screenshots/c4fm-operating.png" alt="C4FM DN 来话" width="220"><br>C4FM DN 来话 | <img src="screenshots/aprs-position-compass.png" alt="APRS 台站方位" width="220"><br>APRS 台站方位 |

> **双守候快速操作**  FM／DMR VFO 默认轮听 A／B。长按 SK1 发 A，实体 PTT 发 B。长按红键选择要调整的频率。

<a name="manual-toc"></a>

## 操作目录

- [01 安装与升级](#chapter-01)
- [02 主屏与按键](#chapter-02)
- [03 信道分区与联系人](#chapter-03)
- [04 VFO 与双守候发射](#chapter-04)
- [05 FM 收发与扫描](#chapter-05)
- [06 DMR 收发与组过滤](#chapter-06)
- [07 C4FM 日常收发](#chapter-07)
- [08 Wires X 与热点桥接](#chapter-08)
- [09 GPS 日期时间与数字位置](#chapter-09)
- [10 APRS 接收与日志](#chapter-10)
- [11 APRS 发信标与消息](#chapter-11)
- [12 日志录音与信号工具](#chapter-12)
- [13 中文输入与屏幕设置](#chapter-13)
- [14 高级设置与系统连接](#chapter-14)
- [15 故障排查与上机验收](#chapter-15)

## 界面图谱

按用途浏览 **52 类菜单入口、226 幅画面**。旧版图例中的版本号和部分文字用于识别界面，实际操作请以本手册正文为准。

- [日常收发（48 幅）](manual/atlas-operating.zh-CN.md)
- [菜单与联系人（11 幅）](manual/atlas-menus.zh-CN.md)
- [设置（30 幅）](manual/atlas-settings.zh-CN.md)
- [信息与定位（19 幅）](manual/atlas-position.zh-CN.md)
- [解码与日志（29 幅）](manual/atlas-logs.zh-CN.md)
- [电台配置（24 幅）](manual/atlas-radio.zh-CN.md)
- [帮助与信息（63 幅）](manual/atlas-help.zh-CN.md)
- [系统连接（2 幅）](manual/atlas-connection.zh-CN.md)

<a name="chapter-01"></a>

## 01 安装与升级

本手册适用于双段 TYT MD-UV380／MD-UV390。先按板型选包，再安装主固件和配套中文资源。普通单段 MD-380／MD-390 使用其他固件。

| 板型 | 下载包标识 | 背光／功放选择 |
| --- | --- | --- |
| 普通 5W＋GPS | 5W_GPS | PD8／PC6 |
| Plus 10W PD8 | PLUS_10W_PD8_GPS | PD8／PC6 |
| Plus 10W PC6 | PLUS_10W_PC6_GPS | PC6／PD8 |

### 用 CPS 安装

1. 备份码表、本机校准和需要保留的日志或录音，保留原来可以开机的固件。10W 两种板型按实物或已验证记录确认，机壳名称和功率标签不足以区分。
2. 下载对应板型，按包内 SHA256SUMS.txt 核对完整性。已有本项目配套中文字库和拼音表时，只刷 03 主固件。首次安装或从 R250326 迁移时，依次刷 01 字库、02 拼音、03 主固件。
3. 在 CPS 的 Extras → Firmware Loader 按该机型的刷机流程加载解压后的固件。01 和 02 各自刷完后正常开机，等到 COMPLETE - VERIFIED 和熄屏，再关机进入下一步。出现写入失败时先检查板型和安装顺序。
4. 主固件的数字语音仍按 CPS 对应流程从有权使用的 donor 合入声码器。公开包提供待合入的固件。完成后正常开机，先确认背光、FM 接收和按键。
5. 首次装中文资源后，可按住 SK1＋5 开机检查。CJK data OK / log reset 表示资源通过检查并重置旧日志索引。这个快捷键涉及日志，先备份需要留下的内容。

> 本版为 v1.2.0-rc.15。双守页右侧的 SK1／PTT 分别对应 A／B 发射。

|   |   |
| --- | --- |
| <img src="ui-atlas/images/M31-000.png" alt="默认开机页" width="220"><br>默认开机页 | <img src="manual/images/firmware-info.png" alt="rc.15 版本信息示意" width="220"><br>rc.15 版本信息示意 |

[返回目录](#manual-toc)

<a name="chapter-02"></a>

## 02 主屏与按键

先识别当前在信道模式还是 VFO，再按相应的按键。信道以码表存储名称和参数，VFO 用 A／B 两组频率即时操作。彩色主屏可显示当前目标、信号表、功率等状态，经典模式采用另一套布局。

|   |   |   |
| --- | --- | --- |
| <img src="ui-atlas/images/M34-000.png" alt="FM 彩色信道" width="220"><br>FM 彩色信道 | <img src="ui-atlas/images/M34-001.png" alt="DMR 彩色信道" width="220"><br>DMR 彩色信道 | <img src="ui-atlas/images/M00-000.png" alt="主菜单" width="220"><br>主菜单 |

| 按键 | 常用操作 |
| --- | --- |
| 绿键／红键 | 绿键打开菜单或确认。红键返回或取消。普通 FM／DMR 主屏短按红键切换信道与 VFO。C4FM 主屏红键保留当前模式 |
| 旋钮／前面板上下 | 旋钮通常换信道、调 VFO 或滚动列表。DMR 主屏前面板上下选 TG，C4FM 选 DG-ID。编辑页面按该页说明操作 |
| SK1＋短按绿键 | 打开信道或 VFO 快捷菜单。旧版图集所写的「橙键」在这两款双段机上对应此组合 |
| SK2＋短按绿键 | 打开信道详情。存储信道的持久保存按页面提示使用 SK2＋绿键，VFO 详情用绿键保存 |
| SK2＋短按 \* | FM → DMR → C4FM → FM |
| SK2＋前面板上下 | 数字模式调发射功率。显示档位取自设置和校准 |
| 按住 PTT | 单守时按当前信道发射。双守时由长按 SK1／实体 PTT 分别发射 A／B |
| SK1／SK2 单独长按 | 作用随模式变化。见双守、DMR 和 C4FM 章节 |

### 屏幕状态

RX 表示接收，TX 表示发射。FMN 为窄带 FM，DMR 和 C4FM 为数字模式。CC／TS 属于 DMR，DG-ID 属于 C4FM。呼号旁的图钉表示收到可用的位置数据。

打开「菜单 → 电台信息」或「信号强度」查看电池、时间及接收电平。S 表及 dBm 用于同场条件下比较接收，发射瓦数应由测量设备确认。

主菜单内短按 * 锁键盘，短按 # 切换 PTT 锁。锁定界面按 SK2＋* 解锁。

[返回目录](#manual-toc)

<a name="chapter-03"></a>

## 03 信道分区与联系人

1. 在 CPS 录入本机呼号和 DMR ID。为每个存储信道设 RX、TX、模式、功率和通话限时。中继有异频时分别核对收发方向。
2. DMR 信道配发送联系人、接收组列表、色码 CC 与时隙 TS。FM 信道配带宽及所需收发亚音。APRS 用 FM 信道关联适用的 1200 波特配置。
3. 将存储信道加入分区。手台主屏绿键进入「分区」，确认后用旋钮选择信道。
4. 临时编辑用 SK2＋绿键打开信道详情。更改后按当前页面指示保存到存储信道或 VFO。红键取消。用「仅接收」禁止该信道发射。

|   |   |   |
| --- | --- | --- |
| <img src="ui-atlas/images/M02-000.png" alt="分区列表" width="220"><br>分区列表 | <img src="screenshots/05_channel_details.png" alt="信道详情" width="220"><br>信道详情 | <img src="ui-atlas/images/M13-000.png" alt="DMR 联系人" width="220"><br>DMR 联系人 |

| 菜单 | 可做的事 |
| --- | --- |
| 联系人 | 浏览 DMR、DTMF 与五音联系人，建立、编辑或删除相应记录 |
| 快捷联系人 | 普通主屏 SK2＋# 调出快捷联系人。C4FM 中 # 和 SK2＋# 用于房间页 |
| 数字输入 | 普通 DMR 主屏短按 # 进入，选组呼、单呼等输入模式，输入后按绿键 |
| 信道／VFO 快捷菜单 | 在信道与 VFO 间复制，选择 FM／DMR 过滤、脱网直通和 VFO 收发频率操作。VFO 可新建存储信道 |
| 电台配置 | 新建信道和分区，管理分区成员、名称、配置密码、五音联系人及 APRS 配置 |

### 功率和校准

50／250／500／750 mW 和 1／2／3 W 为共用低中档。5W 构建还提供 4／5 W，10W 构建提供 5／10 W。＋W 为用户自定义档。按板型使用本机校准资料，勿导入其他电台的校准值。

[返回目录](#manual-toc)

<a name="chapter-04"></a>

## 04 VFO 与双守候发射

进入 FM／DMR VFO 后，默认在 A／B 间轮流收听。蓝色为 A、紫色为 B。青绿标示接收，琥珀标示输入，暖红标示发射。大于号标示调频主路，SK1／PTT 标示发射键。频率末两位印在 MHz 下方。

|   |   |   |
| --- | --- | --- |
| <img src="manual/images/dual-scan.png" alt="双守巡听" width="220"><br>双守巡听 | <img src="manual/images/dual-rx.png" alt="B 路收到 DMR" width="220"><br>B 路收到 DMR | <img src="manual/images/dual-edit.png" alt="A 路录入 RX 频率" width="220"><br>A 路录入 RX 频率 |

| 操作 | 结果 |
| --- | --- |
| 长按红键 | 选择 A 或 B 作为调频主路 |
| 旋钮或数字键 | 暂停轮询并编辑主路。输入中的草稿及另一频率同时可见。结束后约 2.5 秒恢复轮询 |
| 单独长按 SK1 | 按住发射 A 路，达到已设长按阈值后开始。松开停发 |
| 按住实体 PTT | 发射 B 路。松开停发 |
| SK1＋长按绿键 | 在双守与单守之间切换。先按住 SK1，再在长按发射触发前按下绿键 |
| SK1＋短按绿键 | 打开快捷菜单，从「双守候」也能切换 |

|   |   |
| --- | --- |
| <img src="manual/images/dual-tx.png" alt="A 路异频发射与计时" width="220"><br>A 路异频发射与计时 | <img src="manual/images/dual-tx-b.png" alt="B 路异频发射与计时" width="220"><br>B 路异频发射与计时 |

一次发射由触发键控制。两键都松开再发另一路。双守时暂停 VOX 和 PTT 锁存。锁键、仅接收、频段限制、发射超时和频率输入状态仍会限制发射。结束后返回原调频主路。C4FM 或当前主路进入受保护的 APRS 接收时使用单路操作。

[返回目录](#manual-toc)

<a name="chapter-05"></a>

## 05 FM 收发与扫描

### FM 收发和亚音

选择 FM 或 FMN，并核对收发频率、带宽及中继亚音。FM 或 DMR 的普通 VFO 单守状态下，可用 SK2＋旋钮切换输入焦点，再调 RX 或 TX。频率联动打开时，调整 RX 会带动 TX 并保持频差，编辑前可在 VFO 快捷菜单核对联动选择。

FM 直接按 PTT 通话。发射期间按 SK2 可发 1750 Hz 音。接收时超长按 SK2 可进入临时监听，松开退出。音量用旋钮调整，静噪用主屏相应控制或信道详情调整。

### 范围扫描和瀑布图

1. 在普通 VFO 用前面板上键长按进入范围设置。输入低频与高频，确认后再次长按上键开始。扫描时前面板下键可反向，暂停时可按 * 略过干扰频点。按红键停扫。
2. 在 FM VFO 长按 # 打开瀑布图。普通旋钮调整中心，SK2＋旋钮改变跨度。短按 * 启用或关闭遇信号停留，停留时再按 * 跳过该频率。长按 * 在 FAST 和 FINE 间切换。
3. FAST 每行测 80 个频点，调谐后每点等待 15 ms，纯驻留预算约 1.2 秒。FINE 和遇信号停留测 160 点，每点 25 ms，纯驻留约 4 秒。实际成行时间还包括调谐、绘图和其他任务。

|   |   |   |
| --- | --- | --- |
| <img src="ui-atlas/images/M33-005.png" alt="VFO 范围扫描" width="220"><br>VFO 范围扫描 | <img src="screenshots/waterfall-live.png" alt="实时瀑布图" width="220"><br>实时瀑布图 | <img src="ui-atlas/images/M34-004.png" alt="亚音搜索" width="220"><br>亚音搜索 |

### 信道扫描和亚音扫描

信道模式沿用码表扫描选项与扫描跳过标志。进入设置 → 电台设置可核对扫描停顿策略和等待时间。亚音扫描从 VFO 快捷菜单选择 CTCSS 或 DCS 搜索，适用于模拟信号。瀑布图按频率顺序取 RSSI，射频接收机同时只停在一个频点。

[返回目录](#manual-toc)

<a name="chapter-06"></a>

## 06 DMR 收发与组过滤

1. 用有效 DMR ID、收发频率、CC 和 TS 建立信道，并填入发送联系人和接收组列表。直通与中继按实际用途选模式。
2. 主屏用前面板上下键选组。来话期间切组会重新应用接收过滤，避免继续播放旧组音频。
3. 在普通 DMR 单守主屏长按 SK1 切 ALL／指定 TG。短按 SK1 或长按 0 打开 DMR 搜索，绿键锁定搜索结果中的 TG／CC／TS，红键恢复进入前配置。双守中长按 SK1 改为 A 路发射，组过滤从快捷菜单调整。

| 状态 | 含义 |
| --- | --- |
| TG | 采用当前选定目的组过滤 |
| TGL | 使用码表接收组列表过滤 |
| ALL | 放行全部目的组。CC／TS 仍按各自开关过滤 |
| RX TG91 [ALL] | 当前实际来话为 TG91。屏幕下方 TX TG:9 表示本机发射目标为 TG9 |

|   |   |   |
| --- | --- | --- |
| <img src="screenshots/dmr-rx-all.png" alt="ALL 下实际来话组" width="220"><br>ALL 下实际来话组 | <img src="screenshots/dmr-rx-all-chinese.png" alt="中英文姓名与城市" width="220"><br>中英文姓名与城市 | <img src="ui-atlas/images/M58-000.png" alt="DMR 搜索" width="220"><br>DMR 搜索 |

### 时隙与来话身份

普通 DMR VFO 短按 * 切换时隙。单守 VFO 收到可识别的来话时，短按 SK2 可采用来话目标，以及能够取得的时隙和色码。回话前比较 RX 和 TX 栏，确认发射目标。长按绿键可打开带位置图钉的来话详情。

[返回目录](#manual-toc)

<a name="chapter-07"></a>

## 07 C4FM 日常收发

普通 5W 和两种 10W 构建均开放 C4FM DN 收发与 GPS 功能。两种 10W 的 C4FM 空口表现仍需真机确认。切到 C4FM 后，接收默认使用 RAM 路径。可直接从主屏按住实体 PTT 发 DN 语音。

|   |   |   |
| --- | --- | --- |
| <img src="screenshots/c4fm-operating.png" alt="C4FM 主屏来话" width="220"><br>C4FM 主屏来话 | <img src="screenshots/c4fm-tx-trim.png" alt="发射频率微调" width="220"><br>发射频率微调 | <img src="screenshots/c4fm-position-indicator.png" alt="来话位置图钉" width="220"><br>来话位置图钉 |

| 按键 | 功能 |
| --- | --- |
| 前面板上下 | 选 DG-ID 0～127 |
| 短按 \* | 输入 DG-ID，绿键确认，红键取消，\* 退格 |
| 短按 SK1 或长按 SK2 | 临时搜索全部 DG，再按退出。既有发射 DG 保持原选择 |
| 长按 SK1 | 切换并保存 ALL／指定 DG 过滤 |
| SK2＋绿键或长按 \* | 信道详情中设置 DG、接收过滤、发送 GPS 与 TX 微调 |
| 短按 # 或 SK2＋# | 打开 Wires-X 房间页 |
| 实体 PTT／长按绿键 | 按住发送 DN。有效位置来话可长按绿键看距离和方位 |

### 频率与时限

热点接收 433.950 MHz、发送 439.950 MHz 时，手台 RX 填 439.950 MHz，TX 填 433.950 MHz。C4FM TX 微调默认 0 Hz，可用 50 Hz 步进在 ±1500 Hz 内调整。热点的 RXOffset 影响多模式，先确认 DMR 的可用设置，再做独立 C4FM 对照。

主屏发射采用信道 TOT，设为 0 时回退 60 秒。仅接收、频段限制、PTT 锁和声码器条件仍适用。普通发布构建隐藏高级 RF 测试和诊断入口。显式开发构建中的 4:MIC、调制探测和捕获功能属于单独测试范围。

[返回目录](#manual-toc)

<a name="chapter-08"></a>

## 08 Wires X 与热点桥接

1. 在 C4FM 主屏短按 # 打开房间页。进入页面只显示设置，按 # 才发查询。
2. 输入五位房间号并按绿键连接，长按 * 断开。只有核验回复才显示连接结果。出现 No Reply 时，结合热点日志判断查询上行、网关回复和手台下行各环节。
3. 打开 Pi-Star 普通配置页，启用 YSF 和 YSF2DMR 并应用后，在 System Fusion 区配置本人有效 DMR ID、目标主站、Hotspot Security 和目标 DMR TG。测试本机桥时，启动主机选择 00002／Link YSF2DMR。
4. 让热点暂时空闲，按 PTT 发短句。用独立 DMR 接收端或 Hoseline 核对目标 TG 的实际来话。MMDVMHost 的 RF header、end of transmission 和 YSFGateway 的 Received DX、DX Reply 分别对应不同环节。

|   |   |   |
| --- | --- | --- |
| <img src="screenshots/c4fm-room-wait.png" alt="发完查询等待回包" width="220"><br>发完查询等待回包 | <img src="screenshots/c4fm-room-baseline.png" alt="房间页与测试字段" width="220"><br>房间页与测试字段 | <img src="screenshots/c4fm-split-test.png" alt="异频对照示例" width="220"><br>异频对照示例 |

| 名称 | 配置位置 |
| --- | --- |
| DG-ID | 手台 C4FM 目标值。热点默认通常为 0，以自己的配置为准 |
| YSF 房间号 | 五位 Wires-X／网关反射器编号，在房间页输入 |
| DMR TG | 在 YSF2DMR 桥和 DMR 端设置。测试本机桥时保持启动在本机桥 |
| BER 和 RXOffset | BER 需要同条件对比。初测先记录供电、档位、距离、热点空闲状态、原偏移及每次日志 |

调制档位 D22／INV／G4／N2／E1 是已用于普通 5W 单机对照的参数。不同板子和热点可以需要不同参数。热点本地转发尾音或回声只能说明部分链路工作，独立接收端能收到语音才确认语音抵达目标组。

[返回目录](#manual-toc)

<a name="chapter-09"></a>

## 09 GPS 日期时间与数字位置

### GPS 和时间

进入「菜单 → GPS」查看卫星、坐标及定位状态。新装或恢复设置时 GPS 默认开启，自动背光 30 秒。手动关闭 GPS 或改变已保存设置后按菜单保存。定位依赖实际 GPS 硬件和有效卫星数据。当前发行配置关闭 GPS Flash 轨迹记录。

在「菜单 → 电台信息」用上下键找到日期或时间，分别输入 YYYYMMDD 或 HHMMSS，按绿键保存。手动校时后自动 GPS 校时切到关闭，需要时在「设置 → 通用设置 → GPS 校时」重新开启。

「设置 → 显示设置 → 时区」修改偏移后会选用本地时间。例如北京时间用 +8:00。选择「时间 → UTC」可查看 UTC。主屏、电台信息与日志使用同一显示时区，GPS 校时给 RTC 提供 UTC。

|   |   |   |
| --- | --- | --- |
| <img src="screenshots/gps-default-on.png" alt="已开启并等待定位" width="220"><br>已开启并等待定位 | <img src="ui-atlas/images/M03-001.png" alt="电台信息中的时间" width="220"><br>电台信息中的时间 | <img src="screenshots/dmr-position-compass.png" alt="数字位置指南针" width="220"><br>数字位置指南针 |

### 接收与发送数字位置

带图钉的 DMR／C4FM 来话可长按绿键打开位置页，显示经纬度、距离和初始方位。最近收听选中带图钉的对象后，长按绿键看 LAST 历史位置，短按绿键仍选组。没有本机参考坐标时仍可查看对方经纬度。箭头以北向上，不随手台转向变化。

发送 DMR GPS 时，进入信道详情，将所用时隙的「TA 发送」设为 GPS 或两者。C4FM 在信道详情独立打开「发送 GPS」，默认关闭。每次发射取一份有效实时定位，最新有效 RMC 要在 10 秒内。无定位或过期时继续发语音并省略坐标。

<img src="manual/images/c4fm-gps.png" alt="C4FM 发送 GPS 设置示意" width="220"><br>C4FM 发送 GPS 设置示意

[返回目录](#manual-toc)

<a name="chapter-10"></a>

## 10 APRS 接收与日志

1. 在 CPS 建立当地 APRS 的 FM 信道，关联有效的 1200 波特 APRS 配置。切到该信道，或将 FM VFO 调到相同的实际 RX 频率。后台确认匹配后自动解码。
2. 在其他模式时可进入「日志 → APRS」，长按 # 开启优先守候。先取当前有效关联，再找 CPS 中第一个有效配置。列表底部显示实际监听频率。再次长按 #、退出日志或按 PTT 可撤销守候并恢复原收发环境。
3. 有效位置包在允许弹出的空闲状态自动打开位置卡片，约 5 秒回到原频道或页面。通过日志绿键手动打开时可停留查看，左右切换位置与备注，红键返回。
4. APRS 日志最近保存 16 条。满时替换最旧的未收藏记录。按住 SK2 短按 # 收藏或取消收藏，呼号前出现星号。单独短按 # 清除未收藏记录。

|   |   |   |
| --- | --- | --- |
| <img src="screenshots/aprs-position-indicator.png" alt="APRS 台站列表" width="220"><br>APRS 台站列表 | <img src="screenshots/aprs-position-compass.png" alt="经纬度与目标方位" width="220"><br>经纬度与目标方位 | <img src="screenshots/aprs-position-no-own.png" alt="缺本机位置时的显示" width="220"><br>缺本机位置时的显示 |

### 接收排查

调到对应的 FM 实际频率，核对配置和 1200 波特、静噪与接收亚音。APRS 优先守候使用单接收链路暂时占用原频道接收。因此扫频、双守、发射以及某些提示或播放期间可能接不到报文。

后台 GPS 关闭仍能接收别台报文，本机 GPS 只影响自动位置发送和距离参考。文本含类似坐标的内容不会触发位置页。被锁屏、编辑或播放挡住的自动弹窗会在短时间后过期。

[返回目录](#manual-toc)

<a name="chapter-11"></a>

## 11 APRS 发信标与消息

### 配置台址和精度

「设置 → APRS → 位置」选 GPS 发送实时定位，或选信道使用 CPS 固定坐标及可用的电台保存位置。发送前检查报文里会公开的呼号、台址、路径和备注。

「菜单 → 电台配置 → APRS 设置」打开信道关联的配置，调整「模糊度」并保存。新配置默认 0（完整），CPS 导入既有配置保留原值。其余档位按十进制度设定。

| 档位 | 对应报文 |
| --- | --- |
| 0（完整） | 普通报文用 !DAO! 补足精度，支持扩展的接收端可还原四位十进制度小数。压缩模式用 Base-91 |
| 较小步长 | 0.0002°、0.001°、0.002°、0.01° |
| 较大步长 | 0.02°、0.1°、0.2°、1° |

### 信标和文字

1. 手动信标在已关联有效配置的 FM 信道上操作。将模式设为手动，获得有效坐标，在主屏用 SK1＋2 发信标。自动模式按 APRS 设置中的发送策略和间隔运行。
2. 在日志的 APRS 入口按 * 打开消息，也可走「APRS 发送」入口。填接收呼号及内容，按绿键发送。按页面键位选择是否带位置。仅接收或临时 APRS 优先守候时无法用该临时配置发射。
3. 文字页的 WhatsApp／邮件入口依赖 APRS 网关的注册、可用性与转发配置。填写最少的必要资料。以接收端确认交付，电台发包与外部服务送达属于不同环节。

|   |   |   |
| --- | --- | --- |
| <img src="manual/images/aprs-precision.png" alt="APRS 模糊度设置示意" width="220"><br>APRS 模糊度设置示意 | <img src="screenshots/zh-CN/13-aprs-send.png" alt="APRS 消息编辑" width="220"><br>APRS 消息编辑 | <img src="ui-atlas/images/M55-000.png" alt="电子邮件网关编辑页" width="220"><br>电子邮件网关编辑页 |

[返回目录](#manual-toc)

<a name="chapter-12"></a>

## 12 日志录音与信号工具

「菜单 → 日志」汇总 APRS、呼叫记录、录音与摩尔斯相关入口。列表中的来话呼号与日志时间来自对应接收事件。

|   |   |   |
| --- | --- | --- |
| <img src="ui-atlas/images/M51-000.png" alt="日志中心" width="220"><br>日志中心 | <img src="ui-atlas/images/M51-004.png" alt="呼叫记录" width="220"><br>呼叫记录 | <img src="ui-atlas/images/M51-008.png" alt="FM 录音播放" width="220"><br>FM 录音播放 |

| 功能 | 操作与范围 |
| --- | --- |
| FM 接收录音 | 在录音列表开启自动录音。选录音并按绿键播放或停止，按页面提示删除。空间按循环方式管理。DROP 或 I/O 提示代表可能丢帧或写入失败 |
| 通话记录与最近收听 | 在日志打开呼叫记录可看详情。主菜单的最近收听用于选择 DMR 联系对象和查看收到的位置 |
| 五音选择呼叫 | FM 主屏长按 0 打开。可输入或选已保存联系人，按页面发送。接收与应答规则在相应设置中调整 |
| DTMF | 从联系人选择或在 FM 发射中使用数字键生成 DTMF。收到的呼叫可进入呼叫日志 |
| 摩尔斯发送与练习 | FM 主屏短按 \* 进入摩尔斯发送。练习、已接收内容和训练参数从相应页面打开 |
| 猎狐辅助 | 模拟主屏长按 \* 进入，按频率、信号和衰减提示做测向 |

|   |   |   |
| --- | --- | --- |
| <img src="ui-atlas/images/M40-000.png" alt="五音选择呼叫" width="220"><br>五音选择呼叫 | <img src="screenshots/08_morse_send.png" alt="摩尔斯发送" width="220"><br>摩尔斯发送 | <img src="screenshots/12_fox_hunt.png" alt="猎狐辅助" width="220"><br>猎狐辅助 |

关机前结束播放或录音，正常关机给待写记录留出时间。接收录音只覆盖 FM。遗失的开头、结束或掉块应结合播放、录音状态、一定时长的通话和正常关机做分组复测。

[返回目录](#manual-toc)

<a name="chapter-13"></a>

## 13 中文输入与屏幕设置

### 拼音输入

1. 打开信道、DMR 联系人、分区或五音联系人的名称编辑页，按 SK2＋# 进入拼音，底部显示 PY 和候选。
2. 用数字键多击输入字母。2=abc，3=def，4=ghi，5=jkl，6=mno，7=pqrs，8=tuv，9=wxyz。拼音不带声调，ü 用 v。
3. 左右选候选，上下翻页。在这类菜单里旋钮可对应左右。绿键插入汉字，红键退一位拼音，拼音空时退出。再次按 SK2＋# 返回原编辑器，再按存储页面提示保存。
4. 例如输入 zhong 选「中」，输入 guo 选「国」。码表名称上限是 16 字节，纯汉字最多 8 个。呼号与 APRS 协议字段沿用规定字符。

|   |   |   |
| --- | --- | --- |
| <img src="screenshots/chinese-pinyin-input.png" alt="拼音与选字" width="220"><br>拼音与选字 | <img src="screenshots/chinese-native12-comparison.png" alt="中文点阵比较" width="220"><br>中文点阵比较 | <img src="ui-atlas/images/M18-000.png" alt="语言选项" width="220"><br>语言选项 |

### 语言显示和音量

设置 → 语言可选择简体中文或英文。显示设置可切经典／彩色布局、背光、对比与反色，日夜主题可分别编辑。开始调色时保留一套可读的主题。音量旋钮控制播放，声音设置可调整语音提示、按键音、接收提示和麦克风相关选项。

普通状态栏、小字提示、菜单正文和主屏大字使用不同字号。DMR 大字来话页会保留呼号、姓名、城市的换行和分页，双守页使用至多两行的姓名排版。若拼音页提示 FONT/PINYIN MISSING，核对两份资源写入顺序与板型。

[返回目录](#manual-toc)

<a name="chapter-14"></a>

## 14 高级设置与系统连接

| 入口 | 用途与注意事项 |
| --- | --- |
| 通用设置 | GPS、GPS 校时、省电、锁键与自动关机等行为 |
| 电台设置 | 发射限频、功率、扫描、过滤、超时等。没有空口依据时保留已验证的值 |
| 显示与主题 | 背光时间和亮度、时区、经典／彩色、日间／夜间配色 |
| 声音设置 | 音量显示、提示等级、语音资源、接收提示、麦克风与音频相关选项 |
| 校准 | 查看或调整本机校准。先留原始备份，使用对应板卡和测量设备 |
| 卫星 | 查看载入的卫星数据、可见过境与跟踪，核对时钟、位置及资料时效 |
| USB 热点 | 连接兼容主机并配置热点模式。屏幕显示状态与正在经由 USB 处理的通信 |
| CPS 写频 | 电脑连接后读写码表、维护本机备份或更新固件。写入期间保持连接 |
| 固件信息和使用手册 | 核对本机版本、硬件范围，并浏览机内帮助主题 |

|   |   |   |
| --- | --- | --- |
| <img src="ui-atlas/images/M06-000.png" alt="设置菜单" width="220"><br>设置菜单 | <img src="ui-atlas/images/M11-000.png" alt="卫星页面" width="220"><br>卫星页面 | <img src="ui-atlas/images/M27-000.png" alt="USB 热点" width="220"><br>USB 热点 |

### 快捷操作与存储边界

支持快捷键的主菜单选项可用 SK2＋数字登记，之后在主屏按相同组合打开。主屏 SK2＋长按对应数字可清除。外部 Flash 最后 512 KiB 给中文字库与拼音资源。录音和轨迹选项也受空间布局约束，更换资源或回退旧版本前备份。

图谱包含页面内选项、确认框和典型状态。参数和入口随当前收发模式、码表、语言、板型或开发构建切换。颜色与示例频率以手台实际显示为准。

[返回目录](#manual-toc)

<a name="chapter-15"></a>

## 15 故障排查与上机验收

| 表现 | 先核对 |
| --- | --- |
| 有声音且屏幕发黑 | 借助外光查看是否有文字，核对 5W／10W 和 10W PD8／PC6 板型、背光设置、正确的 03 包。保留本机校准 |
| PTT 显示仅接收，或不发射 | 当前页面、板型、发射锁、发射频率、仅接收、频段限制、TOT、声码器条件。双守时先核对发射按键对应哪一路 |
| DMR 串组或组号看起来不对 | 看 RX TG 和 TX TG 两栏，核对 TG／TGL／ALL、CC／TS。用两个组轮流来话确认实际放音 |
| C4FM 热点无记录或房间超时 | 核对手台异频、热点是否正在发射、DG、实际 RF 日志和网关返回。不要把单次收到呼号当成持续通联通过 |
| APRS 位置偏移或未弹窗 | 比对同一时刻 GPS 和原始报文、CPS 模糊度、接收端 !DAO! 解析及底图坐标系。锁屏和编辑时弹窗可能延后 |
| 时间显示仍为 UTC | 显示设置核对偏移与「本地」，电台信息核对日期。手动校时后按需要重新打开 GPS 校时 |
| 日志或录音缺项 | 确认正常关机、录音开关、DROP／I/O 状态和空间。核对 APRS 收藏或清除操作 |

### 双守专用复测

为 A、B 预设不同的合法 RX／TX，保持低功率并用独立接收端确认。测试 SK1 发 A、PTT 发 B，分别记录实际频率、模式和松键恢复。两键交叠应保持先触发的一路，松开后不接续发射。重新验证 SK1＋绿键、独立 SK2 临时监听，以及某一路设为仅接收时的限制。

### 反馈与恢复

记录具体板型、完整包名、显示版本、模式、复现步骤和日志时间。提交前移除密码、私人位置和非必要录音。回退使用本机已验证的对应板型固件与配套中文资源。项目免费、非商业，保留原作者及第三方组件许可。发布入口和致谢见下方链接。

[返回目录](#manual-toc)

[非商业发布与许可](https://github.com/xunyu5800-alt/OpenGD77-DIGIALL-Testing/blob/main/DISTRIBUTION.md) · [作者与呼号致谢](https://github.com/xunyu5800-alt/OpenGD77-DIGIALL-Testing/blob/main/ACKNOWLEDGEMENTS.md)
