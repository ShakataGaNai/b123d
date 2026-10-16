# Object geometry record: LEGO DUPLO ordinary-brick stud interface

## Identity and purpose

- Manufacturer: LEGO Group. Interface: ordinary rectangular DUPLO bricks, intended examples **2×2 and 2×4 DUPLO bricks**, attached to a custom **2×4-stud BRIO-compatible rolling-wagon deck**. These are DUPLO stud counts, not LEGO System stud counts.
- Exact purchased specimen, design/element number, mold revision, production date, color, and wear condition: **unknown; no physical specimen was measured here**. Sources describe a generic interface, not a certified current mold revision.
- Research date: 2026-10-03. Readiness: **approximate with listed assumptions**, sufficient for a supervised trial-fit prototype, not verified clutch or production compatibility.
- Scope excludes wagon wheel/rail geometry, couplers, underside attachment geometry on the custom deck, and DUPLO railway track gauge. DUPLO railway gauge is a separate wheel/rail interface and must not determine this wagon's BRIO wheel spacing.

## Sources

All URLs accessed **2026-10-03**. Official sources were searched first; no current manufacturer dimensioned stud drawing or production tolerance specification was found in that search. This is a search finding, not proof that none exists.

| ID | Publisher / original source | URL | Revision / date and relevant feature | Applicability and license |
|---|---|---|---|---|
| L1 | LEGO Group, *LEGO DUPLO* history | https://www.lego.com/en-us/history/articles/e-lego-duplo | Undated live article, “The LEGO DUPLO brick”; 2:1 system and hollow studs admitting standard LEGO underside tubes | Official qualitative history, not a manufacturing drawing or current mold identification. No redistribution permission established; cited only. |
| L2 | LEGO Group, *Building with LEGO and DUPLO bricks* | https://www.lego.com/en-us/service/help-topics/article/building-with-lego-and-duplo-bricks?age-gate=grown_up | Undated live support page; compatible LEGO 2×2/2×4 examples and hollow-stud requirement | Official compatibility guidance for genuine products, not certification of a printed deck. No redistribution permission established; cited only. |
| C1 | Christopher Finke, original authored `LEGO.scad` | https://github.com/cfinke/LEGO.scad/blob/d717ca8e29dbb62f271bf351b35179060eaa744e/LEGO.scad#L310-L339 ; raw inspected source https://raw.githubusercontent.com/cfinke/LEGO.scad/master/LEGO.scad | File's latest commit identified through https://api.github.com/repos/cfinke/LEGO.scad/commits?path=LEGO.scad&per_page=1 : `d717ca8e29dbb62f271bf351b35179060eaa744e`, 2026-07-18. Constants, envelope expressions, `stud()` implementation | Community CAD parameters, specimen/revision and measurement method unspecified. Source header provides MIT permission with copyright/permission retention and no warranty. Header acknowledges derivation from http://www.thingiverse.com/thing:5699; no claim that its constants originate in an official LEGO specification. No code/geometry copied or executed. |
| M1 | Ross, firsthand caliper measurement comment on Chris the Cynic's *Need help: accurate and reasonably precise measurements of Duplo bricks* | https://stealingcommas.blogspot.com/2018/07/need-help-accurate-and-reasonably.html?showComment=1530814792261#c8372301803184502260 | 2018-07-05 14:19 comment; stud OD, total/body heights, underside tube | Original commenter describes caliper access difficulty for tube OD. Specimen part/revision, instrument calibration/resolution and sample count unknown. No redistribution license established; values summarized, source assets not committed. |

No downloaded assets retained, CAD copied, or downloaded scripts executed. Search summaries are discovery leads, not dimensional evidence; values below are traced to the inspected original source/comment.

## Units and coordinate contract

All dimensions are mm. Origin is the center of the nominal deck grid on its top seating plane, **Z=0**; +X is wagon length (four studs), +Y width (two studs), +Z upward. Stud centers refer to center-to-center distances, and all listed diameters are **diameters**, not radii. Deck thickness is a wagon structural choice, not a DUPLO brick-body-height requirement.

## Dimensions and envelopes

A community-authored CAD constant is classified **assumed nominal**, not authoritative or measured merely because code contains a precise number. Manufacturer production tolerances are unknown for every dimensional row.

