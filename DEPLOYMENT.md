# Deployment

## 1. Create the repository

Create a new public GitHub repository with this exact name:

```text
Stereotaxic-Injection-Atlas
```

Do not add a README, licence or `.gitignore` during repository creation because they are already included in this package.

## 2. Upload the files

Extract the release ZIP. Upload the contents of the `Stereotaxic-Injection-Atlas` folder to the root of the new repository.

The repository root must contain `index.html`, `README.md`, `atlas-data`, `tools`, `assets` and `.github`.

The `.github` folder may be hidden by the operating system. Confirm that it is included before committing.

## 3. Commit the files

Use this initial commit message:

```text
Initial release of the Stereotaxic Injection Atlas
```

## 4. Enable GitHub Pages

1. Open the repository on GitHub.
2. Select **Settings**.
3. Select **Pages** from the left-hand menu.
4. Under **Build and deployment**, set **Source** to **GitHub Actions**.

## 5. Run the deployment

The workflow runs automatically after the files are committed to the `main` branch.

To start it manually:

1. Open the **Actions** tab.
2. Select **Build atlas and deploy Pages**.
3. Select **Run workflow**.
4. Choose the `main` branch.
5. Select **Run workflow** again.

The workflow downloads the official Allen CCF 2017 50 µm volumes, creates the browser assets and deploys the site.

## 6. Open the published viewer

After the workflow completes successfully, the viewer is available at:

```text
https://diego-mediane.github.io/Stereotaxic-Injection-Atlas/
```

The large button in `README.md` points to this address.

## 7. Repository description and website

Recommended repository description:

```text
Interactive mouse-brain stereotaxic injection atlas with Allen CCFv3 3D structures, voxel-based 2D sections and optional rig-tilt correction.
```

Set the repository website field to:

```text
https://diego-mediane.github.io/Stereotaxic-Injection-Atlas/
```

Recommended topics:

```text
neuroscience stereotaxic-surgery mouse-brain allen-ccf brain-atlas threejs webgl neuroanatomy
```

## Updating the application

Commit changes to `main`. Each push rebuilds the atlas assets and redeploys the site automatically.

The launch link remains unchanged while the repository name remains `Stereotaxic-Injection-Atlas`.
