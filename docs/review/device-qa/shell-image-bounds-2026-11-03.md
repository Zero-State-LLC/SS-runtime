# Shell images

Measured 2026-11-03 from the app asset bytes on `9d4656c`. No new image was added. Run-shell § 8.1 stays open. This note does not add a control.

Image coordinates start at the top left of the PNG. Bounds are inclusive. A pixel counts as nontransparent when its alpha is greater than 0.

`TitleView` draws `shell_title_backdrop` as a resizable fill behind the title. It draws `shell_wordmark` as a resizable fit with a maximum width of 520. Each title button draws `shell_plate_wide` or `shell_plate_wide_pressed` at 220×56. `LaunchScreen.storyboard` draws `LaunchMark` aspect-fit at 162×162, centered. `app_icon.png` is the asset-catalog icon.

| File | Canvas | Bounds | Span | sha256 |
|---|---|---|---|---|
| `shell_title_backdrop.png` | 2732×1280 | x 0–2731, y 0–1279 | 2732×1280 | `1892896a18ad95ccab2101d4f680d63d96a738a5b7cc15512c679a4729886036` |
| `shell_wordmark.png` | 1600×400 | x 30–1572, y 17–390 | 1543×374 | `4f06aee7238fa71472ad47ce810520f396be5f59109713d33a6394023915420c` |
| `shell_plate_wide.png` | 512×160 | x 0–510, y 0–152 | 511×153 | `dba96d8e4aca889a51ea626693de5dfe33c4e0da57f158378b60183605a4b6ae` |
| `shell_plate_wide_pressed.png` | 512×160 | x 8–503, y 10–147 | 496×138 | `0e14de0d3281aee2ae4aa7cfb061d5aebe1ad17bc508ced92b834a3f665cbc59` |
| `launch_mark.png` | 1024×1024 | x 48–954, y 40–971 | 907×932 | `3108ef3a31618827e54dc4720780edd35180b4f87cf502414030771795c8ae36` |
| `app_icon.png` | 1024×1024 | x 0–1023, y 0–1023 | 1024×1024 | `fb0c5be6a665defbceb5f854ee8246f19bab8a613a82cee7afe6f0c22b91bfca` |
