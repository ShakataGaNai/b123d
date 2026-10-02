# Measured AirTag octagon and supplied rail

Research date: 2026-10-01. Follow-up to [the holder evidence](existing-holder-examples.md) using the author's confirmed octagon attachment and supplied rail. Dimensions are derived from uploaded meshes, not physical measurements or print-fit tolerances. Future adapters must preserve both mounting routes.

## AirTag rear octagonal peg

Source: [Printables model 1407536](https://www.printables.com/model/1407536-airtag-holder-for-multiboard), file `5927171`, `Multiboard AirTag.3mf`. Original SHA-256: `14b251de08c6094763477e85d1e45d572b9110b89d06a10307bc510cba15ef73`. Original download and license evidence are in the holder record. The archive declares millimeters; the mesh was extracted without scaling, repair or transformation.

The author identifies the rear feature as the octagon mounting interface. Its source frame has the peg cross-section in XZ, centered at `(X, Z) = (0, 6.75)`, with the holder-side root at `Y = 15` and the rear tip at `Y = 21.5`. These are the holder mesh's coordinates, not the board's assembly coordinates.

The author confirms that the octagonal pegs insert into **snaps** and selects **6.5 mm projection** for this reference interface. Use **13.5 mm across flats × 6.5 mm projection** for future holders following the AirTag precedent. The [community follow-up](community-specifications.md) records a separate 13.45 mm-wide, 11 mm-long male peg; that length is not the selected design. The snap variant/revision is unspecified, but the receiver family is confirmed. The peg does not engage the tile's large Multihole directly.

| Derived feature | Source-mesh dimension |
|---|---:|
| Opposite flats, all four directions | approximately 13.5 mm |
| Opposite corners | approximately 14.6123 mm |
| Each octagon side | approximately 5.59188 mm |
| Projection from holder root to tip | 6.5 mm |
| Source-oriented peg envelope X × Y × Z | 13.5 × 6.5 × 13.5 mm |

Sections at source `Y = 15.25`, `18`, and `21.25` have the same eight-sided outline. This is a straight octagonal prism, not a 25 mm octagon. The documented board grid pitch is a separate dimension.

For analytic reconstruction, let `a = 6.75 mm`, `b = a × tan(22.5°) ≈ 2.7959415 mm`. In a centered cross-section, the vertices are `(a,b)`, `(b,a)`, `(-b,a)`, `(-a,b)`, `(-a,-b)`, `(-b,-a)`, `(b,-a)`, `(a,-b)`. Extrude 6.5 mm normal to that plane. Equivalent circumradius: `a / cos(22.5°) ≈ 7.30615 mm`.

For the isolated viewer only, the source coordinates become `(X, Y − 15, Z − 6.75)`. The root is at viewer `Y = 0`, tip at `Y = 6.5`; no rotation or scaling is applied. The cut root is capped for display, and the holder body is omitted. This reconstruction does not assert board-hole dimensions, retention force, or fit compensation.

Reproduction with the project measurement helper, after extracting the declared-millimeter 3MF mesh to an untransformed temporary STL:

```sh
uv run --locked python .agents/skills/stl-measurement/scripts/measure.py section tmp/multiboard-mating/airtag-derived.stl --axis y --offset 18 --max-loops 12
```

The helper reports one closed contour spanning 13.5 × 13.5 mm and correctly rejects a circular fit. Explicit contour simplification and vertex/edge measurements establish the octagon dimensions above. Extra decimal places describe mesh arithmetic, not manufacturing accuracy.

## Supplied preprinted rail

Source: author's supplied `Pegboard Click - Multipoint Rail (Folded).stl`, associated with [official Thangs model 1123315](https://thangs.com/designer/Multibuild/3d-model/Pegboard%20Click%20-%20Rail%20%28Folded%29-1123315). The listing title is currently “Pegboard Click - Rail (Folded)”; its description calls it a 2-Multihole rail for slide-on negative-rail accessories.

Original STL SHA-256: `48128775adfdfe056ea6cf1a1bea2d03708934800c386b6cae890130bf4280cd`. Inspection found 5,612 triangles, finite coordinates, zero degenerate triangles, watertightness and consistent winding. Native X × Y × Z spans are approximately 25.6 × 40.995 × 7.6. STL has no declared units; treating these coordinates as millimeters is an explicit assumption consistent with the ecosystem, not a file declaration.

The file describes the **folded print state**, not the installed rail cross-section. Its native bounds or a single folded section must not be copied as the installed negative receiver. Sections at native `Y = -20`, `-12.5`, and `-5` were inspected without transforming the mesh. No verified fold-to-installed transformation, installed assembly interference check or physical fit was established.

The existing Wio holder is a useful negative-rail example: its listing explicitly requires a rail. A source `Z = 10` section exposes the rear groove, with straight rear-region edges around `Y = 14.1–16` and X coordinates reaching `±8.5`. These are local section observations, not a complete receiver specification or proof that the supplied folded rail mates with it. Recover the installed source geometry/assembly datum before deriving a universal rail receiver.

## Visualization and remaining checks

The requested self-contained HTML is generated at `outputs/research/multiboard/airtag-peg.html`. It contains an isolated 32-triangle display mesh, embedded Plotly, dimension labels and isometric/end/side camera controls. Browser inspection verified the octagonal end and rectangular side views, no external scripts, and the corrected narrow-screen layout. Generated output is ignored and is not a substitute for CAD or physical-fit evidence.

The octagon source profile is now sufficient to reproduce the author's peg geometry. A representative printed coupon is still required to establish insertion, retention and printer/material compensation against the actual mating part. Rail installation geometry and exact mating assembly remain unverified. Other proprietary snap/thread profiles and license-access gaps remain tracked in [issue #10](https://github.com/ShakataGaNai/b123d/issues/10).
