# Three-part PVC laser stand

Original trial-fit design for 3/4 inch Schedule 40 PVC and a user-measured
18 mm laser barrel. [Issue #46](https://github.com/ShakataGaNai/b123d/issues/46).
[Hardware evidence and uncertainties](../../research/objects/pvc-laser-stand/README.md).
All dimensions in mm. Each entrypoint exports one independent printable solid.

| Component | Interface and envelope |
| --- | --- |
| laser_mount | 25.4 pipe engagement; 24 long sleeve; 18.3 circular bore with tangent 45° roof relief; two vertical 3.4 diameter roof pilots spaced 12 apart; 56.05 total height |
| coupler | 12.7 engagement per side; 3 thick separator; 28.4 total height |
| stake | 25.4 pipe engagement; 3 thick stop; 120 ground blade, tapering to 1.2 blunt tip; 148.4 total height |

All pipe inserts are 4 mm thick cross webs clipped to a 20.90 diameter circle.
This gives curved contact ends without oversized square corners. The entry
reduces radius by 0.6 over the first 1 mm. Stops are full 26.67 diameter,
3 mm thick discs, with planar pipe-end seating faces. The stake's two ruled
blade tapers narrow from 20.9 to 14 across the first 90 mm, then to the tip.
The sleeve axis is Y, exactly perpendicular to the pipe's Z axis in CAD.
The laser bottom has 2.5 mm solid material above the stop plate.

Remove the original laser clamp. Slide the bare barrel through the sleeve;
its unknown usable length must accommodate the 24 mm sleeve. The 18.3 bore
has 0.3 diametral allowance. Its upper 90-degree arc opens into a small peaked
roof to avoid an unsupported circular crown. The lower 270 degrees remain
circular; this is not a fully circular hole. Screws enter vertically through the roof at X=0, Y=±6,
pressing the barrel into the lower circular seat. The peaked roof gives about
3.06 mm of material on the hole axis, along the vertical pilot perimeter. M4 × 8 set screws are a
starting choice: approximately 7.15 mm reaches from the roof peak to the top
of an 18 mm barrel resting on the bore floor. Actual screw tip and housing
hardness require a trial; tighten gently for one-time retention.
3.4 mm holes are experimental thread-forming pilots, not M4 clearance holes
or printed threads. Start screws square and avoid excessive torque.

Print each file in its exported orientation: short cross entry on the bed,
pipe axis vertical; stake points upward. Start with PETG, 0.4 nozzle, 0.2 layers,
5 walls and a brim, particularly for the tall stake. These are untested settings.
The circular stop requires roughly 8 mm quadrant bridges and a 2.9 mm radial
outer cantilever beyond the cross envelope. Try bridge cooling and inspect the
slicer; local support under the stop may be needed. The sleeve corners are trimmed to the same 26.67 mm circular envelope as
the stop, eliminating additional mount-to-plate overhangs. No support-free claim is made until sliced
and printed. Roof slopes are 45 degrees; screw pilots are vertical in the print orientation. Do not put support inside the laser seating bore if avoidable.

Check the coupler first as the cheapest fit sample. Nominal pipe ID is 20.9296,
so only about 0.03 diametral clearance is intended. Sand the four contact ends
symmetrically if tight; measure actual pipe ID before changing INSERT_D in
geometry.py. Do not force an excessively tight fit and split the pipe. Square
and deburr pipe ends before seating them flat. A loose pipe joint, pipe flex,
or laser optical alignment can spoil perpendicularity despite exact CAD axes.
Use the ground stake in soft soil, press gently; do not hammer the printed
layers. Soil holding strength and long-term PETG creep are unverified.

Build each with `uv run python scripts/build.py models/pvc_laser_stand/<component> --step`.
Artifacts go to `outputs/pvc_laser_stand/<component>/` (ignored).
Native and STEP checks cover single-solid validity, overall heights, cross
section envelope/material, laser-barrel clearance, pilot clearance and sleeve
floor material. Export reports also check STL watertightness and 3MF units.
Physical fit, slicing and print strength are not yet verified.
