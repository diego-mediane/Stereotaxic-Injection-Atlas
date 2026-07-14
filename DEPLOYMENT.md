# Deployment and updates

## Published address

```text
https://diego-mediane.github.io/Stereotaxic-Injection-Atlas/
```

The large launch button in `README.md` points to this address.

## Initial deployment

1. Create a public GitHub repository named `Stereotaxic-Injection-Atlas`.
2. Upload the contents of this package to the repository root.
3. Confirm that `.github/workflows/deploy-pages.yml` is present.
4. Open **Settings → Pages**.
5. Set **Source** to **GitHub Actions**.
6. Open **Actions → Build atlas and deploy Pages**.
7. Run the workflow if it has not started automatically.

The workflow downloads the official Allen CCF 2017 50 µm volumes, builds the browser atlas, installs the GIF encoder used by the export panel and deploys the site.

## Updating an existing deployment

Replace the updated files in the repository and commit them to `main`. The workflow will start automatically.

For the presentation-export release, update:

```text
index.html
README.md
DEPLOYMENT.md
CITATION.cff
THIRD_PARTY_NOTICES.md
.github/workflows/deploy-pages.yml
```

A successful workflow run shows green ticks for both `build` and `deploy`.

## Repository settings

Recommended description:

```text
Interactive Allen CCF mouse-brain stereotaxic injection atlas with voxel sections, optional tilt correction and presentation media export.
```

Website:

```text
https://diego-mediane.github.io/Stereotaxic-Injection-Atlas/
```

Recommended topics:

```text
neuroscience stereotaxic-surgery mouse-brain allen-ccf brain-atlas threejs webgl neuroanatomy
```

## Local use

The 3D viewer can open directly from `index.html`. The 2D voxel atlas requires a local web server:

```bash
python3 -m http.server 8000
```

Open:

```text
http://localhost:8000/
```

The deployed workflow supplies `assets/gif.js` and `assets/gif.worker.js`. During local development, GIF export can use the jsDelivr fallback when those files are absent. Video and PNG export do not require the GIF library.
