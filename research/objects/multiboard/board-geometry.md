# MultiBoard board, plate, and tile geometry

## Identity, scope, and readiness

- Publisher: MultiBoard LTD; current public ecosystem name **MultiBuild** and board subsystem **MultiBoard**. Research accessed **2026-10-01**.
- Scope: official board/tile/plate placement geometry and the evidence needed for future build123d adapter mating. This is not an adapter implementation, a complete dimensioned vendor catalog, or a physical specimen measurement.
- Exact examples investigated: Thangs models **977706** (currently *10x10 MU – Center Grid Interfitted – MultiBoard Octagon Plate*, description still *Core Tile*), **977727** (*10x10 Multiboard Corner Legacy Tile*), **1321449** (currently *6x6 MU – Top Right Grid Interfitted – MultiBoard Octagon Plate*, description still *Corner Border Tile*), **1320746** (*8x8 MU – MultiBoard Octagon Plate*, description still *Single Border Tile*), and **1306830** (*8x8 MU (4x4 LU) – MultiBoard Square Plate*, description still *Multibin Plate*). [B3–B7]
- **Ready for nominal grid planning on the documented octagon/tile family. Not ready to regenerate an exact board hole, snap-retention profile, or thread from these notes alone.** Separate adapter routes using purchased/printed stock connectors or an independently documented existing-holder connector are not globally blocked by that gap; they need their own connector and fit evidence. No claim of cross-revision interchangeability follows from a similar holder outline.
- No vendor CAD, STL, drawing, poster, or upstream code is committed here. Original-asset redistribution is prohibited by the current license; public access is not an open-source grant. These notes are original analysis with incidental source links. [B11–B13]

## Sources and provenance

All sources below were accessed **2026-10-01**. Publication date and geometry/file revision are **unknown unless stated explicitly**. A listing ID identifies a page, not immutable file bytes. Dates such as “3 years ago” are not used as revision identifiers. Official web documentation declares `current`, not a board engineering revision.

