# Regenerating these scenes

The pack is built from `boneglass`, the renderer these were made
with. With that on the path:

    python -m projects.vista.build             # all ten
    python -m projects.vista.build --only mesa

`scenes.py` holds every scene as a function. The parameters that
matter most, in the order they change the picture:

  `Look.extinction`  how much air. Raise it and the far plane
                     dissolves; the ladder in `pack.DEPTH` is
                     tuned against it and `veil_check` refuses a
                     combination that erases a body.
  `Ridge.seed`       moves the terrain and nothing else.
  `Ridge.freq`       how many hills across the frame. MUST STAY
                     A WHOLE NUMBER or the layer stops looping;
                     `Ridge.tiling_issues()` says so.
  `Plane.colour`     the albedo before light and air.
  `Ridge.blocks`     flat-topped skyline, for cities and mesas.

After any edit run the build - it fails on the checks rather
than warning, and the checks are the ones that catch defects
which render successfully.
