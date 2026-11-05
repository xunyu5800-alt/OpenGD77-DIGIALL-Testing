# Live TG switching and TG9/TG91 audio isolation

[中文](DMR_LIVE_TG_FIX.zh-CN.md) · [Versions](VERSIONS.md)

For **OpenGD77-DIGIALL v1.1.0-alpha.3**. The reported dual-band 5W radio used alpha.1: front up/down appeared ineffective during calls and TG91 speech was heard while TG9 was displayed. The following defects are reproduced in software; the user's on-air case remains pending acceptance.

## Diagnosis and changes

- The central caller overlay trusted historical display state instead of matching the active accepted call, hiding a changed selection. It now checks source/destination/filter and is cleared on selection changes.
- The first key after manual/Finder TG selection merely cleared the override. Front up/down now immediately steps relative to the selected group when present in the list; outside the list, up selects its first entry and down its last. The rotary retains channel selection. An empty group list cannot cycle.
- A reproduced race captured TG91 audio, then changed both the selected TG and LC to TG9 before decoding. Checking only current LC incorrectly authorised the old payload. Captured audio now carries destination/source/selection/CC/TS; mismatches and LC identity changes discard old AMBE/PCM, without destroying auxiliary prompt/playback audio.
- A previous TS lock could override the selected TS. Filtering now uses the user's TS; unrelated-slot headers cannot invalidate the selected slot's call.
- New acquisitions and same-slot Voice LC Headers discard the C6000 initial two voice LC returns. Failed reads do not consume this guard. This can add at least about 120ms; late entry may wait longer for valid full LC. Old identities never grant permission during that wait.

Color normal and caller screens show the actual numeric selection, e.g. `TG 9 [TG]`, with `RX:9` identifying the received destination. A contact named TG9 can be configured with numeric ID 91. `[TG]` selects one ordinary group, `[ALL]` allows all destination groups, `[TGL]` allows the RX list. Standard AllCall and configured own private-call exceptions remain; CC/TS are independent.

Long SK1 toggles ALL/TG; short SK1/long 0 opens Finder, green locks and red restores. Orange quick menu retains TGL. Changing TX TG while ALL is selected does not enable strict TG filtering.

## 5W acceptance

1. Back up codeplug/calibration. Flash the matching **5W 03 v1.1.0-alpha.3**. Current project font/pinyin need no rewrite; lawful CPS donor merge remains required.
2. Configure numeric IDs **9 and 91** in the same RX group list with identical frequency/CC/TS. Exit Finder/temporary monitoring; select `[TG]`.
3. In both channel/VFO modes select `TG 9 [TG]`: TG9 should sound and ordinary TG91 should remain muted. Select TG91 and reverse the expectation.
4. During an active call, short front up/down must immediately change the numeric selection and stop stale caller/audio. The next call must acquire valid identity before audio resumes. Test the first key after manual entry/Finder lock too.
5. Test wrong TS, adjacent calls and deliberate ALL/TGL reception separately.
6. If `TG 9 [TG]` receives `RX:91` with audio, capture version/screen/CC/TS/hotspot settings. If the air destination is `RX:9` but content is believed to originate on 91, inspect MMDVM mapping/bridging: a radio cannot reconstruct the original network TG after rewriting. Existing RTL-SDR + OpenWebRX DMR decoding can help check the actual air destination.

## Evidence and limits

Production C tests under ASan/UBSan reproduce the TG91-payload/TG9-LC race (failed before, passes after), selection changes, PCM discard, startup LC, headers, selected TS versus stale lock, bus faults, auxiliary ownership, TGL and hotspot behavior. UI tests compile actual MD-UV380 key definitions and production selection/overlay functions across channel/two VFO slots and manual-override boundaries.

No on-air RF/audio/BER acceptance is claimed; calibration/modulation are unchanged. Current project names/links use OpenGD77-DIGIALL, with upstream OpenGD77/TA8BMO copyright and license notices retained.
