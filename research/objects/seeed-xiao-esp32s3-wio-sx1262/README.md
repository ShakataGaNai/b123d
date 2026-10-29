# Seeed XIAO ESP32S3 + Wio-SX1262 header interface

Research date: 2026-10-16. Consumer: `models/multiboard/xiao/`.
Primary target: Seeed SKU **102010611**, XIAO ESP32S3 + Wio-SX1262 Meshtastic kit, with two downward-facing seven-pin male headers. The user's actual PCB revision and header supplier are unknown. Scope is a small gravity-supported header cradle with an upright flat LoRa antenna slot, not an enclosure, electrical socket, battery holder or anti-ejection clip.

Readiness: **prior geometry printed and user-approved; deeper-slot revision unprinted**. Manufacturer header coordinates are established; header stock dimensions remain assumptions. User confirmation on 2026-10-16 applies to the prior 8 mm-depth antenna slot, not the subsequent 12 mm-depth revision.

## Sources and provenance

All sources accessed 2026-10-16. Publisher: Seeed Studio. Publication dates and redistribution licenses are unknown unless noted. Original drawings/photos are not committed because redistribution terms were not established; dimensions and original analysis are recorded here instead. Remote files were treated as data, not executed.

| ID | Source | Revision / relevant evidence |
| --- | --- | --- |
| S1 | [Product page](https://www.seeedstudio.com/Wio-SX1262-with-XIAO-ESP32S3-p-5982.html) | SKU 102010611; PCB revision not identified |
| S2 | [XIAO ESP32S3 getting started](https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/) | Specification: 21 × 17.8 mm classic XIAO board; ordinary ESP32S3, Sense and Plus have differing accessories |
| S3 | [Manufacturer Eagle footprint](https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32S3/res/Seeed-Studio-XIAO-ESP32S3-footprint-eagle.lbr) | Eagle 6.4 container; package `MOUDLE14P-2.54-21X17.8MM`, 14 through-hole pads; no PCB revision stated |
| S4 | [Meshtastic kit wiki](https://wiki.seeedstudio.com/xiao_esp32s3_%26_wio_SX1262_kit_for_meshtastic/) | Wio board mates above XIAO through B2B connector; resources include XIAO v1.1 dimensions and v1.2 schematic |
| S5 | [Kit assembly photo](https://files.seeedstudio.com/wiki/XIAO_ESP32S3_for_Meshtastic_LoRa/2.png) | Qualitative orientation: Wio above XIAO, two headers/pins below, external flexible antenna leads; not a calibrated dimensional source |
| S6 | [XIAO v1.1 dimension DXF](https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32S3/res/XIAO_ESP32S3_v1.1_Dimensioning.dxf) | Retrieved and parsed with ezdxf; annotation is not exposed as TEXT. Not used to infer dimensions from page bounds |
| S7 | User design input, 2026-10-16 | Assume LoRa antenna 8 mm wide × 1 mm thick; add fit allowance; ignore cable attachment. Initial 10 mm depth cap superseded by the later request for maximum depth without other geometry changes. Approximation, not a reported measurement |
| S8 | [Manufacturer SKU 102010611 product sheet](https://files.seeedstudio.com/Bazaar/product_pdf/102010611.pdf) | Updated 2026-10-13; confirms included FPC LoRa antenna, but does not give its width/thickness |

S3 original-byte SHA-256: `ae8fda30d2be221fbd34d2bab150405a29757b889d73ff9f3efc17752dcd91e4`.
S6 original-byte SHA-256: `5fd32e3ba7a4bd85b8cc0f5d9413e26dd947e84e27b2d0f03350a7d367903f23`.

S3 also contains an **SMD carrier footprint**, whose pad centroids are not the through-hole header centers. Do not derive row spacing from that package. XML extraction of the through-hole package establishes pads at source Y=±7.62, source X=−7.62, −5.08, −2.54, 0, 2.54, 5.08, 7.62; drill diameter 1.0 mm. S3 outline is approximately 21.0007 × 17.78 mm; S2's rounded 21 × 17.8 mm is used only for a PCB clearance envelope, not for locating pins.

## Units, datums and nominal interface

All dimensions are millimeters. Model X crosses the two rows, model Y runs along them, +Y points toward the Multiboard, +Z is up. XY is the print bed at Z=0. Header array center is X=Y=0. Rotate S3's planar coordinates by −90°: `(x, y) → (y, −x)`, placing its USB end toward model −Y. Lower the pins in −Z; remove in +Z. The header plastic undersides seat at model Z=13.5.

| Feature | Value | Evidence / uncertainty |
| --- | --- | --- |
| PCB nominal length × width | 21 × 17.8 | Authoritative S2; no dimensional tolerance stated |
| Pin rows | 2 × 7 | Authoritative S3, pads 1–14 |
| Pin pitch | 2.54 | Derived adjacent pad-center difference, S3 |
| Row center spacing | 15.24 | Derived `7.62 − (−7.62)`, S3 |
| First-to-last pin center span | 15.24 | Derived `6 × 2.54`, S3 |
| Pin center positions in holder | X=±7.62; Y=−7.62…7.62 at 2.54 pitch | Derived rigid transform of S3 |
| Header pin square section | 0.64 × 0.64 | Assumed common male header stock; not specified by Seeed for user's unit |
| Exposed pin length below plastic | 6.0 | Assumed common male header; slot accepts up to 7.5 with 0.5 bottom clearance |
| Header insulator width / length / height | 2.54 / 17.78 / 2.5 | Assumed common 1×7 header stock; verify on hardware |
| Nominal board underside above seat | 2.5 | Derived from assumed insulator height; solder/underside accessories not included |
| LoRa antenna insertion-end width × thickness | 8 × 1 | Assumed, explicitly authorized by user S7; antenna revision and full length unknown |

There are no board mounting screws in this design. Drill diameters above describe the electrical footprint, not printed pin holes.

## Design decisions, distinct from source dimensions

- Body 19.64 × 29.4 × 13.5; rear snap peg adds 6.5 along +Y, for 35.9 total depth. Width derives from 15.24 mm row spacing + 1.4 mm slot width + two 1.5 mm outer walls. Matching inner walls are also 1.5 mm; each whole arm is 4.4 mm wide. The original front Y=−13, header datum and open-center rear Y=11 stay fixed; the back is at Y=16.4. One solid, no separate hardware in the printed model.
- Two straight rectangular **1.4 × 17.0 × 8.0-deep** pin slots on 15.24 mm row centers. Nominal 0.64 mm pins have 0.38 mm clearance per side and 0.56 mm clearance at each end of the complete array. These are deliberately loose, uncalibrated FDM allowances, not press fits.
- Header plastic rests on the flat rail tops, not on the pin tips. For 2.54 mm-wide plastic, each side of a 1.4 mm slot has 0.57 mm nominal support width.
- A **10.84 mm-wide through-open center between its straight walls**, derived from 15.24 mm row spacing − 1.4 mm slot width − two 1.5 mm inner walls, is open to the front and ends at Y=11. It avoids a solid pad beneath the electronics and provides underside/wire access. The two inner front tips and two rear joins have **R1 full-height vertical fillets**; the rear arcs enter the opening only from Y=10 to Y=11. Header seats and all three slots remain unchanged. The rear spine is 5.4 mm deep with 2 mm front and rear webs around the antenna slot. No wall extends above the header support plane.
- The upright LoRa antenna slot is **8.4 mm across X × 1.4 mm along Y × 12 mm deep**, centered at X=0, Y=13.7, opening at Z=13.5 with a closed floor at Z=1.5. The 1.5 mm minimum floor is a design constraint matching the prong wall thickness, not a tested strength limit. Only slot depth changed from the user-approved 8 mm version. The 8 × 1 mm assumed antenna retains **0.2 mm clearance per side**. Cable attachment clearance remains excluded at the user's request.
- Wio and XIAO upper components remain above the seat. USB exits the open −Y end; the LoRa antenna stands behind the board, while the Wi-Fi antenna and battery are supported separately. GNSS, heatsinks and other underside accessories are outside the verified envelope. Cable forces can lift the board or antenna out; neither slot is a cable anchor. RF effects of the antenna position have not been tested.
- Reuse `models.multiboard.peg.peg`, **13.5 mm across flats × 6.5 mm projection**, bottom flat at Z=0. This mates with a Multiboard **snap**, not directly with a tile Multihole. See [connector evidence](../multiboard/measured-connectors.md) for unspecified snap revision, source attribution and license terms.
- Nonconductive PETG, 0.4 mm nozzle and 0.2 mm layers are initial process assumptions. Check the slicer and a physical trial fit; no thermal, strength, retention-force or RF performance certification.

## Verification contract and limitations

The model's `check(shape)` must verify: one valid solid; envelope; both full-depth continuous pin slots; positive walls and closed slot floors; two complete 7-pin insertion envelopes; supporting ledges under the assumed plastic strips; an open underside/USB-side center; nominal PCB clearance; antenna slot dimensions, closed floor, walls and insertion envelope; front/rear spine webs; and the peg's octagonal cross-section, projection and bottom alignment. Export checks inspect saved STL and 3MF plus previews; STEP additionally exercises the same checks after round trip.

Initial cradle verification, before the antenna revision, 2026-10-16: native/STEP checks, watertight single-body STL (604 triangles), millimeter 3MF round trip and PNG/HTML inspection passed at 22 × 32.5 × 13.5 mm including the peg. This historical result is not evidence for the enlarged antenna-slot geometry; current results belong in `outputs/multiboard/xiao/report.json`.

Antenna revision verification, 2026-10-16: `uv run python scripts/build.py models/multiboard/xiao --step` passed all native and saved/reimported STEP checks, including the new antenna entry, floor, walls, insertion sweep and both rear-spine webs. Report timestamp `2026-10-16T18:42:15.729349+00:00`; bounds 22 × 35.9 × 13.5 mm; watertight, consistently oriented single-body STL (620 triangles); millimeter 3MF round trip passed. PNG and interactive HTML previews inspected. No physical antenna fit or RF test is claimed.

Inner-corner revision verification, 2026-10-16: added R1 fillets at both front inner tips and rear inner joins. Native and reimported STEP checks passed, including probes on both sides of each quarter-circle at 15°, 45° and 75° and at three heights. Full slot clearances and support ledges still passed. Report timestamp `2026-10-16T18:46:55.039679+00:00`; unchanged envelope/volume; watertight single-body STL (1,132 triangles); millimeter 3MF round trip passed. PNG and HTML previews inspected. This is a geometry revision, not renewed physical-fit evidence.

Thin-arm revision verification, 2026-10-16: outer pin-slot walls reduced from 2.68 to 1.5 mm; overall width reduced from 22 to 19.64 mm, with inner walls, slots, seats, corner radii and peg unchanged. `check(shape)` verifies complete outer wall material alongside each slot and clear space beyond the new outer faces, as well as all existing interface checks. Native/STEP checks passed; report timestamp `2026-10-16T18:53:28.797904+00:00`; bounds 19.64 × 35.9 × 13.5 mm; volume 4596.423 mm³; watertight, consistently oriented single-body STL (1,132 triangles) and millimeter 3MF round trip passed. PNG and HTML previews inspected. Reduced-wall strength has not been physically tested.

Matching-wall revision verification, 2026-10-16: thickened inner walls to 1.5 mm, matching the outer walls; center opening is 10.84 mm, whole arms 4.4 mm wide. Outside bounds and all slots remain unchanged. Native/STEP checks passed, including full-length material checks for both sides of both pin slots. Report timestamp `2026-10-16T18:55:45.205165+00:00`; volume 4777.863 mm³; single-body watertight STL (1,132 triangles), millimeter 3MF round trip and PNG/HTML inspection passed. Physical testing remains outstanding.

Classic 2×7 XIAO boards sharing this header arrangement are the intended family, **not universal compatibility with all variants/accessories**. The user confirmed the 8 mm antenna-slot version printed and validated good on 2026-10-16. Current 12 mm-depth geometry is unprinted. Header dimensions, revision, shrinkage and quantified cable/retention loads remain unspecified. Approval is tracked in [#35](https://github.com/ShakataGaNai/b123d/issues/35), deeper slot in [#37](https://github.com/ShakataGaNai/b123d/issues/37).
