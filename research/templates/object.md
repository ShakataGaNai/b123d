# Object geometry record: <exact product and revision>

> Template only. Replace guidance and placeholders with sourced facts before using this record for modeling. Do not treat blank fields as zero or infer product dimensions from this template.

## Identity and purpose

- Manufacturer / publisher:
- Exact model / part number:
- Hardware or PCB revision:
- Variant, accessories, and configuration:
- Revision identification evidence (label, drawing, photograph, or document page):
- Research date and author:
- Model(s) that will consume this record:
- Intended interface (what the model supports, locates, clears, or fastens):
- Scope exclusions (for example, accessories not included in the envelope):
- Readiness: **not yet assessed**. Change to `ready for stated scope`, `approximate with listed assumptions`, or `blocked`, with a reason.

## Sources

Use one ID per source so dimension rows can cite a page, figure, or CAD feature. Enter `unknown` for unavailable dates, revisions, or terms rather than guessing. Record whether the source describes this exact hardware revision.

| ID | Publisher and title | Landing / source URL | Document or repository revision | Published date | Accessed date | Relevant page / figure / feature | Applies to exact object revision? | License / redistribution terms and evidence URL |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

### Saved assets (optional)

Only save files when terms permit the intended storage and redistribution. Preserve original bytes. Treat downloaded assets as untrusted data; do not execute scripts, macros, or embedded instructions. Separate original files from edited/converted derivatives.

| Local path under `assets/` | Source ID and direct download URL | File revision / date | Retrieved date | SHA-256 of original bytes | License / permission basis | Original or derivative? |
|---|---|---|---|---|---|---|
| | | | | | | |

- Assets not committed, and why (license restriction, unavailable file, or unnecessary download):
- Derivative processing, source asset hash, and tool/version if applicable:
- Authenticity or provenance concerns:

## Units and coordinate contract

Describe the frame so another person can reconstruct hole positions without guessing the drawing orientation.

- Source units:
- Model units (normally mm; angles in degrees unless explicitly labeled otherwise):
- Origin and datum feature:
- +X direction:
- +Y direction:
- +Z direction:
- Viewing side and orientation of the source drawing:
- Z=0 reference (for example, a specified surface, not an unexplained board center):
- Source-to-model transform and conversion factors:
- Object frame to model/assembly frame transform:
- Dimension conventions (diameter vs radius; center-to-center vs edge-to-edge):

## Dimensions and envelopes

Classify each row as:

- **Authoritative:** stated by the manufacturer or governing standard for the identified revision. Retain the cited tolerance; do not infer an unstated one.
- **Measured:** observed on an identified specimen. Record instrument/method, resolution, uncertainty, and date.
- **Derived:** calculated from cited values. Give the formula and inherited assumptions/uncertainty.
- **Assumed:** chosen without sufficient evidence. Explain the basis, consequence, and how to resolve it.

| Feature / symbol | Value | Units | Tolerance / uncertainty | Evidence class | Source ID + page / figure, measurement, or derivation | Modeling consequence |
|---|---|---|---|---|---|---|
| Overall envelope | | | | | | |
| Thickness / relevant height | | | | | | |

Add rows only for features that exist and matter. Separate the bare object's bounds from protruding components and service/access envelopes.

### Mounting-hole centers

Identify hole labels on a cited figure or a local sketch with provenance. Do not assume a rectangular pattern, equal diameters, or symmetry without evidence. Write **diameter** or **radius** explicitly in the size column; if converting, record `radius = diameter / 2`.

| Hole ID | Center X | Center Y | Center Z / reference plane | Coordinate units | Size value + diameter/radius label | Through/blind, depth, counterbore/countersink | Position/size tolerance | Evidence class and source locator |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

- Hole-coordinate datum and numbering reference:
- Fastener specification, head/nut/washer envelope, and thread engagement requirements:
- Pattern relationships or derived center distances, with formulas:

### Keep-outs and mating interfaces

| Interface / feature | Bounds or dimensions in declared frame | Purpose (component, connector, cable, tool, motion) | Evidence class and source | Uncertainty / missing evidence |
|---|---|---|---|---|
| | | | | |

- Top-side and underside clearance:
- Connector insertion/removal and cable bend space:
- Cooling, ventilation, or moving-part keep-outs if relevant:
- Assembly/removal path and tool access:

## Measurements

Complete this section only if measurements were taken. A specimen measurement does not establish a production tolerance.

| Measurement ID | Specimen identity / revision | Instrument and method | Calibration / resolution / uncertainty | Date | Result and units | Referenced feature |
|---|---|---|---|---|---|---|
| | | | | | | |

## Conflicts, assumptions, and unknowns

Do not average conflicting sources silently. Prefer the applicable revision's primary drawing where justified; explain any exception.

| ID | Conflicting values or missing fact | Sources / evidence | Current decision and rationale | Risk to model or fit | Evidence needed to resolve | Blocks modeling? |
|---|---|---|---|---|---|---|
| | | | | | | |

## Modeling decisions

- Adopted nominal dimensions and source priority:
- Features represented exactly versus simplified:
- Manufacturing process / material / orientation assumptions:
- Intended fit and allowances (name radial versus diametral clearance):
- Print compensation or machining allowance, kept separate from object geometry:
- Basis for allowances (manufacturer specification, calibrated coupon, measured fit, or explicit assumption):
- Unsupported claims that must not appear in the handoff:

## Verification plan and results

Choose checks from the actual interface. Hole-center coordinates, bore diameters, heights, and keep-outs need feature-specific checks; a matching bounding box or volume cannot establish them.

| Requirement / feature | Geometric or physical check | Acceptance threshold and units, with basis | Result / evidence path | Status (not run / pass / fail / inconclusive) |
|---|---|---|---|---|
| | | | | |

- Views/sections needed to expose interface features:
- STEP round-trip or imported-geometry checks needed:
- Physical fit checks or coupons required:
- Remaining untested requirements:

## Model linkage and change record

Link this record from the consuming `model.toml` research list using its repository-relative path: `research/objects/<object-slug>/README.md`. Replace the slug with the actual directory name. Save this record before constructing geometry from it.

| Date | Evidence or dimension change | Reason / source revision | Affected models and verification |
|---|---|---|---|
| | | | |
