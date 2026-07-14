# Stereotaxic Injection Atlas

Interactive mouse-brain stereotaxic planning with Allen CCFv3 visualisation, genuine 2D atlas sections, optional tilt correction and presentation export.

<p align="center">
  <a href="https://diego-mediane.github.io/Stereotaxic-Injection-Atlas/">
    <img src="assets/launch_atlas.svg" alt="Open the Stereotaxic Injection Atlas" width="760">
  </a>
</p>

<h2 align="center">
  <a href="https://diego-mediane.github.io/Stereotaxic-Injection-Atlas/">CLICK HERE TO START</a>
</h2>

<p align="center">
  The atlas opens directly in your browser. No installation or download is required.
</p>

---

## Quick start

Most users only need these steps:

1. Click **CLICK HERE TO START** above.
2. Enter a site name and the AP, ML and DV coordinates under **Targets**.
3. Add more targets when needed.
4. Choose one target as **2D active** if you want to inspect coronal and sagittal atlas sections.
5. Tick **Include in export** for every target that should appear in a video, GIF or PNG.
6. Rotate, pan and zoom the 3D brain using the mouse, trackpad or touchscreen.

The viewer updates immediately as coordinates are entered.

## What the atlas does

- Plots one or more labelled stereotaxic targets in a 3D Allen CCFv3 mouse brain.
- Displays injection tips and needle trajectories.
- Identifies the Allen structure containing the active target.
- Provides genuine voxel-based coronal and sagittal Allen CCF 2017 sections.
- Allows individual brain structures or complete anatomical divisions to be highlighted.
- Supports optional correction for stereotaxic rig tilt.
- Exports presentation-ready video, animated GIF and PNG files.
- Adds permanent repository attribution to exported media.

## Coordinate convention

Coordinates are entered in millimetres relative to bregma.

| Axis | Convention |
|---|---|
| AP | anterior positive, posterior negative |
| ML | left positive, right negative |
| DV | ventral targets negative |

The advanced atlas-fit values should normally remain at their defaults.

## Adding and selecting targets

Each target row contains:

- **Site**: a short label such as `PAG`, `PL` or `BLA`.
- **AP**: anteroposterior coordinate.
- **ML**: mediolateral coordinate.
- **DV**: dorsoventral coordinate.

Every valid target is displayed with a coloured tip, a needle trajectory and a label.

Each target has two separate controls:

- **2D active** selects the single target followed by the coordinate readout and the coronal and sagittal atlas. Clicking anywhere inside a target row also makes it active.
- **Include in export** selects every target that should appear in exported media. Any number of valid targets can be included.

This means the 2D atlas can follow one target while a video or image shows several injection sites at the same time.

## Viewing brain structures

Open **Brain structures** to search or browse the Allen ontology.

- Select an individual structure to show or hide it.
- Expand a major division to browse its structures.
- Select the square beside a division to toggle the whole group.
- Use **Hide all structures** to clear the current selection.

Displayed colours follow the Allen ontology. Structure opacity can be adjusted separately for exported media.

## Using the 2D atlas

1. Select one target as **2D active**.
2. Open **Voxel-based 2D atlas**.
3. Enable **Show genuine coronal and sagittal sections**.

The coronal view follows the target's AP coordinate. The sagittal view follows its ML coordinate. The nearest available 50 µm atlas plane is shown without stretching.

Move the pointer over either section to inspect:

- the anatomical structure;
- its acronym and full name;
- the AP, ML and DV coordinates of that voxel.

Annotation colours and transparency can be adjusted without changing the underlying reference image.

## Optional stereotaxic adjustment

Rig correction is disabled by default. Use it only when skull landmarks have been measured with the same stereotaxic manipulator.

1. Zero the manipulator at bregma.
2. Enter the readings measured at lambda.
3. Enter the left and right landmark readings.
4. Review the calculated pitch, roll and total tilt.
5. Show the uncorrected ghost trajectory to visualise the estimated displacement.

The correction is a geometric aid. It does not replace pilot injections, local surgical procedures or histological verification.

## Exporting videos, GIFs and images

Open **Export presentation media** after entering at least one valid target.

Available formats:

