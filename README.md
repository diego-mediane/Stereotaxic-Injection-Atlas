# Stereotaxic Injection Atlas

### Interactive stereotaxic planning and Allen CCF visualisation

Diego Hassan Mediane · 2026  
University of Bristol

<p align="center">
  <a href="https://diego-mediane.github.io/Stereotaxic-Injection-Atlas/">
    <img src="assets/launch_atlas.svg" alt="Launch Stereotaxic Injection Atlas" width="760">
  </a>
</p>

<p align="center"><strong>Click the button to open the fully functional atlas.</strong></p>

The Stereotaxic Injection Atlas is a browser-based tool for visualising mouse-brain injection targets in the Allen Mouse Brain Common Coordinate Framework. It combines an interactive 3D atlas with genuine voxel-based coronal and sagittal sections.

## Main functions

- enter one or more targets in bregma-relative AP, ML and DV coordinates;
- display injection tips and needle trajectories in the 3D reference brain;
- identify the Allen structure containing the selected target;
- show or hide 259 brain structures using Allen ontology colours;
- open optional coronal and sagittal Allen CCF 2017 sections;
- inspect voxel-level structure annotations in the 2D atlas;
- apply optional stereotaxic rig-tilt correction from measured landmarks;
- compare corrected and uncorrected trajectories.

The 2D atlas is loaded only when enabled. Section images retain their anatomical aspect ratio and are letterboxed rather than stretched.

## Coordinate convention

Coordinates are entered in millimetres relative to bregma:

- AP: anterior positive, posterior negative;
- ML: left positive, right negative;
- DV: ventral targets negative.

The advanced atlas-fit controls define the bregma and midline positions used to map stereotaxic coordinates into CCF space.

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
│   ├── manifest.json
│   └── README.md
├── tools/
│   ├── build_atlas_assets.py
│   ├── requirements-atlas.txt
│   └── structure_tree_safe_2017.csv
└── .github/
    └── workflows/
        └── deploy-pages.yml
```

The GitHub Actions workflow downloads the official Allen 50 µm template and annotation volumes, converts them into browser-ready files and deploys the completed site to GitHub Pages. The source NRRD files are not committed to the repository.

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

## Scientific basis

The application uses the Allen Mouse Brain Common Coordinate Framework v3 and the Allen CCF 2017 structure ontology. The optional 2D viewer is generated from the actual template and voxel-annotation volumes rather than from projected surface geometry.

Key references:

1. Wang Q, Ding S-L, Li Y, et al. The Allen Mouse Brain Common Coordinate Framework: A 3D Reference Atlas. *Cell*. 2020;181:936–953.e20. doi:10.1016/j.cell.2020.04.007.
2. Allen Institute for Brain Science. Allen Mouse Brain Atlas and Common Coordinate Framework datasets.
3. Cecyn MN, Abrahao KP. Where do you measure the Bregma for rodent stereotaxic surgery? *IBRO Neuroscience Reports*. 2023;15:143–148. doi:10.1016/j.ibneur.2023.07.003.
4. cortex-lab/allenCCF and the Modified Allen CCF 2017 dataset. doi:10.6084/m9.figshare.25365829.

## Intended use

This application is a planning and visualisation aid. The CCF is a population reference and does not reproduce the anatomy of an individual animal. Displayed coordinates and region assignments do not replace pilot work, intra-operative checks, histological verification or local procedures.

## Citation

```text
Mediane, D. H. (2026). Stereotaxic Injection Atlas [Computer software]. GitHub. https://github.com/diego-mediane/Stereotaxic-Injection-Atlas
```

Citation metadata are also provided in `CITATION.cff`.

## Licence

Application code is released under the MIT Licence. Allen atlas data and other third-party materials remain subject to their original terms. See `THIRD_PARTY_NOTICES.md`.
