"""The ten. Each one is a function of nothing, returning (Scene, bands).

WHAT MAKES THESE TEN RATHER THAN ONE WITH TEN PALETTES

The cheap way to fill a pack is to build one stack of ridges and recolour it,
and it is obvious in the preview grid - ten thumbnails with the same silhouette
in different hues. So the axis that varies here is SHAPE, and the palette
follows it rather than carrying it:

    cairn     sharp ridged multifractal, high amplitude      peaks
    hollow    low amplitude, canopy metaballs at four depths belts
    mesa      near-zero octave gain, wide blocks             plateaus
    leeward   one hard flat plane against broken rock        a line
    sodium    stepped skyline, lit windows                   rectangles
    flue      stepped skyline, sparse and tall, smoke        chimneys
    kiln      ridged with heavy warp, ember light from below cones
    tundra    almost flat, very low sun, aurora              a horizon
    canopy    stacked round crowns, no visible ground        mounds
    downs     smooth non-ridged noise, wide and soft         curves

Two of them - `leeward` and `tundra` - are mostly empty on purpose. A pack of
ten busy backgrounds has nothing to put behind a dialogue box, and the quiet
ones are the ones that get used most and screenshotted least.

WHY NONE OF THEM DECLARES A `focus`

`Scene.focus` is a claim that one body carries the frame's detail and
everything else is held flat, and `detail.audit` holds the finished picture to
it. `projects/furlong` makes that claim and it is the whole point of that
scene.

None of these do, and setting one anyway would have been a lie the checker
catches immediately: in every scene here the SKY holds more steps than any
landform, because the sky is half the frame, it is a gradient, and a gradient
needs twelve to fifteen steps to dither smoothly instead of banding. That is
the right way to spend the palette on a background and the wrong shape for a
subject claim.

These are depth compositions. What carries them is the ladder of veils from the
far plane to the foreground, not one busy body against nine quiet ones - so the
honest declaration is no declaration, and `detail.audit` stays quiet rather
than inventing a subject the scene was not built around.

WHY THE SUN IS ALWAYS ON THE SAME SIDE

Left, in every scene, at roughly the same height. Not a stylistic tic: a buyer
placing two of these in one game has sprites lit from one direction, and a
background lit from the other side puts every character in the game in conflict
with the scenery behind them. It is the single most expensive thing to get
wrong across a pack and the cheapest to agree on in advance.
"""
from __future__ import annotations

import numpy as np

from boneglass import scenery as sc

from .pack import CUMULUS, H, W, Look, cumulus, four, plane, ridge, scene

# Light from the left, a little above the horizon, in all ten. See the module
# docstring - this is the pack's one non-negotiable.
SUN = (0.18, 0.12)


