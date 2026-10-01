# MultiBuild / MultiBoard attachment interfaces

> **Scope and status — 2026-10-01.** This is an interface handoff for future
> build123d adapters, not a reproduction of MultiBuild's catalog. It records
> only interfaces documented by MultiBuild or by MultiBuild's official Thangs
> account. It is **not ready to model an exact proprietary mating profile**:
> the public prose establishes compatibility and a few nominal system
> dimensions. Official remix CAD is a source route for exact snap latches,
> push-fit bores, thread flanks and rail/Fix-Point sections; this research did
> not acquire those profiles or establish an exhaustive list of other sources.
> Do not substitute an ISO/metric thread or a smooth cylindrical peg for any of
> those named interfaces.

## Identity, vocabulary, and evidence policy

- **Publisher / system:** MultiBuild; `MultiBoard` tiles and related `MultiBin`
  components. The current official documentation calls the former **Multipoint**
  system **Fix-Points**, and calls Multipoint Rails **Rails** ([S1]). This record
  uses `Multipoint/Fix-Point` where the source's generation is important.
- **Publication/revision:** current unversioned documentation and live official
  model listings, accessed **2026-10-01**. Publication date and a revision ID
  are **unknown** unless stated in the listing metadata; live pages can change.
- **Evidence labels:** **authoritative** means text or a model listing published
  by MultiBuild; **derived** is a stated relationship calculated from such text;
  **assumed** is deliberately not used for mating dimensions. A community
  comment is not geometry authority.
- **Geometry rule:** a public screenshot, name, and grid label are not a
  dimensioned drawing. The official listings identify STEP/STL remix resources,
  but their restricted-license downloads were not acquired or redistributed for
  this research ([S5], [S8]). Exact geometry therefore remains an
  authorized-upstream-file requirement, not an inferred profile.

## Source register

