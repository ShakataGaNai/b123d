# Evidence-to-parametric handoff

Save the object record using the repository [research contract](../../../../research/README.md) before constructing geometry. Keep its required source, coordinate, dimension, uncertainty and verification tables as the single evidence record. Original STL/STEP files stay separate from generated artifacts; permission determines whether they may be committed. Preserve upstream attribution and applicable derivative/share-alike/noncommercial restrictions when rebuilding geometry parametrically.

## Preserve intent, not triangles

Partition measured features into:

- **Functional:** mating planes, mounting centers, bore depths, floor/wall thickness, locating pins, snap/latch contact faces, connector/access openings, standoff stack and assembly motion. Reconstruct these with explicit parameters and checks.
- **Required clearance:** actual object protrusions plus connectors, plugs, cable bends, tool travel, cooling and service access. An enclosure wall is not the object's envelope, and a hole in a case is not automatically a hole in the board.
- **Cosmetic or optional:** surface texture, lettering, decorative chamfers/fillets and unneeded detail. Simplify only where it cannot change fit, strength, access or the requested appearance; record intentional deviations.

Choose sketches/extrusions for constant sections, revolutions for rotational features and localized cuts for openings. Use arrays only for demonstrated patterns; preserve asymmetric offsets. Avoid converting every mesh triangle into a BREP face. Analytic STEP can supply exact edges and surfaces but does not recreate the source feature/history tree.

Follow the [build123d skill](../../build123d/SKILL.md) for model layout and pinned APIs. A parameterless `build()` returns fresh solid geometry. In `model.toml`, link the object record through its repository-relative `research` path. Explain units, datums, revision, measured-versus-assumed dimensions and calibrated versus assumed allowances in model documentation/metadata using existing conventions; do not invent a parallel metadata schema.

## Acceptance at the interface

Implement the model's `check(shape)` around requirements that survive construction and STEP reimport:

- Mounting center coordinates and bore **radius** (convert documented diameter once at the CAD API boundary).
- Floor thickness and blind-bottom height independently; a generic volume/bounds match cannot prove either.
- Boss/support elevations and locating-pin heights in the documented frame.
- Wall/port keep-outs at the actual relevant sections, not only the global AABB.
- Intentional multipart transforms, mating gaps and assembly/tool motion clearances.

Use named tolerance values justified by the reconstruction requirement; separate numerical CAD-check tolerance from mesh uncertainty and print-fit allowance. A simplified model need not duplicate source volume or every cosmetic edge.

Run the repository build/export path and inspect its report and actual STL views, including bottom and perpendicular sections that expose blind cuts. Do not equate watertightness, native validity or STEP round-trip success with hardware fit, thermal suitability or strength. Fit-critical uncertain interfaces need a physical coupon/specimen check before any print-ready claim.

The final handoff identifies source hashes and license basis; native units and adopted scale; coordinate transforms; adopted dimensions with evidence and uncertainty; preserved/simplified features; consuming model paths; executed checks and output paths; and unresolved physical/revision assumptions. Matching the stock enclosure is a separate claim from matching the enclosed hardware.