# ===================================================================== cairn
def cairn():
    """Alpine peaks: three ranges receding into cold air, and a snowfield.

    The whole scene is one parameter used properly. `weighting` is Musgrave's
    multifractal term - an octave multiplied by what the octaves below it
    produced - so detail lands on ground that is already high and the valleys
    stay smooth. That is what real ranges do, and without it every part of the
    silhouette is equally busy, which is the tell of noise used raw. Here the
    far range has the most of it and the near one the least, because the far
    range is all peaks and the near one is the shoulder of a single mountain.
    """
    look = Look(zenith=(46, 92, 164), horizon=(196, 210, 222), gamma=2.2,
                extinction=1.45, sun=SUN, bloom=(0.18, 0.20), bloom_gain=0.24)
    planes = [
        # Depth is spread so that the veil lands at roughly 0.7 / 0.5 / 0.25 /
        # 0.05. The first build ran extinction at 2.6 and put the back range at
        # depth 0.95, which is a veil of 0.92 - the range was drawn, correctly,
        # and was 92% sky. Two mountains disappeared and the picture read as
        # one mountain in fog, which is a composition nobody chose.
        # SHARPNESS BELOW 1 AND A HIGH GAIN, WHICH IS BACKWARDS AND IS RIGHT.
        #
        # `sharpness` raises the folded octave to a power, so above 1 it
        # narrows every crest - and with `weighting` on top of it the profile
        # spends most of its width on the floor with isolated spikes standing
        # out of it. That is a picture of stalagmites. Below 1 the crests
        # broaden into massifs, and the jaggedness that makes them mountains
        # comes from `gain` keeping energy in the fine octaves instead.
        plane("skyline", 0.62,
              # Four octaves, not five: at freq 6 the fifth lands on a 4px
              # wavelength, and `scenery.check` is right that below about six
              # a ridge stops being terrain and becomes hair on the skyline.
              ridge(base=0.44, amp=0.115, freq=6, seed=21, octaves=4,
                    ridged=True, sharpness=0.80, gain=0.58, warp=0.25,
                    warp_freq=0.5),
              (104, 124, 156), 4, relief=0.20, relief_freq=16, fall=0.16,
              slope=0.55, dither=0.6),
        plane("range", 0.34,
              ridge(base=0.575, amp=0.10, freq=6, seed=34, octaves=4,
                    ridged=True, sharpness=0.75, gain=0.58, warp=0.25,
                    warp_freq=0.5),
              (82, 100, 128), 5, relief=0.30, relief_freq=16, fall=0.24,
              slope=0.60, dither=0.55),
        plane("crag", 0.12,
              ridge(base=0.715, amp=0.075, freq=4, seed=47, octaves=5,
                    ridged=True, sharpness=0.75, gain=0.55, warp=0.25,
                    warp_freq=0.5),
              (60, 66, 80), 6, relief=0.38, relief_freq=16, fall=0.28,
              slope=0.55, grain=0.03, grain_freq=64, dither=0.5),
        plane("snow", 0.03,
              ridge(base=0.885, amp=0.035, freq=2, seed=58, octaves=3,
                    ridged=False),
              # Snow in the open is not white, it is the sky's colour lying
              # down. Painted at 240 it quantizes to the palette's top entry
              # across the whole foreground and the scene ends in a blank slab
              # - the one part of the frame nearest the viewer carrying the
              # least information in it.
              (176, 188, 210), 5, relief=0.30, relief_freq=16, fall=0.30,
              slope=0.40, wash=0.12, grain=0.025, grain_freq=64, dither=0.6),
    ]
    s = scene(look, planes, horizon=0.50, focus="", sky_bands=3,
              sky_steps=4, tile_x=True)
    return s, four(s, sky=(), far=("skyline",), mid=("range",),
                   near=("crag", "snow"))


