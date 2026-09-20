"""What every scene in the pack agrees about, and why each agreement is there.

A pack of ten backgrounds is not ten backgrounds in a folder. What makes it a
pack is that a buyer can put any two of them in the same game and not have to
retouch either one, and that is a property of the CONVENTIONS, not of the art.
Each of the four below is a thing that, left to each scene's own judgement,
produces ten files that are individually fine and unusable together.

CANVAS: 384 x 216

    Because 384 x 5 = 1920 and 216 x 5 = 1080, exactly. A pixel-art background
    is displayed at an integer multiple or it is displayed with some pixels
    bigger than others, and there is no third option that anyone will accept.
    480 x 270 also divides 1080p (x4) and is the other defensible choice; 384
    wins because it is also 16:9 at a size where a hand-authored ridge still
    reads, and because 3x lands on 1152 x 648 for a windowed preview.

    Every scene is this size. A pack where one background is 320 wide is a pack
    where one background needs its own camera setup.

BUDGET: 36 colours

    Per scene, shared across that scene's layers - the whole point of the
    single quantize in `parallax.render`. Chosen against what the layers have
    to do rather than for a round number: a sky needs twelve to fifteen steps
    across three or four bands to dither smoothly over half a frame, and that
    leaves about twenty-two for four or five bodies - four each, with a few
    spare for whichever one the scene declares as its subject.

    It was 32, which is the number one reaches for, and three of the ten came
    out asking for 33. `allocate_steps` does not fail on that: it quietly
    shaves the smallest parts, and the smallest part is never the sky - it is
    the foreground detail the scene was built around. Four colours is a much
    cheaper thing to spend than the subject of three backgrounds.

    At 16 the sky bands. Past about 48 the dithering stops being visible and
    the pack stops reading as pixel art, which is what it is being bought for.

HORIZON: 0.52 to 0.58

    Not identical - a scene needs its own composition - but inside one band, so
    two backgrounds cross-faded or used in adjacent rooms do not appear to tilt
    the world. The camera is the thing the buyer holds fixed; the horizon is
    what tells them where it is.

TILING: every plane, every scene

    Not a feature some scenes have. A pack advertised as scrollable in which
    two backgrounds do not loop is a pack with a bug report attached, and the
    buyer finds out at the point where they have already built the level.

    It costs the non-periodic shaping terms - `tilt`, `arc`, `dome` - which is a
    real loss: `arc` is what gives a foreground its camber and `dome` is what
    puts a hill under a town. Those scenes are the ones in `projects/furlong`
    and `projects/simiane`, they are the better pictures, and they are not in
    this pack because they cannot be scrolled. The trade is deliberate and it
    is the right way round for something sold to be built on.
"""
from __future__ import annotations

import dataclasses
from dataclasses import dataclass

from boneglass import atmosphere as atm
from boneglass import scenery as sc
from boneglass.pipeline import Params

W, H = 384, 216
BUDGET = 36
ZOOM = 3                      # 1152 x 648, a legible preview at 1x on any page

# Far to near. The numbers are the fraction of camera motion each layer takes,
# and they are the same four in every scene so a buyer can wire one camera rig
# and drop any of the ten into it.
#
# 0.0 for the sky, because a sky that moves is a gradient that moves, and the
# horizon slides off the frame taking with it the one thing every other layer
# is measured against. Real skies do move, very slowly, and the buyer can set
# 0.02 if they want it - what they cannot easily do is take motion OUT of a
# layer that was authored with it baked in.
SCROLL = {"sky": 0.00, "far": 0.20, "mid": 0.40, "near": 0.80}

# WHY THOSE FOUR AND NOT ANY FOUR THAT LOOK RIGHT
#
# They are 0 : 1 : 2 : 4. That ratio is not cosmetic - it is what makes the
# whole scene return to its start.
#
# A layer repeats when its own offset has moved a whole frame width, so the
# PICTURE repeats only when every layer has, together. With the mid layer at
# 0.45 the camera has to travel twenty screens before that happens, which means
# no preview of it can loop and a level built on it never quite repeats either.
# At 0.40 every factor divides 0.80, the set closes after five screen widths,
# and a promo GIF of it is a real loop rather than a clip that cuts.
#
# The cost is that the mid layer moves slightly slower than the depth ladder
# would strictly imply. Nobody can see that. Everybody can see a jump.
LOOP_WIDTHS = 5           # screen widths of camera travel per full repeat

