# Holes, hardware, threads, and manufacturing allowances

**Separate evidence classes:** constructor behavior is checked against build123d 0.13.0. Fits, wall choices, clearances, strength, and print settings are engineering decisions, not library guarantees. Use the mating component drawing, applicable fastener standard, supplier instructions, and a calibrated process to establish them.

## Hole intent before hole geometry

Specify whether a hole is clearance, tapped, self-tapping, press-fit, insert pocket, dowel location, counterbore, or countersink. An “M3 hole” is ambiguous: M3 names a thread nominal diameter, not every mating hole size.

Keep parameters explicit:

- `shaft_diameter`: measured or specified mating envelope.
- `diametral_clearance`: added to the diameter, not each side.
- `hole_diameter = shaft_diameter + diametral_clearance`.
- `radial_clearance = diametral_clearance / 2`.
- `hole_radius = hole_diameter / 2` at the build123d API boundary.

A bolt's major thread diameter is not a tap drill specification. Use the correct thread series, pitch, engagement, material, and tapping process. Do not infer a thread standard from the nominal diameter alone.

### Straight bores

`Hole(radius, depth=None)` defaults to subtracting and needs a builder to infer a through depth. Its explicit 0.13.0 depth creates a symmetric ±depth cutter, so use a positioned cylinder or negative extrusion for a tightly controlled blind cavity. See [API semantics](api-and-semantics.md#hole-depth-is-not-cylinder-height).

Use a known datum for hole patterns. Define mounting centers once and reuse them for cutters, bosses, mating parts, and checks. Pattern count, center spacing, and edge distance should all be inspectable. Radius checks alone do not prove correct placement.

### Counterbores

`CounterBoreHole(radius, counter_bore_radius, counter_bore_depth, depth=None)` uses the local XY plane as the entry and extends the bore down local −Z. Place it at the entry face. The relief tool also extends above the entry plane to avoid a coplanar lip.

Choose the recess radius for the **head and tool access**, not only the threaded shank. Preserve material below a blind recess, and account for washers, bearing area, and protrusion. Check the remaining section against load requirements; a visually flush screw is not evidence of adequate strength.

### Countersinks

`CounterSinkHole(radius, counter_sink_radius, depth=None, counter_sink_angle=82)` uses an included angle. Supply the screw's actual head angle explicitly; the API default 82° is not universal.

For bore radius `r`, mouth radius `R`, and included angle `a`, the ideal cone-to-bore transition depth is `(R - r) / tan(a / 2)` with the trigonometric angle converted to radians. This relation describes ideal geometry, not screw tolerances or real head seating. Check that the requested countersink does not break through a thin wall or intersect nearby features.

## Threads: represent only what is needed

Use the least detailed representation that satisfies the deliverable:

| Goal | Representation |
| --- | --- |
| Assembly packaging, access, clearance | Smooth shank/major-diameter envelope, head, and label |
| Tapped manufactured part | Correct pre-machining hole plus drawing/metadata specifying thread and depth |
| Printed mating thread or geometric interference study | Explicit flank profile, pitch, handedness, runout, lead-in, and allowance |

A helix is only a path, not an ISO/UNC/etc. thread. Core build123d provides `Helix` and sweep operations, but a triangle swept along a helix is not automatically a standards-correct thread. Real profiles require crest/root treatment, appropriate pitch diameter, and end/runout geometry. A naive helix sweep can self-intersect or leave disconnected thread teeth.

The checked core signature is `Helix(pitch, height, radius, center=(0, 0, 0), direction=(0, 0, 1), cone_angle=0, lefthand=False, mode=Mode.ADD)`. `radius` is the helix path radius, not automatically a thread's major or pitch radius. Choose it from the profile placement. For multistart geometry, one helix's advance per revolution is the lead; distinguish that from adjacent-thread spacing.

For explicit thread modeling:

1. Establish the thread standard, nominal size, pitch, handedness, internal/external form, and engagement length.
2. Obtain authoritative profile and fit dimensions; preserve the source alongside the model's reusable object research.
3. Choose an explicitly modeled thread library or build a profile in the correct radial/axial plane. Confirm lead/pitch relationship for multistart threads.
4. Extend the sweep enough for trimming at both ends, join/cut it with the body using real overlap, and add specified entry/runout features.
5. Inspect a section, check connectivity and validity, and test the mating geometry through the required motion/engagement range.

[bd_warehouse](https://github.com/gumyr/bd_warehouse) is an optional ecosystem library for parametric hardware and threads, not part of the baseline repository contract. Check its released compatibility and actual signatures before adding it; these references do not promise that its current main branch supports the pinned runtime. Keep fasteners simplified unless detailed threads are required, because helical faces can dominate boolean, meshing, and STEP costs.

## Printed fits: calibrate instead of declaring a universal gap

The same nominal gap behaves differently with orientation, material shrinkage, extrusion width, resin exposure, machine compensation, layer height, seam placement, and postprocessing. A single “0.2 mm tolerance” is not a specification.

A useful calibration procedure:

1. Choose the functional fit: free slide, guided slide, friction fit, press fit, or snap engagement.
2. Print a coupon containing the **actual mating geometry** at several allowances. For an exploratory FDM sliding fit, a per-side gap series such as 0.10 / 0.20 / 0.30 / 0.40 mm is a possible experiment, not a recommended universal answer. Adjust the range to the process and feature scale.
3. Use the final orientation, material, nozzle/exposure, layer settings, and postprocessing.
4. Measure both manufactured members, test function, and record the selected allowance and settings.
5. Apply compensation consistently: enlarging the cavity and shrinking the insert each by the full desired gap doubles the intended clearance.

Wall/floor thickness similarly comes from loads, stiffness, process, and feature scale. For FDM, use slicer previews to confirm useful perimeter structure rather than relying only on nominal CAD thickness. For resin, consider drainage, suction/trapped volumes, and cure distortion. For CNC, account for cutter access, reachable corner radii, tool length, and clamping; a printable closed undercut may be unmachinable.

## Practical manufacturability checks

- Orient loading relative to layer anisotropy; increasing infill is not a substitute for load-path design.
- Give pins and sockets lead-ins where assembly requires them; include their effect on engagement length.
- Separate elephant-foot relief from the functional vertical wall dimensions.
- Use supplier hole diameter/depth and installation guidance for heat-set inserts; validate nearby wall thickness and thermal deformation.
- Check bridge spans, unsupported overhangs, internal support removal, and access to captive nuts.
- Keep fits away from seams and support-contact surfaces when possible, or calibrate those exact surfaces.
- Preserve nominal design dimensions and process compensation as separate named parameters so a manufacturing change is traceable.

## Sources

- [Checked hole/counterbore/countersink source](../../../../vendor/build123d-0.13.0/src/build123d/objects_part.py)
- [Core curve objects, including Helix](../../../../vendor/build123d-0.13.0/src/build123d/objects_curve.py)
- [Sweep implementation](../../../../vendor/build123d-0.13.0/src/build123d/operations_generic.py)
- [Optional bd_warehouse scope and documentation](https://github.com/gumyr/bd_warehouse)

No external fastener standard or printer calibration is bundled as verified dimensional truth here; source those requirements for the specific part rather than converting the examples into a universal fit table.
