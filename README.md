# Stereotaxic Injection Atlas

### Interactive stereotaxic planning, Allen CCF visualisation and presentation export

Diego Hassan Mediane · 2026  
University of Bristol

<p align="center">
  <a href="https://diego-mediane.github.io/Stereotaxic-Injection-Atlas/">
    <img src="assets/launch_atlas.svg" alt="Launch Stereotaxic Injection Atlas" width="760">
  </a>
</p>

<p align="center"><strong>Press the button to open the fully functional atlas.</strong></p>

The Stereotaxic Injection Atlas is a browser-based tool for plotting mouse-brain injection targets in bregma-relative coordinates. It combines an interactive Allen CCFv3 brain, genuine voxel-based coronal and sagittal sections, optional rig-tilt correction and presentation-ready media export.

## What the atlas can do

- plot one or more labelled injection sites using AP, ML and DV coordinates;
- display injection tips and needle trajectories in the 3D reference brain;
- identify the Allen structure containing the selected target;
- show or hide 259 structures using Allen ontology colours;
- display genuine Allen CCF 2017 coronal and sagittal sections;
- inspect voxel-level annotations by moving the pointer over a 2D section;
- apply optional stereotaxic rig-tilt correction from measured skull landmarks;
- compare planned and uncorrected trajectories;
- export presentation videos, animated GIFs and PNG images;
- add coordinate captions, target-region highlighting and a repository watermark to exported media.

The 2D atlas is loaded only when requested. Sections retain their anatomical aspect ratio and are letterboxed rather than stretched.

## Quick start

1. Open the atlas using the launch button above.
2. In **Targets**, enter a name and the AP, ML and DV coordinates for the injection.
3. Add further targets with **Add target** when required.
4. Use the mouse or trackpad to rotate, pan and zoom the 3D brain.
5. Open **Brain structures** and select any regions that should be highlighted.
6. Enable **Voxel-based 2D atlas** to inspect the nearest coronal and sagittal planes.
7. Enable **Stereotaxic adjustment** only when landmark measurements are available.
8. Open **Export presentation media** to save a video, GIF or PNG.

## Coordinate convention

Coordinates are entered in millimetres relative to bregma:

| Axis | Convention |
|---|---|
| AP | anterior positive, posterior negative |
| ML | left positive, right negative |
| DV | ventral targets negative |

The advanced atlas-fit values define how bregma and the midline are mapped into CCF space. These controls should normally be left at their defaults.

## Plotting injection sites

Each target row contains:

- **Site**: a short label, such as `PAG`, `PL` or `BLA`;
- **AP**: anteroposterior coordinate;
- **ML**: mediolateral coordinate;
- **DV**: dorsoventral coordinate.

The selected target is shown with a coloured tip, a vertical needle trajectory and a label. The information card reports the entered coordinates and the smallest listed Allen structure containing the tip.

Multiple targets can be displayed simultaneously. Select a row by clicking inside it. The 2D atlas and export caption follow the currently selected target.

## Highlighting brain structures

Open **Brain structures** to search the Allen ontology.

- Click a division name to expand it.
- Click an individual structure to show or hide it.
- Click the square beside a major division to toggle every listed structure in that division.
- Use **Hide all structures** to clear the current selection.

Structure colours follow the Allen ontology. The opacity used in exported media can be set independently in the export panel.

## Using the 2D atlas

Enable **Show genuine coronal and sagittal sections** under **Voxel-based 2D atlas**.

The viewer then loads the locally hosted 50 µm Allen CCF 2017 template and annotation volumes. The coronal plane follows the selected AP coordinate and the sagittal plane follows the selected ML coordinate.

The section header reports the nearest stored plane. Move the pointer over either section to inspect:

- the anatomical structure;
- the structure acronym;
- the AP, ML and DV coordinates at that voxel.

The annotation fill can be hidden or made more transparent without changing the underlying template image.

## Optional stereotaxic adjustment

Rig correction is off by default. Enable it only when bregma, lambda and bilateral skull landmarks have been measured using the same stereotaxic manipulator.

