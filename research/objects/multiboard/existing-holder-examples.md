# Existing Printables Multiboard-holder examples

> **Scope.** This is an evidence record for three community holder models named by
> the requester, not a dimensional specification for Multiboard, AirTag, the Wio
> Tracker L1 Pro, or SenseCAP T1000-E hardware. It records what the original
> holder publications and their downloaded meshes demonstrate. It deliberately
> does not turn a photograph, a holder cavity, or a title into a physical-fit
> claim for a hardware revision.

## Identity, scope, and readiness

- **Publisher / author:** Printables user `ShakataGaNai` for all three examples
  ([S1]–[S3]).
- **Research date:** 2026-10-01.
- **Consuming model:** [MeshTracker X1 Multiboard pocket](../../../models/meshtracker_x1_multiboard_holder/README.md), using the AirTag snap-peg precedent. Physical fit remains unverified.
- **Source revision identity:** Printables print ID, file ID, listing publication
  timestamps, file-creation timestamp, filename, and original-byte SHA-256 are
  the only identified revisions. The author did not provide source CAD or a
  hardware revision identifier.
- **Readiness:** rail and octagon mounting intent is **user-confirmed** for the
  AirTag precedent. Exact mating geometry, feature registration and a new
  adapter's physical fit still require evidence. The listing/mesh observations
  alone do not specify mate revisions or hardware/case production tolerances.

## User-confirmed mounting requirement