# ==================================================================== hollow
def hollow():
    """A conifer valley in mist: four belts of trees, each paler than the last.

    The strongest parallax scene in the pack and the simplest, because it is
    the one where the depth is carried ENTIRELY by the air. Four belts of the
    same colour at four distances, and Koschmieder does the rest - the far belt
    is nearly the sky and the near one is nearly black, from one albedo.

    The trees are `groves`: the cloud metaball field with the flat base
    switched off, which is why there is no second copy of that code to keep in
    step. A cumulus and a canopy differ by one boolean and nothing else.
    """
    look = Look(zenith=(126, 152, 168), horizon=(206, 214, 212), gamma=1.6,
                extinction=2.1, sun=SUN, bloom=(0.20, 0.16), bloom_gain=0.22)

    def belt(name, depth, y, n, w, h, seed, steps):
        # Crowns strung across the frame at an even spacing with a hashed
        # wobble. Even spacing alone is a comb; pure random gives clumps with
        # bald patches between them, and a treeline with a gap in it reads as
        # two treelines.
        cl = []
        for i in range(n):
            j = float(sc._hash(np.int64(i), np.int64(seed), 91))
            cl.append(sc.Cloud(x=(i + 0.5) / n + (j - 0.5) * 0.35 / n,
                               y=y, w=w, h=h * (0.7 + 0.6 * j),
                               puffs=3, seed=seed * 31 + i))
        # SOFTNESS DOWN AND THRESHOLD UP, WHICH IS WHAT MAKES IT A WOOD.
        #
        # `softness` is the puff falloff and `threshold` the iso-level the
        # field is cut at. Fluffy puffs cut low merge into one mass with a
        # smooth top - the first build of this scene was three green hills,
        # correctly rendered, with no tree anywhere in it. Tight puffs cut high
        # leave the crowns just touching, and the bumpy line along the top is
        # the entire difference between a treeline and a hill.
        return sc.Deck(name=name, depth=depth, clouds=tuple(cl),
                       colour=(46, 66, 54), steps=steps, flat_base=False,
                       ambient=0.72, light=0.7, base_shade=0.5,
                       softness=1.15, threshold=0.58, dither=0.45)

    planes = [
        plane("fog", 0.62,
              ridge(base=0.58, amp=0.03, freq=4, seed=12, octaves=3,
                    ridged=False),
              (176, 190, 190), 3, relief=0.0, fall=0.10, slope=0.15,
              dither=0.7),
        # EVERY BELT STANDS ON A SLOPE OF ITS OWN, and that is not decoration.
        #
        # A grove is a row of crowns with gaps between them, and whatever is
        # behind shows through the gaps. Behind them was `fog`, the palest
        # thing in the scene, so each gap came out as a hard white blob -
        # reading as snow patches, or as water, or as nothing identifiable.
        # Placed at the belt's own depth, the slope takes the belt's own veil,
        # so the gaps show ground receding at the right distance instead.
        # 0.60 rather than the belt's 0.62: near enough that the slope and the
        # trees on it take the same veil, far enough that the paint order is
        # DETERMINED. Two planes at one depth sort arbitrarily, and which one
        # ends up in front is then a property of the sort's stability rather
        # than of the picture.
        plane("far_slope", 0.60,
              ridge(base=0.645, amp=0.022, freq=3, seed=76, octaves=3,
                    ridged=False),
              (92, 108, 92), 3, relief=0.08, relief_freq=8, fall=0.14,
              slope=0.25, dither=0.6),
        plane("mid_slope", 0.33,
              ridge(base=0.740, amp=0.026, freq=3, seed=88, octaves=3,
                    ridged=False),
              (74, 92, 72), 3, relief=0.10, relief_freq=8, fall=0.18,
              slope=0.30, dither=0.55),
        plane("floor", 0.06,
              ridge(base=0.870, amp=0.022, freq=2, seed=64, octaves=3,
                    ridged=False),
              (58, 72, 56), 4, relief=0.12, relief_freq=8, fall=0.24,
              grain=0.05, grain_freq=48, dither=0.5),
    ]
    s = scene(look, planes, horizon=0.56, focus="", sky_bands=3,
              sky_steps=4, tile_x=True,
              groves=(belt("far_belt", 0.62, 0.625, 32, 0.017, 0.030, 5, 3),
                      belt("mid_belt", 0.34, 0.715, 24, 0.023, 0.046, 9, 3),
                      belt("near_belt", 0.12, 0.845, 17, 0.032, 0.070, 13, 5)))
    return s, four(s, sky=(), far=("fog", "far_slope", "far_belt"),
                   mid=("mid_slope", "mid_belt"),
                   near=("near_belt", "floor"))


