# CooptryPoul telescopic pole — ASIN B0D8BB46Y6

## Identity and scope

- Brand: CooptryPoul; advertised blue 5–20 ft telescopic extension pole, 26 ft reach.
- Exact product: [Amazon ASIN B0D8BB46Y6](https://www.amazon.com/dp/B0D8BB46Y6). Manufacturing revision and production tolerances: unknown.
- Research date: 2026-10-01. Consumer: `models/pole_l_bracket/`.
- Interface: female screw-on socket and panel beside the pole, clearing the enlarged tip base.
- Readiness: **approximate with user-approved assumptions**. The user chose nominal fit rather than specimen measurements, and a panel running back alongside the pole. No physical fit or load capacity has been established.
- Physical print status: **not test printed yet**, confirmed by the user on 2026-10-01. `models/pole_l_bracket/model.toml` records `print_tested = false`; CAD and nominal-thread checks do not count as a print test.
- Work record: [issue #7](https://github.com/ShakataGaNai/b123d/issues/7).

## Sources

| ID | Publisher / source | Accessed | Applicable evidence | Revision / date / redistribution |
|---|---|---|---|---|
| S1 | [CooptryPoul seller listing](https://www.amazon.com/dp/B0D8BB46Y6) | 2026-10-01 | A+ heading: `3/4" Standard Universal Thread`; tools include paint rollers and dusters | Exact ASIN; hardware revision and publication date unknown; asset redistribution terms unknown |
| S2 | [Seller gallery PT02](https://m.media-amazon.com/images/I/61XTvrTWx7L._AC_SL1500_.jpg) | 2026-10-01 | Explicit `3/4" ACME thread fits twist-on tools`; depicts male tip and wider shoulder/sleeve | Exact listing gallery; not a dimensioned drawing; revision/date/redistribution terms unknown |
| S3 | [Seller gallery PT03](https://m.media-amazon.com/images/I/71muhszMiBL._AC_SL1500_.jpg) | 2026-10-01 | Artwork inconsistently says up to 20 ft and depicts/describes 5–16 ft | Revision uncertain; do not use artwork as a scaled mechanical drawing |
| S4 | [Jameson TPA-1 manufacturer page](https://jamesontools.com/product/tpa-1/) | 2026-10-01 | Commercial paint-roller, broom and window-cleaning heads use `3/4″- 5 Acme threads` | Industry interface evidence, not the exact CooptryPoul revision |
| S5 | [Max-Gain painter's-pole coupler](https://mgs4u.com/product/painters-pole-coupler/) | 2026-10-01 | Manufacturer specifies `3/4″-5 Acme female threaded coupling` | Industry interface evidence, not the exact pole |
| S6 | [Roton thread forms](https://www.roton.com/screw-university/identifying-screw-threads/screw-thread-form/) and [engineering data](https://www.roton.com/products/acme-lead-screws-nuts/engineering-data/) | 2026-10-01 | ACME included angle 29°; ¾–5 lead 0.200 in; RH and LH variants exist | Generic screw data; not evidence of pole handedness or tolerance class |
| S7 | [Dependable Acme dimensional table](https://www.dependableacme.com/internal-and-external-thread-dimensions/) | 2026-10-01 | Generic ¾–5 2G female limits: major 19.558–20.066 mm, minor 13.970–14.224 mm | Manufacturer reference; model's enlarged printing bore is not a certified 2G thread |
| S8 | [ASME B1.5 overview](https://www.asme.org/codes-standards/find-codes-standards/b1-5-acme-screw-threads) | 2026-10-01 | B1.5-1997 (R2024); single-start general-purpose classes 2G/3G/4G | Public overview only; full standard not retrieved |

All six seller gallery images were inspected during research. None supplies numeric tip engagement length, collar diameter, or shoulder datum. No original assets are committed: redistribution permission is unknown. No dimensions were obtained by scaling photographs.

## Dimension and datum contract

Source nominal thread size uses inches; model uses millimeters and degrees. `1 in = 25.4 mm`. Assembly frame: thread axis at X=Y=0, +Z toward the pole tip, socket mouth at Z=24, cap underside at Z=46. The assumed collar lies below the mouth. Panel inner face is X=25; width is along Y, height along Z. Z=0 is the lower panel edge, not a measured pole datum.

| Feature | Value | Class / evidence | Uncertainty / consequence |
|---|---|---|---|
| Male nominal thread diameter | 3/4 in = 19.05 mm | Seller-stated S1/S2; converted | Actual diameter/tolerance unknown |
| Thread form | ACME | Seller-stated S2 | Exact profile and tolerance class not specified |
| Pitch | 5 TPI = 5.08 mm | Assumed nominal universal-pole interface, user approved | Must verify on actual pole; not specified by exact listing |
| Thread handedness / starts | Right-hand / single-start | Assumed | Must verify |
| Exposed thread / usable engagement length | Unknown | No numeric evidence | Socket depth is a design choice, not measured engagement |
| Flare/sleeve/fastener envelope | 40 mm diameter | User-approved assumed envelope | Actual maximum envelope, including protruding fastener, must be measured |
| Collar axial extent and shoulder/runout datum | Unknown | No numeric evidence | Model assumes collar remains below socket mouth |
| Hardware revision | Unknown | No manufacturer drawing or specimen label | Seller artwork is internally inconsistent |

There is one blind internal thread on the declared axis, no mounting-hole pattern. Assembly requires rotating the entire bracket onto the male tip; allow hand access to the socket and sweep clearance for the panel. Final clocking is not indexed or locked by this design.

## Design decisions, separate from hardware facts

- Plain panel: 20 mm wide × 50 mm tall × 2 mm thick; `20m` interpreted as `20 mm`.
- Panel inside face X=25: derived 5 mm radial gap to assumed 20 mm collar radius, not verified actual-pole clearance.
- Socket outside diameter 30 mm; length 26 mm; blind bore depth 22 mm; cap 4 mm thick. A short exposed pole tip may engage only part of this bore. A tip longer than the available bore may bottom before shoulder seating.
- Offset arm 20 mm wide and 4 mm thick, joined to the cap. The panel remains plain: no holes, texture, ribs, or mounting accessories.
- Modeled helical trapezoidal thread, not a smooth clearance bore. Nominal construction and printing allowances are documented below.
- Intended process: trial-fit polymer FDM print for an unspecified light-duty attachment; material, printer, loads, and calibration are unknown. Thread clearance is an uncalibrated trial allowance, not a manufacturing tolerance.
- Thread construction: 5.08 mm pitch, 29° included angle, basic radial depth `pitch/2`. Crest flat derived as `pitch/2 − (pitch/2)*tan(14.5°)` from a half-pitch tooth width at the pitch cylinder. This is a basic mating envelope, not a gauged thread class.
- Female cutting envelope adds **0.25 mm radial clearance**, **0.15 mm axial clearance per flank**, and **0.254 mm additional groove-root radial relief**. These are uncalibrated trial-print decisions. Bore diameter is 14.470 mm; groove-root diameter 20.058 mm; minimum radial wall at the groove root 4.971 mm.
- Entry taper length 1.5 mm; mouth diameter 21.258 mm, leaving 4.371 mm radial wall at the mouth. Trimming the extended helix to the mouth and cap gives partial end turns; no certified thread runout or guaranteed engagement is claimed.
- Assembly orientation uses Z=0 at the panel bottom; this is not a support-free print orientation. Inspect support access and thin-panel stiffness in a slicer. Do not call it print-ready solely from CAD validity.

## Verification and limitations

Completed 2026-10-01:

| Check | Observed result / evidence |
|---|---|
| Actual export command | `uv run python scripts/build.py models/pole_l_bracket` passed; report timestamp `2026-10-01T21:31:40.294433+00:00` |
| Native and STEP | Valid, one solid, 42 × 30 × 50 mm overall; `check(shape)` passed on both |
| Panel | One full 20 × 50 mm plain exterior face; 2 mm free-panel thickness measured by intersection volume |
| Socket | Blind bore 22 mm deep and full 4 mm cap; repeated 5.08 mm grooves/lands and outer-wall material checked |
| Assumed collar | Zero intersection below the socket mouth; panel gap 5 mm to the approved assumed 40 mm diameter envelope |
| Nominal screw motion | Saved STEP against conservative basic male envelope: 9 positions, 0–720° in 90° increments, 5.08 mm/rev advance; 0 mm³ overlap at every sampled position. `outputs/pole_l_bracket/fit_check.json` |
| Saved STL | Watertight, consistent winding, one connected body, 6,358 triangles; mesh/native volume difference about 0.0247%. `outputs/pole_l_bracket/report.json` |
| Visual inspection | Inspected fixed iso/top/bottom/front PNG, actual offline HTML viewer including underside, and saved-STEP Y=0 thread-section contours in `thread_section.png` |

Artifacts: `outputs/pole_l_bracket/pole_l_bracket.step`, `pole_l_bracket.stl`, `preview.png`, `preview.html`, `report.json`, `fit_check.json`, `thread_section.png`, and `thread_section.svg`. STL must be imported as millimeters. Rebuilds regenerate the five standard export/preview files; supplementary fit/section artifacts document this verification run.

Physical screw-on fit, actual collar clearance, achievable engagement, anti-loosening, strength, and final panel clocking remain untested. The sampled nominal motion is not a continuous-motion certification or a measurement of the actual pole. Measure the pole and print a fit trial before functional use, particularly overhead. The unsupported socket in this assembly orientation needs a deliberate slicer orientation/support plan; a 2 mm polymer panel has no established load rating. Update this record and the linked model together when measurements replace assumptions.