| ID | Publisher and title | Source URL | Revision / publication date | Accessed | Applies to | License / evidence |
|---|---|---|---|---|---|---|
| S1 | MultiBuild, *Core Parts Documentation* | <https://docs.multibuild.io/beginner-section/core-parts-documentation> | Current, unversioned; publication date unknown | 2026-10-01 | Current terminology and compatibility map | Copyright footer: © 2026 MultiBuild; no asset licence on page. |
| S2 | MultiBuild, *10x10 MU – Center Grid Interfitted – MultiBoard Octagon Plate* (model 977706) | <https://thangs.com/designer/MultiBuild/3d-model/10x10%20MU%20-%20Center%20Grid%20Interfitted%20-%20MultiBoard%20Octagon%20Plate-977706> | Live listing says “3 years ago”; exact date/revision unknown | 2026-10-01 | Tile holes, pitch, symmetry, design tolerance | Listing says download is restricted by licensing terms; see S11. |
| S3 | MultiBuild, *Multiboard Snap* (model 1311031) | <https://thangs.com/designer/MultiBuild/3d-model/Multiboard%20Snap-1311031> | Live listing says “1 year ago”; exact date/revision unknown | 2026-10-01 | Current standard/regular snap description | Restricted listing; see S11. |
| S4 | MultiBuild, *Raised Multiboard Snap* (model 974295) | <https://thangs.com/designer/MultiBuild/3d-model/Raised%20Multiboard%20Snap-974295> | Live listing says “3 years ago”; exact date/revision unknown | 2026-10-01 | Push-fit snap description | Restricted listing; see S11. |
| S5 | MultiBuild, *Snaps – STL Multiboard Remixing Files* (model 994667) | <https://thangs.com/designer/MultiBuild/3d-model/Snaps%20-%20STL%20Multiboard%20Remixing%20Files-994667> | Live listing says “3 years ago”; exact date/revision unknown | 2026-10-01 | Official snap remix source category | Restricted listing; see S11. |
| S6 | MultiBuild, *20 mm Mid Thread, Plain Head, Bolt* (model 973941) | <https://thangs.com/designer/MultiBuild/3d-model/20%20mm%20Mid%20Thread%2C%20Plain%20Head%2C%20Bolt-973941> | Live listing says “3 years ago”; exact date/revision unknown | 2026-10-01 | Mid-thread use and stated thread length | Restricted listing; see S11. |
| S7 | MultiBuild, *Locking T-Bolt* (model 1310062) | <https://thangs.com/designer/MultiBuild/3d-model/Locking%20T-Bolt-1310062> | Live listing says “1 year ago”; exact date/revision unknown | 2026-10-01 | Bolt-lock installation tool requirement | Restricted listing; see S11. |
| S8 | MultiBuild, *Snaps – STEP Multiboard Remixing Files* (model 994682) | <https://thangs.com/designer/MultiBuild/3d-model/Snaps%20-%20STEP%20Multiboard%20Remixing%20Files-994682> | Live listing says “3 years ago”; exact date/revision unknown | 2026-10-01 | Official editable snap geometry source category | Restricted listing; see S11. |
| S9 | MultiBuild, *Rails – STEP Remixing Files* (model 1145206) | <https://thangs.com/designer/MultiBuild/3d-model/Rails%20-%20STEP%20Remixing%20Files-1145206> | Live listing says “2 years ago”; exact date/revision unknown | 2026-10-01 | Positive/negative rail geometry source category | Restricted listing; see S11. |
| S10 | MultiBuild Parts Library, MultiBoard categories | <https://multibuild.io/parts/multiboard> | Current, unversioned; publication date unknown | 2026-10-01 | Catalog category names: Snaps, Hooks & Pegs, Threads, Nuts & Washers, Fix Points, Rails | No asset licence on landing page. |
| S11 | MultiBuild, *License* | <https://multibuild.io/license> | Current, unversioned; publication date unknown | 2026-10-01 | Rights and redistribution decision | Expressly prohibits sharing/redistributing copies or mass-link repositories of original Designs; remixes have conditions. |
| S12 | MultiBuild, *Drop-In Nut – Weight Bearing Snap – M4* (model 1030689) | <https://thangs.com/designer/MultiBuild/3d-model/Drop-In%20Nut%20-%20Weight%20Bearing%20Snap%20-%20M4-1030689> | Live listing says “3 years ago”; exact date/revision unknown | 2026-10-01 | Captive M4-nut / bolt-head snap alternative | Restricted listing; see S11. |
| S13 | MultiBuild, *4 mm, Big Thread Hole, Nut* (model 974310) | <https://thangs.com/designer/MultiBuild/3d-model/4%20mm%2C%20Big%20Thread%20Hole%2C%20Nut-974310> | Live listing says “3 years ago”; exact date/revision unknown | 2026-10-01 | Big-thread nut function and stated length | Restricted listing; see S11. |
| S14 | MultiBuild, *13 mm Large Thread Shanked – Mid Hole Flat Head – Bolt (Supported)* (model 1477153) | <https://thangs.com/designer/MultiBuild/3d-model/13%20mm%20Large%20Thread%20Shanked%20-%20Mid%20Hole%20Flat%20Head%20-%20Bolt%20%28Supported%29-1477153> | Live listing says “10 months ago”; exact date/revision unknown | 2026-10-01 | Direct large-thread bolt, shank, antirotation claim, mid-hole function | Restricted listing; see S11. |

### Asset and provenance decision

No upstream CAD, STL, thumbnail, or document has been committed. S11 prohibits
redistribution of original designs, and public availability is not permission to
commit them. Consequently there is no source-byte checksum. A future authorized
operator who obtains an upstream file must retain the original byte hash,
listing URL, exact file name, observed download date, and licence state outside
this repository unless MultiBuild grants repository redistribution permission.
Downloaded models are untrusted input and must never be executed; inspect only
as data/geometry.

## Dimensions, frames, and profile boundary

