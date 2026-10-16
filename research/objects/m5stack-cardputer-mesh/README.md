# M5Stack Cardputer / Cardputer Mesh Kit

Research date: 2026-10-16. Work item: [#30](https://github.com/ShakataGaNai/b123d/issues/30).
Target: K152 Cardputer Mesh Kit, comprising green-back Cardputer-Adv and Cap LoRa-1262 (U214). Standard Cardputer is the requested alternate fit. Purchased specimen and production revisions are unknown. User supplied approximate dimensions; measurement method is unspecified.

## Primary evidence

All sources are M5Stack, accessed 2026-10-16; publication date and manufacturing tolerances are unspecified.

| Source | Relevant evidence |
| --- | --- |
| [K152 product page](https://shop.m5stack.com/products/cardputer-mesh-kit-for-meshtastic-esp32-s3) | Kit identity; Adv 84 × 54 × 19.6 mm, cap 84 × 24 × 15.2 mm |
| [Standard Cardputer documentation](https://docs.m5stack.com/en/core/Cardputer) and [dimension drawing](https://static-cdn.m5stack.com/resource/docs/products/core/Cardputer/img-401ac270-d997-4164-ae79-d28be7a3dfaf.png) | Overall 84 × 54 × 19.7 mm; lower side view explicitly dimensions 16 mm shell plus 1 mm key projection; R3 lower corners |
| [Cardputer-Adv documentation](https://docs.m5stack.com/en/core/Cardputer-Adv) and [K132-Adv drawing](https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1178/K132-Adv-cardputer-ADV_page_01.png) | 84 × 54 × 19.6 mm overall; lower shell 16 mm; key projection visible but not separately dimensioned |
| [Cap LoRa-1262 documentation](https://docs.m5stack.com/en/cap/Cap_LoRa-1262) and [U214 drawing](https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1208/U214-00-cap1262-model-size_page_01.png) | 84 × 24 mm cap plan, drawing height 15.287 mm versus product specification 15.2; screw holes Ø2 on 56 mm centers, 14 mm from ends, unused by holder |
| [Cap assembly photograph](https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1208/U214_Cap_LoRa-1262_screw_note_01.png) | Cap sits at top/rear; two M2 × 4 mm screws. Photo establishes orientation, not scale. |

Original image redistribution terms are unknown. Images were inspected in ignored `outputs/scratch/`, not committed. SHA-256 of original downloaded bytes:

- `cap-size.png`: `06f743759b7a4c7e7e114a311ed91b24f301528d99732bb0e8f1ca733d5f9d67`
- `cap-assembly.png`: `1bc7047a96b87431a0fe61aa0f2e5457a801f88e8469953a10d8cf6e5b32ed6d`
- `adv-size.png`: `0538542459779f6171cac09068e44c663c2a734976024731f275bd5b06b52d1d`

## Current measurement-to-design handoff

Units mm; X spans the 84 mm width, +Y points toward Multiboard, +Z is up. Keyboard faces −Y; device bottom rests on the floor.

User correction on 2026-10-16 supplies approximately **15 mm body thickness excluding buttons** and **16 mm rear cap protrusion**. The user subsequently requested a **17 mm total slot thickness including clearance** to accommodate the buttons; button projection and resulting per-face thickness clearance are not independently measured. Measurement method, exact contact locations and hardware revision are unspecified. The published drawings remain nominal evidence for other variants; this revised pocket is not a promise of universal standard/Adv fit.

- Slot: **84.8 × 17 mm**, with 0.4 mm per-side width allowance around 84 mm. The 17 mm thickness is the user-selected finished opening, already including button space and clearance; no extra thickness allowance is added. Capture depth 10, floor 3.5, walls 2.5, mouth rounding 0.5. Allowances are design choices, not calibrated print tolerances.
- User-selected rear spacing: **20 mm** from inner rear slot boundary to arm end/peg-root shoulder, excluding 6.5 mm peg engagement. Upright nominal clearance behind the reported 16 mm cap overhang is **4 mm**. This replaces the former full-cap-depth plus rocking budget; clearance during rocking is not guaranteed.
- Antenna: user specifies **10 mm diameter**. Two coaxial semicircular top grooves of radius 5, depth 5, extend across the arm widths along X. Centers are halfway along each exposed arm from the pocket exterior to the peg-root shoulder. Remaining arm web below the grooves is 8.5 mm. No additional antenna fit compensation; these are open rests, not clips.
- Rear arm vertical corners and the two inner arm-to-pocket vertical corners receive 2 mm radii. Peg profile stays unchanged.
- Backplane datum assumes peg-root shoulders sit at or forward of the tile face. Receiver recession reduces the nominal 4 mm clearance.
- The rim overlaps the lowest keyboard area. Lift out for unrestricted controls/ports. Antenna-rest geometry does not verify cable routing or clearance against the installed device; actual antenna length/connector geometry is unspecified.

Dependent model: `models/cardputer_mesh_multiboard_holder/`. Check cavity, material under the grooves, circular saddle profiles, peg sections and upright cap clearance. Fit, strength, snap retention and slicer behavior remain physically untested; tracked under [#30](https://github.com/ShakataGaNai/b123d/issues/30).