| ID | Publisher / source | URL and locator | Publication / revision evidence | License / use evidence |
|---|---|---|---|---|
| B1 | MultiBuild Knowledge Hub, Core Parts Documentation | [Core parts](https://docs.multibuild.io/beginner-section/core-parts-documentation), Measurement System; MultiBoard §§1, 4, 5; MultiBin §7 | Undated current page; no dimensioned board drawing or model-file revision provided | Official documentation; current license includes documentation in Designs; see B11–B12 |
| B2 | MultiBuild, current plate selector | [MultiBoard Plates](https://multibuild.io/parts/multiboard-plates); browser-loaded filters and exact model links | Dynamic current catalog; page revision unknown | B11–B12; filter labels are not dimensional drawings |
| B3 | MultiBuild / Jonathan K, octagon center/core example | [Thangs 977706](https://than.gs/m/977706), description and Printing Guidelines | Public page `__NEXT_DATA__.props.pageProps.fallback["v4/models/977706/stats"].published` = **2023-12-23T14:54:12.103Z**; geometry revision unknown. Current title and older Core wording coexist | Page says restricted licensing; B11–B12 |
| B4 | MultiBuild / Jonathan K, legacy corner example | [Thangs 977727](https://than.gs/m/977727), description | Exact publication date unknown; title explicitly Legacy; no file revision recovered | Restricted licensing; B11–B12 |
| B5 | MultiBuild / Jonathan K, border corner example | [Thangs 1321449](https://than.gs/m/1321449), description | Exact publication date and file revision unknown; old descriptive title redirects to current Octagon Plate title | Restricted licensing; B11–B12 |
| B6 | MultiBuild / Jonathan K, regular single-border example | [Thangs 1320746](https://than.gs/m/1320746), description | Exact publication date and file revision unknown | Restricted licensing; B11–B12 |
| B7 | MultiBuild / Jonathan K, square plate example | [Thangs 1306830](https://than.gs/m/1306830), description | Exact publication date and file revision unknown; current title uses MU/LU, description uses Multibin Plate | Restricted licensing; B11–B12 |
| B8 | MultiBuild, legacy selector | [Legacy Parts](https://multibuild.io/parts/legacy-parts), browser-loaded Legacy Part / Legacy Tile Type filters | Current live catalog classification, not a dated supersession drawing | B11–B12 |
| B9 | MultiBuild, official remix route | [Remixing Files](https://multibuild.io/parts/remixing-files), Tile Components → STEP or STL | Current live route; [old remix URL](https://www.multiboard.io/parts-library/remixing) redirected here | B11–B12 |
| B10a | MultiBuild / Jonathan K, Tile Components – STEP Multiboard Remixing Files | [Thangs 994681](https://than.gs/m/994681), description, Download, public page metadata | `v4/models/994681/stats.published` = **2024-01-19T16:59:08.140Z**. Exact member filenames, modification dates, byte hashes, and geometry revisions unknown: original files not retrieved | Restricted licensing, with external license link to B12. Browser Download opened login; public `can-download` metadata alone does not deliver file bytes |
| B10b | MultiBuild / Jonathan K, Tile Components – STL Multiboard Remixing Files | [Thangs 994663](https://than.gs/m/994663), description | Exact publication date and file revisions unknown; vendor description's unfinished “including…” is not a component inventory | Restricted licensing; B11–B12 |
| B11 | MultiBuild License summary | [License](https://multibuild.io/license), Original Designs / Remixed Designs / Footnotes | Undated current summary; explicitly not the legal license | No sharing original Designs; personal modification and qualifying remixes described |
| B12 | MultiBoard LTD, full MultiBuild Licence | [Legal document](https://docs.google.com/document/d/1C0-Iyxydqk_d2I3o_5ualJ9Ywt9gwVdl9eukvC8JeKA/); accessible [plaintext export](https://docs.google.com/document/d/1C0-Iyxydqk_d2I3o_5ualJ9Ywt9gwVdl9eukvC8JeKA/export?format=txt), §§3–4 | States **last updated 19/December/2025** | Original Designs may not be redistributed; substantial-change remix conditions, attribution, and retained underlying rights apply. §4 allows reasonable incidental links for discussion/review/education; do not turn this record into a substitute design repository |
| B13 | MultiBuild, Community Promise summary | [Community Promise](https://multibuild.io/community-promise), Relationship to Licence | Undated current summary; full legal promise linked from page | Materials remain under MultiBoard Licence until a triggering event. This research establishes no triggering event and makes no CC0 claim |
| B14 | MultiBuild Knowledge Hub, Printing Guidelines | [Printing guidelines](https://docs.multibuild.io/beginner-section/printing-guidelines), Default Settings / Ironing Stack Printing | Undated current page | B11–B12 |
| B15 | MultiBuild Knowledge Hub, mounting guide | [Tile mounting guide](https://docs.multibuild.io/beginner-section/tile-mounting-guide), advanced installation | Undated current page; mounting illustrations are not dimensioned engineering drawings | B11–B12 |
| B16 | MultiBuild Knowledge Hub discovery | [Hub](https://docs.multibuild.io/), [sitemap](https://docs.multibuild.io/sitemap.xml), [Common Connections](https://docs.multibuild.io/beginner-section/common-connections) | Hub says documentation is still developing. Accessed sitemap exposed beginner pages, not a dimensioned advanced engineering spec | B11–B12 |

### Evidence classes

**Authoritative** = explicit publisher statement, within its stated family/revision scope; not a physical-fit guarantee. **Measured** = identified physical specimen measurement; none was performed here. **Derived** = arithmetic, safely parsed CAD/mesh geometry, or coordinate construction using identified sources, with qualifications. **Assumed** = a local modeling choice, never promoted to a vendor dimension. Unknowns remain unknown, not nominal zeros.

## Geometry facts and dimension table

Source/model length units are **millimeters**. Pitches are **center-to-center placement distances**, not hole diameters. Threads require major/minor/pitch diameter distinctions; an octagonal snap opening additionally requires across-flats/across-corners dimensions and depth-dependent sections. No single “hole diameter” is adopted for the Multihole.

| Feature / symbol | Value and size convention | Tolerance / uncertainty | Class | Evidence / exact scope | Consequence |
|---|---|---|---|---|---|
| Multi Unit, `MU` | **25 mm**, nominal modular sizing | No MU dimensional tolerance stated | Authoritative | B1, Measurement System | Grid/module unit, not guaranteed part envelope |
| Tile / octagon family large-hole pitch, `pL` | **25 mm** between Multiholes | No hole-position tolerance stated | Authoritative | B3 and B4 explicitly say big holes are 25 mm apart; B1 calls tiles based on a 25 mm grid | Same-family neighboring grid centers can be laid out; retain target variant's actual presence/absence mask |
| Tile / octagon family small-hole pitch, `pS` | **25 mm** between Pegboard Holes | No hole-position tolerance stated | Authoritative | B3 and B4 separately say small holes are 25 mm apart | This does **not** determine small-grid phase relative to large grid or to the perimeter |
| Cell Unit, `CU` | **50 mm**, nominal modular sizing; `2×2 MU = 1×1 CU` | No tolerance stated | Authoritative | B1, Measurement System | Do not substitute this cell spacing for the tile's small-hole pitch |
| Square plate cell spacing | **50 mm** between cells | No cell-position tolerance stated; source says “Each cell is 50 mm apart” without a dimensioned center datum | Authoritative nominal layout | B7, square plate 1306830 | Distinct square/bin-support surface; not an octagon hole definition |
| DS Offset Snap Mount surface separation | **6.25 mm**, nominal offset from mounting surface | No reference-face drawing or offset tolerance supplied | Authoritative | B1 §2.2, specific Part A variation | Mount-dependent offset, **not** board thickness or automatic allowance for every wall mount |
| Vendor design “tolerance” wording | **0.25 mm** | Radial vs diametral vs per-face vs total allowance **unknown**; not stated as `±0.25 mm` | Authoritative wording; interpretation unknown | B3–B7 Printing Guidelines; B14 says **most** parts | Do not add a blanket CAD offset or claim a hole-position tolerance from it |
| Ironing-stack separation | **0.2 mm gap** between prints | No process/actual gap tolerance stated | Authoritative | B14, Ironing Stack Printing | A stack's bounding-box height is not a single board's thickness |
| Example nominal modular span, current regular 8×8 octagon plate | **200 mm × 200 mm** modular span = `8 × MU` in each in-plane direction | Actual perimeter and edge offsets unknown | Derived | B6 identifies 8×8 MU; MU from B1 | For layout only; **not** an observed bounding box or bed-clearance measurement |
| Example distance over `k` consecutive octagon-grid steps | `d = |k| × 25 mm` along a grid axis | Inherits unstated pitch/position tolerance; no production bounds | Derived | B1 + B3/B4 | Supported relative-center placement only |
| Board thickness, `t` | **unknown** | Not measured; no applicable dimensioned section recovered | Unknown | B1–B10 examined | Required before wraparound, rear engagement, and through-fastener depth decisions |
| Overall perimeter / edge-to-center offsets | **unknown**, variant-specific | Rounded/chamfered/interfitted/straight-border bounds not quantified | Unknown | B2–B8 | Do not use `MU count × 25 + a guessed border` |
| Small-grid phase `(δx, δy)` from large-grid origin | **unknown** | Visual interstitial layout is not a dimensioned coordinate source | Unknown | B1 illustrations and B3/B4 pitch statements | Do not silently set half-MU offsets |
| Large-hole opening cross-sections | **unknown** across flats, across corners, thread major/minor diameters, chamfers, lip/undercut heights | No permitted original CAD bytes inspected | Unknown | B1 and B10a establish function/file route, not section dimensions | Cannot reconstruct board snap retention from grid spacing |
| Small-hole diameter/profile | **unknown** diameter(s), relief/chamfer, thread form/depth | “Pegboard compatible” is not a dimensional standard citation | Unknown | B1 §1.1, B3/B4 | No universal commercial peg diameter adopted |
| Large / small internal thread definitions | **unknown** major/minor/pitch diameters, lead, pitch, starts, handedness, flank form, runout, engagement depth | No applicable thread drawing recovered | Unknown | B1 §5, B3/B4 | Names “Large/Big” and “Small” do not mean an ISO metric thread size |
| Screw-on wall mounting fastener holes | **unknown** centers, bore size, countersink geometry for a selected mount | Mount separate from tile, dependent on mount variant | Unknown | B1 §2.2; B15 | Do not call every tile small hole an ordinary screw clearance hole |

No numerical board diameter, thread pitch, nominal board thickness, edge increment, or retention depth from community code, a photograph, or search-engine summary is accepted as authoritative here.

### Hole geometry and placement semantics

The official tile illustration distinguishes a polygonal **Large Hole / Multihole** and a **Small Hole / Pegboard Hole**; both hole families are threaded. Large Holes accept board Snaps and Large Threads; Small Holes accept Peg Click, Small Threads, and non-printed pegboard accessories. A **Mid Hole** is normally in a **Snap**, not a third hole family automatically present in the base tile. [B1 §§1, 2.3, 4, 5; B3–B4]

B3 and B4 state the tile is symmetrical on both sides. That supports intended two-sided use for those described tile families, not an undocumented symmetry plane, exact Z datum, or identical printed quality. B14 specifically warns that a stack-printed tile can have a less clean side. The core diagram and poster were viewed, but neither provides a dimensioned cross-section; no pixel measurement was performed. [B1; B3–B4; B14]

The threaded openings are not modeled as simple smooth cylinders for fit. Through/blind status, start location on each face, chamfer extent, internal relieved volume, and useful thread engagement still require revision-specific CAD/measurement. A visual see-through opening does not establish the length of its full mating profile.

## Local coordinate contract — conventions, not new source facts

Use this **local assembly frame** for future octagon/tile adapter work. The choices below are local modeling conventions; import coordinates may differ.

1. Select and label a real target **large-hole center** `L00` and the board's accessory/front face. Let `O` be that center projected onto the chosen front datum plane. Set `O = (0, 0, 0)` by definition.
2. Viewed from the accessory side, choose `+X` toward a neighboring large hole to the right, `+Y` toward a neighboring large hole above, and `+Z` outward toward the accessory. The grid rows/columns determine in-plane axes; any angular registration needed by an octagonal or directional connector must be established from its CAD/features separately.
3. Define the front reference plane as `Z = 0`; if a uniform overall thickness `t` is later measured, the back envelope is `Z = -t`. Do not infer `t`, thread seating depth, or the board midplane from these definitions.
4. Transform the imported board/connector to this frame using the identified face, axis, and centers. Record the transform and STEP length unit or mesh unit evidence. Do not assume an STL declares millimeters.
5. Preserve a **hole-presence mask** for the selected variant. A mathematical lattice point is not proof that a full mating hole exists there, particularly at seams and cut edges.

For a supported orthogonal tile-grid region, relative large-hole centers can be represented as:

`L(i,j) = (i × pL, j × pL, 0)`, with `pL = 25 mm`. [Derived from B1's 25 mm grid and B3/B4's large-hole spacing; indexing and origin are local conventions.]

The small-hole family must retain its unresolved phase:

`S(a,b) = (δx + a × pS, δy + b × pS, 0)`, with `pS = 25 mm`, **δx and δy unknown**. [Derived placement form from B3/B4; no local numeric cross-family registration claimed.]

| Local center ID | X | Y | Reference | Meaning / evidence |
|---|---|---|---|---|
| `L00` | 0 | 0 | Front datum, mm | Local origin by definition, not an edge datum |
| `L10` | 25 mm | 0 | Same datum | Derived neighboring grid center, only if the selected variant contains it |
| `L01` | 0 | 25 mm | Same datum | Derived neighboring grid center, same qualification |
| `L11` | 25 mm | 25 mm | Same datum | Derived square-grid location, same qualification |
| `S00` | δx, unknown | δy, unknown | Same datum | Do not fill with a guessed interstitial offset |

These coordinates locate mating **axes**, not diameters, fillets, thread phase, or snap shoulders. Radius conversion would be `r = diameter / 2` only after a sourced diameter exists. No radius is currently specified. An edge-origin coordinate system remains blocked until the appropriate variant's edge-to-center dimensions are recovered.

## Current versus legacy geometry and naming pitfalls

The current [plate selector](https://multibuild.io/parts/multiboard-plates) exposes **Surface Connection: Octagon Plate, Square Plate, Other Plates**. It separately exposes **Outer Shape: Regular, Interfitted, Triangle**, interfit layout **Grid / Horizontal Strip / Vertical Strip**, grid position **Center / edges / oriented corners**, strip position **ends / centers**, and stack count. These are selection axes, not evidence that every combination has the same geometry. [B2, browser-loaded filters]

For Other Plates the selector names Plain, Thin Plain, Small Thread SU, Small Thread MU, Small Thread Offset MU, Small Thread LU, Mid Hole/Small Thread MU, and Fix Point Hole MU. This note does not assign dimensions to **SU/LU**, infer Thin Plain thickness, or treat Offset MU as a known XY phase; those names alone do not specify a mating drawing. The square-plate listing explicitly identifies its 50 mm cells and bin/Plate Snap/Dual Clip connections. **“Square Plate” does not mean a square-shaped octagon tile.** [B2; B7]

| Family/example | Confirmed source description | Adapter risk |
|---|---|---|
| Center grid/interfitted octagon plate, 977706 | Still described as Core Tile; has pegboard holes on two sides and forms the board's main region | Current title can change without a new ID. Need file bytes to know whether geometry changed too; two-sided edge pattern cannot be extrapolated to every perimeter |
| Legacy corner tile, 977727 | Explicit Legacy title; described as having no pegboard holes on its sides | Its edge profile/hole mask is not the current oriented border-corner profile by default |
| Current oriented border corner, 1321449 | Creates straight border; four oriented corner choices plus edge-border and core tiles make a full board | Corner orientation and seam choice affect usable attachment holes and clearance |
| Regular single-border plate, 1320746 | Nice borders on all sides; can make an entire board, but small thread holes **between tiles will be missing** | A peg/small-thread adapter spanning a seam can fail even when large-grid spacing is correct |
| Square plate, 1306830 | Supports bins, Plate Snaps and Dual Clips; 50 mm cells | Requires its own connection geometry, not direct reuse of a board-Multihole profile |

The [Legacy Parts selector](https://multibuild.io/parts/legacy-parts) explicitly contains Legacy Tile, Legacy Stack, Legacy Tools, and a separately named **8mm Legacy Parts** group; Legacy Tile Type includes Corner and Side. **The “8mm Legacy Parts” category name is not evidence that a legacy tile is 8 mm thick.** [B8, browser-loaded filters]

No exact effective date for a tile-profile change, complete dimensioned legacy/current comparison, or vendor guarantee that all old and new mating profiles are identical was recovered. The homepage's compatibility assurance is not a substitute for revision-specific fit evidence. Retain publisher, exact listing ID, current title, downloaded filename, publication timestamp if available, asset hash, selected edge/stack variant, and measured interface sections when future geometry is obtained.

### Rejected numeric leads

A search result attributed **257.32 mm** to the official legacy corner example. Reading B4 showed this number is in a **user comment about a side tile's long side**, not the publisher's corner-tile specification. It is excluded from the authoritative and measured geometry tables. Likewise, secondary parametric remixes' generic thickness/edge-growth formulas were not imported into this record: different border and stack choices make an unqualified formula unsafe.

## Official geometry access recipe and safe reuse

1. Start with [current Parts Library](https://multibuild.io/parts), **Other → Remixing Files → Tile Components → STEP**. The observed exact result links to **Thangs 994681**. [Direct STEP filter](https://multibuild.io/parts/remixing-files?Part%20Type=Tile%20Components&File%20Type=STEP). The corresponding **STL** filter links to **Thangs 994663**. [Direct STL filter](https://multibuild.io/parts/remixing-files?Part%20Type=Tile%20Components&File%20Type=STL). [B9–B10]
2. Read the original model description and the linked full legal license, not just the Download button. The STEP listing describes **Tile Core Components**; that is not proof it contains all current perimeter, square-plate, or Other Plate variants. Select the actual target plate's own files as well where exact fit/edge clearance depends on them. [B2; B10–B12]
3. The **STEP listing Download was exercised in a clean unauthenticated browser**. It opened a login modal. The page's public `can-download` response was true, but no original CAD bytes, member filenames, or signed download URLs were delivered through that interaction. No credentials, subscription purchase, or access-control workaround was attempted. Generic public metadata and thumbnail access are not CAD inspection. Exact CAD file revision and modification date remain unknown; the publication timestamps above describe the listing only.
4. With lawful access, retain originals **outside the public repository** unless specific written redistribution permission changes the situation. Record exact member filename, source landing/download URL, download date, SHA-256 of original bytes, units, STEP header/author/export data if present, and license version. Hashes identify bytes; they do not establish accuracy or rights. This research records no fake checksum for inaccessible files. [B12]
5. Inspect data, not executable behavior. List archive members before extraction; reject traversal paths and executable/macro resources. Import a STEP's static geometry without executing bundled generators, CAD scripts, plugins, or macros. For mesh inspection use an isolated static parser and record meshing/fit uncertainty; no upstream scripts need to run.
6. A useful measurement set is: front/back face separation; named large/small center lattices and their relative phase; edge-to-center coordinates by edge variant; front/back/mid-depth sections through a Multihole; across-flats/corners and fillets; all retention shoulders/undercuts; small-hole diameter sections; thread pitch/lead/starts and engagement depth. Compare corresponding connector and board geometry in a common frame rather than only comparing bounding boxes. Mark inspected CAD geometry **derived from a pinned design file**, not manufacturer tolerances or a physical specimen measurement.
7. Reuse an official connector's mating region without arbitrary scaling only within the license's allowed personal/remix workflow and after confirming revision/application. Sharing a substantial custom holder may be permitted, but redistributing untouched Tile Components or placing original CAD into a public source package is not. No claim is made that reverse-engineered dimensions automatically remove all underlying rights; resolve intended public/commercial use against the applicable terms. [B11–B12]

No authoritative dimensioned board drawing was found in the accessed Hub pages. The [Core Parts illustrations](https://docs.multibuild.io/beginner-section/core-parts-documentation#1-multiboard-tile), poster, and [Common Connections](https://docs.multibuild.io/beginner-section/common-connections) are useful topology/selection references, **not** scale drawings. The Hub describes an Advanced section but says it is developing; the accessed sitemap exposed only beginner pages. That is a search/access boundary, not proof no private technical resources exist. [B1; B16]

## What future adapters can safely use

- **Nominal planning:** the documented 25 mm same-family tile-grid pitch, hole-family connection roles, and local grid-origin coordinate convention. Preserve the selected plate's hole mask, especially across seams. [B1; B3–B6]
- **Stock-connector route:** design the object's holder around a separately documented bolt, insert, rail, or other connector that mounts using the vendor's existing piece. This can avoid reconstructing a board's internal thread/snap opening, but the holder-side fastening hole, support face, stack thickness, and assembly access still need specific evidence.
- **Existing-holder route:** independently byte-identified/permission-cleared holder meshes can establish their own geometry, not the vendor board's profile. A measured tab is not automatically a Friction-Fit Insert, Fix-Point, Rail, or board Snap. Its actual mate and physical fit must be identified. Keep those example records' dimensional evidence and limitations separate from the official values here.
- **Direct board snap/thread route:** obtain the relevant original CAD or measure a revision-identified board and mate, then validate a coupon. The unknowns in this record block claiming a ready-to-print exact direct-mating profile, not the entire future-adapter workflow.
- **Keep-outs:** check wall clearance for the chosen mount, rear protrusion/engagement, installation rotation or translation, tool access, neighboring occupied holes, tile seams, and removal motion. B1 says directional Moderate/Heavy Snaps require angled insertion and Heavy Snaps require a wall-offset tile; the 6.25 mm Part A offset must not be treated as a universal sufficient motion clearance. No load rating or mechanical safety claim is made here.

## Research checks and remaining verification

| Check | Observed result | Limit |
|---|---|---|
| Static official Hub and model descriptions | Both large and small hole families explicitly described as 25 mm apart in B3/B4; current Hub confirms 25 mm grid | No diameter, thickness, phase, or production tolerance recovered |
| Real browser current catalog | Tile Components STEP/STL filters linked to 994681/994663; plate and legacy selectors exposed current taxonomy; regular octagon/square selections linked to 1320746/1306830 | Dynamic listing labels are mutable; no complete catalog scrape performed |
| Actual STEP Download interaction | Unauthenticated login modal observed; no original CAD downloaded | No file measurement, checksum, or physical fit claim |
| Official diagram/poster inspection | Hole/connector topology identified visually; no dimensioned interface section present | No pixel-based inference |
| License review | Full plaintext legal document dated 2025-12-19 read; original Design redistribution restricted | Not legal advice; underlying geometry reuse needs use-specific review |
| Physical fit / CAD section check | **Not run** | Research-only assignment; original board CAD inaccessible and no specimen supplied |

Before any direct mating model is described as compatible, pin the exact board/connector revisions, recover the unknown section/profile dimensions, and exercise insertion/removal and retention on a representative printed coupon. Acceptance thresholds must come from that interface's actual geometry and calibrated process, not the unspecified “0.25 mm tolerance” wording.

The missing exact mating geometry and example-asset license version are recorded in [issue #10](https://github.com/ShakataGaNai/b123d/issues/10). That issue's closure does not resolve the interface-specific unknowns or confer permission to redistribute vendor originals.

## Change record

| Date | Change | Effect |
|---|---|---|
| 2026-10-01 | Initial official board-geometry research; current/legacy listing identity distinctions, sourced pitches, coordinate conventions, explicit missing mating data, license/access recipe | No adapters or consuming model geometry changed |