# HOW FAR AWAY EACH BAND STANDS, AND WHY IT IS NOT 0.9 FOR THE FAR ONE.
#
# `depth` feeds Koschmieder: the share of a body that is airlight rather than
# body is 1 - e^(-k*d). That is an exponential, and the intuition it defeats is
# that "far away" should be near 1.0 - at k = 2 and d = 0.9 the far plane is
# 83% sky, and at k = 3 it is 93%. It is still being drawn, correctly, and it
# is gone.
#
# Nine of the first ten scenes here were built that way and nine of them lost
# their back plane. Every one looked like a deliberate choice: the picture is
# simply hazier than intended, with nothing in it to say a mountain range had
# been authored and erased.
#
# So the ladder is fixed and the extinction varies instead. At k = 2 these give
# veils of about 0.71 / 0.49 / 0.21 / 0.06 - a far plane that is mostly air and
# still legibly a shape, and a foreground that is essentially unveiled.
DEPTH = {"far": 0.62, "mid": 0.34, "near": 0.12, "fore": 0.03}

# The band that still reads. Past this a body is more than four fifths air, and
# `veil_check` says so before the render rather than after.
MAX_VEIL = 0.80


def veil_check(look: "Look", planes) -> list[str]:
    """Which bodies this scene's air is about to erase."""
    import numpy as np
    out = []
    for pl in planes:
        v = 1.0 - float(np.exp(-look.extinction * pl.depth * pl.haze))
        if v > MAX_VEIL:
            out.append(f"{pl.name}: depth {pl.depth} at extinction "
                       f"{look.extinction} is {v:.0%} airlight - it will be "
                       f"drawn and will not be visible")
    return out


def params(budget: int = BUDGET) -> Params:
    return Params(
        budget=budget,
        max_steps=6,
        iterations=14,
        # Off, both of them, and for the reason `projects/furlong` documents:
        # the scenes are dithered end to end, and despeckle's rule is "recolour
        # any pixel all of whose neighbours disagree", which is the definition
        # of a dithered pixel. It would delete every gradient in the pack and
        # report it as tens of thousands of successful fixes.
        despeckle=False,
        smooth=False,
        outline="none",
        colour_regions=0,
    )


@dataclass(frozen=True)
class Look:
    """A scene's light: the sky it happens under, and the air it is seen through.

    Held together in one object because they are not independent. `Sky.air()`
    derives the haze from the horizon colour, and the one build where those
    were separate values put the furthest ridge in front of the sky as a
    visibly different grey - immediately wrong, and impossible to attribute to
    either number alone.
    """
    zenith: tuple
    horizon: tuple
    gamma: float = 1.9
    extinction: float = 2.0
    sun: tuple = (0.24, 0.10)         # where the light comes from
    bloom: tuple | None = None        # where the sky is bright, if anywhere
    bloom_rgb: tuple = (1.0, 0.96, 0.86)
    bloom_gain: float = 0.30
    bloom_reach: float = 0.55

    def sky(self) -> atm.Sky:
        return atm.Sky(zenith=self.zenith, horizon=self.horizon,
                       gamma=self.gamma, sun=self.bloom,
                       sun_rgb=self.bloom_rgb, sun_gain=self.bloom_gain,
                       sun_reach=self.bloom_reach)

    def air(self) -> atm.Air:
        return self.sky().air(self.extinction)