- **Video** for smooth presentation playback and better colour fidelity.
- **Animated GIF** for convenient looping in slides and documents.
- **PNG** for a high-resolution still image.

The default **Presentation sweep** is designed for labelled injection sites. It:

- includes all targets marked **Include in export**;
- centres the camera on the included sites;
- highlights the Allen structures containing the target tips;
- displays each trajectory and label;
- moves through several useful 3D viewpoints;
- adds coordinates and anatomical information;
- adds permanent repository attribution.

Users can also adjust the background colour, output size, duration, frame rate, camera path, brain opacity, region opacity, labels and captions.

Every exported file contains:

```text
github.com/diego-mediane/Stereotaxic-Injection-Atlas
```

For most presentations, video is preferable to GIF because it produces smoother movement, more accurate colours and a smaller file.

## Navigation controls

| Action | Control |
|---|---|
| Rotate | left-drag or one-finger drag |
| Pan | right-drag or two-finger drag |
| Zoom | mouse wheel or pinch |
| Preset view | use the controls at the lower right |
| Reset view | select **Reset 3D view** |

## Intended use

The atlas is designed for:

- pre-surgical planning;
- communication of injection coordinates;
- teaching and training;
- preparation of figures, presentations and lab-meeting material;
- visual comparison of planned targets.

It is a planning and visualisation aid, not a substitute for experimental verification. The Allen CCF is a population reference and cannot reproduce the anatomy of an individual animal. Final placement should be verified using appropriate histology and experimental controls.

## Scientific basis

The application uses the Allen Mouse Brain Common Coordinate Framework v3 and the Allen CCF 2017 structure ontology. The 2D viewer is generated from the genuine template and voxel-annotation volumes rather than from projected surface geometry.

Key references:

1. Wang Q, Ding S-L, Li Y, et al. The Allen Mouse Brain Common Coordinate Framework: A 3D Reference Atlas. *Cell*. 2020;181:936–953.e20. doi:10.1016/j.cell.2020.04.007.
2. Allen Institute for Brain Science. Allen Mouse Brain Atlas and Common Coordinate Framework datasets.
3. Cecyn MN, Abrahao KP. Where do you measure the Bregma for rodent stereotaxic surgery? *IBRO Neuroscience Reports*. 2023;15:143–148. doi:10.1016/j.ibneur.2023.07.003.
4. cortex-lab/allenCCF and the Modified Allen CCF 2017 dataset. doi:10.6084/m9.figshare.25365829.

<details>
<summary><strong>Local use and development</strong></summary>

The 3D viewer can open directly from `index.html`. The voxel-based 2D atlas requires a local web server because it loads atlas files using browser `fetch()` requests.

```bash
python3 -m http.server 8000
```

Then open:

```text
http://localhost:8000/
```

To build the atlas files locally:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r tools/requirements-atlas.txt
python tools/build_atlas_assets.py --official --resolution-um 50 --overwrite
```

Windows PowerShell activation:

```powershell
.venv\Scripts\Activate.ps1
```

</details>

<details>
<summary><strong>Repository structure</strong></summary>

```text
Stereotaxic-Injection-Atlas/
├── index.html
├── README.md
├── DEPLOYMENT.md
├── CITATION.cff
├── LICENSE
├── THIRD_PARTY_NOTICES.md
├── assets/
│   └── launch_atlas.svg
├── atlas-data/
├── tools/
└── .github/workflows/
```

The GitHub Actions workflow downloads the official Allen 50 µm volumes, builds the browser-ready atlas, installs the GIF encoder and deploys the completed site to GitHub Pages.

</details>

## Citation

```text
Mediane, D. H. (2026). Stereotaxic Injection Atlas [Computer software]. GitHub. https://github.com/diego-mediane/Stereotaxic-Injection-Atlas
```

Citation metadata are also available in `CITATION.cff`.

## Licence

Application code is released under the MIT Licence. Allen atlas data and other third-party materials remain subject to their original terms. See `THIRD_PARTY_NOTICES.md`.

---

<p align="center">
  <strong>Ready to use the atlas?</strong><br><br>
  <a href="https://diego-mediane.github.io/Stereotaxic-Injection-Atlas/"><strong>CLICK HERE TO START</strong></a>
</p>
