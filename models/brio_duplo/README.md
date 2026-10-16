# BRIO-style track and DUPLO wagon

Original, printable trial-fit designs, not manufacturer CAD or certified toys. Track and DUPLO nominal dimensions are informed by the repository's [wooden-track research](../../research/objects/brio-wooden-track/README.md) and [DUPLO research](../../research/objects/lego-duplo/README.md). Socket clearance, chassis, wheels, axle layout and graded-track geometry are original design choices. Physical fit, durability and child safety remain unverified; small removable parts and hardware are not suitable for unsupervised child use.

## Configurable track

`track/model.py` has one parameterless `build()` entrypoint. It reads `track/config.toml` at invocation; importing the configuration module does not read files or build geometry. All configuration dimensions are millimeters and angles are degrees. `BRIO_TRACK_CONFIG` selects another TOML file. Relative paths resolve from `track/config.py`'s directory, **not** the working directory; absolute paths also work.

From the repository root:

```sh
uv run python scripts/build.py models/brio_duplo/track --step
BRIO_TRACK_CONFIG=presets/large_left.toml uv run python scripts/build.py models/brio_duplo/track --step
BRIO_TRACK_CONFIG=presets/rise.toml uv run python scripts/build.py models/brio_duplo/track --step
```

Every snapshot specifies these fields:

| Field | Meaning | Default |
| --- | --- | --- |
| `length` | Straight shoulder-to-shoulder length; ignored for curves | 54 |
| `turn_radius` | Horizontal centerline radius of a curve | 202 |
| `turn_angle` | Signed turn in degrees; positive left, negative right, zero straight | 0 |
| `rise` | End height minus start height | 0 |
| `double_sided` | Grooves on both faces; `false` retains a plain underside | true |
| `ends` | Start and end connector names, each `female` or `male` | `["female", "male"]` |
| `end_flat` | Level horizontal-path pad at each end of graded tracks | 24 |

Unknown keys, invalid types (including booleans in numeric fields), nonfinite dimensions and invalid connector names are rejected. Turns are strictly between −180 and 180 degrees; radius must exceed the 20 mm half-width. Geometry requires at least 41.4 mm horizontal route length for independent connector pockets, `end_flat` ≥21.2 mm, and enough middle length that the ideal eased grade's maximum slope is ≤0.5 mm/mm. These are this implementation's geometry limits, not toy specifications.

The start shoulder is `(0, 0)` with initial tangent along +X; +Z is up. The curve's circle center is `(0, sign(angle) * radius)`. Its endpoint is `(radius * sin(abs(angle)), sign(angle) * radius * (1 - cos(abs(angle))))`, using radians for trigonometry. Grades use level end pads and a smooth middle with zero slope at each join. Falling tracks are lifted so the lower endpoint is at Z=0. Double-sided means grooves on both faces, not that a graded track is guaranteed interchangeable when flipped.

Flat curves are exact circular sweeps. Graded transitions are smooth lofts through
explicitly oriented sections, not copies of BRIO bridge parts. Their normal
cross-section preserves the grooves and thickness; CAD checks sample the ideal
route with a 0.04 mm material-probe tolerance rather than certify global surface
error. Splitters and mergers intentionally belong in separate models.

Complete presets in `track/presets/`:

| File | Configuration |
| --- | --- |
| `default.toml` | 54 straight, female/male, double-sided |
| `male_male.toml` | 54 straight, male/male, double-sided |
| `female_female.toml` | 54 straight, female/female, double-sided |
| `single_sided.toml` | 54 straight, female/male, single-sided |
| `large_left.toml` | Radius 202, +45 degrees |
| `large_right.toml` | Radius 202, -45 degrees |
| `tight_left.toml` | Radius 110, +45 degrees |
| `rise.toml` | Length 216, rise +18 |
| `fall.toml` | Length 216, rise -18 |
| `curved_rise.toml` | Radius 202, +45 degrees, rise +18 |

Curves and grades otherwise retain mixed female/male ends, double-sided grooves and 24 mm end pads. Connectors and double-sided settings can also be changed in a copied snapshot.

**Each configuration overwrites the same artifact folder:** `outputs/brio_duplo/track/`. Save outputs elsewhere before switching configurations if they must be retained. The generic catalog name and metadata do not identify the loaded preset; keep its TOML snapshot with exported artifacts. Outputs are `track.stl`, `track.3mf`, optional `track.step`, `preview.png`, `preview.html` and `report.json`. Mesh-only builds remove a previous STEP artifact.

## Wagon, wheels and hardware

