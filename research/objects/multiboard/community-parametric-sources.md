# Community parametric source inspection

Research date: 2026-10-01. Scope: published creator-owned CAD/source
text inspected **statically** for useful MultiBuild/MultiBoard mating
geometry. No downloaded model, script, macro, or STL was executed; no vendor
asset is committed. These sources are evidence of their authors' designs, not
an official MultiBuild specification. See [attachment-interfaces.md](attachment-interfaces.md)
for the official-source boundary.

## Result first

The strongest new lead for the author's measured AirTag rear **male** straight
octagon (13.5 mm across flats (AF), 14.6123 mm across corners (AC), 6.5 mm
projection) is a published, independent OpenSCAD adapter by `k0nze`:
`mb_snap_inner_octagon_width = 13.45` constructs an **additive male octagonal
peg** by intersecting two equal squares, one rotated 45 degrees ([S1]). The
Boolean call site places this positive feature outside the surrounding
`difference()`; it uses `snap_height = 11` along its axial direction. For a
regular octagon, that source's 13.45 mm AF gives 14.558 mm AC and 5.571 mm
sides.

This is a close *community-design correspondence*, not proof of a mating
chain: its nominal AF is 0.05 mm less and its axial length 4.5 mm greater than
the author's 13.5 mm × 6.5 mm male peg. Those are dimensions of two separate
male designs, **not** a socket/peg interference or a fit allowance. S1 calls
the feature a `Multiboard snap insert`, but does not name the board-side
receiver, tile revision, an official source file, or a physical fit. In
particular, it must **not** be described as a direct large-board-hole fit.
The author confirms that their octagonal pegs insert into snaps and selects
**13.5 mm across flats × 6.5 mm projection** for the reference interface.
The particular snap variant/revision remains unspecified.

The public rail sources found are either (a) cutters which construct a
community rail/Fix-Point slot or (b) accessories which import MultiBuild's
restricted `Lite Multipoint Rail - Negative.stl`. Neither identifies the
installed transform for the supplied folded official rail or proves that its
profile is the same as the supplied rail.

## Evidence register

All GitHub `git/blobs/<SHA>` links below are immutable content objects; a tree
SHA is retained where GitHub exposed it as the inspected repository snapshot.
Dates are commit dates only where returned by the source API; otherwise
publication/revision date is unknown. `Source-authored` means the creator
published the source, not that MultiBuild endorsed the geometry.