| Feature | Value | Tolerance / uncertainty | Evidence class and locator | Modeling consequence |
|---|---:|---|---|---|
| Square stud pitch | 16.0 | Production tolerance and measurement uncertainty unknown | Assumed nominal, C1 `stud_spacing = 8 * 2` | Preserve pitch; do not scale grid to tune clutch. |
| Stud external diameter | 9.40 | M1 uncertainty unspecified; calibration unknown | Measured report M1, independently matching assumed nominal C1 `stud_diameter` | Supported trial-fit starting OD, not guaranteed actual OD. |
| Stud height above seating plane | 4.50 | Actual profile/datum and production variation unknown | Assumed nominal C1 `stud_height` | Deck studs extend to Z=4.5 before any separate fit allowance. |
| Measured stud height comparison | 4.55 = 23.7 − 19.15 | Two readings' uncertainty unknown; no averaging with C1 | Derived from M1 reported measured overall/body heights | Supports approximately 4.5; does not establish ±0.05 tolerance. |
| Nominal 2×4 grid footprint | 64 × 32 | Grid nominal, not measured external brick bounds | Derived, 4p × 2p, C1 pitch | Grid edges X=±32, Y=±16; center setback 8. |
| 2×4 stud-center coordinates | X={−24,−8,8,24}; Y={−8,8}; Z=0 | Inherits assumed pitch | Derived, Cartesian product | Eight studs; 48 × 16 center-span. |
| 2×2 grid footprint / centers | 32 × 32; X,Y=±8 about its own center | As above | Derived from pitch | Can occupy either end's four studs or another grid-aligned 2×2 region. |
| Actual outer brick footprint approximation | 63.8 × 31.8 for 2×4; 31.8 × 31.8 for 2×2 | Not an official manufacturing tolerance | Derived community CAD: C1 `overall_length/width = stud_count * pitch − 2 * wall_play`, `wall_play=0.1` | Distinguish physical envelope approximation from 64 × 32 grid; deck need not copy the brick shell. |
| Hollow stud internal diameter | 6.5 | Unverified; C1 comment says wall 1.4, which with OD 9.4 would imply 6.6, not 6.5 | Assumed nominal C1 `hollow_stud_inner_diameter` | Optional blind recess for a hollow-stud trial; do not claim exact System compatibility. |
| Hollow stud recess depth / floor | Unknown | No applicable measurement found | Missing | Deck designer must explicitly choose and label recess depth; no need for through-hole into wagon. |
| External stud profile | Cylindrical body with rounded/chamfered entry is a prototype simplification | Mold draft, top radius, lettering, parting-line geometry unknown | C1 has configurable rounding (`stud_top_roundness=0.2`, not a measured radius); exact LEGO profile unavailable | Do not reproduce code's shape as verified geometry. |
| DUPLO underside tube OD | 13.5 measured report vs 13.1 CAD parameter | M1 expressly low confidence because caliper cannot grip well | M1 measured report; C1 assumed nominal `post_diameter` | Unresolved disagreement; not needed to build male deck studs, but warns against deriving clutch solely from simplified tube circles. |
| DUPLO underside tube interior | Irregular octagon from two squares, reported 10.7 and 11.25 | Shape orientation and uncertainty unspecified | M1 firsthand report | Not a verified round 9.4 bore; do not equate tube bore with a deck-stud hole. |

## Mating rationale and system distinctions

Ordinary DUPLO blocks press down over the **outside** of the deck studs. Their underside walls/splines and interstitial tubes establish locations and clutch; those tubes lie between stud positions, not concentrically over each deck stud. This is the mechanism represented in C1's wall-spline/post layout; it remains a community model rather than a production drawing. With a 16 mm square grid, the distance from a cell center to any corner stud is `16/sqrt(2)=11.314` mm; subtracting nominal stud radius 4.7 leaves 6.614 mm, giving a geometric near-tangent tube OD of 13.227 mm. This **derived idealization** explains why a roughly 13 mm interstitial tube can contact studs; it is not a tolerance/fit prescription, particularly given M1's irregular tube interior and OD uncertainty.

The hollow center of a genuine DUPLO stud serves another interface: LEGO's official history [L1] explains that **standard LEGO System underside tubes** fit into hollow DUPLO studs. It is not the primary clutch surface for an ordinary DUPLO block placed on this wagon. L2's 2×2/2×4 examples refer to **LEGO System** blocks in its compatibility explanation, not the DUPLO block examples in this record. C1 gives System pitch 8, OD 4.8 and height 1.8 versus DUPLO 16, 9.4 and 4.5; simply doubling a System stud would give 9.6 × 3.6, inconsistent with the inspected DUPLO evidence. The official “2:1” statement is a system-scale description, not a license to double every mold detail.

