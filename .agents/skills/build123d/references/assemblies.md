# Assemblies, placements, and interference

## Grouping is not fusion

Use `Compound(children=[...], label="...")` to preserve independently named assembly components. Use a union only when components represent one continuous manufactured body. A compound does not resolve interference or turn disconnected volumes into one solid.

Return a compound from `build()` for intentional multipart geometry, and invoke the build tool with `--expected-solids N`. Keep an assembled configuration and a print-bed layout conceptually separate: a working assembly may include raised, rotated, or interlocking parts that are not directly printable in that arrangement. Export individual manufactured members or an explicitly arranged print layout when required.

Set labels such as `base`, `lid`, and `spacer_left` on actual finished shapes. Colors aid review but do not define topology or material requirements. STEP can preserve richer assembly semantics than STL; an STL is tessellated geometry without the assembly tree or unit metadata.

## Coordinate ownership

In the 0.13.0 assembly tree, a child's `.location` is relative to its parent. `.global_location` accumulates ancestor transforms. A transformed parent moves the group without changing each child's local placement.

For arbitrary nested assemblies, compare parts in a common frame. A detached copy of a child placed with `child.global_location` is suitable for a world-frame query; do not multiply its already accumulated transform twice. For a flat assembly under an identity root, component locations already share a frame and direct pairwise queries are simpler.

Build prototypes around meaningful local datums: a pin along local Z with its insertion end at zero, a plate with a base datum, or a lid with its mating plane defined. Placement then becomes a mechanical relation rather than a compensating chain of translations.

Use separate instances for repeated parts. `copy.copy(prototype)` shares the underlying OCCT geometry while giving the instance its own placement/metadata; use it for many immutable identical screws/spacers. `copy.deepcopy` duplicates geometry and is appropriate when independent geometric edits are needed. Attaching the same Python node to a second parent reassigns its parent rather than creating a second occurrence.

## Interference and clearance are separate tests

For two solids in the same coordinate frame:

1. **Interference:** compute their common solid region and inspect its volume. A nonzero common volume means overlap. A touching face/edge can have zero common volume.
2. **Clearance:** use `a.distance_to(b)` for minimum separation. Zero can indicate touch or overlap, so it does not distinguish them by itself.
3. **Function:** check insertion/removal access, fastener/tool envelopes, and the required range of motion. A collision-free final pose does not prove an assembly path exists.

For a known coaxial pin and bore, the radial gap `(bore_diameter - pin_diameter) / 2` is an independent analytic check. Check both diameter and concentric placement; a large bore with an offset pin can still bind. Use a positive small numeric tolerance for interference volume to account for kernel numerical noise, but do not reinterpret that tolerance as a manufacturing allowance.

A bounding-box test is a useful early rejection for many parts, not a definitive collision test. Rotated or hollow components can have overlapping boxes and no material interference. Pairwise material queries are required for candidates.

### Pairwise query fragment

```python
# Fragment: a and b are finished solids/parts in the SAME frame.
common = a & b
common_volume = 0.0 if common is None else sum(s.volume for s in common.solids())
assert common_volume < 1e-7, "Unexpected material interference (mm^3)"
minimum_gap = a.distance_to(b)
```

The intersection operator can return `None` for disjoint shapes in 0.13.0; handle it before querying topology. Choose a meaningful scale-aware volume threshold for your own model. Use intentional contact allowances for mating seats; requiring positive separation everywhere would reject legitimate seating contact.

## Joints and kinematics

build123d offers `RigidJoint`, `RevoluteJoint`, `LinearJoint`, `CylindricalJoint`, `BallJoint`, and other joint helpers. They describe relationships and positions; they are not a dynamic simulation or an automatic proof of collision-free motion. Verify the particular joint's constructor and `connect_to` parameters before use because joint types have different degrees of freedom.

For fixed assemblies, explicit `Location` composition is often sufficient. For a mechanism, define joint axes/datums consistently, sample its required motion range, and test moving members against static obstacles at each relevant pose. Finite sampling can miss an intermediate collision: use conservative swept envelopes or a finer/adaptive analysis for critical clearances. Document any unverified continuous-motion requirement.

## Sources

- [0.13.0 assembly tree, global locations, and copy behavior](../../../../vendor/build123d-0.13.0/docs/assemblies.rst)
- [Joint concepts](../../../../vendor/build123d-0.13.0/docs/joints.rst)
- [Shape distance/intersection and global_location implementation](../../../../vendor/build123d-0.13.0/src/build123d/topology/shape_core.py)
- [Complete separated pin-and-bushing recipe](recipes.md#pin-and-bushing-assembly)