The following are the only numerical facts suitable for this attachment record.
They are system or component values, **not** a complete board coordinate model.
`board plane` below means the tile face receiving the attachment; the official
sources do not publish an assembly datum/origin or full X/Y coordinates here.
The board geometry record is the source of truth for tile envelopes and complete
hole placement.

| Feature / symbol | Value and convention | Evidence class and source | Modeling consequence |
|---|---:|---|---|
| Multi Unit (MU) | **25 mm** nominal sizing basis | Authoritative, S1 | MU is a naming/module convention, not by itself a snap, thread, or peg profile. |
| Same-type large Multihole pitch | **25 mm center-to-center** | Authoritative, S2 | May locate a pattern of large-hole anchors only after the intended tile variant is identified. It does not establish small-to-large phase. |
| Same-type small/Pegboard-hole pitch | **25 mm center-to-center** | Authoritative, S2 | May locate a pattern of small-hole anchors only after the intended tile variant is identified. It does not establish the actual Peg Click pair spacing/orientation. |
| Offset Snap Mount (DS Part A) standoff | **6.25 mm** from mounting surface | Authoritative, S1 | This is rear clearance created by that named mounting component, not a universal tile-back clearance. |
| Lite Multipoint/Fix-Point thickness delta | **1 mm thinner** than a regular Multipoint | Authoritative, S1 | Choose the exact positive/negative family; do not make a regular profile thinner by guesswork. |
| Listed mid-thread length | **20 mm**, named by S6 as *thread length* | Authoritative listing claim, S6 | It is a length designation for that particular plain-head bolt, not a thread standard or a required engagement depth. The delivered file must be verified before using it. |
| Published print-design tolerance | **0.25 mm** | Authoritative claim on S2–S4, S6–S7, S9 | A design/print recommendation for the listed parts, **not** a radial or diametral clearance to copy into a new adapter and not a system load tolerance. |
| Big-thread nut length (specific S13 part) | **4 mm** length | Authoritative listing claim, S13 | Applies only to S13’s named nut; it does not specify the big-thread profile or required engagement. |
| Shanked large-thread bolt thread length (specific S14 part) | **13 mm** thread length | Authoritative listing claim, S14 | Intended by S14 to join two tiles without rear protrusion; do not generalize to another tile thickness or bolt revision. |
| Shanked large-thread bolt smooth shank (specific S14 part) | **6.5 mm** shank | Authoritative listing claim, S14 | S14 says this forms a press connection between two tiles without unintended rotation; it is not a general antirotation specification. |
| Hardware nut family in one snap variant | **M4** nut / M4 bolt head | Authoritative compatibility claim, S12 | The external fastener is M4; this does not make any named MultiBuild small/mid/large thread an M4 thread. |

### Explicitly unknown mating dimensions

No cited official prose supplies a major/minor diameter, pitch, flank angle,
lead, thread handedness, tooth/latch dimensions, insertion depth, retention
force, push-fit interference, socket diameter, snap undercut, rail cross
section, Fix-Point cross section, center-to-center location of a Peg Click's
two anchors, or load rating. Names such as `small`, `mid`, `large`, and `20 mm`
are **not ISO designations**. Do not derive them from photos, screenshots, MU,
or a claimed metric-looking name.

For exact geometry, obtain the *current authorized official* file which matches
the selected family and use it as a provenance-controlled reference:

- **Snap positive / direct integration:** S8 (*Snaps – STEP Multiboard Remixing
  Files*), checked against the current S3/S4 production listing.
- **Snap socket / accessory negative:** use the negative/cut-out geometry from
  the same matching official snap/insert resource. S8's old listing does not
  prove it contains every current flush, raised, directional, or locking-snap
  revision; confirm file names and revision before CAD work.
- **Rail / Multipoint-Fix-Point:** S9 explicitly identifies `Lite Rail -
  Negative.step`, `Lite Rail - Positive.step`, `Rail - Positive.step`, and
  `Rail Slot - Negative.step`. Use *Positive* to add the named male feature and
  *Negative* to cut its complementary socket; do not offset a mesh or reverse a
  guessed profile.
