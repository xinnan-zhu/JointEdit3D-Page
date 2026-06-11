# JointEdit3D Project Page

Static project page for GitHub Pages.

## Replace Demo Media

Put before/after videos in:

```text
project_page/assets/media/
```

Then edit `COMPARE_CASES` at the top of `project_page/assets/app.js`:

```js
{
  id: "scene-01",
  label: "Scene 01",
  before: "assets/media/scene_01_before.mp4",
  after: "assets/media/scene_01_after.mp4",
  beforeLabel: "Original",
  afterLabel: "JointEdit3D"
}
```

The comparison component accepts `.png`, `.jpg`, `.mp4`, `.webm`, and `.mov`. Video pairs are muted, looped, and synchronized.

## Replace 3D Assets

The page uses lightweight browser-side `<model-viewer>` cards that load `.glb` / `.gltf` assets. Put exported 3D previews in:

```text
project_page/assets/models/
```

Then edit `DATASET_SAMPLES` and `CLOUD_SCENES` at the top of `project_page/assets/app.js`:

```js
{
  id: "scene-01",
  label: "Scene 01",
  title: "Scene 01 sample",
  before: "assets/media/scene_01_before.mp4",
  after: "assets/media/scene_01_after.mp4",
  model: "assets/models/scene_01_edit.glb",
  thumb: "assets/media/scene_01_thumb.png"
}

{
  id: "scene-01",
  label: "Scene 01",
  thumb: "assets/media/scene_01_thumb.png",
  cards: [
    { label: "Source", url: "assets/models/scene_01_source.glb" },
    { label: "JointEdit3D", url: "assets/models/scene_01_ours.glb" },
    { label: "Edited 3D", url: "assets/models/scene_01_target.glb" }
  ]
}
```

If your source assets are `.ply`, convert them to `.glb` / `.gltf` before publishing so the page remains consistent with the `model-viewer` implementation.

## Local Preview

From this directory:

```bash
python3 -m http.server 8090
```

Then open `http://localhost:8090`.