# ====================================================================== mesa
def mesa():
    """Desert badlands: flat-topped plateaus, warm dust, a low sun.

    Plateaus are the same stepped profile a city skyline uses, and that is not
    a coincidence or a reuse hack - a mesa IS a flat top with a cliff either
    side, and the thing that makes it read as rock rather than as architecture
    is the block count and the relief inside it. Twelve wide blocks with heavy
    interior relief is a butte; forty narrow ones with none is a tower block.
    """
    look = Look(zenith=(96, 132, 186), horizon=(230, 202, 166), gamma=2.4,
                extinction=1.6, sun=SUN, bloom=(0.16, 0.22), bloom_gain=0.30,
                bloom_rgb=(1.0, 0.90, 0.72))
    planes = [
        plane("far_mesa", 0.62,
              sc.Ridge(base=0.52, amp=0.10, freq=3, octaves=4, ridged=False,
                       seed=71, tile=True, blocks=9, block_jitter=0.55,
                       block_gap=0.10),
              (176, 152, 140), 4, relief=0.16, relief_freq=8, fall=0.16,
              slope=0.30, dither=0.6),
        plane("butte", 0.34,
              sc.Ridge(base=0.64, amp=0.14, freq=4, octaves=4, ridged=False,
                       seed=83, tile=True, blocks=12, block_jitter=0.6,
                       block_gap=0.16),
              (162, 112, 86), 5, relief=0.34, relief_freq=16, fall=0.28,
              slope=0.45, grain=0.03, grain_freq=64, dither=0.5),
        plane("scree", 0.12,
              ridge(base=0.78, amp=0.06, freq=6, seed=95, octaves=4,
                    ridged=True, weighting=0.3),
              (128, 84, 62), 5, relief=0.26, relief_freq=16, fall=0.26,
              grain=0.05, grain_freq=64, dither=0.5),
        plane("sand", 0.03,
              ridge(base=0.90, amp=0.03, freq=2, seed=107, octaves=3,
                    ridged=False),
              (196, 158, 116), 4, relief=0.10, relief_freq=8, fall=0.18,
              wash=0.12, grain=0.03, grain_freq=48, dither=0.6),
    ]
    s = scene(look, planes, horizon=0.52, focus="", sky_bands=3,
              sky_steps=4, tile_x=True)
    return s, four(s, sky=(), far=("far_mesa",), mid=("butte",),
                   near=("scree", "sand"))


# =================================================================== leeward
def leeward():
    """Cliffs over open sea. Two thirds of the frame is one flat colour.

    The quietest thing in the pack and the hardest to get right, because there
    is nothing in it to hide behind. The sea is a plane with a dead-flat ridge
    and almost no relief, which quantizes to three or four bands of blue - and
    those bands ARE the picture. Give it grain and it turns to television
    static; give it more steps and the bands stop being bands.
    """
    look = Look(zenith=(70, 128, 190), horizon=(196, 216, 226), gamma=2.0,
                extinction=1.7, sun=SUN, bloom=(0.16, 0.18), bloom_gain=0.26)
    planes = [
        plane("headland", 0.62,
              ridge(base=0.535, amp=0.045, freq=3, seed=131, octaves=4,
                    ridged=True, weighting=0.4, warp=0.30, warp_freq=1.0),
              (128, 142, 148), 3, relief=0.14, relief_freq=8, fall=0.14,
              slope=0.40, dither=0.55),
        plane("sea", 0.22,
              # Dead flat. `amp` is not zero because a sea horizon that is
              # mathematically level quantizes to a ruled line one pixel high,
              # and the eye reads a ruled line as a border rather than as water.
              ridge(base=0.585, amp=0.004, freq=2, seed=143, octaves=2,
                    ridged=False),
              (58, 96, 128), 4, relief=0.05, relief_freq=4, fall=0.30,
              slope=0.0, grain=0.0, wash=0.14, dither=0.75),
        plane("cliff", 0.05,
              ridge(base=0.80, amp=0.09, freq=4, seed=157, octaves=5,
                    ridged=True, sharpness=1.2, weighting=0.5, warp=0.25,
                    warp_freq=0.5),
              (76, 78, 74), 6, relief=0.40, relief_freq=16, fall=0.32,
              slope=0.55, grain=0.04, grain_freq=64, dither=0.45),
    ]
    cl = tuple(cumulus((i + 0.5) / 4, 0.320, 0.108, ratio=0.50, puffs=5,
                       seed=200 + i * 7) for i in range(4))
    s = scene(look, planes, horizon=0.54, focus="", sky_bands=3,
              sky_steps=4, tile_x=True,
              decks=(sc.Deck(name="cumulus", depth=0.34, clouds=cl,
                             colour=(248, 248, 246), steps=4, **CUMULUS),))
    return s, four(s, sky=("cumulus",), far=("headland",), mid=("sea",),
                   near=("cliff",))