- **Small/mid/large threaded interfaces and locking hardware:** obtain the
  currently matching official thread/bolt/nut source from the S10 **Threads**
  and **Nuts & Washers** categories. This study found no public dimensioned
  thread drawing. Record the exact file/revision and test against the target
  printed board before releasing an adapter.

## Practical interface matrix

“Rear clearance” means clearance behind a wall-mounted tile or in the direction
needed by a named installation motion. “Tool” records only tools named by the
publisher; absence means unknown, not tool-free.

| Attachment route | What mates to what | Installation/removal and clearance | Retention / removability / antirotation evidence | Exact-geometry handoff |
|---|---|---|---|---|
| **Regular direct snap** | A MultiBoard **Snap** enters a tile's **large Multihole**; its mid-hole can receive a bolt-locked insert or a thread (S1, S3). | Regular is documented as completely symmetrical and clicks into place (S1). The exact press/release motion and rear clearance are unknown. | It is detachable by its snap function, but no published rotation restraint, pull-out force, moment capacity, or cycle life was found. Symmetry is not evidence of an antirotation key. | Require current S3/S8 matching snap positive and the target tile revision. Do not integrate a visually similar hex/octagon-like feature. |
| **Directional moderate/heavy snap** | Named snap variant enters a tile large Multihole; the accessory uses its mid-hole route (S1). | Moderate and heavy variants must be inserted **at an angle** (S1): keep an unquantified front insertion/removal sweep. Heavy works only with tiles offset from the wall (S1); quantify actual rear space from the selected mounting parts, not the accessory. | Official prose says both hold load in **one direction**; heavy is described as holding more than moderate, without a rating (S1). Direction must match the expected gravity/moment direction. | Require the exact directional-snap file/revision and orientation instruction. Do not turn “heavy” into a numerical rating. |
| **Double-sided (DS) snap** | **DS Part A** and **DS Part B** snap together from opposite sides of the tile (S1). | Part A is normally at the back and Part B at the front. An **Offset Snap Mount (DS Part A)** creates **6.25 mm** surface offset and has a wall screw hole (S1). Both sides must be accessible during installation unless the exact mount says otherwise. | Documented use includes removable surface-mounted tiles and two-sided/freestanding support (S1). Exact locking geometry and the screw size/head/washer envelope are unknown. | Require both exact A and B files plus selected wall-mount variant. Model/verify rear volume, screw drive access, and tile thickness against those parts. |
| **Raised / push-fit snap** | A **Raised Multiboard Snap** enters the tile; its published **push-fit hole** takes a push-fit accessory or a mid-thread bolt (S4). The current documentation calls equivalent snap center feature a Mid Hole and lists friction-fit inserts, locking inserts, and mid threads (S1). | Push-fit accessories are inserted/pulled at the front; exact insertion stroke, force, socket depth, and extraction clearance are unknown. A listed **20 mm** mid-thread plain-head bolt is intended for boards mounted away from a surface so it can screw deeper (S6). | Friction fit is explicitly pull-removable and intended for lightweight hooks/pegs (S1). No antirotation, retention, or load value is published. | Require matching current raised-snap and chosen insert/socket geometry. Treat `push-fit` as a proprietary fit family, not a nominal diameter. Physically coupon-test the actual material, print process, and orientation. |
| **Bolt-locked snap insert** | An insert goes into a snap Mid Hole; a named **Locking Bolt** locks it to the snap so the insert cannot be pulled out (S1). | The lock adds a separate operation and access envelope. The **Locking T-Bolt** listing says to screw it into Bolt-Lock Mounts using a **coin** (S7); preserve a coin-accessible approach path for that named part. Exact bolt direction, coin-slot size, and clearance are unknown. | S1 supports prevention of insert pull-out, not a load rating or rotation guarantee. Use the specified locking component rather than claiming a friction insert is equivalent. | Require exact insert plus matching current locking bolt/T-bolt geometry, and a section check proving tool/head clearance. |
| **Drop-in metal-nut snap alternative** | S12’s named **Weight Bearing Snap** accepts an **M4 nut at the back** so an accessory using a screw can attach; it can also accept an **M4 bolt head**. | The nut is installed at the back of the snap, therefore needs rear insertion access before the tile is inaccessible. S12 says its directional arrow points upward during tile insertion. Exact nut-pocket dimensions, screw length, and tool envelope are unknown. | S12 calls it weight bearing and says it takes more than regular snaps, but supplies no rating. The M4 designation applies to the captured purchased fastener, not the MultiBuild snap/multihole profile. | Require the exact S12 revision, actual M4 hardware specification, and physical coupon. Treat rear nut capture and directional orientation as mandatory assembly conditions. |
| **Friction-fit snap insert** | A friction-fit insert mates to a snap Mid Hole; common functional variations include hooks, pegs, shelves, and brackets (S1). | No locking bolt; insert can be pulled out (S1). Needs open front extraction path; exact path/clearance unknown. | Officially suited to lightweight hooks and pegs (S1). It is intentionally removable; do not choose it for an adapter that must resist accidental pull-out or significant applied moment without a successful physical test. | Require official matching friction-fit insert or its official negative. Do not reuse bolt-lock geometry with its lock omitted. |
| **Small thread / direct tile bolt** | **Small Thread** screws into a tile **Small Hole** (S1); S2 calls them threaded Pegboard Holes and says they accept Small Thread Bolts. | Requires rotational access to the bolt head and clearance for the chosen head/accessory. Thread profile, engagement depth, head envelope, hand/tool, and rear protrusion are unknown. | Threaded retention is stated; no torque, load, or antirotation rating is stated. A single threaded fastener cannot be assumed to index an adapter rotationally. | Obtain the exact current small-thread bolt/nut and complementary tile geometry. Avoid treating “small” as M-size or using a standard M-thread generator. |
| **Large thread / direct tile bolt** | **Large Thread** screws into a tile **Large Hole / Multihole** (S1); S2 calls it a Big Thread Bolt. A current S14 shanked bolt is a concrete chain: large thread → tile; its head has a Mid Hole for push-fit accessories or mid-thread rods. | Requires rotational access to the bolt head. S14’s specific **13 mm** thread length is intended to join two tiles without protruding through the rear, and its flat head is intended for nearby clearance; that does not establish a generic adapter rear envelope. | S14’s specific **6.5 mm shank** is claimed to form a press connection between two tiles without unintended rotation. This is an exact-part/two-tile claim, not an antirotation rating for a holder. | Obtain exact current large-thread bolt/nut and target tile revision. The 25 mm Multihole pitch is a placement fact, not a large-thread profile definition. |
| **Large-thread nut / threaded-rod alternative** | S13’s named **4 mm Big Thread Hole Nut** fits a Big Thread and is described for use with threaded rods to fasten objects together; the publisher also says it can fasten bolts. | Nut rotation requires accessible flats/body and a thread run long enough for the actual assembly. The stated **4 mm** is the length of that named nut only; rear protrusion, wrench/finger envelope, rod length, and thread engagement are unknown. | S13 says it can increase a bolt’s weight capacity, but gives no value or assembly configuration. Treat that as a qualitative component role, not a load claim. | Require S13/current exact nut and the matching official rod/bolt, then section-check the full stack. Do not model an ISO nut or infer the big-thread profile from the **4 mm** part length. |
| **Mid thread / snap or push-fit center** | **Mid Thread** screws into a snap **Mid Hole** (S1). S6 additionally says a mid thread fits push-fit holes in snaps and in bolts/rods with a push-fit hole. | Requires rotational installation. The S6 plain-head example expressly cannot receive accessories and names a **20 mm thread length**; it is a particular part, not a general socket depth rule. | A screw connection is documented; no moment or antirotation rating is documented. The public listing has a user report of an 18 mm download under the 20 mm listing, so the on-disk identity must be verified before use (S6; non-authoritative comment). | Require exact mid-thread, target snap, and target accessory hole/receiver. Verify file name and measured thread length on the authorized source file; never size an adapter solely from the listing title. |
| **Peg Click / pegboard hook** | **Peg Click** connects to **two Small Holes**, like a pegboard accessory; the official guide calls Peg Click Hook the easiest tile hook route (S1). S1 also permits non-3D-printed pegboard accessories in Small Holes. | It is a two-point placement; no official pair orientation, engagement motion, rear envelope, commercial pegboard standard, or removal path was published. | Two discrete holes provide two locations, but the publisher does not specify their torque/moment performance. Do not call all “pegboard accessories” compatible without validating their hook geometry on the actual tile. | For an integrated adapter, obtain the official Peg Click geometry/negative and target tile. For a purchased pegboard hook, measure the exact maker/model and physically fit-test rather than infer from the generic term. |
| **Multipoint / Fix-Point to accessory hole** | A regular **Multipoint/Fix-Point** slides onto an accessory's **Multipoint Hole**; lite mates with **Multipoint Rail (Negative)** (S1). | Officially a **slide-on** installation/removal (S1): retain an unobstructed, unquantified lead-in and removal travel along the rail/slot axis. | S1 calls it strong but provides no load/moment value; a slide-on joint needs a documented stop/retainer before it is treated as captive. Exact anti-translation/antirotation behavior is profile-specific and unknown from prose. | Use S9's corresponding positive/negative STEP resource. Require direction of slide, end-stop/retainer choice, and an interference/coupon check. |
| **Multipoint/Fix-Point to tile** | A Multipoint connects to a tile through **small, mid, or large threads**, or **bolt-locking** (S1). | Clearance is the union of the chosen thread/bolt operation and the slide-on accessory operation. It cannot be sized from Fix-Point naming alone. | Retention depends on the selected thread or locking route. The authoritative source does not establish an interchangeable, equally strong family. | Specify the entire chain: tile revision → named small/mid/large thread *or* locking insert/bolt → exact regular/lite Fix-Point → mating Multipoint Hole/Rail negative. |
| **Rail / MultiBin alternative** | MultiBin shell side-wall rails accept Multipoints (bin-to-tile), Rail Click Connectors (bin-to-bin), or Rail Pop-Ins (bin-to-bin/tile) (S1). Pop-Ins unfold and pop in, then do not slide on/off (S1). | Rail Click Connector slides onto shell rail and clicks (S1). Pop-In requires its unfolding/pop-in motion; dimensions and tool clearance are unknown. | Pop-In’s no-slide-on/off behavior is stated; numeric retention/torque capacity is not. | Use exact S9 regular/lite rail positive or negative only after distinguishing whether the adapter needs a male rail, cut slot, or an official Pop-In. `Multiconnect` was not found in current official documentation; do not silently map that name to a rail or Fix-Point. |

