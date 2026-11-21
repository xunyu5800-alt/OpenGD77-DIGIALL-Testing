# rc.20 安装与操作 / Installation and controls

**不能直接刷 ZIP。ZIP 只是打包文件，先解压，CPS 每次只选择一份 BIN。完整安装需要分别刷写 3 次。**

1. 按实际机型进入 DFU，用桌面 OpenGD77 CPS 刷 01_font 字库 BIN；正常开机运行写入器，看到 COMPLETE - VERIFIED、等背光熄灭后关机。出现 FAILED 时停止。
2. 重新进入 DFU，刷 02_pinyin 拼音 BIN；正常开机运行写入器，看到 COMPLETE - VERIFIED、等背光熄灭后关机。
3. 再次进入 DFU，刷 03_main 主固件 BIN；完成后松开按键正常开机。

01/02 是临时资源写入器，不能作为最终固件使用。误刷 ZIP 或停留在 01/02 后出现循环重启时，关机后重新进入 DFU，按三步完成安装，最后必须刷 03_main。资源已确认完整的项目固件升级可只更新 03_main；首次安装或资源状态不明时完成全部三步。

按实际板型选择一个 DIGIALL ZIP，不要跨机型刷写。沿用 CPS 合法 donor 合入流程；公开包不含 codec 或 donor。

双守：短红键选 A/B；旋钮调频或换频道；SK2+* 循环 FM/DMR/C4FM；按住 SK1 查看当前侧详情；实体 PTT 在箭头选中侧发射；长红键退出。本版替换 rc.15 的 SK1=A / PTT=B 映射，SK1 恢复详情用途。菜单与设置结束后恢复双守。长 C4FM 驻留会延长另一侧等待，单接收机可能漏收短呼叫。

Do not flash the ZIP itself. Extract it first and select one BIN at a time in desktop CPS. Full installation needs three separate flashes: 01_font → 02_pinyin → 03_main, re-entering DFU for each. Run both resource writers to COMPLETE - VERIFIED before switching off. Finish with 03_main. Existing verified compatible resources: update 03 only. Keep the CPS lawful-donor workflow; no proprietary codec is distributed. Red selects A/B; physical PTT uses the selected side; hold SK1 for details.

继承双守 APRS 位置弹窗修复：切到另一侧 DMR/C4FM 后仍可显示已解码位置，5 秒后或短红键关闭，恢复原双守和选中的 PTT 侧；后续非位置报文不再清除排队提示。

继承 rc.16 的六种板型和 10W C4FM 收发；DM-1701/RT-84 现启用主屏 C4FM DN 发射，六种板型均编入 C4FM 收发，真机表现待验证。未重新发布的十一种上游参考包继续使用 rc.16。主固件与资源均为清理构建，软件回归与摘要核对通过；真机 LCD、空口、音质和 BER 待验收。

Retains all six rc.16 board profiles and 10W C4FM TX; DM-1701/RT-84 now enable main-screen C4FM DN TX; all six profiles compile RX/TX, pending on-radio validation. Unchanged upstream reference packages remain in rc.16. Hardware RF/LCD/audio/BER acceptance is pending. See GUIDES and per-board README and licences.


# v1.2.0-rc.20 — 修复 DM-1701 显存越界写入

底层矩形绘制增加屏幕边界裁剪。DM-1701 的屏幕为 160×120，中文输入面板原先仍按 128 像素高度绘制，会越过显存尾部写入其他内存。该越界已用生产绘图代码和内存检查复现并修复；同时处理负坐标、超出右侧/底部及无效尺寸。

新增回归覆盖 DM-1701、RT-84、MD-UV380 的真实布局、中文/英文文字绘制、彩色/经典菜单、1～64 项列表连续上下翻页、矩形裁剪和中文输入面板。六种机型使用同一绘图修复，分别清理构建主固件、字库和拼音写入器。

**用户反馈的“主菜单翻到首尾后继续短按上下键卡死”尚未在真机复现，未确认与上述越界同因。本版不宣称已解决所有死机。LCD、RF、音质和 BER 仍待对应实机验收。** 保留 rc.19 的六机型 C4FM DN 收发、PTT 保护、双守和 50 Hz 频偏设置。

已确认兼容字库和拼音完整的升级，只更新对应机型的 `03_main`。首次安装或资源状态不明：先解压 ZIP，按 `01_font → 02_pinyin → 03_main` 分别刷写三次，每次重新进入 DFU；两个资源写入器均须正常开机运行至 `COMPLETE - VERIFIED`、等待背光熄灭后关机。ZIP 不能直接刷入电台，最后必须刷主固件。

排查旧设置时：关机，按住 SK2 开机，启动画面出现后松开；确认 Settings Updated 并选择语言。这不会擦除 CPS 信道、联系人、字库和所有历史记录。通联记录列表长按 `#` 清空；APRS 记录页短按 `#` 清理，收藏项保留，需先用 `SK2+#` 取消收藏再清理。

Six board packages retain rc.19 features. Framebuffer rectangle clipping fixes a reproduced out-of-bounds write when a 128-pixel-high UI panel is drawn on the DM-1701's 120-pixel display. Host regressions and clean builds are software checks; the reported main-menu boundary freeze has not been reproduced on hardware or established to share this cause. Existing verified compatible resources: update matching `03_main` only. Otherwise extract the ZIP and complete `01_font → 02_pinyin → 03_main`, running both writers to COMPLETE - VERIFIED before switching off. Hardware validation remains pending.