# =================================================================== sodium
def sodium():
    """A city after dark: three depths of tower, and the lights on in them.

    The windows are a SHADING term on the wall rather than a part of their own,
    so a lit window takes its colour from the wall's ramp with the light on. As
    a separate part they would each need their own budget share, and the four
    or five entries that would cost is a quarter of the palette spent on
    something that is already expressible as "this wall, brighter".

    Which windows are lit is hashed off the cell, so it is stable between runs
    and between the 1x and the 3x - a city whose lights move when you rescale
    it is a city nobody can composite anything onto.
    """
    look = Look(zenith=(10, 12, 30), horizon=(74, 62, 92), gamma=3.0,
                extinction=1.9, sun=(0.18, 0.30),
                bloom=(0.20, 0.66), bloom_gain=0.30,
                bloom_rgb=(1.0, 0.66, 0.40), bloom_reach=0.46)
    planes = [
        plane("skyline", 0.62,
              sc.Ridge(base=0.50, amp=0.16, freq=3, octaves=4, ridged=False,
                       seed=211, tile=True, blocks=48, block_jitter=0.7,
                       block_gap=0.08),
              (52, 54, 78), 3, relief=0.0, fall=0.10, slope=0.0,
              windows=0.55, window_cols=192, window_rows=108,
              window_lit=0.14, dither=0.5),
        plane("blocks", 0.34,
              sc.Ridge(base=0.62, amp=0.18, freq=4, octaves=4, ridged=False,
                       seed=223, tile=True, blocks=32, block_jitter=0.6,
                       block_gap=0.12),
              (38, 38, 58), 4, relief=0.0, fall=0.14, slope=0.0,
              windows=0.85, window_cols=128, window_rows=72,
              window_lit=0.18, dither=0.45),
        plane("near_towers", 0.10,
              sc.Ridge(base=0.80, amp=0.20, freq=2, octaves=3, ridged=False,
                       seed=239, tile=True, blocks=16, block_jitter=0.5,
                       block_gap=0.18),
              (20, 20, 32), 5, relief=0.0, fall=0.12, slope=0.0,
              windows=1.30, window_cols=64, window_rows=36,
              window_lit=0.22, dither=0.4),
    ]
    s = scene(look, planes, horizon=0.56, focus="", sky_bands=3,
              sky_steps=5, tile_x=True)
    return s, four(s, sky=(), far=("skyline",), mid=("blocks",),
                   near=("near_towers",))


# ===================================================================== flue
def flue():
    """Chimneys and gasholders under a sodium sky, with the smoke going over.

    The same stepped profile as `sodium` and a completely different picture,
    from two numbers: the blocks are far fewer and the amplitude is far higher,
    so the silhouette is a handful of tall thin things instead of a mass with a
    texture. That is the difference between a skyline and a works, and it is
    worth knowing it is only two numbers - it is why this pack has ten shapes
    and not ten palettes.
    """
    look = Look(zenith=(72, 76, 106), horizon=(212, 156, 104), gamma=2.3,
                extinction=1.8, sun=SUN, bloom=(0.16, 0.28), bloom_gain=0.32,
                bloom_rgb=(1.0, 0.82, 0.56), bloom_reach=0.60)
    # A BANK, NOT A SCATTER, and `Deck.bank` is the flag that says which.
    #
    # Evenly spaced separate masses came out as a row of identical discs - the
    # failure `scenery.check` calls a scatter with no silhouette, arrived at
    # from the other direction. Smoke over a works is one continuous layer
    # whose identity is its RAGGED UNDERSIDE, so the puffs are deliberately
    # overlapped and varied, and what the eye reads is the outline of the whole
    # mass rather than any cloud in it.
    smoke = tuple(cumulus((i + 0.5) / 11, 0.255 + 0.02 * ((i * 7) % 3),
                          0.115 + 0.02 * ((i * 5) % 3), ratio=0.52, puffs=4,
                          seed=300 + i * 13) for i in range(11))
    planes = [
        plane("works", 0.62,
              sc.Ridge(base=0.54, amp=0.22, freq=2, octaves=3, ridged=False,
                       seed=311, tile=True, blocks=24, block_jitter=0.85,
                       block_gap=0.30),
              (124, 118, 126), 4, relief=0.0, fall=0.14, slope=0.0,
              dither=0.55),
        plane("sheds", 0.34,
              sc.Ridge(base=0.70, amp=0.10, freq=3, octaves=3, ridged=False,
                       seed=323, tile=True, blocks=16, block_jitter=0.5,
                       block_gap=0.14),
              (86, 78, 82), 5, relief=0.0, fall=0.18, slope=0.0,
              windows=0.26, window_cols=96, window_rows=54, window_lit=0.14,
              dither=0.5),
        plane("yard", 0.08,
              ridge(base=0.86, amp=0.03, freq=4, seed=337, octaves=3,
                    ridged=False),
              (54, 48, 50), 5, relief=0.14, relief_freq=8, fall=0.22,
              grain=0.04, grain_freq=64, dither=0.5),
    ]
    s = scene(look, planes, horizon=0.52, focus="", sky_bands=3,
              sky_steps=5, tile_x=True,
              decks=(sc.Deck(name="smoke", depth=0.40, clouds=smoke,
                             colour=(150, 140, 136), steps=4,
                             flat_base=False, bank=True,
                             **dict(CUMULUS, threshold=0.46, softness=1.15,
                                    base_shade=0.26, ambient=0.86)),))
    return s, four(s, sky=("smoke",), far=("works",), mid=("sheds",),
                   near=("yard",))