## Modeling decisions and unresolved fit

- Adopt 16 mm pitch, 9.4 mm external OD and 4.5 mm height as **trial-fit nominals**. A 2×4 male deck supplies all eight stud positions and leaves ordinary block bottoms unobstructed around them. Any deck rim must avoid the descending brick walls and insertion/removal path.
- Implemented initial print allowance is **−0.10 mm diametral**: modeled stud OD **9.30 mm**, radius reduced by **0.05 mm**. This is an assumed fit choice, not a LEGO tolerance or guaranteed clutch fit. `models/brio_duplo/dimensions.py` keeps nominal diameter and allowance separate for calibration.
- Implemented **0.3 mm equal-leg 45° top chamfer** is an insertion lead-in, not sourced LEGO profile. Studs have 4.2 mm cylindrical engagement below the 0.3 mm tapered top; total height is 4.5 mm.
- The wagon uses **solid studs** for ordinary DUPLO exterior mating. Hollow ID 6.5 mm remains an unverified community value; this model is not a LEGO System adapter. Neither solid nor hollow printed studs establish compatibility without physical testing.
- Unknowns: exact recipient mold revision, wall/spline dimensions, draft/rounding, recess depth, molding tolerances, aged/worn-brick variation, material elasticity, layer orientation, and required insertion/extraction force. No manufactured-fit or safe-child-use claim is supported.

## Verification plan and results

No physical measurements or trial prints performed by this research task. No downloaded model executed. Source inspection and calculation establish provenance only; they do not establish mating fit.

| Requirement | Check / acceptance basis | Result |
|---|---|---|
| Eight-stud grid | CAD centers at the listed Cartesian-product positions; 16 mm pitch independently in X/Y; stud volume and local OD/lead-in material probes | Passed on native and reimported STEP; `outputs/brio_duplo/wagon/report.json`. Physical clutch not tested. |
| Stud OD/height/profile | Inspect actual printed coupon and measure OD at several heights; compare against intended 9.30 print-target OD and 4.5 height, recording measurement uncertainty | Not run |
| 2×2 and 2×4 ordinary DUPLO mating | Identify genuine brick design/element and mold marks; compare insertion/removal with genuine reference bricks, full seating, no rocking, no cracking or permanent deformation; record printer/material and observed force | Not run; no numeric force specification available |
| Printed fit allowance | Coupon sweep around the starting −0.10 mm diametral choice; keep pitch fixed; select with actual recipient bricks | Not run; proposed allowance uncalibrated |
| Rolling wagon/load clearance | CAD component intersections, groove alignment, wheel/deck clearance, and passage across two joined default straights at five sampled positions | Passed native/STEP assembly checks and static passage smoke; `outputs/brio_duplo/assembly/report.json`, `outputs/brio_duplo/variants/report.json`. Physical rolling, loaded stability and curve/grade running not tested. |

Printed prototypes are for supervised engineering trial fit, **not a child-safe toy**. Studs, wheels and axle hardware can detach; printed parts can crack or produce sharp fragments. Material/toxicity, choking hazards, strength, cleaning, heat, magnets/couplers and applicable toy-safety compliance are not assessed. Do not give an unvalidated prototype to a child or transfer LEGO product safety claims to it.

## Model linkage and change record

Consuming `models/brio_duplo/wagon/model.toml` and `assembly/model.toml` reference this record. Source is in `models/brio_duplo/`; printable components are exported separately. Chassis has a 63.8 × 31.8 mm deck, eight solid studs, and 3.4 mm clearance bearings for original-design 3 mm metal shafts; none of those shaft/retention choices are LEGO specifications.

| Date | Change | Affected verification |
|---|---|---|
| 2026-10-03 | Initial official qualitative evidence, original community CAD constants and firsthand caliper report; separated nominal grid, print allowances and unknown revisions | Future wagon deck geometry and physical trial-fit coupons; all fit tests not run |
| 2026-10-03 | Built the eight-stud wagon and separate wheels; native/STEP interface and mesh checks passed; recorded solid-stud simplification and retained all physical-fit/safety limitations | Wagon/assembly reports and PNG previews inspected; no physical prints or brick trials. |
