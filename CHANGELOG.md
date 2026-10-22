# Changelog · 更新日志

What changes in each NimbleMap (凌波微图) release. The newest release is at the top.
Versions follow [Semantic Versioning](https://semver.org/); the format follows
[Keep a Changelog](https://keepachangelog.com/).

Found a bug or want something? [Open an issue](https://github.com/kangning-huang/NimbleMap/issues).

## [Unreleased]

## [0.7.4] - 2026-10-22 (preview)

For Macs with Apple silicon running macOS 13 or later. Free.
[Download](https://github.com/kangning-huang/NimbleMap/releases/latest/download/NimbleMap-macos-arm64.dmg)
· If you have 0.7.2 or 0.7.3, choose **Update Now** in the app (or NimbleMap › Check for Updates…).

- **More ways to sign in:** Continue with Apple, Google, GitHub, LinkedIn or X, besides email.
- **Email sign-in works for everyone.** The email now comes from NimbleMap (subject “Your NimbleMap
  sign-in code”) with a 6-digit code to type into the app, or a link to click on the same Mac.
- **The table is never covered.** With the data table open, the Ask box (or the sign-in card), the map
  buttons, the scale bar and notices move above it.
- **About NimbleMap** now credits the developer, Kangning Huang, Assistant Professor of Environmental
  Studies at NYU Shanghai, with links to kangning-huang.com and nimblemap.com.
- 登录方式更多：Apple、Google、GitHub、LinkedIn、X 或邮箱；登录邮件来自 NimbleMap，附 6 位验证码。打开数据表时，提问框和地图按钮不再遮挡表格。“关于凌波微图”加入开发者介绍。

## [0.7.3] - 2026-10-21 (preview)

For Macs with Apple silicon running macOS 13 or later. Free.
[Download](https://github.com/kangning-huang/NimbleMap/releases/latest/download/NimbleMap-macos-arm64.dmg)
· If you have 0.7.2, choose **Update Now** in the app (or NimbleMap › Check for Updates…).

- **Analysis is free.** The analysis buttons on a layer's card (count points in each area, show an
  area within a distance, measure, summarize, keep the part inside another layer, join by location,
  nearest distance, find where, rank) now work for everyone, with no sign-in. Results are previewed
  on the map until you Keep them, as before.
- **NimbleMap Pro is the Ask box.** Asking about your layers in plain words (with voice input and the
  built-in world layers) still unlocks when you sign in, free with an account.
- 分析工具改为免费：图层卡片上的分析按钮无需登录即可使用。凌波微图 Pro 现在只包括用大白话提问的助手（登录即可免费使用）。

## [0.7.2] - 2026-10-21 (preview)

For Macs with Apple silicon running macOS 13 or later. Free.
[Download](https://github.com/kangning-huang/NimbleMap/releases/latest/download/NimbleMap-macos-arm64.dmg)

- Signed with a Developer ID and notarized by Apple: it opens without the Open Anyway step.

### Updates inside the app

- Update Now: future versions download, verify and install from inside the app (NimbleMap › Check
  for Updates…). If you have 0.7.0 or 0.7.1, download this version once by hand.
- **Update Now.** When a new version is out, the notice at the bottom right of the map has an
  **Update Now** button: NimbleMap downloads the new version in the background (with a progress
  bar you can cancel), checks that it is genuine (a digital signature and a checksum), replaces
  itself and reopens. If you have unsaved changes, it asks first. No trip to the website, and no
  "Open Anyway" again.
- **NimbleMap › Check for Updates…** checks on demand and says "You're up to date" when you are.
- The example maps and the built-in world layers ship inside the app, so they update with it. The
  online basemap is always current.
- In mainland China the update comes from the GitCode mirror (also used whenever GitHub can't be
  reached). The check sends no identifiers, only the app's version number, and never runs with
  View › Work Offline on.
- If NimbleMap can't replace itself (it runs from the disk image, or your account can't change the
  Applications folder), it opens the new version in Finder for you to drag to Applications.

### Search

- Chinese place search matches simplified and traditional characters (纽约 finds New York City).
- Searching a place now flies there in one smooth arc.

## [0.7.1] - 2026-10-21 (preview)

For Macs with Apple silicon running macOS 13 or later, and Windows 10 (1809+) / 11, x64. Free.
[Download for Mac](https://github.com/kangning-huang/NimbleMap/releases/latest/download/NimbleMap-macos-arm64.dmg) ·
[Download for Windows](https://github.com/kangning-huang/NimbleMap/releases/download/v0.7.1/NimbleMap-windows-x64-setup.exe)

### Windows preview

- A per-user installer with examples, offline help, reference layers and the same sign-in service as the Mac app.
- DirectX 12 is the default graphics backend, avoiding a native Vulkan startup crash seen during Windows testing.
- The app respects Windows Animation effects at startup. Restart after changing the setting.
- The installer is not signed yet; Windows SmartScreen may display a warning.

Still not notarized: the first time you open it, macOS blocks it. Open System Settings ›
Privacy & Security and click Open Anyway (once).

### One app, Pro when you sign in

- There is one NimbleMap. Pro's features (the Ask box and the analysis buttons on cards) unlock
  when you sign in inside the app, free with an account. Signed out, everything else works as
  before, and Pro's features show a lock with Sign In….
- Ask (Pro) shows the answer on the map: the matching features are highlighted, an empty answer
  highlights nothing, built-in places (like world cities) are drawn when they're the answer, and
  'nearest' answers draw a line to the nearest feature.

### Share

- Share is on for everyone: export a map image (slide, A4 or square, as PNG or PDF), the data, or a
  map package, from the Share button or the File menu (⌘E for a map image).

### Feedback

- Help › Send Feedback… sends an idea, a problem or anything else from inside the app. It is posted
  publicly on [GitHub Discussions](https://github.com/kangning-huang/NimbleMap/discussions), where you
  can follow the replies; you don't need a GitHub account. An email address is optional and never
  shown.
- Send Feedback: signed-in users' feedback is linked to their account privately (never shown
  publicly).

### Fixes

- Image layers (GeoTIFF and NetCDF) now repeat across the world when you zoom out, like the other
  layers and the basemap, instead of stopping at a hard edge. Grids stored from 0° to 360° fill
  both sides of the 180° line.
- Lines coloured by a category or a value keep the layer's transparency, so overlapping storm
  tracks still show where they are densest.
- The table scrolls to the selected row, even far down a long table, when you open it with ⌘T.
- Matching a table to places is free again; it showed a Pro lock by mistake.
- The Ask box settles in place right after a message appears.

## [0.7.0] - 2026-10-19 (preview)

The first public preview, for Macs with Apple silicon running macOS 13 or later. Free.
[Download](https://github.com/kangning-huang/NimbleMap/releases/latest/download/NimbleMap-macos-arm64.dmg)

Not notarized yet: the first time you open it, macOS blocks it. Open System Settings ›
Privacy & Security and click Open Anyway (once).

### Open

- Double-click a Shapefile, GeoJSON, CSV, Excel, GeoPackage, KML, GPX, GeoTIFF or NetCDF file in
  Finder, or drag it onto the window, and it appears on the map.
- Files in other coordinate systems are reprojected from their `.prj`, and GeoTIFFs land in the
  right place.
- CSV and Excel files with latitude and longitude columns are placed automatically. When the app
  has to guess which columns hold the coordinates, it says so in one line and lets you change it.
- When a file uses China's GCJ-02 or BD-09 coordinates, the app says so and converts it with one click.
- Your files stay on your Mac.

### Explore

- Click any point, line, area or grid cell to see its details and where it ranks: "higher than 99%
  of 4,547 storms".
- Colour by a value, filter, compare, label, and join a table to the map by a shared column.
- A time slider for climate grids.
- Light, dark and satellite basemaps that work offline.
- Eight example datasets, including typhoon tracks since 1980, China's walled cities in 1866 and the
  2023 summer heatwaves.

### Share

- Export a finished map image, with title, legend, scale bar and data credits, sized for a slide,
  an A4 page or a square social post.
- Export the data.

### Language

- The interface in English, Chinese (凌波微图), German, Spanish, French, Italian, Dutch, Brazilian
  Portuguese, Russian, Japanese and Korean, following the Mac's language (View › Language to change
  it). Translations other than English are machine-made and being reviewed.
