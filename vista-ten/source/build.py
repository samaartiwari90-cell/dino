"""Render the pack, check it, and lay it out the way a buyer opens it.

    python -m projects.vista.build                 # all ten
    python -m projects.vista.build --only cairn
    python -m projects.vista.build --contact       # just the preview grid

THE BUILD FAILS ON THE CHECKS, WHICH IS THE ONLY REASON THEY ARE WORTH HAVING

Every rule in `parallax.issues` and `parallax.verify` describes a defect that
renders successfully and looks fine in a still. A build that printed them as
warnings would ship all of them, because a warning at the end of a
two-hundred-line log is not a warning. So `--force` exists and nothing in the
pack uses it.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

from boneglass import parallax as px

from .pack import BUDGET, H, W, ZOOM, params
from .scenes import ALL

OUT = Path("projects/vista/out")
LICENCE = "CC0-1.0"


def one(name: str, *, out: Path, zoom: int = ZOOM, force: bool = False) -> dict:
    """Render one scene into its own folder. Returns its line of the report."""
    scene, bands = ALL[name]()

    bad = px.issues(scene, bands)
    if bad and not force:
        raise SystemExit(f"{name}: {len(bad)} issue(s) before rendering:\n  "
                         + "\n  ".join(bad))

    # The tiling gate, and it is asked of the SCENE rather than of the files:
    # `periodic` paints the picture twice, half a frame apart, and requires the
    # two to agree exactly. Anything that reads x without wrapping fails it by
    # eleven orders of magnitude, so there is no threshold in this build.
    loop = px.periodic(scene)
    sheet = px.render(scene, params(), bands, name=name)
    checks = px.verify(sheet)

    fail = []
    if not checks["composites"]:
        fail.append("the layers do not composite back into the preview")
    if checks["holes_px"]:
        fail.append(f"{checks['holes_px']} px of the frame are covered by no "
                    f"layer at all")
    if checks["colours_used"] > BUDGET:
        fail.append(f"{checks['colours_used']} colours against a budget of "
                    f"{BUDGET}")
    if not loop["periodic"]:
        fail.append(f"the painting is not periodic in x: colour differs by "
                    f"{loop['rgb_max_error']:.3g} and "
                    f"{loop['part_mismatch_px']} samples change part when the "
                    f"frame is slid half a width. It will not loop.")
    if fail and not force:
        raise SystemExit(f"{name}: {len(fail)} defect(s) after rendering:\n  "
                         + "\n  ".join(fail))

    px.write(sheet, out / name, name=name, zoom=zoom, licence=LICENCE)

    return {
        "name": name,
        "canvas": [sheet.w, sheet.h],
        "layers": [b.name for b in sheet.bands],
        "scroll": [b.scroll for b in sheet.bands],
        "colours": checks["colours_used"],
        "budget": BUDGET,
        "tiles_x": bool(sheet.info.get("tiles_x")),
        "periodic": loop["periodic"],
        "seam_ratio": checks.get("seam_ratio"),
        "warnings": bad,
    }


def contact(rows: list[dict], out: Path, *, cols: int = 2, zoom: int = 2):
    """The preview grid, which is the thing the store page actually sells.

    Two columns rather than five, because an itch.io page renders an image at
    the column width and a five-wide grid arrives as ten thumbnails 150 pixels
    across, where every one of these scenes looks like a gradient.
    """
    tiles = []
    for r in rows:
        f = out / r["name"] / f"{r['name']}.png"
        if f.exists():
            tiles.append((r["name"], Image.open(f).convert("RGB")))
    if not tiles:
        return None
    pad, label = 8, 14
    tw, th = W * zoom, H * zoom
    n = len(tiles)
    nrows = (n + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * pad,
                              nrows * (th + label) + (nrows + 1) * pad),
                      (18, 18, 22))
    for i, (nm, im) in enumerate(tiles):
        cx, cy = i % cols, i // cols
        x = pad + cx * (tw + pad)
        y = pad + cy * (th + label + pad)
        sheet.paste(im.resize((tw, th), Image.NEAREST), (x, y))
    f = out / "contact.png"
    sheet.save(f)
    return f


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    force = "--force" in argv
    only = None
    if "--only" in argv:
        only = argv[argv.index("--only") + 1]
    names = [only] if only else list(ALL)
    out = OUT / "full"
    out.mkdir(parents=True, exist_ok=True)

    if "--contact" in argv:
        rows = json.loads((out / "report.json").read_text(encoding="utf-8"))
        print(contact(rows["scenes"], out))
        return 0

    rows = []
    for i, nm in enumerate(names, 1):
        print(f"[{i}/{len(names)}] {nm} ...", flush=True)
        r = one(nm, out=out, force=force)
        rows.append(r)
        print(f"    {r['colours']}/{BUDGET} colours, "
              f"{len(r['layers'])} layers, seam {r['seam_ratio']}")

    f = contact(rows, out)
    report = {"canvas": [W, H], "budget": BUDGET, "licence": LICENCE,
              "scenes": rows}
    (out / "report.json").write_text(json.dumps(report, indent=2),
                                     encoding="utf-8")
    print(f"\n{len(rows)} scenes -> {out}")
    if f:
        print(f"contact sheet -> {f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
