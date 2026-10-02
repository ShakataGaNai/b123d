# Community and publisher rail measurements

> **Scope and status — 2026-10-01.** This is a provenance-first record of
> published information about MultiBoard's old **Multipoint** / current
> **Fix-Point** rail family, concentrating on installed profile, folded-print
> state, and community-created receiver geometry. It is not a replacement for
> the current authorized MultiBuild remix file and it does not establish a
> physically fitting adapter. In particular, a source author's dimensions
> describe that author's design, not a MultiBuild-controlled specification.
>
> **Result:** no public dimensioned drawing or verified installed assembly
> transform was found. The strongest actionable evidence is (1) MultiBuild's
> authoritative role/variant statements and named positive/negative source
> files, and (2) a community OpenSCAD model that declares an 18.6-unit maximum
> rail width and 2.2-unit maximum depth while subtracting the official *Lite
> Multipoint Rail - Negative.stl*. The latter is useful as a receiver-envelope
> precedent only; its source units, rail-file revision, and physical fit are
> unstated.

## Vocabulary, evidence rule, and source register

MultiBuild's current documentation says that **Multipoints** were renamed
**Fix-Points** and **Multipoint Rails** were renamed **Rails**. It calls a
regular Multipoint suitable for a Multipoint Hole, and a Lite Multipoint
**1 mm thinner** than regular and suitable for a negative Multipoint Rail
([S1]). This record retains the older names where they occur in an original
source.