def ridge(*, base: float, amp: float, freq: int, seed: int, octaves: int = 5,
          ridged: bool = True, sharpness: float = 1.0, weighting: float = 0.0,
          gain: float = 0.5, warp: float = 0.0, warp_freq: float = 0.5,
          lacunarity: float = 2.0) -> sc.Ridge:
    """A tiling ridge. `freq` and `warp_freq * freq` must be whole.

    This wrapper exists so no scene in the pack can author a non-tiling ridge
    by forgetting a keyword. `tile=True` is not a default on `Ridge` itself
    because most of this repo's scenes are single frames that should not pay
    for a constraint they do not use.
    """
    r = sc.Ridge(base=base, amp=amp, freq=freq, octaves=octaves,
                 lacunarity=lacunarity, gain=gain, ridged=ridged,
                 sharpness=sharpness, weighting=weighting, warp=warp,
                 warp_freq=warp_freq, seed=seed, tile=True)
    bad = r.tiling_issues()
    if bad:
        raise ValueError(f"this ridge does not loop: {bad}")
    return r


def plane(name: str, depth: float, r: sc.Ridge, colour: tuple, steps: int,
          **kw) -> sc.Plane:
    """A plane with the pack's texture frequencies rounded to whole cycles.

    `relief_freq` and `grain_freq` are lattice frequencies exactly as a ridge's
    `freq` is, so a fractional one does not close either - and unlike the
    silhouette, a texture that does not close is easy to miss in a still and
    impossible to miss once it scrolls.
    """
    for k in ("relief_freq", "grain_freq"):
        if k in kw:
            kw[k] = float(round(kw[k]))
    return sc.Plane(name=name, depth=depth, ridge=r, colour=colour,
                    steps=steps, **kw)


def cumulus(x: float, y: float, w: float, *, ratio: float = 0.52,
            puffs: int = 5, seed: int = 0) -> sc.Cloud:
    """A cloud whose height is stated as a fraction of its own WIDTH.

    `Cloud.w` is a fraction of the canvas width and `Cloud.h` a fraction of its
    HEIGHT, so on a 16:9 frame the same number means 384 pixels in one and 216
    in the other. Authoring both by eye gives a cloud with a pixel aspect of
    1.78 to 1 flatter than intended - which is not read as "a slightly flat
    cloud", it is read as a grey lozenge, because the puff radius is driven by
    the height and a short height makes a row of small discs on a long base.

    `projects/furlong` is square, so the two are the same pixels there and the
    factor could be left out without anything looking wrong. It was, and then
    the numbers were carried over to a 16:9 pack, and every cloud in four
    scenes came out as a kidney.

    `ratio` is the height in units of the width, IN PIXELS. About half is a
    fair-weather cumulus.
    """
    return sc.Cloud(x=x, y=y, w=w, h=w * (W / H) * ratio, puffs=puffs,
                    seed=seed)


# What `projects/furlong` settled on, which is the one deck in this repo that
# has been looked at hard. Copied as a block rather than re-derived: these
# numbers interact, and picking three of the six is how a cloud ends up lit
# from inside.
CUMULUS = dict(ramp="soft", threshold=0.52, softness=1.30, ambient=0.84,
               light=0.78, base_shade=0.34, base_band=0.020, dither=0.45)


def scene(look: Look, planes, *, horizon: float = 0.55, **kw) -> sc.Scene:
    bad = veil_check(look, planes)
    if bad:
        raise ValueError("this scene's air erases what it is made of:\n  "
                         + "\n  ".join(bad))
    s = sc.Scene(w=W, h=H, sky=look.sky(), air=look.air(), horizon=horizon,
                 sun=look.sun, planes=tuple(planes), ss=2, **kw)
    return s


def four(scene_, sky=(), far=(), mid=(), near=()):
    """The pack's standard four bands, by body name."""
    from boneglass import parallax as px
    return px.assign(scene_, [
        ("sky", SCROLL["sky"], tuple(sky)),
        ("far", SCROLL["far"], tuple(far)),
        ("mid", SCROLL["mid"], tuple(mid)),
        ("near", SCROLL["near"], tuple(near)),
    ])


def retune(s: sc.Scene, **kw) -> sc.Scene:
    return dataclasses.replace(s, **kw)