| ID | Creator source and exact inspected record | Date/revision | Origin and rights | What it supplies |
|---|---|---|---|---|
| S1 | k0nze, [`multiboard.scad`](https://api.github.com/repos/k0nze/wera_kraftform_holder_multiboard_adapter/git/blobs/fe553c95756414fdbca3b725add57addb224f3c9) and [adapter call-site](https://api.github.com/repos/k0nze/wera_kraftform_holder_multiboard_adapter/git/blobs/70344203e16606d3a5c83f3c812352a086f42140), repository tree [`8b74ae5d…`](https://api.github.com/repos/k0nze/wera_kraftform_holder_multiboard_adapter/git/trees/8b74ae5d56c5892404208c202163e82988ea552e?recursive=1) | Date unknown; inspected tree snapshot | Independent recreation/adapter; repository declares [CC0-1.0](https://github.com/k0nze/wera_kraftform_holder_multiboard_adapter/blob/main/LICENSE). No vendor asset import occurs in the source. | 13.45 mm additive male octagonal-peg construction and 11 mm axial extent. |
| S2 | haliphax, [`parts/snap.scad`](https://api.github.com/repos/haliphax/multiboard-openscad/git/blobs/94044f1ed716e14c085b83c72d950a20492e993e) and [`parts/README.md`](https://api.github.com/repos/haliphax/multiboard-openscad/git/blobs/90e61226631bde66c778a18f23f91bf55dafe23e), tree [`95a37a6b…`](https://api.github.com/repos/haliphax/multiboard-openscad/git/trees/95a37a6b75fe3feaac61db63dfac0576480ac1df?recursive=1) | Repo created 2026-07-13; source date unknown | Independent community library; [MIT](https://api.github.com/repos/haliphax/multiboard-openscad/git/blobs/a5d34377c8924ef0eee89161d174ed7cd81bd157), copyright 2026 haliphax. | A positive `snap()` with octagonal body, flare, four prongs, and slots. |
| S3 | haliphax, [`parts/fix-point-slot.scad`](https://api.github.com/repos/haliphax/multiboard-openscad/git/blobs/b5f2a8359cbf34de31f43f7fd3e8b96b65212705), [part description](https://api.github.com/repos/haliphax/multiboard-openscad/git/blobs/90e61226631bde66c778a18f23f91bf55dafe23e), same tree as S2 | Repo created 2026-07-13; source date unknown | Same independent MIT library. | Analytic 1×1 LU Fix-Point slot *cutting solid*, including a 2.2 mm transition. |
| S4 | asciipip, [`multiboard_base.scad`](https://api.github.com/repos/asciipip/multiboard-parametric-stacked/git/blobs/c65b53c0e001cabc4f76cde64d4cde0b4748d7ab), [README](https://api.github.com/repos/asciipip/multiboard-parametric-stacked/git/blobs/fb313d047aa5fd13bdda43f7762a46609198d041), tree [`4db5f07a…`](https://api.github.com/repos/asciipip/multiboard-parametric-stacked/git/trees/4db5f07abb4653193014eb1bba761011bc29eb87?recursive=1) | Source says values are based on MultiBoard tile remixing files uploaded 2024-01-19; inspected snapshot | **Vendor-derived** recreation/fork of S5, explicitly covered by the included [MultiBoard licence](https://api.github.com/repos/asciipip/multiboard-parametric-stacked/git/blobs/6dc1752700b1680b1c27e539e32a19d4422a1250), not an open interface grant. | Full analytic tile multihole and small/peg-hole construction, nominal threads, and no accessory octagon socket. |
| S5 | Victor Zagorski (`shaggyone`), [`multiboard_base.scad` at commit `d9131ab…`](https://github.com/shaggyone/multiboard-parametric/blob/d9131ab8480de327c34618820c12212b1e8063c7/multiboard_base.scad) and [README](https://github.com/shaggyone/multiboard-parametric/blob/d9131ab8480de327c34618820c12212b1e8063c7/README.md) | 2024-02-12 commit, source API author Victor Zagorski | Original of S4's named lineage; repository carries no licence file / API licence is `null`. README points to a Keep Making official tile listing but does not say that its numeric recreation was approved. | Earlier similar tile/hole formulas; useful conflict/provenance only. |
| S6 | IOIO72 / Tamio Honma, [`multiboard-pegboard-headphone-holder.scad`](https://api.github.com/repos/IOIO72/multiboard-pegboard-headphone-holder/git/blobs/75feb74eb4b6496b4bb37af5845cf3d44a07a48b) and [README](https://api.github.com/repos/IOIO72/multiboard-pegboard-headphone-holder/git/blobs/67c847d4375b30d22ec67f1c9c7a34f3b0dd4cc8), tree [`58661c72…`](https://api.github.com/repos/IOIO72/multiboard-pegboard-headphone-holder/git/trees/58661c723ac5ed88a3b03061712406508e5dbc3a?recursive=1) | Latest source-file commit returned 2024-12-27; inspected tree snapshot | Accessory uses the creator's own MIT SCAD, but requires downloaded official `Pegboard Click.stl` and `Lite Multipoint Rail - Negative.stl`; generated models are CC BY-NC-SA 4.0 ([license](https://api.github.com/repos/IOIO72/multiboard-pegboard-headphone-holder/git/blobs/6a8569cc3c80c0ecd30edbf2c142856b47098e77)). | Placement conventions and a 2.2 mm rail-depth assumption, **not** a rail profile. |
| S7 | IOIO72 / Tamio Honma, [`Container On Multipoint Rails.scad`](https://api.github.com/repos/IOIO72/containers-on-multipoint-rails/git/blobs/bad94f5b65ceed7d4cc2872998004f95dbb71a1a) and [README](https://api.github.com/repos/IOIO72/containers-on-multipoint-rails/git/blobs/29cddb1361b24922f96bd969055d29cb769456de), tree [`d0e018db…`](https://api.github.com/repos/IOIO72/containers-on-multipoint-rails/git/trees/d0e018db890c4580b176f6f7b8d0b09ccaf8c3d6?recursive=1) | Latest source-file commit returned 2025-06-20; inspected tree snapshot | Same MIT-for-SCAD / CC BY-NC-SA-4.0-for-generated-models split ([license](https://api.github.com/repos/IOIO72/containers-on-multipoint-rails/git/blobs/e363c0445c049ab9db51221b366c87d1e7fbb2ea)); imports official negative rail STL. | A conservative rail-safe-zone placement convention, **not** a profile. |
| S8 | B20bob, [`multiboard_gen_v1-1-3.scad`](https://api.github.com/repos/B20bob/Multiboard_local_Plate_Generator-OpenSCAD/git/blobs/eaab9934e28671ca5ec456fa2675929a0981c650), [README](https://api.github.com/repos/B20bob/Multiboard_local_Plate_Generator-OpenSCAD/git/blobs/91cf490a1177d56158e5c38414844be7b80141cb), tree [`3907cce2…`](https://api.github.com/repos/B20bob/Multiboard_local_Plate_Generator-OpenSCAD/git/trees/3907cce28827f1d42c10a6b5c4c13d161f6f3a31?recursive=1) | Source calls itself v1.3.0; repo date unknown | Imports included base STLs; no SPDX/licence file. README calls logic open source but says the MultiBoard system/base STLs are Keep Making material. | 25/50 mm array placement only; no profile source. |

## Extracted geometry

`AF` and `AC` below name the exact convention. OpenSCAD itself is unitless.
Values below are interpreted as millimeters in the 3D-printing context; this
is an assumption unless the linked author explicitly states mm. Derived math
preserves the source construction without raising its authority.
No row supplies a published manufacturing tolerance or a fit clearance unless
it says so explicitly.

| Interface; sex and datum | Constants / construction | Depth, chamfer, clearance | Evidence and limitation |
|---|---|---|---|
| **S1 `mb_snap_inner_octagon`: additive male peg**, centered source cross-section, axis is the caller's local X after `rotate([0,90,0])` | `width = 13.45` mm. Intersect a 13.45 × 13.45 square with a copy rotated 45°. Thus regular-octagon **AF = 13.45**, **AC = 13.45 / cos(22.5°) = 14.558** mm; edge `= 13.45 × tan(22.5°) = 5.571` mm. | The additive call site sets `snap_height = 11` mm and extrudes centered, creating an 11 mm axial male peg. No lead-in, chamfer, taper, backlash, or clearance is authored. | **Source-authored / independent.** The source symbol calls it `inner octagon`; README calls the surrounding object a MultiBoard adapter and `snap insert`, but neither identifies its female mate. Compared with author-measured male peg: 13.45 vs 13.5 AF (-0.05 mm) and 11 vs 6.5 mm axial length; these are two separate male constructions, not an interference calculation or a fit allowance. This does not prove fit or identify a board hole. |
| **S2 `snap`: positive male snap**, local Z insertion axis | Bottom regular octagon vertices `(±10.57, ±4.38)` permutations: **AF 21.14**, **AC ≈22.883**, side ≈8.76 mm. `linear_extrude(4)` makes this lower prism. A hull from z=4.00 to z=5.52 expands to top vertices `(±11.43, ±4.73)`: **AF 22.86**, **AC ≈24.739**, side ≈9.46 mm. | The authored 1.52 mm planar frustum is the only lead-in/flared section. Four prongs are 90° apart; each uses source-profile points `(0,0)`, `(0.6,0.48)`, `(1,0.48)`, `(2.24,0)` and is 3 mm extruded. Four perimeter slots cut a 7.16 × 0.8 × 3.41 mm region plus a 7.16 × 1.61 × 1 mm upper enlargement, at local `[-3.58, 8.97, -0.01]` before rotation. | **Source-authored / independent.** The README only calls it a “Basic snap for attaching objects to Multiboard panels.” No tile revision, tolerance, load evidence, or physical test is given. Its 21.14–22.86 mm AF family is not the 13.5 mm AirTag peg. |
| **S3 `fix_point_slot`: female/cut negative**, the polygon's local XY face; actual cut solid is translated +1.99 mm X then rotated `[0,-90,0]` | At one end face (`inside_pts`): bounded 0–33.5 mm along profile X and ±8.5 mm along profile Y (33.5 × 17 mm envelope); named vertices make 1.5 mm steps at X 7.5/9 and 16/17.5, then a 5 mm diagonal to X=33.5, Y=±3.5. Opposite face (`outside_pts`) reaches 0–32 mm and ±8.5, with 1.5 mm step/chamfer-like changes and 4 mm diagonal to `(32,±3)`. | Hull corresponding vertices across `z_dist = 2.2` mm; tiny `eps=0.01` caps. This is an **offset between two unequal profiles**, not a separately declared fit gap. README calls it a 1×1 LU Fix-Point connection slot and says to cut/repeat every **25 mm** for larger slots. | **Source-authored / independent.** It has no provenance assertion to official rail/Fix-Point geometry and no assembly/fold datum. Use as a documented candidate cutter only after physical comparison to the exact rail; do not substitute it for the supplied folded rail's receiver. |
| **S4 MultiBoard tile `multihole`: board-side female large hole**, Z=0/6.4 tile faces | `cell_size=25`, `height=6.4`; `multihole_thin_size=23.4` and `multihole_thick_size=21.4` are regular-octagon **AF** values. Source calculates radius `AF/[2(1+2cos45°)sin22.5°]` to make the octagon; it rotates it 22.5°. Centers are at `(25i+12.5,25j+12.5)`. | `multihole_thick_height=2.4`: taper 23.4 AF →21.4 AF from z=0 to 2.0, straight 21.4 AF z=2.0–4.4, taper back 21.4→23.4 z=4.4–6.4. The source adds a modeled trapezoidal thread: `d1=22.6`, `d2=21.4`, radial-wall height 0.5, inner height 1.583, pitch 2.5. These are source geometry parameters, not published tolerances. | **Vendor-derived community reconstruction.** It explicitly says it is based on official remix files but is not itself an official file. Its narrowest large-hole AF=21.4, so it cannot directly receive a 13.5 AF peg without an intervening component. |
| **S4 `peg_hole`: board-side female small/peg hole**, same Z datum | Circular, not octagonal: **diameter 7.5** at the face and **diameter 6.0** in the middle. It is placed at `(25i+25,25j+25)` only where its cell-neighbor logic permits. The source's thread profile is `d1=7`, `d2=6`, radial-wall height .77, inner height 2.5, pitch 3.0; source rotates the thread -129°. | `peg_hole_thick_height=2.9`: 7.5→6.0 taper z=0–1.75, straight 6.0 z=1.75–4.65, taper out z=4.65–6.4. No authored clearance. | **Vendor-derived community reconstruction.** A 13.5 mm octagon is neither this 6–7.5 mm circular small hole nor evidence of a Peg Click pair. |
| **S6/S7 Lite Multipoint Rail negative: imported female cutout**, creator accessory local frames | S6 calls `multipoint_rail_max_width=18.6`, `multipoint_rail_max_depth=2.2`, and uses a 36.8 mm rail height; S7 sets `multipoint_rail_depth=2`, then defines `multipoint_rail_safe_zone = 2 + back_wall`. Both use 25 mm grid placement; S7 places a second rail `n×25` mm away. | S6 subtracts an imported official `Lite Multipoint Rail - Negative.stl` after a source-specific rotate/translate; S7 likewise imports/rotates it. Values are accommodation/placement envelopes, not profile measurements or clearance. | **Mixed provenance.** The code never contains the rail profile: the README tells the user to download the official remix STL. Thus these records cannot establish the supplied folded rail's installed cross-section, transform, or mate. |
| **S8 octagon-board array: imported mesh assembly**, local XY | `hole_pitch=25.0`, `block_pitch=50.0`; each imported 2×2 block is translated `(50x,50y,0)`. | No profile, depth, chamfer, or allowance is authored; program selects edge/corner mesh assets. | **Vendor-geometry dependent.** Useful only as a separate community confirmation of 25/50 placement nomenclature; not an adapter profile. |

### S5 versus S4 reconstruction conflict

The named upstream source S5 is not independently licensed and should not be
copied into an adapter. It is recorded because S4's README says its work is
based on Victor Zag's project. S5 uses `height=6.4`, 25 mm cells, large-hole
AF values 21.4/23.4 and 2.4 mm middle band—the same broad large-hole family as
S4—but differs in small-hole and thread constants: `hole_sm_d=6.069+0.025`
(6.094 mm), small thread `d1=7.025`, `d2=6.069`, height 0.768/2.5, while S4
uses 7.5/6.0 face/middle diameters and 7/6, .77/2.5 thread parameters. Neither
source supplies a physical measurement, tolerance, or evidence that it matches
current production. Treat the difference as a revision/reconstruction conflict,
not as an allowance to average.

## Reusable static construction descriptions

These are safe to reuse as *provenance-labelled construction recipes*, not as
general compatibility claims:

1. **Community male peg construction (S1):** intersect a centered square
   `w=13.45` with its 45° rotation and add 11 mm along its axis. This describes
   S1 only. For the requested reference interface, use the author's
   **13.5 mm across-flats × 6.5 mm projecting male insert into a snap**.
   Treat printer compensation separately; do not adopt S1's longer peg.
2. **Community basic snap (S2):** extrude the 21.14 AF octagon 4 mm; hull to
   the 22.86 AF octagon at z=5.52; add four rotated prongs and subtract the
   four documented slots. It is a distinct large snap, not a template for the
   13.5 mm peg or the official current snap.
3. **Community 1×1 Fix-Point cut (S3):** hull the two cited 14-vertex profiles
   2.2 mm apart, apply S3's +1.99 X offset and `[0,-90,0]` rotation, cut it
   from an accessory; repeat on 25 mm centers only when the intended route is
   that exact creator's LU slot. Do not use the `2.2` transition as FDM
   clearance.
4. **Vendor-derived board reconstruction (S4):** build a 6.4 mm tile from
   25 mm cells; cut a 23.4/21.4/23.4 AF octagon with 2.0/2.4/2.0 mm
   taper/straight/taper Z zones, then apply that source's thread mesh only if
   its licence/provenance permits. This is useful to compare geometry, not a
   licence-safe replacement for official source data.

## What remains blocked

- **Snap revision:** the author confirms that the 13.5 mm across-flats,
  6.5 mm projecting peg inserts into a snap. Its particular variant/revision
  remains unspecified. S1's female mate is still unspecified in that source.
- **Rail assembly:** no source supplies the supplied folded rail's installed
  fold transform, board datum, end-stop, or a verified relation between the
  folded official rail and S3's analytic slot. Do not derive a universal rail
  negative from either.
- **Fit / tolerancing:** no inspected source gives a usable radial, diametral,
  or per-face fit allowance for the unidentified S1 mate, S2 snap, S3 slot, or
  S4 hole. The author-measured AirTag dimensions are mesh-derived geometry, not
  a production tolerance. A physical coupon remains required.
- **Authoritative public profile:** searches did **not** find an official
  dimensioned drawing or an authoritative public full profile for this octagon
  receiver or installed rail. Community public sources exist, but their claims
  and geometry cannot close that gap.

## Search coverage and blocked routes

Searched GitHub repository metadata and static source for `Multiboard` /
`MultiBuild` plus `OpenSCAD`, `rail`, `octagon`, `peg`, `FreeCAD`, `CadQuery`,
and Fusion-parameter terms. The productive primary source set above includes
independent sources, a clearly vendor-derived fork, and sources that explicitly
import official remix assets. Additional GitHub result families (covers,
trays, generic storage, and unrelated mounting ecosystems) were not recorded
as geometry evidence unless they supplied a static, interface-specific source.
GitHub code-search API required authentication (HTTP 401); several repeated
commit-history API requests were rate-blocked (HTTP 403). Those blocks do not
affect the exact source-blob/tree records cited above. Web-search snippets that
suggest generic Fusion clearances or reinterpret the 25 mm grid were rejected;
they are not primary geometry evidence.

No GitLab, FreeCAD, CadQuery, build123d, JSCAD, or creator-published Fusion
parameter/dimension source with an independently inspectable near-match
13.5 mm **female receiver** or installed rail profile was found in this
search. This is an absence within the stated search coverage, not evidence that
no such source exists.