1. Zero the manipulator at bregma.
2. Enter the AP, ML and DV readings at lambda.
3. Enter the corresponding readings at the left and right landmarks.
4. Review the calculated pitch, roll and total tilt.
5. Enable the uncorrected ghost trajectory to visualise the estimated displacement.

The correction is a geometric aid. It does not account for individual anatomy, tissue deformation, injection spread or experimental error.

## Exporting presentation media

Open **Export presentation media**, then choose one of the following formats:

- **Video**: records the animation using the best supported browser format, normally WebM and, where available, MP4;
- **Animated GIF**: produces a looping, presentation-friendly animation at a reduced resolution and frame rate;
- **PNG image**: saves a single high-resolution frame.

### Presentation sweep template

The default template is intended for labelled injection sites in talks, posters and lab meetings. It:

- centres the camera towards the selected target;
- highlights the Allen structure containing the selected injection tip;
- shows the injection trajectory and target label;
- moves through a sequence of oblique, lateral, dorsal and frontal views;
- adds the selected coordinates and anatomical region as a caption;
- adds a subtle repository watermark.

### Export controls

Users can adjust:

- background colour;
- output resolution;
- duration and frame rate;
- camera path;
- custom camera-view sequence;
- whole-brain opacity;
- highlighted-region opacity;
- automatic target-region highlighting;
- inclusion of structures already visible in the 3D viewer;
- target centring;
- coordinate caption;
- watermark text, position and opacity.

The watermark defaults to:

```text
https://github.com/diego-mediane/Stereotaxic-Injection-Atlas
```

GIF encoding is more computationally intensive than video recording. For most presentations, video gives smoother motion, better colour fidelity and a smaller file.

## Mouse, trackpad and touch controls

| Action | Control |
|---|---|
| Rotate | left-drag or one-finger drag |
| Pan | right-drag or two-finger drag |
| Zoom | mouse wheel or two-finger pinch |
| Preset view | use the view controls at the lower right |
| Reset | select **Reset 3D view** |

## Scientific basis

The application uses the Allen Mouse Brain Common Coordinate Framework v3 and the Allen CCF 2017 structure ontology. The optional 2D viewer is generated from the actual template and voxel-annotation volumes rather than projected surface geometry.

Key references:

1. Wang Q, Ding S-L, Li Y, et al. The Allen Mouse Brain Common Coordinate Framework: A 3D Reference Atlas. *Cell*. 2020;181:936–953.e20. doi:10.1016/j.cell.2020.04.007.
2. Allen Institute for Brain Science. Allen Mouse Brain Atlas and Common Coordinate Framework datasets.
3. Cecyn MN, Abrahao KP. Where do you measure the Bregma for rodent stereotaxic surgery? *IBRO Neuroscience Reports*. 2023;15:143–148. doi:10.1016/j.ibneur.2023.07.003.
4. cortex-lab/allenCCF and the Modified Allen CCF 2017 dataset. doi:10.6084/m9.figshare.25365829.

## Intended use and limitations

This application is a planning, communication and visualisation aid. The CCF is a population reference and does not reproduce the anatomy of an individual animal. Displayed coordinates and region assignments do not replace:

- pilot injections;
- local surgical procedures;
- brain-surface depth checks;
- experimental controls;
- post-operative histology;
- verification of viral expression or injection spread.

An exported image or animation represents the planned target, not a measured injection volume.

## Local use

The 3D viewer can open directly from `index.html`. The voxel-based 2D atlas uses browser `fetch()` requests and therefore requires a local web server:

```bash
python3 -m http.server 8000
```

Open `http://localhost:8000/` in a browser.

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

## Repository structure

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

The GitHub Actions workflow downloads the official Allen 50 µm volumes, builds the browser-ready atlas, installs the GIF encoder used by the export module and deploys the completed site to GitHub Pages.

## Citation

```text
Mediane, D. H. (2026). Stereotaxic Injection Atlas [Computer software]. GitHub. https://github.com/diego-mediane/Stereotaxic-Injection-Atlas
```

Citation metadata are also provided in `CITATION.cff`.

## Licence

Application code is released under the MIT Licence. Allen atlas data and other third-party materials remain subject to their original terms. See `THIRD_PARTY_NOTICES.md`.