On 2026-10-01, the requester, who identified these as their own holders, clarified
that future adapters should support **both preprinted rails and octagon mounting**,
citing the AirTag holder as the precedent. The work record preserves this
[clarification](https://github.com/ShakataGaNai/b123d/issues/8#issuecomment-5941363440).
Treat that functional confirmation as ground truth. It resolves the earlier
overbroad claim that the AirTag attachment function was unidentified; it does not
supply numerical profiles, component revisions or source-to-assembly transforms.
The author subsequently confirms that the octagonal pegs insert into snaps and selects **13.5 mm across flats × 6.5 mm projection** for future holders following the AirTag precedent. This resolves the receiver-family question; individual snap revisions and the T1000E's exact source profile remain unspecified.

## Sources and access record

The three web listings returned HTTP 403 to a direct reader on the research date.
The public Printables GraphQL endpoint returned their first-party public metadata
and download links without authentication. The endpoint, fields requested, and
IDs below make that access reproducible; it is not a claim that the pages will
remain publicly downloadable.

| ID | First-party source and exact object | Source URL | Identified revision / publication data | Accessed | What it establishes | License evidence |
|---|---|---|---|---|---|---|
| S1 | Printables, **AirTag holder for Multiboard**, print `1407536`, author `ShakataGaNai` | <https://www.printables.com/model/1407536-airtag-holder-for-multiboard> | `firstPublish` 2025-09-07T04:53:18.712029+00:00; `datePublished` 2025-09-07T04:54:50.858891+00:00; `modified` 2025-09-07T04:54:50.868899+00:00 | 2026-10-01 | Title, author, description, file inventory, and listing metadata returned by [G1]. | API `license.id` `4`, name **Creative Commons — Attribution — Noncommercial — Share Alike**. The API result did not state a version or link to full terms. |
| S2 | Printables, **Seeed Wio Tracker L1 Pro Multiboard Holder**, print `1407547`, author `ShakataGaNai` | <https://www.printables.com/model/1407547-seeed-wio-tracker-l1-pro-multiboard-holder> | `firstPublish` / `datePublished` 2025-09-07T05:32:35.481413+00:00; `modified` 2025-09-07T05:32:35.495283+00:00 | 2026-10-01 | Title, author, description, file inventory, and listing metadata returned by [G1]. | Same API license result as S1; full license version/terms URL is unknown from this source. |
| S3 | Printables, **Seeed Studio T1000E holder for Multiboard**, print `1407525`, author `ShakataGaNai` | <https://www.printables.com/model/1407525-seeed-studio-t1000e-holder-for-multiboard> | `firstPublish` / `datePublished` 2025-09-07T05:34:01.426653+00:00; `modified` 2025-09-07T05:34:01.438282+00:00 | 2026-10-01 | Title, author, description, file inventory, and listing metadata returned by [G1]. | Same API license result as S1; full license version/terms URL is unknown from this source. |
| G1 | Printables public GraphQL API | <https://api.printables.com/graphql/> | Public query/mutation access observed 2026-10-01; no API schema revision supplied. | 2026-10-01 | `print(id)` returned `id`, `name`, `description`, `user.publicUsername`, `license`, `slug`, `firstPublish`, `datePublished`, `modified`, `image.filePath`, and `stls`; `getDownloadLink` returned each D-link. | Not a content license. |

### Reproducing first-party metadata access

For each print ID, the read-only metadata portion used this shape (with that
print's ID):

```graphql
query {
  print(id: "1407536") {
    id name slug description
    user { publicUsername }
    license { id name }
    firstPublish datePublished modified
    image { filePath }
    stls { id created name folder note fileSize filePreviewPath order }
    otherFiles { id name }
  }
}
```

Each listed file was resolved with the Printables mutation
`getDownloadLink(id: <file-id>, printId: <print-id>, fileType: stl,
source: model_detail)`. `fileType: stl` is the API collection name even though
all three source files are `.3mf`; it is not a statement that the bytes are STL.
Only returned data was parsed. No downloaded code, macro, or model script was
executed.

## File inventory and original-download provenance

Each print currently has exactly one item in `stls` and no `otherFiles`.
There are no source-CAD files, separate Rail files, installation instructions,
or declared variants in those inventories. `created` is the file-record time
returned by Printables; it is not a CAD-revision date.

| Example | File ID / filename / API order | File-record `created` | Original bytes and SHA-256 | Direct original download | License and retention decision |
|---|---|---:|---|---|---|
| AirTag | `5927171`; `Multiboard AirTag.3mf`; 1 | 2025-09-07T04:48:07.018122+00:00 | 611,192 bytes; `14b251de08c6094763477e85d1e45d572b9110b89d06a10307bc510cba15ef73` | [D1] | Listing reports Attribution–Noncommercial–Share Alike. Original was retrieved and inspected in ignored scratch storage, but is **not committed**: the repository has no declared redistribution/use context and the API did not give full license terms/version. The checksum identifies the inspected bytes, not permission or authenticity. |
| Wio L1 Pro | `5927201`; `Multiboard Seeed L1.3mf`; 1 | 2025-09-07T05:10:55.790767+00:00 | 23,882 bytes; `90deae95851e73f4a5ec4bf097d20744f502656e3327b1a0b9d8034125dfd801` | [D2] | Same license/retention decision as AirTag. |
| T1000E | `5927125`; `T1000e Multiboard.3mf`; 1 | 2025-09-07T04:13:16.742498+00:00 | 253,479 bytes; `720967811293b306cfc9e209914e9e72d269f7b4415fe62a8bb1b06bb14eb412` | [D3] | Same license/retention decision as AirTag. |

The retrieved originals were ZIP-based 3MF packages. Before parsing, each archive
was listed: it contains only `3D/3dmodel.model`, `[Content_Types].xml`, and
`_rels/.rels` (no path traversal, executable, macro, or embedded source code).
The model XML declares `unit="millimeter"`, one build item, and one mesh object:
`Body_01` (AirTag, 19,342 vertices / 38,680 triangles), `Body_04` (Wio,
798 / 1,592), and `Body_01` (T1000E, 8,864 / 17,724). Those counts are
mesh facts, not feature or tolerance specifications.

## Mesh-inspection coordinate and evidence contract

The [follow-up connector measurements](measured-connectors.md) supersede the initial uncertainty about the AirTag rear feature's function and profile: the author identifies it as the octagon mount, and sections recover a straight 13.5 mm across-flats, 6.5 mm projecting peg. The initial inspection below retains its source frame; the follow-up records the isolated-viewer transform and supplied rail separately. Physical fit remains untested.

- **Source and model units:** the original 3MF XML declares millimetres. A
  temporary binary STL derivative was made from each XML mesh with no scaling,
  repair, recentering, orientation change, or component transform, solely so
  the repository's STL inspection helper could parse it. STL itself does not
  declare units; its native coordinates inherit the 3MF declaration for these
  derived measurements.
- **Frame:** the maker's mesh frame is retained. `+X`, `+Y`, and `+Z` are only
  source-mesh axes; no image or source document establishes which face is a
  functional Multiboard datum, a user-facing side, or a hardware datum. No
  source-to-assembly transform has been established.
- **Method / uncertainty:** inspected with the repository helper using NumPy
  2.5.3 and trimesh 4.12.2. Exact-coordinate indexing found finite coordinates,
  no zero-area triangles, watertight meshes, and consistent winding; it did not
  check self-intersections or establish physical validity. Values below are
  **derived from the particular faceted upload**, with no stated manufacturing
  tolerance. They are not physical measurements, fit clearances, or product
  dimensions.
- **Size convention:** every span is an axis-aligned bounding-box span in the
  unmodified source mesh, reported as `X × Y × Z` in mm. A section span is its
  axis-aligned `u × v` span in the named source-coordinate plane; it is not a
  diameter, a hardware envelope, or a declared interface dimension.

### Derived mesh envelopes

| Holder source mesh | Source-frame bounds `[min, max]` mm | Span `X × Y × Z` mm | Evidence class / source | Modeling consequence |
|---|---|---:|---|---|
| AirTag 3MF | `[-17.5, -15.0, 0.0]` to `[17.5, 21.5, 13.5]` | `35.0 × 36.5 × 13.5` | **Derived**, D1 original bytes; no mesh transform | Bounds only the printed holder mesh, not any AirTag or board clearance. |
| Wio 3MF | `[-30.0, -16.0, 0.0]` to `[30.0, 16.0, 45.0]` | `60.0 × 32.0 × 45.0` | **Derived**, D2 original bytes; no mesh transform | Bounds only the carrier; the author separately requires a Rail that is absent from D2. |
| T1000E 3MF | `[0.0, 0.0, 0.0]` to `[62.0, 19.5, 24.0]` | `62.0 × 19.5 × 24.0` | **Derived**, D3 original bytes; no mesh transform | Bounds only the printed holder, not the tracker or a charging/cable envelope. |

### Selected section observations

These are deliberately observations rather than reconstructed dimensions. The
closed interior loops are not called holes, slots, or a mating profile unless
another source establishes their function. A section alone also cannot prove a
through-cut or a retention direction.

| Mesh / source plane | Derived observation in mesh coordinates | Evidence class / source | What it does and does not show |
|---|---|---|---|
| AirTag, `Z=3.0` | Outer contour span `35.0 × 36.5` mm; two closed non-circular interior contours, each `14.257 × 4.577` mm. | **Derived**, D1 sectioned mesh | Demonstrates a repeated pair of internal contours in that plane; does not establish AirTag dimensions, insertion direction, or a physical retention load. |
| AirTag, `Z=8.0` | Same outer contour span; two closed non-circular interior contours, each `26.210 × 7.593` mm. | **Derived**, D1 sectioned mesh | Together with the listing's “multiple AirTags” description, this supports a two-bay holder interpretation, but not a generation-specific AirTag fit. |
| T1000E, `Z=5.0` | Outer contour span `62.0 × 19.5` mm; one inner contour span `56.0 × 7.0` mm. | **Derived**, D3 sectioned mesh | Demonstrates a long internal contour within the carrier at this plane; it is not a published tracker envelope. |
| T1000E, `Z=20.0` | Outer contour span `62.0 × 13.0` mm; the inner contour remains `56.0 × 7.0` mm. | **Derived**, D3 sectioned mesh | Confirms the same contour at a separated source height; it still does not prove a complete service/access path or the meaning of “snap.” |

## What each example actually demonstrates

### 1. AirTag holder: small repeated cradle precedent, not a product fit model

The author describes S1 as “a holder for multiple AirTags, for your
multiboard,” recommends a 0.2 setting, says supports should not be required,
and notes sample PETG/fuzzy-skin results. The accompanying author image [I1] shows
a single AirTag standing in the printed part. The source mesh has the two repeated
interior-contour observations recorded above. These together demonstrate a
small, repeated, object-specific cradle pattern; they do **not** establish the
number of usable bays under a particular print process, an AirTag generation,
battery-service removal force, or a board attachment profile.

- **Retention and access evidence:** the photo shows an exposed AirTag face;
  the mesh shows repeated internal geometry. Neither specifies a retention
  feature name, insertion/removal path, or force. No hardware drawing or
  physical test was supplied.
- **Cable/charging evidence:** none. The record does not infer that a cable is
  unnecessary, nor provide a clearance for one.
- **Multiboard attachment evidence:** S1 does not name its mating accessory,
  but the author/requester's later clarification establishes the AirTag holder
  as a rail/octagon mounting precedent. Map its mesh features to those routes
  using original CAD or the identified counterparts; do not infer a standard
  profile or assign dimensions solely from a tab's bounding box.

### 2. Wio Tracker L1 Pro: case-specific, Rail-dependent carrier precedent

S2 is more explicit than the other examples: it says the holder is compatible
with a “Seeed Studio Wio Tracker L1 Pro for Meshtastic,” **fits exactly the case
it ships with**, prints without supports, and **requires a Rail for the rear
connection to the Multiboard**. D2 is only one holder body; its inventory has
no Rail file or revision. The author image [I2] depicts a front-facing cased device
in a sloped white carrier, with the device display/buttons visible and an
antenna visible in that photographed configuration. The image is not used for
measurement.

- **Retention scope:** the evidenced target is the unspecified shipping case,
  not a bare Wio Tracker L1 Pro, a replacement case, or a differently equipped
  antenna/cable assembly. S2 supplies no case part number or revision.
- **Access/service evidence:** the image makes the photographed front face
  visible, but S2/D2 do not specify USB, charge, antenna, switch, fastener,
  ventilation, cable-bend, or removal clearance. No physical service claim is
  warranted.
- **Attachment interface:** “Rail” and “rear connection” are author-stated.
  The actual Rail mating profile, its revision, its dimensions, insertion
  direction, and retention/load rating are absent. This is the only one of the
  three examples that proves a separate rear Rail dependency.

### 3. T1000E: card-like pocket with an author-confirmed snap-insert route

S3 calls the model a holder for the “Seeed Studio T1000E” and advises printing
at 0.2 “to make sure the fits the snap,” with no supports. That sentence alone
does not define the attachment. The author subsequently confirmed that the
octagonal pegs insert into snaps; the T1000E's exact profile dimensions and
receiver revision remain unspecified. D3's two separated section observations
show a long internal contour. The author image [I3] shows a card-like,
transparent device face exposed above a white lower carrier. It establishes
the depicted configuration, not a scale drawing or hardware revision.

- **Retention and access evidence:** the mesh/photo support an object-specific
  pocket/carrier interpretation and exposed front face, but do not identify the
  snap geometry, insertion/removal direction, or force. They do not prove
  charging, button, radio, or connector access.
- **Cable/charging evidence:** none. In particular, do not infer clearance for
  a charging puck, USB lead, or antenna from the listing image.
- **Multiboard attachment evidence:** the author confirms the snap-insert route.
  S3 names no Rail; D3's central/tab-like feature remains to be dimensioned and
  registered against the selected snap revision.

## Future-adapter decision: a demonstrated boundary, not a common profile

The safe reusable precedent is an **interface boundary**, not a dimension set:

1. Model each target's **object retainer** against an identified hardware/case
   revision, with its own retention, front/side access, and cable/service
   requirements.
2. Make the **board attachment** an independently named requirement containing
   a cited mating asset/profile revision, insertion/removal direction, and load
   conditions. For the Wio pattern, a rear Rail is required and must be supplied
   as a separate, revision-identified mate.
3. Preserve the author-confirmed **rail and octagon** routes for future adapters.
   Identify their exact counterparts and register the mating features rather
   than choosing a connector from a title or bounding-box coincidence. The
   T1000E mesh still does not establish a common profile with AirTag.

This separation is actionable for future build123d adapters: an object-specific
cradle may be swapped while the selected board-mate geometry stays explicit.
The downloaded holder meshes are usable geometric references once their mating
features are registered; lack of a connector name in S1 is not a functional block.

## Unknowns, conflicts, and modeling blocks

Missing mating geometry and the example-asset license version were recorded in
[issue #10](https://github.com/ShakataGaNai/b123d/issues/10), now closed at the
user's request. Revisit compatibility only if print testing exposes a problem;
the evidence limits below do not require further research for the current holder.

| ID | Missing or ambiguous fact | Evidence and current decision | Risk / resolution needed | Blocks |
|---|---|---|---|---|
| U1 | Snap variant and feature registration for the author's octagonal inserts | Author confirms insertion into snaps and selects the AirTag's measured 13.5 mm across-flats × 6.5 mm projection. D1/D3 preserve their own mesh geometry; the particular snap revision and T1000E's exact profile are unspecified. | Use the confirmed AirTag dimensions for that precedent; identify the snap revision and register its seating face for a new assembly. | New assembly/revision compatibility claims, not the confirmed snap-insert route or chosen 6.5 mm projection. |
| U2 | Wio Rail identity and geometry | S2 requires a rear Rail; D2 has no Rail file. | Obtain a revision-specific Rail CAD/drawing and assemble/section it with D2. | Wio board connection. |
| U3 | Hardware/case revision and actual envelope for each target | No official hardware drawings were used; no scale is taken from photographs. S2 names only the shipping case. | Obtain revision-specific official mechanical source or identified specimen measurements, including accessories. | Any physical-fit statement or replacement retainer. |
| U4 | Retention, removal, cable, connector, charging, cooling, and tool clearances | Listing text and one author image per model do not specify them. | Define intended use and verify with a representative assembly / fit coupon. | Claims about serviceability, cable routing, or reliable retention. |
| U5 | T1000E's exact attachment profile and snap variant | The author confirms that the octagonal pegs insert into snaps. D3's exact feature dimensions and specific receiver revision remain undocumented. | Inspect its source attachment feature and register it against the chosen snap if reproducing T1000E-specific geometry. | T1000E-specific reconstruction, not the confirmed snap-insert route. |
| U6 | License version/full terms and durable redistribution basis | API returns a license name only; repository has no stated redistribution/use context. | Obtain the listing's full license text/version and establish intended repository distribution before committing originals or derivatives. | Asset redistribution only; source links/checksums remain usable. |

## Verification status and required next evidence

| Requirement | Performed evidence | Status |
|---|---|---|
| All three named records reviewed | First-party GraphQL metadata/description/file inventory retrieved for S1–S3; page-reader 403 recorded. | pass |
| Original mesh bytes safely inspected | All three 3MF archives listed before parsing; original hashes recorded; XML meshes parsed without executing downloaded content. | pass |
| Mesh geometry inspection | Derived temporary STL meshes inspected/sectioned without transform; finite/watertight/winding checks recorded, with self-intersection and physical validity explicitly unverified. | pass |
| Exact board mate / physical fit | No mating assembly, official target envelope, print, or physical test. | inconclusive / blocked |
| Future adapter validation | Register retainer and named mate to real datums; inspect clearances in CAD; then print a target-specific retention and service-access coupon before asserting fit. | not run |

The X1 holder's `model.toml` links this record and its hardware and measured
connector records. Future consumers should likewise link
`research/objects/multiboard/existing-holder-examples.md` and the hardware and
Multiboard mating-interface records they use. CAD checks do not establish
physical insertion, retention or service access.

## Source links

[S1]: https://www.printables.com/model/1407536-airtag-holder-for-multiboard
[S2]: https://www.printables.com/model/1407547-seeed-wio-tracker-l1-pro-multiboard-holder
[S3]: https://www.printables.com/model/1407525-seeed-studio-t1000e-holder-for-multiboard
[G1]: https://api.printables.com/graphql/
[D1]: https://files.printables.com/media/prints/6eaef87d-d698-42e3-ab1a-8fba325acfca/stls/10623499_0570af87-a084-4889-864c-46c5f2f85b7e_cec1ed8b-4df9-44cc-9be2-784ef207bcaf/multiboard-airtag.3mf
[D2]: https://files.printables.com/media/prints/a17aef88-7906-403e-9063-1d673e9f293d/stls/10623563_5ca70f44-f778-4e56-868a-e1664e5a854d_aab949c7-b245-446a-a211-319c07dd2edb/multiboard-seeed-l1.3mf
[D3]: https://files.printables.com/media/prints/857c75df-142a-4073-85b5-79d5e90e8f69/stls/10623412_76c99634-b85d-48a1-9272-c244b2272304_adeded65-3139-4d80-8082-d1de7e7268ca/t1000e-multiboard.3mf
[I1]: https://media.printables.com/media/prints/a17972dc-f4bd-4eec-ae72-605476bb7adc/images/10623511_928a985e-50f1-4fca-9aec-b7b12aa0d74f_38a7e540-0450-43a3-bab0-b5c067e9a56a/img_3108.jpeg
[I2]: https://media.printables.com/media/prints/590a3be7-460e-4b29-8da7-e8bed885cbe0/images/10623614_e2fdcc0f-3a79-4642-b8d3-36c9a4ecded3_10bda709-4dcf-4a4c-927e-bc13af564015/img_3349.jpeg
[I3]: https://media.printables.com/media/prints/252c4ebc-7c4c-4028-8388-236aae6bffd7/images/10623625_e5676f15-cb72-4c4a-8917-e4ed1341b8a0_afdf8c03-8965-4497-9073-8bc053ed4229/img_3355.jpeg