# ===================================================================== kiln
def kiln():
    """Volcanic ash: cones under a dark sky, lit from BELOW by what is in them.

    The only scene in the pack whose light does not come from the sky, and the
    one place the pack's left-sun rule is answered rather than broken: the sun
    is still nominally left, and the ember light is the `wash` term, which is a
    brightening across the frame rather than a second light with its own
    direction. A genuine second light source would need shading terms that know
    about it, and every buyer's sprite would then be lit wrongly for this one
    background out of ten.
    """
    look = Look(zenith=(28, 24, 34), horizon=(126, 62, 44), gamma=2.8,
                extinction=2.0, sun=(0.20, 0.34),
                bloom=(0.34, 0.58), bloom_gain=0.42,
                bloom_rgb=(1.0, 0.52, 0.26), bloom_reach=0.50)
    ash = tuple(cumulus((i + 0.5) / 9, 0.215 + 0.025 * ((i * 5) % 3),
                        0.130 + 0.025 * ((i * 7) % 3), ratio=0.50, puffs=4,
                        seed=400 + i * 11) for i in range(9))
    planes = [
        plane("cone", 0.62,
              ridge(base=0.52, amp=0.16, freq=2, seed=411, octaves=5,
                    ridged=True, sharpness=1.6, weighting=0.6, warp=0.40,
                    warp_freq=1.0),
              (78, 62, 66), 4, relief=0.20, relief_freq=8, fall=0.16,
              slope=0.45, wash=0.16, dither=0.55),
        plane("flank", 0.34,
              ridge(base=0.68, amp=0.11, freq=4, seed=423, octaves=5,
                    ridged=True, sharpness=1.3, weighting=0.4, warp=0.30,
                    warp_freq=0.5),
              (56, 42, 44), 5, relief=0.34, relief_freq=16, fall=0.24,
              slope=0.40, wash=0.22, grain=0.03, grain_freq=64, dither=0.5),
        plane("ash", 0.06,
              ridge(base=0.84, amp=0.05, freq=4, seed=437, octaves=4,
                    ridged=False),
              (40, 32, 34), 5, relief=0.18, relief_freq=16, fall=0.20,
              wash=0.30, grain=0.05, grain_freq=64, dither=0.5),
    ]
    s = scene(look, planes, horizon=0.50, focus="", sky_bands=3,
              sky_steps=5, tile_x=True,
              decks=(sc.Deck(name="plume", depth=0.42, clouds=ash,
                             colour=(118, 94, 92), steps=4,
                             flat_base=False, bank=True,
                             **dict(CUMULUS, threshold=0.46, softness=1.15,
                                    base_shade=0.26, ambient=0.88)),))
    return s, four(s, sky=("plume",), far=("cone",), mid=("flank",),
                   near=("ash",))