| ID | Original source / publisher | Revision or date | What it directly establishes |
|---|---|---|---|
| S1 | MultiBuild, [Core Parts Documentation](https://docs.multibuild.io/beginner-section/core-parts-documentation#11-multipoint) | Current unversioned page, accessed 2026-10-01 | Rename, slide-on behaviour, Regular-vs-Lite relationship, and Lite-to-negative-rail compatibility. |
| S2 | MultiBuild, [*Pegboard Click - Rail (Folded)*, model 1123315](https://thangs.com/designer/MultiBuild/3d-model/Pegboard%20Click%20-%20Rail%20%28Folded%29-1123315) | Listing says 2 years ago; exact release date/revision unknown | A 2-Multihole Rail with a Pegboard Click; it accepts accessories having a negative Rail; print orientation is the supplied file orientation. |
| S3 | MultiBuild, [*Multipoint Rails - STL Remixing Files*, model 1142254](https://thangs.com/designer/MultiBuild/3d-model/Multipoint%20Rails%20-%20STL%20Remixing%20Files-1142254) | Listing says 2 years ago; exact release date/revision unknown | Official names and roles of `Lite Multipoint Rail - Negative.stl`, `Lite Multipoint Rail - Positive.stl`, `Multipoint Rail - Positive.stl`, and `Multipoint Rail Slot - Negative.stl`. |
| S4 | Tamio Patrick Honma / GitHub user IOIO72, [`multiboard-pegboard-headphone-holder.scad`](https://github.com/IOIO72/multiboard-pegboard-headphone-holder/blob/46050819926777cae965b06eacd51125af6e73b6/multiboard-pegboard-headphone-holder.scad) | Commit `46050819926777cae965b06eacd51125af6e73b6`, 2024-12-27 | Author's negative-Lite-rail receiver construction and parameters. The repository README identifies the author and tells users to acquire the named official negative STL separately. |
| S5 | haliphax, [*Multiboard rail slot die.scad* gist](https://gist.github.com/haliphax/16ef2057867fe5dbdd2436996791a073) | Created and last updated 2026-07-10 | A community-authored polygonal *slot* reconstruction / cutting die, including its own coordinates and a 2.2-unit interpolation depth. No variant, source asset, units, or fit test is stated. |
| S6 | MultiBuild, [*Pegboard Click - Multipoint Rail (Supported)*, model 1470823](https://thangs.com/designer/MultiBuild/3d-model/Pegboard%20Click%20-%20Multipoint%20Rail%20%28Supported%29-1470823) | Listing says 10 months ago; exact release date/revision unknown | A separately listed 2-Multihole Pegboard Click rail with the same prose functional description as S2. Its thumbnail source filename contains `Non-Folded`; that is not an assembly transform or proof of geometric identity with S2. |
| S7 | Printables author `ShakataGaNai`, **Seeed Wio Tracker L1 Pro Multiboard Holder**, print 1407547, provenance retained in [existing-holder-examples.md](existing-holder-examples.md#2-wio-tracker-l1-pro-case-specific-rail-dependent-carrier-precedent) | First published 2025-09-07; one 3MF (`Multiboard Seeed L1.3mf`) | The author says a rear **Rail** is required. The print inventory contains no rail file, rail variant, profile, transform, or installation instruction. |
| S8 | Tamio Patrick Honma / GitHub user IOIO72, [`Container On Multipoint Rails.scad`](https://github.com/IOIO72/containers-on-multipoint-rails/blob/a24c3c4e578a350b18b8b02cbd7873d57abf8348/Container%20On%20Multipoint%20Rails.scad) | Commit `a24c3c4e578a350b18b8b02cbd7873d57abf8348`, 2025-06-20 | A second community source that subtracts `Lite Multipoint Rail - Negative.stl` in horizontal, vertical and cross layouts; its author chooses a 2-unit rail-depth/safe-zone parameter. |


The live MultiBuild sources describe their own parts and are **authoritative**
for named compatibility, but their prose is not a dimensioned cross-section.
S4, S5, and S8 are **community/source-authored evidence** only. Values named below
as `units` are OpenSCAD coordinate units where the author did not declare a
unit; they must not be silently relabelled mm.

## What is actually known about the installed mating chain

| Interface / side | Published relationship | Evidence class | Installed-profile consequence / limitation |
|---|---|---|---|
| Regular Multipoint/Fix-Point, male positive | Regular Multipoint connects to a Multipoint Hole. | Authoritative, S1 | This is not established as a rail mate; do not substitute it for Lite. Exact cross-section, depth and clearance are unknown. |
| Lite Multipoint/Fix-Point, male positive | Lite is 1 mm thinner than Regular and connects to a Multipoint Rail (Negative). | Authoritative, S1 | This is the documented male-to-female rail chain. The baseline Regular thickness and the Lite positive profile remain unpublished in prose. |
| Lite rail, female negative | S3 calls `Lite Multipoint Rail - Negative.stl` a negative part used to make cut-outs. | Authoritative, S3 | It is the appropriate upstream *receiver/cut-out* source category, not a printable male rail. No mouth width, groove depth, flank angle, radius, end condition, or clearance convention is stated. |
| Rail positive, male | S3 names `Lite Multipoint Rail - Positive.stl` and `Multipoint Rail - Positive.stl`; it says positives are added to designs. | Authoritative, S3 | Confirms distinct Lite and non-Lite positive files, but does not say that they share a cross-section, nor how either relates to S2's rail. |
| Pegboard Click rail, male rail + tile-side attachment | S2 says its Rail is 2 Multiholes long, has a Pegboard Click, and lets negative-Rail accessories slide on. | Authoritative, S2 | Supports an installed assembly chain of tile small holes → Pegboard Click → positive rail → accessory negative rail. It does **not** name Regular or Lite, does not publish its profile, and does not declare an end stop. |
| Wio holder rear receiver | The creator says the Wio holder requires a rear Rail; no such Rail is in the one-file download. | Community author claim, S7 | `Rail` cannot be resolved to Lite/Regular, positive/negative, source revision, or insertion direction. It is a dependency, not a usable mating specification. |

The current documentation further says Multipoints have **slide-on installation
and removal** ([S1]). None of S1–S8 gives a terminal stop, detent, secondary
lock, permitted overtravel, or a load/retention rating. A future adapter must
therefore reserve the full slide-in/out path and choose an identified retention
method instead of assuming the rail is captive.

## Published numerical details

### A. Officially stated values

| Feature | Value, unit and datum | Variant / male-female | Evidence class | Clearance versus nominal geometry | Limitation |
|---|---|---|---|---|---|
| Lite thickness delta | **1 mm thinner than Regular**; no shared face, datum, or absolute thickness stated | Lite male Multipoint/Fix-Point relative to Regular male | Authoritative, S1 | Nominal relative geometry, **not** a clearance | Cannot produce either profile or its groove depth. |
| S2 rail nominal span | **2 Multiholes long**; source gives no mm end-to-end datum | Positive Rail carried by Pegboard Click | Authoritative, S2 | Nominal component description, not a measured physical length | MU pitch does not establish actual ends, click spacing, rail start/end, or any end stop. |
| Listing tolerance | **0.25 mm**, direction/convention not defined | S2 and S3 listed printable parts | Authoritative listing claim, S2/S3 | A publisher design/print tolerance statement; it is not declared radial, diametral, per-face, or specifically rail clearance | Do not offset a custom rail slot by 0.25 mm from this prose alone. |

### B. Community author parameters — useful envelope precedent, not a rail specification

S4 constructs a `railSlot()` receiver by subtracting the separately obtained
`Lite Multipoint Rail - Negative.stl`. The following values are literal source
parameters at the linked commit. OpenSCAD does not declare a length unit in this
file; `25` is used there as `multiboard_grid_offset`, which is consistent with
but does not prove millimetres.

| Source symbol and value | Interface / datum in S4 | Variant / male-female | Evidence class | Clearance versus nominal geometry | What may be used / what may not |
|---|---|---|---|---|---|
| `multipoint_rail_max_width = 18.6` **source units (unit unspecified)** | Named maximum width used to size a housing around the imported negative Lite rail. | Lite negative receiver/cutout only | Community author parameter, S4 | The source does not label it clearance or nominal profile width. | A conservative *author-design envelope* lead only. It is not a verified official width or groove-mouth width. |
| `multipoint_rail_max_depth = 2.2` **source units (unit unspecified)** | Named maximum depth, used in the offset support material and import translation for the negative Lite rail. | Lite negative receiver/cutout only | Community author parameter, S4 | Not identified as clearance or nominal groove depth. | Useful only as a lead for comparing against the exact referenced official file; do not set a custom receiver depth to it. |
| `click_height = 36.8`, `click_mount_depth = 4` **source units (unit unspecified)** | S4's headphone-holder rail-slot housing length and host-material depth; the slot is constructed as an 18.6 + 4 wide / 4 deep envelope before subtraction. | Holder-specific negative Lite receiver housing | Community author design, S4 | Host geometry, not interface tolerance. | These are not rail dimensions. They show that the author retained material around the imported cutout. |
| `multipoint_rail_offset = -6` **source units (unit unspecified)** | Explicit comment: adjusts holder position to match the rail slot, in the author's preview layout. | Holder-to-preview placement, not rail section | Community author transform, S4 | Not a clearance. | It is neither an installed rail transform nor a universal attachment datum. |
| `multiboard_grid_offset = 25` **source units (unit unspecified)** | Community model's grid layout variable. | Model layout, not profile | Community author parameter, S4 | Nominal layout choice. | It corroborates the author's intent to align to the system grid, but cannot turn the other source-unit parameters into official mm dimensions. |

S8 independently imports that same named official Lite-negative file as a boolean cutout. Its current committed source declares `multipoint_rail_depth = 2` and `multipoint_rail_safe_zone = multipoint_rail_depth + back_wall`, with `back_wall = 1.8`; it translates the imported cutout by `multiboard_grid_offset / 2 + position` and rotates it `[0, 90, 90]` for its **own** horizontal container layout. Its vertical branch uses `[90, 0, 180]`. These are creator-local source transforms and host-wall parameters, not an installed MultiBuild rail datum or a measurement of the official file.

| Source symbol and value | Interface / datum in S8 | Variant / male-female | Evidence class | Clearance versus nominal geometry | What may be used / what may not |
|---|---|---|---|---|---|
| `multipoint_rail_depth = 2`, `back_wall = 1.8`, and safe zone `= 3.8` **source units (unit unspecified)** | S8's container clearance behind an imported Lite-negative cutout. | Lite negative receiver/cutout only | Community author parameter, S8 | The code does not call the 2-unit value a measured rail depth or a clearance allowance. | It is a second *design-envelope precedent*. It does not confirm S4's 2.2-unit value, define a groove depth, or specify an installed positive rail. |
| `multiboard_grid_offset = 25`; cutout placement at half-grid plus a 2-unit author parameter **source units (unit unspecified)** | S8's horizontal container layout. | Receiver position in a particular container | Community author source transform, S8 | Not a clearance. | It shows a useful candidate placement strategy, but cannot be transplanted into the Wio or folded Pegboard-Click assembly without their datums. |

### C. Independent unverified community slot reconstruction

S5 produces a **negative cut-out die** by subtracting a `slot()` solid from a
40-unit cube. Its code sets `z_dist = 2.2` and defines an inner polygon with
extents `x = 0…33.5`, `y = -8.5…8.5`; an outer polygon has
`x = 0…32`, `y = -8.5…8.5` and intermediate shoulders. The solid linearly
interpolates between those two polygons over 2.2 source units, then applies
`rotate([0, -90, 0])` before the final boolean.

These are exact **coordinates of the gist author's cutting tool**, not verified
rail measurements: the gist does not name Regular/Lite, positive/negative
compatibility, source file/revision, measurement method, intended installation
orientation, tolerance, or a successful fit. Its source units are also
undeclared. In particular, the apparent 17-unit polygon height and 33.5-unit
span must not be used as an installed rail width/height, a dovetail angle, or a
cross-family match. The non-vertical polygon segments can be computed from the
coordinates, but calling them a rail dovetail angle would be unsupported.

## Folded print-state versus installed assembly

S2 is the requested lead, but its public listing supplies only a **part name**,
functional description, thumbnail images, and the instruction to print in the
orientation provided by the file. It does *not* publish:

- an unfolded CAD configuration;
- hinge-line/axis coordinates, angle, fold direction, or a stop angle;
- a print-frame-to-installed-frame transform;
- a datum linking the Pegboard Click, rail cross-section, and tile front plane;
- a separately identified hinge, fastener, or assembly operation; or
- an assertion that model 1470823 (S6) is the unfolded geometry of S2.

Therefore no fold transform is recorded. **Do not treat the S2 mesh frame as an
installed frame**, rotate it by an assumed 90 degrees, or call its file bounds
an installed rail profile. S6 is a useful comparison lead because it is a
separate, newer official listing with the same 2-Multihole/Pegboard-Click
functional wording; its thumbnail URL labels its image `Non-Folded`. That
filename and parallel prose are insufficient to establish identity, a transform,
or replacement status.

S2 does add a genuine assembly-clearance warning: an original Thangs discussion
comment says the Pegboard Click requires **8 mm or 15 mm offset snaps** because
pegboard accessories go behind the tile. This is community evidence, not an
official model dimension, does not identify the click's rear projection or a
minimum clearance, and does not establish compatibility with the newer 6.25 mm
standoff discussed in replies. Preserve rear clearance as unknown until the
exact Pegboard Click and installed tile/mount are available.

## Unverified matches and missing dimensions

| Lead / apparent match | Why it remains unverified | Required evidence before adapter use |
|---|---|---|
| S4's `Lite Multipoint Rail - Negative.stl` versus the current S3 listing | S4 tells users to download that filename, but records no byte hash, download date, listing revision, units, or physical test. A live same-name file can change. | Authorized current file identity/hash and a section comparison; coupon with the intended male positive. |
| S5 polygonal slot versus any MultiBuild rail | S5 is a community-made cutting die with no cited upstream geometry or stated fit. | Creator measurement method/source, identified variant/file, and a physical mating result. |
| S2 folded rail versus S6 supported/non-folded rail | Similar prose and names do not establish common geometry, revision, or unfold relation. | Original-file identities plus a declared common datum and verified assembly transform. |
| Wio print 1407547 rear `Rail` versus Lite Multipoint Rail | The creator names only “Rail”; its one-file inventory contains no rail geometry or variant. | Creator clarification or the missing Rail CAD/file and an assembly with the Wio holder. |
| 0.25 mm listing tolerance versus a custom receiver clearance | The publisher does not define whether it is total, per-face, radial, or tied to a particular surface. | Exact source geometry and a printer/material-specific fit coupon. |

The following requested specifications remain genuinely missing from original
publisher material inspected here: installed rail cross-section, groove/mouth
width, total rail depth, groove depth, flank/dovetail angles, radii, nominal
male and female dimensions, tolerance allocation, end-stop geometry, slide
travel, retainer/detent geometry, Pegboard Click pair registration, rear
projection, fold hinge axis/angle, and print-frame-to-installed transform.

## Practical handoff

1. For a **Lite receiver**, obtain the licensed current official
   `Lite Multipoint Rail - Negative` file named in S3; record its source URL,
   filename, access date, revision if present, byte hash, units, and licence
   state. Use it as the cut-out reference rather than reproducing S4/S5.
2. For an exposed **positive rail**, distinguish the exact Lite positive from
   the Regular positive listed in S3. S1 establishes the families are related
   but not geometrically interchangeable.
3. For the supplied folded model, obtain the original asset through an
   authorized route and inspect it as data only. Register a tile-front datum,
   Pegboard Click engagement datum, rail slide axis, hinge/fold geometry, and
   final installed transform before modelling around it.
4. Treat the Wio record as a design precedent requiring a separate rear rail,
   not as evidence of any of the profiles above.
5. Print and physically test an interface coupon on the target tile and mate
   before making a fit, retention, end-stop, or load claim. No physical print,
   assembly, or test was performed for this research.

## Search coverage and blocked routes

- Reviewed original MultiBuild documentation; official Thangs records 1123315,
  1142254, 1145162, and 1470823; original creator-owned GitHub repositories
  `IOIO72/containers-on-multipoint-rails` and
  `IOIO72/multiboard-pegboard-headphone-holder`; and the original S5 gist.
- The direct Printables page for 1407547 returns HTTP 403 to the reader. Its
  first-party GraphQL metadata, description and file inventory are already
  captured with reproducible query details in
  [existing-holder-examples.md](existing-holder-examples.md#sources-and-access-record).
  That inventory confirmed the absence of the needed Rail file, rather than
  proving an interface.
- The official Thangs pages make files licence-restricted and expose no
  downloadable source bytes or dimensioned drawing through the inspected page
  text. No vendor asset was downloaded, reverse engineered, executed, or added
  to this repository.
- Searches for published end stops and fold/unfold instructions found no
  original source that supplied a measurable rail terminal condition or an
  assembly transform. Search-engine-only narratives claiming an approximately
  right-angle fold were not treated as evidence.
