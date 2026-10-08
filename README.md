# Kerala residence — interactive 3D viewer

Explore the two-storey house with day/night lighting, six camera presets, and orbit, pan and zoom controls.

Public address after deployment: https://elhamhashir43-eng.github.io/sample3d/

## Enable GitHub Pages

1. Open https://github.com/elhamhashir43-eng/sample3d/settings/pages.
2. Under **Build and deployment**, set **Source** to **GitHub Actions**.
3. Open the repository's **Actions** tab.
4. Select **Deploy 3D viewer to GitHub Pages**, then **Run workflow** on `main` if the initial run failed before Pages was enabled.
5. Wait for both `build` and `deploy` to succeed, then open the public address above.

Future pushes to `main` deploy automatically. No paid server or Blender installation is needed to view the website.

## Run locally

Install Node.js 22.12 or later, then run:

```sh
npm ci
npm run dev
```

Open the address printed by Vite. Drag to orbit, right-drag to pan and scroll to zoom. H restores hidden controls.

## Assets and assumptions

`public/two-storey/house.glb` contains the textured geometry; `lighting.json` supplies browser light positions. The website contains only the assets needed to view the house. Editable Blender scenes remain in the original local project.

Dimensions, hidden room layouts and side elevations are estimated from architectural reference imagery.
