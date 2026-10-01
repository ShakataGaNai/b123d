# CLI smoke scenarios

Run from the repository root after the locked environment has been initialized. These exercise the CLI without builds, extra dependencies or a permanent test suite. No source CAD code is executed. Stock inputs are local original downloads, not redistributed by this skill.

## Stock backplate

```sh
uv run --locked python .agents/skills/stl-measurement/scripts/measure.py inspect tmp/station-g3-reference/SG3-04-Backplate.stl
uv run --locked python .agents/skills/stl-measurement/scripts/measure.py section tmp/station-g3-reference/SG3-04-Backplate.stl --axis z --offset 1.5 --max-loops 12
uv run --locked python .agents/skills/stl-measurement/scripts/measure.py section tmp/station-g3-reference/SG3-04-Backplate.stl --axis z --offset 0.5 --max-loops 12
```

Observed with NumPy 2.5.3 / trimesh 4.12.2: the identified original has SHA-256 `c8829add9f78e7a2ce547966fa9ce8cf13fa643ca88aafebd7659195f9b26024`, 40,774 triangles and spans `[65,112,6.5]` in **unknown native units**. Z=1.5 produces eight closed contours: one rejected outer contour and seven near-circular candidates near `(−29,−52.5)`, `(29,−52.5)`, `(−29,−29.5)`, `(29,−29.5)`, `(−29,52.5)`, `(2.3,52.5)`, `(29,52.5)`. Their spans are approximately 2.5; uniform-perimeter fitted diameters are approximately 2.498 with maximum radial residual below 0.001. This differs slightly from fits weighted by triangulation vertices. Z=0.5 produces one noncircular outer contour and zero circular candidates: the upper openings are not thereby proven through-holes. A different source hash requires fresh expectations.

## Synthetic translation, noncircular contours and invalid data

The following creates only disposable STL data and calls the actual helper as a subprocess. It prints observed behavior rather than installing tests. Observed with the same dependency versions: the translated cylinder produces one accepted contour centered at `[10,-20]` with fitted diameter approximately 3.99699; the rectangle has spans `[8,4]` and no accepted circle; the semicylindrical open arc remains open and unclassified. The X-normal cylinder uses `uv=yz` and centers near `[-20,7]`. The no-intersection case succeeds; empty and non-finite inputs exit 2 with explicit errors.

```sh
uv run --locked python - <<'PY'
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

import numpy as np
import trimesh

helper = Path('.agents/skills/stl-measurement/scripts/measure.py')
with TemporaryDirectory(prefix='stl-measurement-') as directory:
    root = Path(directory)
    rectangle = trimesh.creation.box(extents=[8, 4, 2])
    rectangle.apply_translation([10, -20, 7])
    cylinder = trimesh.creation.cylinder(radius=2, height=4, sections=64)
    cylinder.apply_translation([10, -20, 7])
    x_cylinder = trimesh.creation.cylinder(radius=2, height=4, sections=64)
    x_cylinder.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]))
    x_cylinder.apply_translation([10, -20, 7])
    angles = np.linspace(0, np.pi, 33)
    bottom = np.column_stack((2*np.cos(angles), 2*np.sin(angles), -np.ones(33)))
    top = bottom.copy()
    top[:, 2] = 1
    faces = []
    for i in range(32):
        faces.extend([[i, i+1, i+34], [i, i+34, i+33]])
    arc = trimesh.Trimesh(vertices=np.vstack((bottom, top)), faces=faces, process=False)
    nonfinite = trimesh.Trimesh(vertices=[[0, 0, 0], [1, 0, 0], [0, float('nan'), 1]], faces=[[0, 1, 2]], process=False)
    for name, mesh in [('rectangle', rectangle), ('cylinder', cylinder), ('x-cylinder', x_cylinder), ('arc', arc), ('nonfinite', nonfinite)]:
        mesh.export(root / f'{name}.stl')
    (root / 'empty.stl').write_bytes(b'')
    scenarios = [
        ('rectangle', 'section', ['--axis', 'z', '--offset', '7']),
        ('cylinder', 'section', ['--axis', 'z', '--offset', '7']),
        ('x-cylinder', 'section', ['--axis', 'x', '--offset', '10']),
        ('arc', 'section', ['--axis', 'z', '--offset', '0']),
        ('cylinder', 'section', ['--axis', 'z', '--offset', '100']),
        ('empty', 'inspect', []),
        ('nonfinite', 'inspect', []),
    ]
    for name, command, options in scenarios:
        result = subprocess.run([sys.executable, str(helper), command, str(root / f'{name}.stl'), *options], text=True, capture_output=True)
        payload = json.loads(result.stdout if result.returncode == 0 else result.stderr)
        print(json.dumps({'scenario': name, 'options': options, 'exit': result.returncode, 'result': payload.get('section', payload)}, indent=2))
PY
```

A rejected fit should contain a reason, never a fitted diameter/center presented as a measurement. Coarse faceting may reject an intended circle; do not loosen criteria to force a preferred result. Large offsets can destroy small features in binary STL's float32 coordinates before the helper sees them; translation conditioning cannot recover precision absent from the file.