Sources are `wagon/model.py`, `wheel/model.py`, `assembly/model.py` and shared `dimensions.py`. The chassis has a 63.8 × 31.8 mm seating deck carrying eight solid studs on 16 mm pitch; modeled OD is 9.3 mm (nominal 9.4 minus 0.1 diametral allowance), height 4.5 mm including a 0.3 mm 45° lead-in. It targets ordinary DUPLO blocks, not LEGO System hollow-stud compatibility. Print one chassis and four wheels; each wheel has a 16 mm tread diameter, 4 mm tread width, 1 mm inward hub and 3.4 mm bore. Physical rolling and clutch remain unverified.

Hardware bill of materials:

- Two smooth 3 mm diameter × 42 mm shafts.
- Four retaining shaft collars: nominal 3 mm bore, outside diameter **at most 8 mm**, width 5 mm. The inspection envelope uses a 3.1 mm bore; choose hardware compatible with the actual 3 mm shafts.
- One printed chassis and four printed wheels, plus the desired printed track pieces.

Allow nominal 0.25 mm endplay between each wheel and its adjacent collar. Secure collars to the shafts; **do not torque-clamp wheels** between collars and the chassis. Wheels should turn freely on their clearance bores. Smooth shafts, real collar screw protrusions and retention must be checked physically; inspection envelopes are not hardware manufacturing models.

For each axle, slide a wheel on each side of the chassis with hubs inward, insert
the smooth shaft through both wheels and the bearing bore, then secure the
outside collars with the stated endplay. Tread centres are Y=±13 mm and axles
X=±20 mm (40 mm wheelbase). The default assembly gives 1 mm tread side gap,
1 mm hub-to-keel gap, 1 mm wheel-to-deck gap, and 2 mm chassis-to-track gap.
Deck-side overhangs and horizontal bearing bores need slicer/support evaluation;
print wheels flat, tread face down and hub up. The deck has no raised rim that
would obstruct descending DUPLO brick walls. No magnetic/train couplers are added.

```sh
uv run python scripts/build.py models/brio_duplo/wagon --step
uv run python scripts/build.py models/brio_duplo/wheel --step
uv run python scripts/build.py models/brio_duplo/assembly --expected-solids 12 --step
```

Corresponding artifacts are under `outputs/brio_duplo/wagon/`, `outputs/brio_duplo/wheel/` and `outputs/brio_duplo/assembly/`. The assembly always uses the default straight, independent of `BRIO_TRACK_CONFIG`. It is a fit-inspection scene, not a single printable part; export and print chassis, wheels and track separately. Its shaft/collar shapes are hardware envelopes, not supplied or printable hardware.

## Printing limits

Double-sided grooves are the default for wooden-track-style reversibility, but underside channels may require bridging or support. Single-sided flat straight track is the simpler bed-contact option. Curves and grades may require different orientation, support and build-plate capacity; nominal length is not the full connector-inclusive envelope. Groove floors, peg necks, socket throats and axle bores depend on printer accuracy, material and orientation. Trial-fit small pieces before committing to a layout. Check underside support removal, socket clearance, wheel freedom, stud clutch and collar retention physically. No material, slicer settings, load rating, child-safe retention or successful print is established by these design dimensions.

Printing-strategy work is explicitly deferred in
[#26](https://github.com/ShakataGaNai/b123d/issues/26); it must not change the
double-sided geometry default merely to simplify printing.

## Exercised verification and artifacts

All four catalog models passed native and saved/reimported STEP checks, valid
solid-count checks, watertight STL validation, and millimetre 3MF round trips.
The default track output is the 54 mm double-sided female/male straight:
71.75 × 40 × 12 mm including its peg. Chassis: 63.8 × 31.8 × 20.5 mm.
Wheel: 16 × 16 × 5 mm. Inspection assembly: 12 solids.

Saved exports, PNG/HTML previews, and exact configuration reports for **12**
exercised cases are in `outputs/brio_duplo/variants/`: the six straight
connector/face combinations; R202 left/right 45°; R110 left 45°; +18/−18 mm
over a 216 mm straight; and R202 left 45° rising 18 mm. Both endpoint mating
directions passed with complementary native CAD coupons, also against each
saved/reimported STEP target. The flipped double-sided default passed, and
the wagon cleared two joined default tracks at five sampled positions.
`variants/report.json` records the matrix; each variant has its own report.

All variant PNG iso/top/bottom/front views and component previews were inspected.
Straight/assembly HTML views were exercised interactively; graded-curve HTML
screenshots timed out and remain unverified interactively
([#25](https://github.com/ShakataGaNai/b123d/issues/25)).
This does not supersede the inspected PNG evidence or the passed CAD checks.
No print, genuine-brick/track trial, strength test, loaded stability test,
or wagon running on curves/grades was performed.
