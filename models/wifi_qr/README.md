# Wi-Fi QR magnet plaque

A parametric rectangular plaque with a raised Wi-Fi QR code, the label `Wifi SSID: WorkshopWiFi`, and four rear blind magnet pockets. The default base is 70 × 80 × 5 mm; the QR and text add 1 mm, for 6 mm overall thickness. The native model and exported STEP are checked as one valid solid; the saved STL is checked for watertightness. Physical printing and scanning still require verification.

## Build

From the repository root, using the locked Python 3.14 environment:

```sh
uv sync --locked
uv run python scripts/build.py models/wifi_qr
uv run python scripts/usdz.py outputs/wifi_qr/wifi_qr.stl --relief-z 5
open outputs/wifi_qr/wifi_qr.usdz
```

The pipeline writes `outputs/wifi_qr/wifi_qr.step`, `wifi_qr.stl`, `preview.png`, `preview.html`, and `report.json`. Inspect the report and previews before slicing. The mesh uses absolute linear deflection 0.05 mm and angular deflection 0.1 rad; STEP retains the native geometry.

`build()` uses the defaults below. Python callers may pass `build(Parameters(...))`; `check(shape)` checks the default design, not arbitrary custom parameters. `wifi_payload(params)` returns the encoded string, and `qr_matrix(params)` returns top-to-bottom Boolean symbol rows without an encoded quiet border. Importing or building the model writes no artifacts. The separate macOS USDZ conversion gives the body a light grey material and raised QR/text a black material; these do not assign printer filaments.

The `[preview]` table in `model.toml` sets a light grey body and black relief above Z=5 mm for HTML and PNG. Builds save those settings in `report.json`, so `uv run python scripts/preview.py outputs/wifi_qr/wifi_qr.stl` preserves them without rebuilding geometry.

## Parameters

Dimensions are in millimeters. Clearances are additions to nominal magnet dimensions, not printer compensation inferred from measurements.

| Parameter | Default | Meaning |
| --- | --- | --- |
| `plate_width` | 70.0 | Base width along X |
| `plate_height` | 80.0 | Base height along Y |
| `base_thickness` | 5.0 | Base thickness before relief |
| `qr_size` | 60.0 | QR pattern width and height, **excluding any quiet border** |
| `qr_top_margin` | 5.0 | Plate top edge to QR pattern top |
| `relief_height` | 1.0 | Raised QR and text height above the base |
| `qr_run_gap` | 0.02 | Total gap between adjacent horizontal dark runs; positive and at most 5% of module pitch |
| `magnet_diameter` | 10.0 | Nominal round magnet diameter |
| `magnet_depth` | 3.0 | Nominal magnet thickness |
| `magnet_diametral_clearance` | 0.2 | Total diameter addition, 0.1 mm per side by default |
| `magnet_depth_clearance` | 0.1 | Pocket depth addition |
| `magnet_edge_inset` | 9.0 | Magnet center distance from each adjacent plate edge |
| `text_height` | 4.5 | Nominal font size; actual glyph bounds are checked before extrusion |
| `ssid` | `WorkshopWiFi` | Public sample network name, also printed on the plaque |
| `password` | `SamplePass123!` | Public sample password encoded in the QR |
| `auth` | `WPA` | `WPA`, `WEP`, or `nopass`; use an empty password for `nopass` |
| `hidden` | `False` | Hidden-network flag encoded as `true` or `false` |

The XY origin is the lower-left corner; the back sits at Z=0. The default QR pattern spans X=5..65 and Y=15..75, leaving 5 mm top, left, and right margins on the 70 × 80 mm plate. Only dark modules rise from Z=5 to Z=6. There is no extra blank border inside the 60 × 60 mm pattern. The QR encoder chooses the version automatically and uses error correction M. Changing credentials can change module count and physical module pitch.

Internal edges of each dark horizontal run are inset by half `qr_run_gap`; edges on the pattern's outer boundary stay exact. The tiny separation prevents diagonally adjacent dark regions from sharing only a vertical edge—a contact that can pass BREP validity but produces a nonmanifold STL. The base remains continuous and the plaque remains one solid. Default gaps are a topology allowance, not intended resolvable white print lines; confirm the slicer preserves the intended QR pattern. Increasing the gap substantially can harm scanning, so it is limited relative to module pitch.

