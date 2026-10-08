# Kerala residence — interactive 3D project

The repository contains the interactive web viewer and the source assets used to build the house. The live viewer is deployed automatically from this branch:

https://elhamhashir43-eng.github.io/sample3d/

## Run the viewer

Install Node.js 22.12 or later, then in the repository folder run:

```sh
npm ci
npm run dev
```

Open the local Vite address. The controls include day/night lighting, eight camera presets, orbit, pan, zoom, roof visibility, and ground/first/all-floor views. Drag to orbit, right-drag to pan, and scroll to zoom.

To build the deployable site, run `npm run build`. GitHub Actions publishes the built site after pushes to `main`.

## Blender source

- `blender/build_reference.py` builds the Blender scene and exports the web model.
- `blender/house.blend` and `blender/house-night.blend` are editable day and night scenes.
- `exports/textures/` contains the textures referenced by the builder.
- `public/two-storey/house.glb` and `lighting.json` are the viewer-ready assets.

With Blender installed, run the build script from the repository root:

```sh
blender -b --python blender/build_reference.py
```

It writes the editable scenes under `blender/` and the GLB and light manifest under `exports/two-storey/`. Copy the exported `house.glb` and `lighting.json` into `public/two-storey/`, then build the site.

## Architectural assumptions

The floor-plan dimensions are treated as centimetres and converted to metres. The clipped small toilet label is estimated as approximately 120 × 240 cm. Wall thickness, floor heights, roof pitches and unlabelled dimensions are approximations from the supplied drawings. This is a visualization model, not construction documentation.

The interactive assets are optimized for web performance; they do not match the photorealistic quality of the exterior rendering.

## GitHub Pages setup

The repository uses GitHub Actions for Pages deployment. In **Settings → Pages**, set **Build and deployment → Source** to **GitHub Actions**. The workflow deploys after pushes to `main`.
