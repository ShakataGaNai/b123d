# MultiBuild / MultiBoard adapter reference

Research date: 2026-10-01. Publisher: MULTIBOARD LTD / Keep Making. Work record: [b123d #8](https://github.com/ShakataGaNai/b123d/issues/8).

Purpose: design an object-specific holder with a documented MultiBoard attachment, using this repository's build123d workflow. This record covers the connection system and the three supplied holder examples. It does not promise a dimensioned specification for every vendor part, a physical fit, or an adapter for an unidentified hardware revision.

**Confirmed adapter requirement:** support both **preprinted rails** and **octagon mounting**. The requester identified their AirTag holder as the precedent on 2026-10-01; this is user-confirmed functional evidence, not a newly measured mating profile. Record both routes in each future holder's design contract rather than defaulting to rails alone or to a generic friction-fit insert. Whether one body accommodates both or uses route-specific backs depends on the object's geometry and installation path.

## Read this first

1. [Board geometry and datums](board-geometry.md): nominal grid, board variants, dimensions, source geometry and revision limits.
2. [Attachment interfaces](attachment-interfaces.md): mating chains, snaps/inserts, threads, Peg Click, Fix-Points/rails, geometry gaps and selection guidance.
3. [Ecosystem, printing and licensing](ecosystem-printing-license.md): terminology, official resources, print settings, strength limitations and redistribution terms.
4. [Existing holder examples](existing-holder-examples.md): AirTag, Seeed Wio Tracker L1 Pro and Seeed T1000E; listing evidence, files and any measured geometry.

Use a cited dimension or identified source file for a mating profile. A grid pitch, bounding box, photograph or part name cannot specify snap teeth, thread form, insertion clearance or a locking feature. Keep source dimensions separate from print-fit allowances.

## Primary entry points

| Resource | Use |
|---|---|
| [MultiBuild](https://multibuild.io/) | Ecosystem identity and subsystem navigation |
| [Getting started](https://multibuild.io/get-started) | Current parts, Knowledge Hub, community and planner routes |
| [Parts library](https://multibuild.io/parts) | Find exact components and their descriptions/downloads |
| [Core parts documentation](https://docs.multibuild.io/beginner-section/core-parts-documentation) | Units, named mating families and installation behavior |
| [Printing guidelines](https://docs.multibuild.io/beginner-section/printing-guidelines) | Vendor defaults; check each part for overrides |
| [License](https://multibuild.io/license) and its linked full legal code | Personal use, original-file restrictions and remix publication |
| [Community Promise](https://multibuild.io/community-promise) | License page says this prevails where inconsistent |

The official pages above have no engineering revision identifier in the page text reviewed here. The specialist records identify revision/date information when available. Recheck current downloads before using a changed component.

## Verified system facts

These are authoritative statements from the [core parts documentation](https://docs.multibuild.io/beginner-section/core-parts-documentation), not a complete mating specification. The source gives no manufacturing tolerance for MU/CU.

| Fact | Value / relationship | Modeling consequence |
|---|---|---|
| Multi Unit, MU | Based on 25 mm sizing | Locate compatible board attachments on the documented grid; do not infer tile edge margins |
| Cell Unit, CU | Based on 50 mm sizing | MultiBin sizing; 2 × 2 MU corresponds to 1 × 1 CU in footprint |
| Dimension order | Width (front) × depth (side) × height | Preserve named axes when reading part sizes |
| Small tile holes | Small Threads, Peg Click and nonprinted pegboard accessories | Different interface from the large multihole |
| Large tile holes / multiholes | Snaps and Large Threads | Two alternative mating families |
| Snap mid hole | Bolt-Locked Inserts, Friction-Fit Inserts and Mid Threads | A holder insert mates to the snap, not directly to the tile multihole |
| Moderate weight-bearing snap | Directional; angle insertion | Preserve load direction and installation sweep |
| Heavy weight-bearing snap | Directional; angle insertion; requires wall-offset tiles | Do not select for a flush board without checking clearance |
| Friction-fit insert | Removable by pulling; intended for lightweight accessories | No positive pull-out lock |
| Bolt-locked insert | A Locking Bolt prevents pulling the insert from its snap | Keep bolt access and the complete component chain |
| Multipoints naming | Renamed Fix-Points; Multipoint Rails renamed Rails | Match names across older models and current library |
| Lite Multipoint | 1 mm thinner than Regular; mates to negative rails | Do not interchange hole and rail profiles based on the name |

The official [printing guide](https://docs.multibuild.io/beginner-section/printing-guidelines) specifies 0.2 mm layers, a 0.4 mm nozzle, 3 perimeter walls, 15% infill, no supports and the supplied file orientation, with per-part exceptions. Its statement that most parts have a 0.25 mm tolerance does not define whether that is radial, diametral or per-face. Do not turn it into an automatic clearance offset. Treat the guide's material and strength claims as vendor guidance, not proof for a new holder.

## Default adapter strategy

The following choices are engineering decisions, not vendor ratings:

- Start with the two required routes: a holder mating to the selected preprinted rail, and an octagon-mounting holder following the user-confirmed AirTag precedent. Preserve the object retainer across routes where practical. Do not silently replace either route with a generic friction-fit insert or assume their mating profiles are interchangeable.
- For an object that must resist pull-out, consider a bolt-locked insert with an identified snap and Locking Bolt. A locking connection does not prove strength of the cradle, tile or wall fastener.
- If a screw-clamped plate is enough, use an identified official printed thread/bolt through the holder rather than inventing a thread profile. Measure the shank, head, engagement and access envelope from the exact part before sizing the plate hole.
- For a broad or projecting object, consider separated attachment points to resist rotation. Choose coordinates from the proven grid/frame, and check that multiple connections can engage along a compatible installation path. Do not assume a rigid multi-snap holder can install simply because its centers align.
- Choose Fix-Points/rails when slide-on removal serves the object. Leave the full sliding and release envelope clear; obtain the actual positive/negative profile.
- Treat Multiconnect/community mechanisms as separate interfaces unless the evidence establishes compatibility. Similar names do not establish mating.

No universal safe mass or cantilever length follows from these choices. For design calculations, record object mass, center-of-mass projection and anchor separation. A static moment estimate is `M = m × g × e`; it is a derived load demand, not a printed-part strength rating. Handling, cable pulls and impacts may govern the design.

## What the existing holders contribute

All three originals were retrieved as 3MF through Printables' public API despite page-reader HTTP 403. The [examples record](existing-holder-examples.md) contains file IDs, original download URLs, dates, hashes and section observations.

| Holder | Derived source-mesh envelope, X × Y × Z, mm | Demonstrated design precedent | Board-side limit |
|---|---|---|---|
| AirTag | 35.0 × 36.5 × 13.5 | Small repeated cradle; user-confirmed rail/octagon mounting precedent | Exact mate/profile revision and feature registration remain to be documented |
| Wio Tracker L1 Pro | 60.0 × 32.0 × 45.0 | Carrier for the case it ships with; separate rear Rail | Rail file/revision absent from holder download |
| Seeed T1000E | 62.0 × 19.5 × 24.0 | Card-like pocket; listing mentions a snap | Meaning and mating geometry of that snap remain unidentified |

These are holder bounds in the original mesh frames, not hardware envelopes or fit allowances. The practical precedent is to design the object retainer and the named board attachment separately. No official tile/mate assembly or physical fit was checked.

## Future object intake

A product link or named item is a starting point. First use tool-accessible drawings, official CAD and existing research; ask only for unresolved facts that affect the holder.

For the board-side reference, prefer the original AirTag CAD (STEP or native CAD) and the exact rail/octagon mating-component files, listing links and assembly photos. The published AirTag 3MF is already accessible through the recorded API/download route; no resend is needed. If analytic CAD is unavailable, derive candidate dimensions from those identified meshes, then request only the physical measurements needed to resolve remaining profile/fit uncertainty.

| Needed fact | Record before modeling |
|---|---|
| Object identity | Exact product/revision, case/battery/accessories and intended orientation |
| Supported envelope | Width, depth, height, radii/tapers and contact surfaces; source units and tolerances |
| Mounting geometry | Hole diameters and center coordinates in a declared datum, if used |
| Functional access | Buttons, screen, connectors, antenna, battery cover, ventilation and removal path |
| Cable/tool clearance | Plug insertion, bend space, screw/locking tool access and service motion |
| Retention | Gravity cradle, clip, strap or fastener; insertion direction and desired removability |
| Loads and environment | Mass, projection, handling/pull loads, temperature and indoor/outdoor use |
| Existing board | Tile/plate variant, wall standoff, available attachment parts and occupied neighboring holes |
| Print process | Material, nozzle/layer settings and fit calibration for the intended printer |
| Distribution | Private use or publication/commercial prints; provenance/license of every borrowed interface |

Save object-specific evidence under `research/objects/<object>/README.md`. This MultiBoard record supplies the board-side evidence; it cannot substitute for the object's mechanical specification. A holder mesh establishes that holder's geometry, not the original object's production tolerance.

## Coordinate and parameter contract

This is a proposed local design convention. Source drawings may use another frame; record the transform explicitly.

- Units: mm and degrees. Attachment center is the local origin. Board-facing plane is local `z = 0`; `+z` projects toward the object, `+x` is right and `+y` is up when viewing a wall-mounted board from its front.
- Record the actual board front/rear surfaces and attachment engagement depths relative to that datum. Do not silently treat the tile center plane as its front surface.
- Keep `board_pitch`, source-interface geometry, attachment coordinates, object envelope, chosen clearances, wall/floor thickness and service keep-outs as distinct design parameters.
- For centers on the same documented 25 mm grid, use `(x, y) = (25 i, 25 j)` relative to a chosen grid center. This does not locate interstitial small holes or establish tile edge offsets; use [board geometry](board-geometry.md) for those facts.
- Apply a declared object-to-attachment transform. For manufacturing, rotate the complete design to XY bed / +Z up and record attachment-to-print placement. A wall-view frame and a print frame need not match.
- For any imported interface, record original file/revision/checksum, source units, normalization transform and license. Keep an unchanged source mesh separate from a converted or reconstructed derivative.
- State clearance conventions: radial, diametral or per-face. Check the object pocket and board attachment separately; calibration of one does not establish the other.

## Build and verification handoff

1. Resolve the exact mating geometry and object evidence. If only prose-level interface names exist, choose an available exact component or obtain its source profile before claiming a compatible adapter.
2. Create `models/<name>/model.py` and `model.toml`, with a fresh `build()` result and both research records in its `research` array. Keep reusable helpers beside the model, not in this research record.
3. Maintain `check(shape)` for object clearance, attachment centers/engagement, critical wall/floor thickness, fastener/head space and service keep-outs. Include pull-out locks and installation sweeps where relevant.
4. Run `uv run python scripts/build.py models/<name>`; inspect the timestamped report, STEP round trip and exported STL previews. Export separate printable assembly components independently.
5. Check assembly interference with the exact tile/snap/bolt and the object. Inspect sections through the mating feature; a matching outer bounding box cannot establish engagement.
6. Slice with the intended printer/material. Print an attachment coupon and object-contact coupon where fit is uncertain, then confirm installation, retention and removal on the actual board/object. A valid watertight export is not a physical-fit or load test.
7. Before publication, apply the licensing review in [ecosystem-printing-license.md](ecosystem-printing-license.md). Do not bundle original vendor geometry as an asset pack.

## Readiness and limits

Ready for attachment-family selection, object intake and evidence-led adapter planning. Exact mating-profile readiness depends on the chosen interface and the source geometry identified in the specialist records. No new adapter, physical print, physical fit or load test belongs to this research deliverable.

The detailed records preserve missing dimensions and source-access limitations. Do not fill those gaps from memory or imply that researching the ecosystem makes an arbitrary future object dimensionally specified.

Missing exact mating geometry and the example asset-license-version prerequisite are recorded in [b123d #10](https://github.com/ShakataGaNai/b123d/issues/10), closed as not planned at the owner's request on 2026-10-01. Closure does not resolve these evidence gaps. Official STEP listings identify a route to source geometry, but the observed download flow requires authenticated access. Until an exact mate is acquired or an identified assembly is measured, this reference supports planning rather than guaranteed-compatible connector CAD.

## Research verification performed

- Independently checked official core-part, printing and license text; checked the current snap and shanked-bolt listing descriptions.
- Queried all three holder descriptions/file inventories through Printables' public GraphQL API.
- Verified all three original 3MF SHA-256 values, millimeter declarations and absence of build-item transforms. Ran the repository mesh-inspection CLI on all three untransformed STL derivatives; observed finite coordinates, no zero-area triangles, watertightness and consistent winding.
- Ran the section CLI on T1000E at source `Z = 5 mm`; confirmed the recorded `56 × 7 mm` interior-contour spans. This does not identify a mating profile or a tracker tolerance.
- Ran the local documentation-link smoke check under locked Python 3.14.7: all 12 relative links resolved across the research catalog and five MultiBoard records. No new CAD model, export, physical fit or load test was performed.

## Model linkage and maintenance

Future consuming models should link `research/objects/multiboard/README.md` plus their object-specific record in `model.toml`. No consuming adapter model exists yet. Revisit the chosen interface when upstream geometry, board variant, hardware revision or print process changes; update affected geometry and checks together.

| Date | Change | Verification |
|---|---|---|
| 2026-10-01 | Created coordinated board/interface/printing/license/example research and adapter intake contract | Primary pages reviewed; final link and evidence checks recorded in issue #8 |