# =================================================================== tundra
def tundra():
    """Frozen moor under a green sky. Almost nothing in it, on purpose.

    The second of the pack's two quiet scenes, and the one most likely to end
    up behind a menu. The aurora is the sky's `bloom` moved off-centre and
    given a cold hue - not a painted ribbon, because a ribbon is a shape and a
    shape in the sky competes with whatever the buyer puts in front of it.
    """
    look = Look(zenith=(20, 34, 62), horizon=(126, 156, 152), gamma=2.4,
                extinction=1.6, sun=(0.22, 0.16),
                bloom=(0.30, 0.24), bloom_gain=0.34,
                bloom_rgb=(0.56, 1.0, 0.78), bloom_reach=0.48)
    planes = [
        plane("hills", 0.62,
              ridge(base=0.585, amp=0.035, freq=3, seed=511, octaves=4,
                    ridged=False, warp=0.25, warp_freq=1.0),
              (74, 88, 108), 3, relief=0.10, relief_freq=8, fall=0.12,
              slope=0.30, dither=0.6),
        plane("moor", 0.30,
              ridge(base=0.70, amp=0.045, freq=4, seed=523, octaves=4,
                    ridged=False),
              (52, 62, 74), 4, relief=0.14, relief_freq=8, fall=0.20,
              slope=0.25, grain=0.03, grain_freq=48, dither=0.55),
        plane("snowfield", 0.04,
              ridge(base=0.855, amp=0.035, freq=2, seed=537, octaves=3,
                    ridged=False),
              (186, 198, 210), 5, relief=0.10, relief_freq=8, fall=0.20,
              slope=0.20, wash=0.14, dither=0.7),
    ]
    s = scene(look, planes, horizon=0.56, focus="", sky_bands=4,
              sky_steps=5, tile_x=True)
    return s, four(s, sky=(), far=("hills",), mid=("moor",),
                   near=("snowfield",))


# =================================================================== canopy
def canopy():
    """Rainforest: crowns on crowns, and no ground visible anywhere.

    The one scene with no ground plane in it. Everything is `groves`, stacked
    until the floor is covered, which is what a rainforest looks like from
    inside it - and it means the near band is a canopy silhouette with holes,
    so the buyer gets a foreground that a character can genuinely walk behind.
    """
    look = Look(zenith=(96, 148, 138), horizon=(198, 214, 176), gamma=1.8,
                extinction=2.1, sun=SUN, bloom=(0.22, 0.14), bloom_gain=0.28,
                bloom_rgb=(0.94, 1.0, 0.78))

    def crowns(name, depth, y, n, w, h, seed, steps, colour):
        cl = []
        for i in range(n):
            j = float(sc._hash(np.int64(i), np.int64(seed), 57))
            # The vertical wobble is SMALL. At 0.05 it is a fifth of the
            # frame height and several times a crown's own diameter, so the
            # crowns scatter up and down until they overlap into one smooth
            # mass - which is what the first build of this scene was: a green
            # dome with no tree in it. The wobble should be a fraction of a
            # crown, not a multiple.
            cl.append(sc.Cloud(x=(i + 0.5) / n + (j - 0.5) * 0.4 / n,
                               y=y + (j - 0.5) * h * 0.35,
                               w=w, h=h * (0.65 + 0.7 * j),
                               puffs=4, seed=seed * 17 + i))
        return sc.Deck(name=name, depth=depth, clouds=tuple(cl), colour=colour,
                       steps=steps, flat_base=False, ambient=0.70, light=0.75,
                       base_shade=0.55, softness=1.7, threshold=0.44,
                       dither=0.45)

    planes = [
        plane("haze", 0.62,
              ridge(base=0.60, amp=0.02, freq=2, seed=611, octaves=3,
                    ridged=False),
              (176, 196, 168), 3, relief=0.0, fall=0.08, slope=0.10,
              dither=0.7),
    ]
    s = scene(look, planes, horizon=0.58, focus="", sky_bands=3,
              sky_steps=4, tile_x=True,
              groves=(crowns("far_crowns", 0.62, 0.660, 24, 0.026, 0.048, 3, 3,
                             (92, 126, 88)),
                      crowns("mid_crowns", 0.34, 0.790, 17, 0.036, 0.074, 7, 4,
                             (58, 94, 60)),
                      crowns("near_crowns", 0.12, 0.985, 11, 0.052, 0.125, 11, 5,
                             (28, 52, 34))))
    return s, four(s, sky=(), far=("haze", "far_crowns"),
                   mid=("mid_crowns",), near=("near_crowns",))


