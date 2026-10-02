# Community-published thread and geometry research

Research date: 2026-10-01. This record is deliberately narrower than the
[board geometry](board-geometry.md) and [attachment-interface](attachment-interfaces.md)
records: it preserves community source geometry and older publisher guides which
may help identify a future *specific* adapter. It does **not** turn a community
reconstruction into a current MultiBuild specification or establish that the
user's 13.5 mm-AF AirTag peg mates directly with a board Multihole.

## Evidence classes and source register

| ID | Creator / source | Revision, date, and scope | Evidence class | Why it matters |
|---|---|---|---|---|
| C1 | Pip! Gold (`asciipip`), [stacked parametric tile source at immutable commit `4db5f07`](https://github.com/asciipip/multiboard-parametric-stacked/blob/4db5f07abb4653193014eb1bba761011bc29eb87/multiboard_base.scad#L48-L90) | Commit [2025-01-09](https://github.com/asciipip/multiboard-parametric-stacked/commit/4db5f07abb4653193014eb1bba761011bc29eb87). The source comments say its measurements are based on official Tile Component remix files, Thangs 994681, uploaded 2024-01-19. It is a fork of `shaggyone/multiboard-parametric`, not a MultiBuild release. | **Community source-authored geometry** for C1's legacy-style parametric tile; not vendor authority and not a physical measurement. | The strongest static, complete, inspectable community parameter set found. Its comments label the source units millimetres. |
| C2 | Victor Zag (`shaggyone`), [parametric tile source at `d9131ab`](https://github.com/shaggyone/multiboard-parametric/blob/d9131ab8480de327c34618820c12212b1e8063c7/multiboard_base.scad#L8-L44) | Latest file-change commit shown by GitHub is 2024-02-12; its own [history page](https://github.com/shaggyone/multiboard-parametric/commits/master/multiboard_base.scad) identifies the immutable revision. It is C1's upstream/fork parent. | **Community source-authored geometry**, conflicting where stated below. | A useful conflict control: do not blend two community reconstructions into a fictional universal profile. |
| C3 | LengAwaits, [*Official Components* community wiki](https://github.com/LengAwaits/Multiboard_Community_Resources/wiki/Official-Components) | Undated, mutable community catalogue. Its tile table gives nominal assembled areas and claimed printable areas, but no hole section, thread drawing, or revision-pinned source asset. | Community catalogue/guide only. | A broad parts index, **not** a comprehensive dimensional specification. |
| C4 | `trenaryja`, [creator-owned 2×2 tile dimensional SVG, pinned revision `7705519`](https://gist.githubusercontent.com/trenaryja/6f22d61431a611a2d853c1a52d9985e7/raw/77055191edfda55a7d3acbbad33ae9d92d951f27/2x2-tile-dimensions.svg), linked by the archived [original Reddit post record](https://api.pullpush.io/reddit/submission/search?ids=1h7wsmg) | Reddit author `trenaryja`; post timestamp 2024-12-06; SVG is a creator-owned immutable Gist revision. The author explicitly says it was made from an STL/mesh rather than the official remixable CAD and planned a future update. | **Primary evidence for the creator's drawing**, with the post text preserved by a third-party archive; not publisher authority. | The genuine detailed 2×2 drawing found. It is a useful mesh-reconstruction cross-check, but must remain revision-limited. |
| C5 | `davidkclark`, [“Where are the up-to-date remixing files?” archived post record](https://api.pullpush.io/reddit/submission/search?ids=1mmfk9n) | Post timestamp 2025-08-10; no CAD or physical measurement attached. | Community author claim only. | A specific version-drift warning: its author reports the older STEP components as 6.4 mm versus Multipoint 6.21 mm and says their threads look “VERY different.” It must not be treated as verified current geometry. |
| O1 | Multiboard / Keep Making, [archived Knowledge Hub index](https://web.archive.org/web/20240824223819id_/https://www.multiboard.io/knowledge-hub) | Publisher page captured 2024-08-24. The page itself says all Knowledge Hub pages were under construction and lists its complete then-public guide set. | Authoritative publisher prose for that historical page, not a CAD drawing. | Provides a bounded check for an older official guide that may have disappeared during the site transition. |
| O2 | Multiboard / Keep Making, [archived Tiles guide](https://web.archive.org/web/20240824222327id_/https://www.multiboard.io/knowledge-hub/tiles), [Bolts guide](https://web.archive.org/web/20240829101306id_/https://www.multiboard.io/knowledge-hub/bolts), [Snaps guide](https://web.archive.org/web/20241209045359id_/https://www.multiboard.io/knowledge-hub/snaps), and [Nuts and Rods guide](https://web.archive.org/web/20240918010154id_/https://www.multiboard.io/knowledge-hub/nuts-and-rods) | Publisher pages captured from May--December 2024; original page dates/revisions are not exposed. | Authoritative publisher prose within the captured historical revision. | Confirms older terminology/function and a few named lengths, but none is a comprehensive cross-section/dimension guide. |

C1 never provides a tolerance, clearance, physical specimen, source-file hash, or
fit result. Its values are therefore **nominal reconstruction parameters**, not
clearance targets. A future adapter must record its own allowance convention and
coupon result separately.

### C4 creator drawing and C5 revision warning

C4 is the sought **genuine detailed community guide**: its SVG contains a 2×2
tile drawing with labelled sections and its own millimetre document units. Its
visible numeric labels include 6.4 (tile thickness), 25 (layout/pitch
dimension), 21.4 (large-hole section), and 7.5/6 (small-hole sections), but
the drawing does not declare a tolerance, feature revision, thread lead,
start-count, handedness, or a mating male component. Use the primary SVG for
the drawing itself and C1's source for unambiguous parameter semantics; do not
promote a label from the drawing to an official/current specification.

C5 is the strongest post-C1 version warning located. It is not evidence of a
6.21-mm nominal board: it is one community author's report about their
comparison of stale STEP files and Multipoint output. It does, however, rule
out assuming C1/C2 or C4 matches every current Multipoint tile.

## C1 static source parameters — useful, but revision-scoped

C1 builds a tile body and subtracts `multihole()` and `peg_hole()` from it. Thus
the following are **female tile-hole** values in C1's coordinate system, not
male-bolt dimensions. The `z = 0` face is the start of its 6.4 mm extrusion;
its comments call the reduced middle band the "thick" portion because the
remaining tile wall is thicker there. `AF` means across flats. No row supplies
clearance: none is declared by C1.

| Interface / source scope | C1 value and datum | Evidence and geometry meaning | Clearance vs. nominal; limitation |
|---|---|---|---|
| Tile body, C1 core/side/corner generator | **6.4 mm** in `z`, from its `z = 0` to `z = 6.4` body faces | `height = 6.4`; source-defined board thickness. [C1 lines 48--55](https://github.com/asciipip/multiboard-parametric-stacked/blob/4db5f07abb4653193014eb1bba761011bc29eb87/multiboard_base.scad#L48-L55). | Nominal reconstruction only. It is not a current-plate thickness, production tolerance, or an engagement depth. |
| **Large Multihole**, female octagonal base | **23.4 mm AF** at both source faces; **21.4 mm AF** in the middle; middle-band depth **2.4 mm**. With C1's 6.4 mm body, the two source tapers each span **2.0 mm** (`(6.4 − 2.4)/2`, derived). | C1 explicitly calls the Multihole an octagon and constructs its base with `multihole_thin_size`, `multihole_thick_size`, and `multihole_thick_height`; its `tapered_hole_base` locates the band symmetrically about the body midplane. [Parameters](https://github.com/asciipip/multiboard-parametric-stacked/blob/4db5f07abb4653193014eb1bba761011bc29eb87/multiboard_base.scad#L55-L69), [section construction](https://github.com/asciipip/multiboard-parametric-stacked/blob/4db5f07abb4653193014eb1bba761011bc29eb87/multiboard_base.scad#L226-L280). | Nominal C1 void geometry. It does **not** identify the user's 13.5 mm-AF male AirTag peg as this hole's mate, nor establish a snap latch/retention depth. |
| **Large Thread** cut into C1 female Multihole | Source spiral `d1` (outer diameter) **22.6 mm**; `d2` (inner diameter) **21.4 mm**; outer-wall height `h1` **0.5 mm**; inner-cylinder height `h2` **1.583 mm**; pitch **2.5 mm**. The source calls its profile trapezoidal. | C1 defines `d1` as the outer spiral diameter and `d2` as its inner diameter, then uses a four-point trapezoidal profile in `trapz_thread`. [Definitions](https://github.com/asciipip/multiboard-parametric-stacked/blob/4db5f07abb4653193014eb1bba761011bc29eb87/multiboard_base.scad#L70-L90), [helix construction](https://github.com/asciipip/multiboard-parametric-stacked/blob/4db5f07abb4653193014eb1bba761011bc29eb87/multiboard_base.scad#L245-L300). | These are C1 parameter names, **not verified ISO major/minor diameters** or an official thread callout. No thread allowance is coded. Official lead, starts, handedness, flank angle, root/crest radii, runout, usable engagement, and revision compatibility remain unknown. Do not select an ISO thread from 22.6/2.5. |
| **Small / Pegboard hole**, female C1 base | **7.5 mm diameter** at source faces; **6.0 mm diameter** in the central band; central-band depth **2.9 mm**. It is generated by `rotate_extrude`, so C1 models it as circular, unlike its large octagon. | [C1 parameters](https://github.com/asciipip/multiboard-parametric-stacked/blob/4db5f07abb4653193014eb1bba761011bc29eb87/multiboard_base.scad#L84-L90) and [base construction](https://github.com/asciipip/multiboard-parametric-stacked/blob/4db5f07abb4653193014eb1bba761011bc29eb87/multiboard_base.scad#L226-L280). | Nominal C1 void geometry, no clearance. It is not evidence that an arbitrary commercial pegboard hook fits a current tile. |
| **Small Thread** cut into C1 female Pegboard hole | Source spiral `d1` **7.0 mm**; `d2` **6.0 mm**; `h1` **0.77 mm**; `h2` **2.5 mm**; pitch **3.0 mm**. | [C1 parameter block](https://github.com/asciipip/multiboard-parametric-stacked/blob/4db5f07abb4653193014eb1bba761011bc29eb87/multiboard_base.scad#L84-L90) and [small-thread construction](https://github.com/asciipip/multiboard-parametric-stacked/blob/4db5f07abb4653193014eb1bba761011bc29eb87/multiboard_base.scad#L217-L244). | Same limitation as the Large Thread: C1's `d1`/`d2` are reconstruction parameters, not official major/minor diameters. Official profile, lead, starts, handedness, fit allowance and present-version compatibility are unknown. |
| C1 local **large-to-small phase** for a populated core cell | Large-hole centre: `(25i + 12.5, 25j + 12.5)` mm. Its selected diagonal small-hole centre: `(25i + 25, 25j + 25)` mm. Therefore **`(+12.5, +12.5) mm`** relative to that same cell's large-hole centre. | This is a direct coordinate subtraction from C1's two `translate` calls. The generator conditionally omits small holes depending on core/side/corner and neighbour state. [Placement and condition](https://github.com/asciipip/multiboard-parametric-stacked/blob/4db5f07abb4653193014eb1bba761011bc29eb87/multiboard_base.scad#L126-L145). | Source-local, nominal phase only. It does not establish the phase/presence mask of a current plate, a border, a seam, or every historical tile. |
| C1 local angular registration | Large octagon base is rotated **22.5°** in C1's XY plane; its large thread is rotated **−170°**. C1 rotates its Pegboard-hole/thread group **−129°**. | [C1 hole modules](https://github.com/asciipip/multiboard-parametric-stacked/blob/4db5f07abb4653193014eb1bba761011bc29eb87/multiboard_base.scad#L181-L225). | A C1 source-frame registration, not an official assembly datum or proof of current thread-start phase. |

### Why the thread table is intentionally incomplete

C1 does provide an executable geometric construction, but static reading shows
only its own chosen pitch and profile dimensions. It has no declaration of a
vendor thread designation, start count, handedness, tolerance band, or a
mating male counterpart. Even though its one swept spiral *looks like* a
single-start implementation, that is not sufficient evidence to label the
proprietary interface's official lead or start count. Modelers must retain the
following as explicit unknowns for **Small**, **Mid**, and **Large** threads:

| Interface | Still unknown from all accepted community/older-publisher evidence here |
|---|---|
| Small Thread / Pegboard hole | Official major, minor, pitch and pitch diameter; lead; starts; handedness; flank angle/profile; crest/root form; entrance/runout; profile depth; usable engagement; current revision and print-fit allowance. C1 only supplies its reconstruction values above. |
| Mid Thread / snap Mid Hole | Major/minor/pitch/pitch diameter; lead; starts; handedness; full profile; snap socket depth; and any locking/retention geometry. C1 does not model this interface at all. |
| Direct snap ↔ board Multihole | Exact male snap outside section (AF/corners/fillets), flex-arm/latch dimensions, board undercut/lip, axial insertion stroke, fully seated depth, front/rear protrusion, removal path/force, angular registration, tolerance and revision. Neither C1/C2/C4 models a snap, and O2 has no dimensioned snap section. |
| Large Thread / Multihole | Official major, minor, pitch and pitch diameter; lead; starts; handedness; flank angle/profile; crest/root form; entrance/runout; useful engagement; exact multihole/snap depth; current revision and print-fit allowance. C1's `22.6/21.4/2.5` parameters are not a substitute for those facts. |

## Community-source conflicts — do not merge parameters

C2 is an earlier independent/ancestor parametric source, not a measurement of
C1. It gives a useful warning that even community CAD values are revision- and
author-specific.

| Feature | C1 (`4db5f07`, 2025-01-09) | C2 (`d9131ab`, 2024-02-12) | Modeling status |
|---|---:|---:|---|
| Tile thickness | 6.4 mm | 6.4 mm | Agreement between community sources is not publisher tolerance evidence. |
| Large reduced octagon AF / middle depth | 21.4 mm / 2.4 mm | `25 − 3.6 = 21.4` mm / 2.4 mm | Same reconstructed values, but neither asset pins a current official file. |
| Large thread `d1` / `d2` / pitch | 22.6 / 21.4 / 2.5 mm | 22.5 / 21.4 / 2.5 mm | **Conflict at `d1`: do not average or call either an official major diameter.** [C2 parameter block](https://github.com/shaggyone/multiboard-parametric/blob/d9131ab8480de327c34618820c12212b1e8063c7/multiboard_base.scad#L28-L44). |
| Small thread `d1` / `d2` / pitch | 7.0 / 6.0 / 3.0 mm | 7.025 / 6.069 / 3.0 mm | **Conflict:** C2 also uses a simple `6.069 + 0.025` mm small-hole bore rather than C1's tapered 7.5/6.0-mm base. [C2 source](https://github.com/shaggyone/multiboard-parametric/blob/d9131ab8480de327c34618820c12212b1e8063c7/multiboard_base.scad#L14-L44), [C2 small-hole construction](https://github.com/shaggyone/multiboard-parametric/blob/d9131ab8480de327c34618820c12212b1e8063c7/multiboard_base.scad#L199-L216). |
| Cross-family phase | Large centres at cell centres and populated small centres at cell corners | Same local placement equations | The agreement applies only to these two legacy-style community generators; it does not override the selected official plate's hole mask. |

## Older official documentation check

No genuine older **complete dimensioned technical guide** was found. This was
not inferred from a missing search result: the 2024 archived publisher index
(O1) enumerates Basics, Snaps, Tiles, Bolts, Honeycomb, Mounting Systems,
MultiGrid, Printing Guidelines, and Nuts and Rods, while explicitly describing
the pages as under construction. All dimension-relevant entries were opened.

- The archived **Tiles** page gives 6×6 = **158 × 158 mm** and 8×8 =
  **208 × 208 mm** as named printable tile sizes; it also says both hole
  families are 25 mm apart. It contains no hole cross-section, board-thickness
  datum, thread drawing, or small/large-phase dimension.
- The archived **Bolts** page identifies **9/13/20 mm** Big and Small thread
  lengths, **10/18/20 mm** Mid thread lengths, and **3 mm** and **6.5 mm**
  shanks. These are named-part length claims, not thread profile dimensions or
  snap seating depths.
- The archived **Snaps** page describes push-fit positions and 8/15 mm offset
  variants, but supplies neither a snap section nor latch/insertion depth.
- The archived **Nuts and Rods** page lists 4/8-mm nut lengths and 40-mm rods,
  again without any thread cross-section.

Accordingly, O1/O2 are useful historical functional documentation but are **not
a missed detailed engineering guide**. The exact original official-file route
remains the revision-matched remix CAD identified in the other Multiboard
records; it was not available for measurement here.

## Access limits and unaccepted leads

| Route | Result | Treatment |
|---|---|---|
| [r/Multiboard “Multiboard Tile Dimensions Drawing”](https://www.reddit.com/r/Multiboard/comments/1h7wsmg/multiboard_tile_dimensions_drawing/) | Live Reddit JSON/normal page returned HTTP 403 and `old.reddit` redirected to login. A PullPush-preserved post record identified author `trenaryja`, date, mesh/STL caveat, and the creator-owned pinned SVG (C4). | Use the SVG as primary evidence of its author's drawing; use PullPush only as an archival route to the author’s post text. It remains a mesh-derived, not official/current, drawing. |
| [r/Multiboard “Where are the up-to-date remixing files”](https://www.reddit.com/r/Multiboard/comments/1mmfk9n/) | Live Reddit remained blocked, but PullPush preserves the named author’s post text (C5). It does **not** substantiate the search-result claim of a 3.125-mm pitch. | Use only as a community-reported version-drift warning. Do not use 6.21 mm or any suggested pitch as a vendor dimension. |
| Current MultiBuild pages and older Knowledge Hub snapshot set | Current prose is captured in the sibling records; Wayback exposed the bounded 2024 guide set above. | No hidden historical comprehensive drawing was recovered. |
| C3 community wiki | Static and accessible, but it is a catalogue with no pinned geometry source or thread/snap dimensions. | Link only; not used as a mating specification. |

## Adapter handoff

The C1 geometry can be useful for a **clearly identified C1-compatible legacy
tile reconstruction** or for preparing a measurement checklist. It does not
clear a direct board-mating adapter. Before future CAD uses any source-derived
profile, acquire the exact target tile and counterpart revision, retain the
source-file identity outside this repository as licensing requires, compare
front/middle/back sections, establish the complete insertion/locking path, and
coupon-test the printed interface. For the requested AirTag route, the author
confirms a **13.5 mm across-flats male insert with 6.5 mm projection into a
snap**. Its specific snap variant/revision remains unspecified. Keep this
interface separate from C1's larger female board Multihole.