The base's coplanar faces retain row partitions using `SkipClean` during the batch booleans. With this locked OCCT 8 kernel, a single large top face containing hundreds of relief footprints left open STL edges even though the BREP was valid and meshing reported success. Row seams avoid that triangulation failure without cutting or separating the physical base. Do not call `.clean()` indiscriminately on this model: re-export and rerun the watertightness regression after any topology simplification.

The SSID text is centered by its actual glyph bounding box in the band below the QR (Y=0..15 by default), leaving approximately **5.32 mm between the lettering and QR**. Its 4.5 mm nominal font is about 29% larger than the original 3.5 mm font; the default glyph bounds are approximately 54.06 × 4.35 mm. Custom dimensions must leave at least 0.25 mm clearance to the band edges. Text is not silently resized or cropped. The exact label prefix is `Wifi SSID: `. The font is the `DejaVuSans.ttf` shipped by the locked matplotlib dependency, explicitly selected by file path rather than by an operating-system font name. Its license is shipped alongside it as `matplotlib/mpl-data/fonts/ttf/LICENSE_DEJAVU`; no separately installed font is required. Unsupported glyphs cause a clear error rather than a missing-character replacement.

The four default magnet centers are (9,9), (61,9), (9,71), and (61,71). Each pocket is Ø10.2 × 3.1 mm deep, open on the back at Z=0 and ending at Z=3.1. This leaves a 1.9 mm roof and a 3.9 mm minimum side wall. They are glue-fit recesses, **not through holes or specified interference fits**. Dimensions, QR placement, text fit, pocket separation, and positive roof thickness are validated. Invalid layouts raise errors instead of dropping requested elements.

## Credentials and scanning

**These credentials are intentionally public samples. Do not commit real Wi-Fi secrets to Git.** A Wi-Fi QR contains plaintext credentials: anyone with the plaque, QR image, CAD file, mesh, or source can recover them. Use a guest network with access appropriate for public sharing. Reserved payload characters (`\`, `;`, `,`, `:`, and `"`) are escaped; the printed label keeps the original SSID spelling.

A scanner needs **dark QR modules on a light background**. Print the body light grey and switch to black filament at Z=5 mm (the beginning of the relief), or carefully paint only the raised surfaces black. The layout omits the internal quiet border. Its 5 mm outer margins and roughly 5.32 mm separation from the label still do **not** provide the recommended four-module quiet zone on every side. Keep the surrounding background light and verify scanning with the intended phones; a successful digital decode does not certify this reduced-clearance physical layout.

Review the slicer's layer preview to confirm the material change occurs at the base/relief boundary, the smallest modules survive extrusion-width settings, and lettering remains legible. Higher-density custom credentials may require a larger QR field rather than smaller printed modules. Scan the finished part with the intended phones at the intended distance and lighting, verify the SSID and network connection, and repeat after applying paint or finishing. BREP-derived decoding checks the designed geometry, not camera performance or a finished print. This sample is not certified as a functioning physical QR until that scan succeeds.

## Printing and magnets

Print with the broad back at Z=0 on the build plate and the relief facing up. The rear pockets open downward in this orientation. Their roofs require bridging roughly 10.2 mm; bridging quality varies by printer, cooling, layer height, and material. Sagging can reduce magnet clearance. Tune bridging or use removable support in the pockets, and inspect the recesses before gluing. Reversing the part avoids these bridges but puts fine relief against the bed or supports, which can damage QR readability.

Measure the actual magnets and print a fit coupon before making a batch. Adjust explicit clearance parameters for your printer, adhesive, and magnets; the sample dimensions are not a certified fit. Dry-fit all four magnets, confirm their polarity against the mating surface, then secure with a suitable adhesive. Keep adhesive out of the QR face and allow it to cure before mounting. Loose strong magnets are a swallowing hazard; this is not a toy.

## Format references

- [ZXing Wi-Fi network configuration format](https://github.com/zxing/zxing/wiki/Barcode-Contents#wifi-network-config-android-ios-11) specifies the `WIFI:` fields and reserved-character escaping.
- [DENSO WAVE's QR code area guidance](https://www.qrcode.com/en/howto/code.html/index.html) requires a clear four-module quiet zone on every side.
- The locked `qrcode` encoder selects symbol version and error correction; `zxing-cpp` independently decodes a raster sampled from the CAD in the tests. Neither library measures real-world print contrast or camera performance.
