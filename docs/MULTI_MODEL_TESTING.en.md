# Multi-radio installation and testing

**Release credit · VRWZI / BIAOQ**

[Release v1.2.0-rc.16](https://github.com/xunyu5800-alt/OpenGD77-DIGIALL-Testing/releases/tag/v1.2.0-rc.16) · [Detailed Chinese instructions](MULTI_MODEL_TESTING.zh-CN.md)

| Radio | Included firmware |
| --- | --- |
| TYT dual-band MD-UV380/390 5W, Plus 10W PD8, Plus 10W PC6 | Three DIGIALL profiles with experimental C4FM DN RX/TX |
| Retevis RT-3S with an OpenMDUV380-compatible board | DIGIALL candidate with experimental C4FM DN RX/TX |
| Baofeng DM-1701, Retevis RT-84 | Separate DIGIALL candidates. Verify display, keypad, FM and DMR. C4FM receive awaits testing and C4FM transmit is disabled |
| GD-77, GD-77S, supported MK22 DM-1801/DM-1801A and RD-5R | Original OpenGD77 R20260131 packages and model-specific installation notes |
| TYT MD-9600/Retevis RT-90 | Original OpenGD77 R20260131, in four separate hardware profiles V1, V2, V4 and V5 |
| TYT MD-2017/Retevis RT-82 | Original OpenGD77 R20260131 package |
| Confirmed OpenDM1701-compatible variants | Original OpenDM1701 reference package |

Use the OpenGD77 CPS model-specific loader. Back up the codeplug, local calibration and important records before flashing. DIGIALL packs include Stages 01/02/03. Use only Stage 03 if the matching Chinese resources are already installed. For first installation, boot each writer, wait for `COMPLETE - VERIFIED` and screen-off, then shut down before the next stage. Use the appropriate CPS donor for each distinct platform. STM32 and MK22 donor files differ. The existing Windows one-pass wizard v0.2.0 is pinned to rc.15 UV380/390 packages. [Upstream installation guide](https://github.com/LibreDMR/OpenGD77_UserGuide/blob/master/OpenGD77_User_Guide.md)

On C4FM transmit-enabled DIGIALL builds, open **Channel Details → TX trim**. Tap SK1 to toggle **0 and +300 Hz** and save; ordinary adjustments still use 50 Hz steps. The preset is opt-in and affects only the C4FM transmit frequency. Existing saved values carry over. +300 Hz is a useful test point from one radio/hotspot pair. The MMDVM modem adds RXOffset to its shared receive frequency. Keep the hotspot at its working DMR setting when comparing C4FM trims, then retest DMR. [MMDVM-Host frequency calculation](https://github.com/g4klx/MMDVM-Host/blob/94d81993023fe26a56fd4960fd0f94f4c024b31b/Modem.cpp)

For your report, include exact radio and board revision, ZIP filename, CPS version, installation stage, and whether display, buttons, FM and DMR pass. For C4FM, include TX trim, RXOffset, power, distance, BER and whether the receiver lost lock while PTT was held. These builds need independent radio acceptance.