# ==================================================================== downs
def downs():
    """Rolling green hills. The friendliest thing in the pack and the default.

    Non-ridged noise at low frequency, which is the one combination this repo
    usually avoids - it makes soft lumps, and soft lumps are what downland is.
    The scene it is standing in for is `projects/furlong`, which is a better
    picture and cannot be here: its foreground camber is `Ridge.arc`, a
    parabola, and a parabola does not meet itself at the frame edge.
    """
    look = Look(zenith=(64, 130, 202), horizon=(206, 222, 226), gamma=2.1,
                extinction=1.7, sun=SUN, bloom=(0.18, 0.16), bloom_gain=0.26)
    # Small enough to stay separate. A cloud whose width plus its puff radius
    # exceeds the spacing merges with its neighbour, and `scenery.check` calls
    # a merged scatter what it is: a deck with no silhouette.
    cl = tuple(cumulus((i + 0.5) / 5, 0.300, 0.088, ratio=0.52, puffs=5,
                       seed=700 + i * 9) for i in range(5))
    planes = [
        plane("far_downs", 0.62,
              ridge(base=0.575, amp=0.030, freq=3, seed=711, octaves=4,
                    ridged=False, warp=0.20, warp_freq=1.0),
              (140, 164, 150), 3, relief=0.10, relief_freq=8, fall=0.12,
              slope=0.35, dither=0.6),
        plane("hills", 0.34,
              ridge(base=0.66, amp=0.055, freq=4, seed=723, octaves=4,
                    ridged=False, warp=0.25, warp_freq=0.5),
              (108, 148, 92), 5, relief=0.18, relief_freq=8, fall=0.22,
              slope=0.45, grain=0.03, grain_freq=48, dither=0.55),
        plane("pasture", 0.08,
              ridge(base=0.80, amp=0.045, freq=2, seed=737, octaves=3,
                    ridged=False),
              (84, 126, 66), 6, relief=0.16, relief_freq=8, fall=0.26,
              slope=0.40, wash=0.12, grain=0.05, grain_freq=64, dither=0.5),
    ]
    s = scene(look, planes, horizon=0.55, focus="", sky_bands=3,
              sky_steps=5, tile_x=True,
              decks=(sc.Deck(name="cumulus", depth=0.32, clouds=cl,
                             colour=(250, 250, 248), steps=4, **CUMULUS),))
    return s, four(s, sky=("cumulus",), far=("far_downs",), mid=("hills",),
                   near=("pasture",))


# ====================================================================== all
#
# Ordered as the store page should show them: the two most immediately
# striking first, because a visitor decides from the first two thumbnails, and
# the two quiet ones last, because they are the ones that sell on use rather
# than on the screenshot.
ALL = {
    "sodium": sodium,
    "cairn": cairn,
    "hollow": hollow,
    "mesa": mesa,
    "canopy": canopy,
    "flue": flue,
    "kiln": kiln,
    "downs": downs,
    "leeward": leeward,
    "tundra": tundra,
}

# The order matters and it is the store page's, not the build's: a visitor
# decides from the first two thumbnails, so the night city and the peaks go
# first, and the two deliberately empty ones go last - they are the pair that
# get used most and screenshotted least.