## Conservative attachment selection for future custom holders

This is a **selection heuristic**, not a load-rating table. It intentionally
uses no inferred kilogram/Newton limits. Assess object mass, center-of-mass
projection from the tile, accidental pull-off risk, required removal frequency,
tile mounting method, print material/orientation, and the exact authorized
interface revision as a single system.

For this workspace's requested holders, the design contract is **both preprinted
rails and octagon mounting**, using the author-confirmed AirTag precedent. The
table below supplies alternatives and load/access considerations; it does not
replace either requested route with a generic default. See the
[holder clarification](existing-holder-examples.md#user-confirmed-mounting-requirement)
and [adapter reference](README.md). Exact profile dimensions remain a separate
CAD/measurement requirement.

| Holder need | Conservative first choice | Do not assume / required check |
|---|---|---|
| Light object, small projection, intentional frequent removal | Official **friction-fit insert** in a matching snap, or a validated **Peg Click** hook where two small-hole support is appropriate. | S1 only calls friction fit suitable for light hooks/pegs. Coupon-test retention; leave the stated extraction path clear. |
| Light object needing a clean direct integrated connector | Current official **regular or raised snap** geometry, selected by required flush/raised stand-off and accessory route. | Confirm whether the accessory needs a friction receiver, locking insert, or mid-thread socket; neither snap name establishes socket dimensions. |
| Object with nontrivial projection, potential pull-off, or persistent mount | **Bolt-locked insert + snap** or a documented **threaded** route; use two independently separated official anchors when the adapter must resist a twisting moment. | Bolt-lock prevents pull-out of insert from snap, but does not publish a rating. The second anchor's exact pattern must come from the intended tile and upstream components; use 25 mm only where the actual same-type grid relationship is applicable. |
| Directional gravity load with known clearance behind tile | Exact **moderate/heavy directional snap** only if the expected force is aligned with its documented one-direction capability; heavy requires offset tile. | “Heavy” has no published numeric capacity. Preserve the angle-insertion sweep and rear stand-off; test the full mounted system. |
| Flat / low-profile removable accessory where slide-on service is desired | **Regular Fix-Point** plus exact Multipoint Hole, or **Lite Fix-Point** plus exact Rail negative, with an explicit end-stop/retainer plan. | The documented slide-on action means removal travel must stay free. Do not treat a rail as captive without its actual retention component. |
| Bin/rail ecosystem integration | Official **rail** or **Rail Pop-In** family selected for the shell/tile path. | Do not replace the rail with a generic T-slot; exact profile and naming/revision must be verified from S9/current library. |

### Anti-rotation and multi-anchor rules

1. A single snap, single thread, friction insert, or slide-on profile has no
   published general antirotation/moment specification. Never claim that one is
   self-indexing or sufficient for an eccentric holder merely because it fits.
   The narrow exception is S14's exact **6.5 mm** shanked bolt in a two-tile
   press connection; do not transfer that statement to another bolt, snap, or
   holder configuration.
2. For an adapter expected to resist twisting, use two or more **independent
   official attachment locations** or an official keyed/rail interface whose
   exact mating geometry has been obtained. The two locations must be separated
   in the plane of the board. The only published placement pitch in this record
   is **25 mm center-to-center for same-kind large holes and same-kind small
   holes** (S2); it is not evidence for a mixed-hole pattern or every tile
   variant.
3. Keep the attachment chain's front-side installation, tool swing, and any
   rear standoff clear. Directional snaps specifically require angle insertion;
   heavy snaps require an offset tile; DS assembly accesses both sides (S1).
4. Validate a physical coupon followed by the complete holder under its intended
   use. Record print material, orientation, layer height, wall count, fixture,
   tile mounting method, applied direction, observed permanent deformation, and
   retention—not merely whether the part initially clicks together.

## Exact future-adapter intake contract

Before modeling a custom holder, the requester/modeler must supply or acquire:

1. **Tile identity:** exact tile style/revision, face orientation, installed
   wall/backing method, and every attachment location the holder will occupy.
   Do not select locations from MU alone.
2. **Complete upstream component chain:** the exact current MultiBuild model
   listing/file for each tile-side part (snap variation / thread / locking
   bolt / DS A+B / Fix-Point), the accessory-side positive or negative file,
   and every separate nut, insert, retainer, or tool-operated bolt. A label
   such as “snap mount” is insufficient.
3. **Controlled geometry provenance:** source URL, listing/model ID, file name,
   file revision/date if present, access date, local byte SHA-256, licence state,
   and whether it is positive or negative geometry. Do not commit original
   upstream bytes under the observed licence.
4. **Motion and access envelope:** insertion direction and sweep, extraction
   direction, front tool access (including coin access where S7 is selected),
   rear clearance, wall/neighbor interference, and whether the holder must be
   removed while loaded. Unknown dimensions remain blockers, not default zero.
5. **Object loading envelope:** object mass, center of mass, maximum projection,
   handling forces, number of anchors, and desired intentional-removal behavior.
   These are design inputs, not published MultiBuild ratings.
6. **Fit validation:** a print coupon for every proprietary mating feature,
   checked against the actual printed tile and upstream components; then an
   assembled, orientation-specific functional test. Retain outcome and observed
   fit separately from MultiBuild's stated **0.25 mm** design tolerance.

## Geometry-gap and revision risks

| ID | Missing/conflicting fact | Consequence | Resolution / modeling status |
|---|---|---|---|
| G1 | Exact profiles and tolerances of large/small/Mid threads, snap latches, push-fit receiver, locking bolt, Peg Click, Fix-Point, and rail are not published as text/drawings in S1–S14. | Any hand-modeled approximation can jam, wobble, fail to lock, or damage a printed counterpart. | **Blocks exact adapter mating.** Obtain and inspect the current authorized matching official file; physical coupon-test. [Issue #10](https://github.com/ShakataGaNai/b123d/issues/10) records this unresolved evidence/asset-license gap. |
| G2 | S8 is an older Remix STEP listing and a public comment asks for newer chamfered-back snap geometry. The comment is non-authoritative, but demonstrates version drift. | Old remix geometry may not match current flush/raised/directional production part. | **Blocks version-sensitive use.** Match file names/revision and test against the actual source part. |
| G3 | S6 labels the listing 20 mm and text says 20 mm thread length, but a user comment says the delivered file was 18 mm. | Selecting rear clearance or engagement from title alone can be wrong. | **Blocks use of that dimension until inspected.** Verify authorized byte/file identity; record measured/authoritative result. |
| G4 | No published numerical load, torque, pull-out, fatigue, or safety rating; “moderate/heavy/strong” are qualitative only. | A catalog adjective could be misused as a structural design specification. | **Blocks rated-load claims.** Treat as un-rated; test the entire printed/mounted assembly for the actual use. |
| G5 | `Multiconnect` does not appear in current official core documentation or the current Parts Library categories examined. | It may be a community/older name, or refer to an unrelated component. | **Blocks mapping by name.** Require source listing/photo/file before choosing Multipoint/Fix-Point or Rail. |
| G6 | Generic “pegboard accessory” compatibility is stated, but no commercial standard, brand, hook profile, or tolerance is identified. | A purchased hook can conflict with the tile despite the generic term. | **Blocks no-measurement purchased-hook design.** Identify and measure the exact hook or use official Peg Click geometry. |

## Verification plan for a future implementation

| Requirement | Check | Acceptance basis | Status |
|---|---|---|---|
| Correct upstream mating profile | Compare model's imported/constructed positive or negative feature to the identified authorized source, then print a coupon. | Exact file/revision provenance plus mating with the actual counterpart; no unsupported nominal tolerance. | Not run — no adapter scope or authorized files supplied. |
| Installation and service clearance | Section and motion-envelope review, then physical install/remove on installed tile. | No collision along named snap angle, slide-on, front tool, or rear clearance path. | Not run. |
| Anti-rotation / multi-anchor behavior | Apply intended eccentric object configuration to complete physical assembly. | No undesired rotation, pull-out, unlocking, interference, or permanent deformation under documented intended use; no generic threshold claimed. | Not run. |
| Directional / offset snap validity | Install exact directional snap in expected orientation and selected tile mount. | Correct one-direction orientation; for heavy snap, verified actual tile offset and angle-insertion clearance. | Not run. |
| Licence/provenance | Review source file record before model release. | Current source URL/model ID, file identity/hash, access date, licence state, and no unauthorized original CAD committed. | Not run. |

## Change record

| Date | Evidence / decision | Effect |
|---|---|---|
| 2026-10-01 | Initial official-source interface handoff; no upstream assets saved because S11 restricts original-design redistribution. | Future adapters must select an exact authorized component chain and coupon-test proprietary interfaces before claiming fit. |
