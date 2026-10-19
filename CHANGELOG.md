# Changelog · 更新日志

What changes in each NimbleMap (千层图) release. The newest release is at the top.
Versions follow [Semantic Versioning](https://semver.org/); the format follows
[Keep a Changelog](https://keepachangelog.com/).

Found a bug or want something? [Open an issue](https://github.com/kangning-huang/NimbleMap/issues).

## [Unreleased]

The first public release, for Macs with Apple silicon running macOS 13 or later. Free.

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

- English interface with Chinese place names. A Chinese interface is in progress.
