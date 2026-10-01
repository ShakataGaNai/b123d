# BQ Voyage Station G3: enclosure geometry research

Research date: 2026-10-01. Work item: [#4](https://github.com/ShakataGaNai/b123d/issues/4). Scope: find hardware evidence, compare five community designs, and prove that their downloadable geometry can supply dimensions for a build123d enclosure. No new case has been designed or physically tested.

**Readiness: approximate with listed assumptions.** Use beanfield's model 1855194 as the preferred functional reference. Its STL files provide measurable mounting geometry, a shell, faceplates, a jumper hatch, and antenna spacers. Model 1816444 also provides STEP solids. Neither source is an authoritative model of the hardware. Verify the actual board revision and fit before committing to a close-fitting enclosure.

## Identity and official evidence

Reference configuration: Station G3 **ESP32S3-BQ35LORA900V1M**, consisting of the motherboard, **BQESP32V1M** MCU daughterboard with a 1.3-inch OLED, and **BQ35LORA900V1M** RF daughterboard. The Raspberry Pi MCU alternative and optional second RF board require separate clearance checks. Firmware compatibility with G2 establishes no mechanical compatibility. [S1]

The official shop identifies motherboard revision **30 Dec 2025**; official motherboard photographs show the corresponding silkscreen. An illustrated MCU board bears **02/Jan/2026**. These identify documented examples, not the revision of an unexamined physical unit. The main shop page also warns that it retains some historical G2 information. [S2]

| Official product | Published dimensions, converted from cm to mm | Evidence and limitation |
|---|---|---|
| Motherboard | 113 × 65 × 16 | Authoritative product metadata, not a dimensioned bare-PCB drawing. [S3] |
| Motherboard plus RF daughterboard | 122 × 65 × 26 | Explicitly excludes MCU daughterboard. [S4] |
| RF daughterboard | 90 × 34 × 12 | Undatumed module product envelope. [S5] |
| Complete ESP32 assembly | Not specified | Main listing gives N/A. [S2] |

No source above specifies tolerances, measurement datums, or whether connectors/standoffs count toward the envelope. Do not scale photographs to manufacture hole coordinates. In particular, the 113 mm motherboard product dimension and the 112 mm community backplate length below are **not interchangeable**; their scope differs or remains unknown.

No official G3 board schematic, STEP model, PCB/Gerber package, or dimensioned mounting drawing was located in the inspected wiki, store/component listings, interactive pinout resources, or manufacturer-associated public repository inventory. This is a bounded search result. The pinout viewer provides electrical connections and a photograph; the linked SX1262 datasheet describes a component, not the G3 board. [S1, S6, S7]

### Enclosure-facing hardware

- Preserve access to separate motherboard **USB-C power** and MCU **USB-C communication** ports, the **DC5521** input, Grove GPS/I²C connections, MCU programming/restart buttons, and the PG button/LEDs. The manufacturer says not to power the installed MCU board through its communication port. [S1]
- The PA/LNA jumpers need service access. The stock primary RF slot and an added secondary RF daughterboard have different clearance requirements. [S1]
- Official MCU replacement instructions mention three or four **M2.5 screws**, depending on the module. This does not specify motherboard-to-case hole diameters or standoff lengths. [S1]
- Keep the RF heatsink and antenna connection clear. Thermal requirement [INFERENCE]: evaluate enclosure temperature under the intended transmit duty cycle. Whole-device electrical consumption is not a heat-dissipation specification, and no verified ventilation area or closed-case thermal limit was found. [S1]

## Community design comparison

Primary evidence: live records from Printables' public GraphQL API, including descriptions, authors, licenses and complete `stls`/`otherFiles` inventories. The normal pages returned HTTP 403 and managed Chrome showed a Cloudflare challenge. The API and original file host remained accessible. Search summaries and mirrors were discovery aids only.

The API's `stls` field can contain **STEP files**; its name does not establish the file format. All five records had empty `otherFiles` arrays. Counts below describe that inspected downloadable-model inventory, not any uninspected print-profile attachments.

| Original listing | Author | Verified geometry files | License name reported by Printables | Relevance and limits |
|---|---|---|---|---|
| [1816444: BQ Station G3 Case][C1] | Chakolicous | **7 STEP files** | CC BY-NC-SA | Best analytic CAD alternative. Hardware, no-heatset, superglue, and loose variants. One hardware-base STEP was downloaded and imported successfully. |
| [1818451: snap-fit case][C2] | Adroit Jones / Lux3MC | **2 STL files** | CC BY-NC-SA | Current lid is `BQ Station G3-lid-snapfit-V2.stl`. Author reports a corrected heatsink position and says they do not own a G3. Lid snaps; board mounting still uses screws/inserts. |
| [1807804: baseplate][C3] | Mattchew | **7 STL files** | CC BY-SA | Useful independent baseplate reference. V5/V7 and clip variants. Author states a 5 mm mounting grid with M3 screws; that is not a PCB-hole specification. V7 supports a Pi, with a Pi 4 PoE-pin warning. |
| [1833926: BayMesh3 weatherproof-box bracket][C4] | Uncle Lit | **2 STL files** | CC BY-SA | Two-piece mounting bracket remixing Mattchew's baseplate and beanfield's filter mount. It mounts hardware inside another box; it does not establish weather sealing itself. |
| [1855194: Meshtastic/MeshCore enclosure][C5] | beanfield | **12 STL files** | CC BY-SA | Preferred reference: complete desktop shell, three faceplates, two hatches, two alternate plates, four spacers. Four actual meshes measured below. No STEP/native CAD appears in its inspected file inventory. |

The reported CC license **versions remain unverified**. Preserve attribution and applicable ShareAlike terms; C1/C2 also specify Noncommercial. Reconstructing parametric CAD from their geometry does not automatically remove those conditions. Do not silently combine C1/C2 geometry into a design claimed to be unrestricted commercial-use CAD. Confirm the full license terms and upstream attribution before publishing a derivative. No downloaded third-party files are included in this research directory.

C1's author states a **59.5 × 126.5 mm external case mounting pattern** and **0.5 mm extra room** in loose variants, without defining which axes or whether that allowance is total/per side. These are author claims about enclosure geometry, not Station G3 mounting coordinates. The author uses M3 hardware for their case/board attachment. Do not confuse that with C5's M2.5 standoff assembly.

C3's listing photograph shows a Station G3 fitted on a printed baseplate. C1's photograph shows an assembled case. Such evidence supports those examples, not guaranteed fit across revisions. The C2 correction and C1 loose variants are reasons to retain a physical-fit check.

## Preferred reference: 1855194

The author describes a desktop enclosure with all ports exposed, an optional vented heatsink guard, and a PA-jumper hatch. They credit an earlier G2 enclosure by **Alley Cat** as the design's origin, redesigned for G3. This is enclosure lineage, not evidence of G2/G3 board interchangeability. [C5]

### Author-specified hardware and features

| Feature | Stated value | Evidence class / interpretation |
|---|---|---|
| RF-side standoffs | 3 × M2.5, **12 mm body + 4 mm stud** | Community-author specification; separate body length from stud length. |
| MCU-side standoffs | 4 × M2.5, **7 mm body + 4 mm stud** | Community-author specification. |
| Faceplate screws | 6 × M2.5 × 6 mm | Author's assembly, not a general board specification. |
| Hatch screws | 2 × M2.5 × 3 mm | Author's assembly. |
| Optional guard rise | 6.4 mm above faceplate | Author-stated, not measured in this investigation. |
| Antenna spacers | Heights 1, 1.5, 2, 2.5 mm; Ø10 to Ø9 taper, Ø6.5 bore | Author-stated. The 1 mm file's outer envelope was checked. |
| Optional sensor | Hatch provision for Adafruit BME280/BME680 | Author claim; sensor fit and cable route not checked. |

The author explicitly warns that different standoff or stud lengths will prevent correct assembly. Stock standoff dimensions have not been physically verified. [C5]

### Downloaded geometry: measurements, not board specifications

Used the original Printables downloads with file IDs below; verified their byte counts against API metadata and computed SHA-256 checksums. Parsed STLs with **trimesh 4.12.2 / NumPy 2.5.3** under the repository's locked environment. All four inspected meshes were watertight.

Rendered and inspected the backplate's isometric, top, bottom and front views with the repository preview command. The top view shows the seven perimeter mounting openings and separate interior support features; the bottom view is closed. Section-loop measurements above the floor must not be mislabeled as through-holes.

| File | API file ID | Native XYZ extents | Triangle count | Evidence |
|---|---:|---|---:|---|
| `SG3-01-Case.stl` | 7750403 | **70.60 × 122.20 × 22.30** | 475160 | Measured mesh bounds. |
| `SG3-02a-Faceplate-Plain.stl` | 7750400 | **65.00 × 118.07 × 6.50** | 69720 | Measured mesh bounds. |
| `SG3-04-Backplate.stl` | 7750399 | **65.00 × 112.00 × 6.50** | 40774 | Measured mesh bounds. |
| `SG3-06a-AntennaSpacer-1.0mm-TPU.stl` | 7750394 | **10.00 × 10.00 × 1.00** | 1024 | Measured mesh bounds; agrees with the author's Ø10/1 mm specification. |

**Units:** STL stores no unit declaration. Treating native coordinates as millimeters is supported by the named 1 mm spacer measuring exactly 1 native unit high and 10 units across. It is not a physical calibration. Decimal precision above describes file geometry, not manufacturing accuracy. Extents of separately oriented files cannot be added to obtain assembled height.

### Coordinate contract and recovered mounting pattern

Backplate datum: retain original file axes. Origin is the center of its XY bounding box on its lowest Z plane. X spans **−32.5…32.5**, Y **−56…56**, and Z **0…6.5**. View from +Z toward the base, with +X to the right and +Y up. These are file coordinates; no independent manufacturer datum or physical compass direction has been established.

At **Z=1.5**, intersect the backplate mesh with an XY plane. For each closed section loop, fit `x²+y² = 2cx·x + 2cy·y + c`; derive radius as `sqrt(c + cx² + cy²)`. Seven loops have approximately Ø2.50 spans, a least-squares fitted diameter around 2.499, and maximum radial residual below 0.001 native unit. Polygon facets explain the small difference from 2.50. Other noncircular loops are not classified as holes.

| Hole label | X | Y | Section reference | Opening diameter |
|---|---:|---:|---|---|
| H1 | −29.00 | −52.50 | Z=1.5 | approximately 2.50 |
| H2 | 29.00 | −52.50 | Z=1.5 | approximately 2.50 |
| H3 | −29.00 | −29.50 | Z=1.5 | approximately 2.50 |
| H4 | 29.00 | −29.50 | Z=1.5 | approximately 2.50 |
| H5 | −29.00 | 52.50 | Z=1.5 | approximately 2.50 |
| H6 | 2.30 | 52.50 | Z=1.5 | approximately 2.50 |
| H7 | 29.00 | 52.50 | Z=1.5 | approximately 2.50 |

Values are **derived from community mesh geometry**, in presumed mm. H1–H4 span **58 × 23 mm** center-to-center. H1–H5 span **105 mm** in Y. H6 is **not centered at X=0**. This labels section openings, not verified PCB holes; it does not establish threads, through/blind depth, or countersink geometry.

**Independent part cross-check:** all seven corresponding shell openings match this pattern after **X_shell=X_backplate, Y_shell=Y_backplate+1.30**. Shell section Z=1.5 gives approximately Ø2.50 with maximum radial residual below 0.00001. This confirms a shared XY mounting pattern within this design and demonstrates that its exported parts have different local origins. It does not establish their assembled Z transform. Do not assemble files by blindly matching their raw origins.

### STEP comparison actually exercised

Downloaded C1 file **7641511**, `g3 case (hardware).step`, 160952 bytes. build123d **0.13.0** imported it as **one valid solid**, with analytic circular edges rather than only tessellated boundaries. Native bounds were approximately X −69.24478…68.25522, Y −35.75…35.75806, Z −3…20. These belong to that different enclosure; they are not the preferred case's dimensions or a G3 board model. This demonstrates that editable solid geometry is available as an alternative to mesh reconstruction. No source feature/history tree was supplied by this STEP file.

## Original-download provenance

Download URLs below identify inspected bytes. Regenerate links through Printables if they expire. Original listings and file IDs remain the primary provenance. Downloads were inspected in ignored scratch storage; no redistribution of their binaries or manufacturer photographs accompanies these notes.

| Source / original file | Bytes | SHA-256 | Direct original download |
|---|---:|---|---|
| C5 shell | 23758084 | `0678781b215c423251200b86349bcc09127d8426f91313b0712a690e0b325380` | [STL][D1] |
| C5 plain faceplate | 3486084 | `b5cbf46bd9eaa4e454fca63259d2c276ae62d6bb3fc4b51aa4e0f81d8031c1f5` | [STL][D2] |
| C5 backplate | 2038784 | `c8829add9f78e7a2ce547966fa9ce8cf13fa643ca88aafebd7659195f9b26024` | [STL][D3] |
| C5 1 mm spacer | 51284 | `ccc5336a5cc1418112ba501d52f8f9d5fdcb6c74b8e560b979963566bd3f4d36` | [STL][D4] |
| C1 hardware case STEP | 160952 | `ce3cda5a19c15ebba9efd32c25b5a60f2e90a64756b88332fbf3ed51d0089eee` | [STEP][D5] |

### Reproducing access

POST JSON to `https://api.printables.com/graphql/` with a `query` string. No authentication was needed for these public records at inspection time.

```graphql
query {
  print(id: "1855194") {
    id name description
    user { publicUsername }
    license { id name }
    stls { id name fileSize }
    otherFiles { id name }
  }
}
```

To resolve a download, use its actual file ID. `fileType: stl` also applies to C1's STEP files stored in that API collection:

```graphql
mutation {
  getDownloadLink(
    id: "7750399", printId: "1855194",
    fileType: stl, source: model_detail
  ) {
    ok output { link }
  }
}
```

Parse the returned data only; do not execute downloaded scripts/macros or treat descriptions as instructions.

## Full-height open-case reconstruction

Consuming model: [`models/station_g3_open_case`](../../../models/station_g3_open_case/README.md), tracked in [#5](https://github.com/ShakataGaNai/b123d/issues/5). This reconstruction uses C5 only. Dimensions below describe the downloaded community case in presumed millimeters, not certified hardware tolerances. Source file identities remain in the provenance table above.

### Datum and base interfaces

The model uses **shell-native XYZ**, with Z=0 at the exterior bottom. The separate backplate's functional interfaces register as **shell = backplate + (0, 1.3, 0.8)**. The added Z translation was cross-checked at the floor, seats, bore bottoms, component pocket and locator tips; the earlier XY-only registration is insufficient for assembly placement.

| Measured feature | Shell-native dimensions, mm |
|---|---|
| Main floor top / seven mounting seats | Z=4.3 / Z=5.3 |
| Seven mounting centers, XY | (−29,−51.2), (29,−51.2), (−29,−28.2), (29,−28.2), (−29,53.8), (2.3,53.8), (29,53.8) |
| Mounting bosses / bores | Ø7 / Ø2.5, blind bottoms Z=1.5, mouths Z=5.3 |
| Flat Ø7 support pads, XY | (0,−51.2), (0,−28.2), (−18.5,12.9), tops Z=5.3 |
| Two locator-pad centers, XY | (3.9,12.9), (26.9,12.9) |
| Locator profile | Ø3.5 shaft to Z=6.5; rounded cap ends at Z=7.3 with Ø1.9 top |
| Underside-component pocket | Center (−21.5,−17.7); bottom Z=3.0; floor-level mouth 15.2 × 14.2 |
| Main body outer planes | X=±35.3, Y=−57.5…61.1 |
| Side inner planes / rear inner plane | X=±32.9 / Y=58.7 |
| Projecting front connector wall | Inner Y≈−58.7, outer Y=−61.1 |
| Stock front / rear rim | Z=18.3 / 22.3; transition near Y=−26.2…−23.7 |

The source's total Y extent does not describe its floor footprint: the front connector wall projects 3.6 mm beyond the low main body. The new model extends the floor to this wall and keeps its connector space. Moving the wall inward to Y=−57.5 would risk hardware interference.

The new uniform 22.3 mm rim raises the front by 4 mm. Its external footprint is 70.6 × 122.2; the cavity is 65.8 × 117.4. The model replaces rounded locator caps with smaller conical lead-ins, preserves the full component-pocket mouth down to Z=3.0, and uses a flat outside bottom. These are design changes, not measured stock geometry.

### Connector and button apertures

For X walls, `u` is world Y; for Y walls, `u` is world X. Width is horizontal in that wall, height is Z. Profiles below are the minimum through-openings, before exterior relief.

| Interface | Wall | Center (u,Z), mm | Width × height / diameter, mm |
|---|---|---|---|
| DC5521 power | −X | (−17.70,13.85) | Ø8.02 |
| Motherboard USB-C power | −X | (−5.70,8.90) | 9.02 × 3.02 capsule, R1.51 |
| Power-good test button | −X | (4.30,8.95) | 3.62 × 3.52 |
| Four power-good LED windows | −X | (8.60,7.60), (10.60,7.60), (12.60,7.60), (14.70,7.60) | Each 1.02 × 2.02 |
| Grove nearer MCU | +X | (1.30,11.40) | 12.02 × 8.02 |
| Grove nearer antenna | +X | (24.30,11.40) | 12.02 × 8.02 |
| Additional MCU side button | +X | (−40.30,12.55) | 7.02 × 3.52 |
| MCU firmware-download button | −Y | (−24.50,12.55) | 7.02 × 3.52 |
| MCU USB-C communication | −Y | (−14.05,12.80) | 9.02 × 3.02 capsule, R1.51 |
| MCU restart button | −Y | (−3.60,12.55) | 7.02 × 3.52 |
| Antenna insertion notch | +Y | X=12.90 | Width 6.42; Z=15.09 through open rim |

The source MCU button corners have R≈1.01. The new rectangular cuts enclose those profiles. Grove/PG corners have R≈0.01; their rectangular replacements do not reduce the measured openings. The antenna is an **open-top notch**, not a closed circular hole.

The [official wiki][S1], its [motherboard pinout photograph](https://wiki.bqvoy.com/devkits/station-g3/station_g3_pinout.jpg), and C5's [MCU photograph](https://files.printables.com/media/prints/3f6701e4-8248-4ceb-9507-07d66fb04326/images/13911493_9661b095-c534-4928-bdeb-1b46bd8e5816_14e9734e-9982-459e-be3d-6dc99a0b11f0/pxl_20260919_143739590macro_focus.jpg) support the functional mapping. The additional side button shows an info/user icon; its firmware behavior is unverified. The two sockets are Grove; this record does not substitute Qwiic connector dimensions or assign GPS/I2C to an uncertain physical order. PG means power-good test, not an on/off switch. The MCU communication USB-C has manufacturer power restrictions; mechanical access does not authorize powering it.

### Exterior cable and antenna relief

Sections show core apertures unchanged through |X|=33.97 or |Y|=59.77, with enlarged recesses immediately beyond. These shoulders leave a **1.07 mm inner lip**. The reconstruction uses constant rectangular shallow pockets from those planes outward:

| Pocket | In-plane bounds, mm | Z bounds, mm | Evidence |
|---|---|---|---|
| Shared DC/power USB, −X | Y=−24.7…1.8 | 4.4…20.85 | Conservative analytic envelope from measured flare; source rounding merges the outer contour |
| PG button, −X | Y=2.18…6.42 | 6.88…11.02 | Closed section at X=−35.2 |
| Grove nearer MCU, +X | Y=−7.6…10.2 | 4.5…18.3 | Closed near-mouth section at X=35.29 |
| Grove nearer antenna, +X | Y=15.4…33.2 | 4.5…18.3 | Closed near-mouth section at X=35.29 |
| MCU side button, +X | Y=−46.7…−33.9 | 7.9…17.2 | Analytic mouth envelope; upper source contour merges with rounding |
| Shared MCU front controls, −Y | X=−30.9…2.8 | 7.9…17.2 | Measured lower boundary at Y=−61.09 plus analytic flare envelope |
| Antenna nut/base, +Y | X=2.8…23.0 | 9.8…open top | Conservative envelope of near-mouth curved relief |

These rectangular replacements remove more exterior material than the source curved pockets while retaining the small through-apertures. The lowest pocket remains above the Z=4.3 floor. At Y=61.09, the antenna relief's lower curve reaches Z≈9.8935 and fits an ellipse centered at (X,Z)=(12.9,20.9) with semiaxes ≈(10.0095,11.0075); the model retains an enclosing rectangular access envelope, not that exact surface.

### Measurement method and verification

Measured the original STL with trimesh/NumPy under the locked environment, preserving coordinates. Used horizontal sections and planar triangle normals for floor/seat levels; radial extrema and endpoint Z for bores/pins; X=±33/±33.5 and Y=−59/−59.5 for port cores; fine shoulder sections and near-exterior sections for flares. Matched corresponding features across the shell and translated backplate rather than aligning bounding-box centers.

Plane and center coordinates agree to about 0.00001 mm within these files; a Ø7, 64-sided contour has roughly 0.00422 mm radial facet sag. Values rounded to 0.01 mm describe file reconstruction precision, **not manufacturing tolerance**. The independent reusable [STL measurement helper](../../../.agents/skills/stl-measurement/SKILL.md) recovered seven backplate mounting contours above the blind floors, none at Z=0.5, and a shell DC circle centered near (−17.70,13.85) with fitted diameter 8.01982.

The consuming model exported as one valid native/STEP solid and a watertight, single-body STL. Its interface checks passed on both native and reimported STEP geometry. The PNG and HTML were inspected, including external power/Grove/front-button recesses and the open antenna path. No physical fit or thermal test was performed.

## Modeling decision and unresolved fit requirements

1. Reconstruct a small, parametric build123d model from measured planes, hole centers and analytic dimensions rather than turning hundreds of thousands of mesh triangles into CAD faces. Keep source geometry separate from chosen print allowances.
2. Prefer C5's functional arrangement and M2.5 standoff scheme for the requested reference. Use C1 STEP as a separately licensed alternative, not an unexplained mixture of parts.
3. Before a fit claim, identify the physical motherboard/MCU/RF revisions; confirm mounting centers, PCB thickness/underside keep-outs, standoff body/stud lengths, and complete assembly height.
4. Confirm plug insertion/bend clearance, button travel, jumper/tool access, OLED and heatsink clearance on the physical assembly. The reconstruction above retains measured case openings, but no authoritative complete hardware solid or physical test establishes clearance to the real device.
5. Verify physical fit with a mounting/cutout coupon before printing a complete enclosure. Check thermal behavior for the intended radio operation. A vented desktop case is not weatherproof.

No physical specimen measurement, print, thermal test or exact-revision fit has been performed. The open-case model and its exports now exist; its metadata links this record. The earlier research-only conclusions remain source evidence, not a fit certification.

## Sources

All sources accessed 2026-10-01. Official document publication/revision and tolerances are unknown except the explicitly noted hardware markings. Community model-file revisions are identified by current file IDs, filenames and checksums rather than assumed to match board revision numbers.

[S1]: https://wiki.bqvoy.com/en/devkits/station-g3
[S2]: https://store.bqvoy.com/product/mesh-device-station-edition/
[S3]: https://pro.bqvoy.com/product/motherboard-for-station-g3/
[S4]: https://pro.bqvoy.com/product/motherboard-with-bq35lora900v1m-rf-daughterboard-for-station-g3/
[S5]: https://pro.bqvoy.com/product/bq35lora900v1m-rf-daughterboard-module/
[S6]: https://tools.bqvoy.com/stationg3/pinout/?board=BQESP32V1M-40pin
[S7]: https://api.github.com/users/neilhao/repos?per_page=100
[C1]: https://www.printables.com/model/1816444-bq-station-g3-case
[C2]: https://www.printables.com/model/1818451-bq-station-g3-case-with-snap-fit
[C3]: https://www.printables.com/model/1807804-bq-station-g3-baseplate
[C4]: https://www.printables.com/model/1833926-station-g3-baymesh3-bracket-for-weather-proof-box
[C5]: https://www.printables.com/model/1855194-station-g3-case-meshtastic-meshcore-enclosure
[D1]: https://files.printables.com/media/prints/93c513b8-f804-4a94-be4d-801ac9a67675/stls/13911104_30a8f245-d7ea-4bb8-913b-210ad1ebef48_00edb86e-afb6-4f29-9ad3-41bbbef3d415/sg3-01-case.stl
[D2]: https://files.printables.com/media/prints/ce7e01bb-08a6-451d-991b-bc877fd1b496/stls/13911106_19ebb95c-27b9-4d4d-9f0c-0800c548637b_8ab157a2-9b0a-4ee5-b722-49271a54cfb2/sg3-02a-faceplate-plain.stl
[D3]: https://files.printables.com/media/prints/b58423b5-180a-4101-97f6-887f2866b709/stls/13911100_0e12b73b-3a55-465c-83ab-31c6182c4dee_c66a3df6-8109-45cc-a15f-b19a018ba223/sg3-04-backplate.stl
[D4]: https://files.printables.com/media/prints/c1d586f2-dfd9-491f-af9c-544e4613352f/stls/13911097_78e88a55-9da4-4e55-9831-aa33158860fa_4557af24-53af-4d00-ae91-c7e72e7f6925/sg3-06a-antennaspacer-10mm-tpu.stl
[D5]: https://files.printables.com/media/prints/1d563eb4-2a39-468e-b901-e29846e1d39b/stls/13725586_61eb999c-363a-4629-8c1d-a81b48010d89_a408af47-c29a-45a2-be34-d55b5053e4de/g3-case-hardware.step
