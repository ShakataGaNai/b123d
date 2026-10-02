# Wi-Fi QR plaque request

Create a parametric build123d model of a rectangular Wi-Fi QR plaque with rear magnet pockets. Use Python 3.14 and build123d 0.13.0. Return one fused, valid solid from `build()`; do not write export files inside the model. Supply `check(shape)` for the default native geometry and for round-tripped STEP when the build CLI is invoked with `--step`.

## Default dimensions and placement

- Base: 70 × 80 × 5 mm, spanning X=0..70, Y=0..80, Z=0..5.
- QR pattern: 60 × 60 mm, centered horizontally with 5 mm top, left, and right margins. The pattern spans X=5..65 and Y=15..75.
- Do not include an encoded quiet border inside the pattern. Generate a real Wi-Fi QR with automatic version selection and error correction M. Map matrix rows from the top of the plaque toward decreasing Y.
- Raise only dark QR modules by 1 mm, from Z=5 to Z=6. Leave light modules and the surrounding plate at the base surface.
- Separate horizontal dark runs with a 0.02 mm total gap (0.01 mm inset on internal perimeter edges) to avoid corner-only contacts and nonmanifold STL edges. Preserve the exact outer pattern bounds. Expose `qr_run_gap`, strictly positive and no more than 5% of module pitch. Keep the base continuous.
- Put the exact text `Wifi SSID: WorkshopWiFi` below the QR. Use nominal font size 4.5 mm and the DejaVuSans font file from the locked matplotlib dependency, with its bundled license. Check the actual text bounds before extrusion, and center them within the lower Y=0..15 band. This leaves approximately 5.32 mm between the label and QR. Custom parameters must retain at least 0.25 mm clearance to each band edge. Raise the text by the same 1 mm. Do not resize it to hide an overflow, omit characters, or substitute an operating-system font.
- Add four rear blind pockets for round 10 mm diameter × 3 mm thick magnets. Use 0.2 mm diametral clearance and 0.1 mm depth clearance: Ø10.2 × 3.1 mm pockets, open at Z=0.
- Place pocket centers 9 mm from their adjacent plate edges: (9,9), (61,9), (9,71), and (61,71). Preserve the resulting 1.9 mm roof above each pocket.

## Parameters and Wi-Fi content

Expose a frozen `Parameters` dataclass with these defaults:

```python
plate_width = 70.0
plate_height = 80.0
base_thickness = 5.0
qr_size = 60.0
qr_top_margin = 5.0
relief_height = 1.0
qr_run_gap = 0.02
magnet_diameter = 10.0
magnet_depth = 3.0
magnet_diametral_clearance = 0.2
magnet_depth_clearance = 0.1
magnet_edge_inset = 9.0
text_height = 4.5
ssid = "WorkshopWiFi"
password = "SamplePass123!"
auth = "WPA"
hidden = False
```

Support `build(params)` as well as the default `build()`. Export `wifi_payload(params)` and `qr_matrix(params)` for inspection and tests. Escape backslashes, semicolons, commas, colons, and double quotes in the Wi-Fi payload. Allow `WPA`, `WEP`, and `nopass`; open networks must use an empty password. Reject empty SSIDs, nonprintable credential characters, and unsupported text glyphs.

These are **public sample credentials**. Do not use or commit real passwords. Anyone who sees the QR or receives the model can recover its plaintext credentials.

## Engineering assumptions and checks

Use millimeters. Treat clearances as explicit glue-fit allowances, not measured compensation for a particular printer. Reject nonfinite or nonpositive dimensions, negative clearances, overlapping pockets, pockets touching plate edges, nonpositive pocket roofs, QR fields outside the plate, and text that does not fit. Keep all requested features instead of shrinking or dropping them. Build QR relief from horizontal runs and fuse in a batch rather than performing a long chain of pairwise unions.

Preserve coplanar base-face row partitions during booleans if needed for the locked kernel's triangulation. A single highly perforated top face has produced open mesh edges despite a valid BREP. The partitions must not create physical gaps, extra solids, or change the plate dimensions. Keep exported-STL regression checks rather than accepting the kernel's success flag alone.

Check overall bounds, one valid solid, pocket voids and roofs, raised and unraised QR module occupancy, and expected volume including run insets and text. Tests should rasterize the actual BREP relief and decode that raster, rather than decoding the encoder's own matrix. Export STL for both default and changed parameters and verify watertightness, winding, positive volume, and one connected body.

Print back-down with the relief up. This requires bridging the downward-opening pocket roofs; sagging can reduce magnet clearance. Inspect a trial print and dry-fit the magnets before gluing. Document printer-specific tolerances and magnet safety.

Use black raised QR/text and a light grey body in HTML, PNG, and USDZ previews. Set `[preview]` in `model.toml` to `base_color = "#d3d3d3"`, `relief_color = "#000000"`, and `relief_z = 5.0` for HTML/PNG. Change filament at the 5 mm base/relief boundary or paint the raised surfaces for printing. The requested layout does not provide a full four-module quiet zone. Require a scan and connection check on the finished physical print: a geometric test or rendered preview does not certify real-world readability.
