import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.axes
import numpy as np
from matplotlib import font_manager
from os.path import join, dirname, realpath
from typing import Union, List


def make_subplots(
    ncols=1,
    nrows=1,
    axes_w=8,
    axes_h_to_w=1 / 1.618,
    wspace=None,
    hspace=None,
    **subplots_kwargs
):
    box_aspect = axes_h_to_w
    h = box_aspect * axes_w
    fig, axes = plt.subplots(
        figsize=(ncols * axes_w, nrows * h),
        ncols=ncols,
        nrows=nrows,
        subplot_kw=dict(box_aspect=box_aspect),
        **subplots_kwargs
    )
    fig.subplots_adjust(wspace=wspace, hspace=hspace)

    if isinstance(axes, mpl.axes.Axes):
        axes = np.array([[axes]])

    return fig, axes


def load_custom_fonts(fontpaths, verbose=False):
    # fontpaths is a list of directories where your .ttf files are stored
    font_files = font_manager.findSystemFonts(fontpaths=fontpaths)

    for font_file in font_files:
        font_manager.fontManager.addfont(font_file)

    # check that the font is loaded
    if verbose:
        print(font_manager.fontManager.ttflist)

    mpl.rcParams["text.usetex"] = False  # make sure usetex is off


def set_global_font(fontname, fontpaths=None, verbose=False):
    if fontpaths is None:
        fontpaths = []
        load_custom_fonts(fontpaths, verbose)

    mpl.rcParams["font.family"] = fontname


def use_latex(font=False):
    mpl.rcParams["text.usetex"] = True
    mpl.rcParams["mathtext.fontset"] = "cm"
    if font:
        mpl.rcParams["font.family"] = "STIXGeneral"


STYLE_DIR = realpath(join(dirname(__file__), "styles"))
COMMON = "common.mplstyle"


def use_style(style=None, palette=None):
    """Some of the tick properties cannot be set using ``plt.style.use``."""
    styles = [COMMON] if style is None else [COMMON, style + ".mplstyle"]
    plt.style.use(join(STYLE_DIR, s) for s in styles)

    if palette is not None:
        set_palette(palette)


PALETTES = {
    "tianyi": [
        "#1d437d",
        "#ee442f",
        "#0099ad",
        "#dec923",
        "#a95aa1",
        "#f78f1e",
        "#ccbe9f",
        "#29562a",
        "#99cc83",
    ],
    "bmh": [
        "#348ABD",
        "#A60628",
        "#7A68A6",
        "#467821",
        "#D55E00",
        "#CC79A7",
        "#56B4E9",
        "#009E73",
        "#F0E442",
        "#0072B2",
    ],
    "solarized-light": [
        "#268BD2",
        "#2AA198",
        "#859900",
        "#B58900",
        "#CB4B16",
        "#DC322F",
        "#D33682",
        "#6C71C4",
    ],
    "fivethirtyeight": [
        "#008fd5",
        "#fc4f30",
        "#e5ae38",
        "#6d904f",
        "#8b8b8b",
        "#810f7c",
    ],
    "ggplot": [
        "#E24A33",
        "#348ABD",
        "#988ED5",
        "#777777",
        "#FBC15E",
        "#8EBA42",
        "#FFB5B8",
    ],
    "degas-high-contrast": [
        [0.372549, 0.596078, 1],
        [1.0, 0.3882, 0.2784],
        [0.20784314, 0.67843137, 0.6],
        [0.59607843, 0.25882353, 0.89019608],
        [0.803922, 0.0627451, 0.462745],
        [0.917647, 0.682353, 0.105882],
        [0.7, 0.7, 0.7],
    ],
    "degas-pastel-rainbow": np.array(
        [
            [221, 59, 53],
            [211, 132, 71],
            [237, 157, 63],
            [165, 180, 133],
            [63, 148, 109],
            [50, 122, 137],
            [44, 115, 178],
            [43, 52, 124],
        ]
    )
    / 255.0,
}


def get_palette(palette_name):
    return PALETTES[palette_name]


def set_palette(palette: Union[str, List[str]]):
    if isinstance(palette, str):
        palette = get_palette(palette)

    from cycler import cycler
    from matplotlib import pyplot as plt

    plt.rcParams["axes.prop_cycle"] = cycler("color", palette)


# From  https://github.com/williamgilpin/degas/blob/master/degas/degas.py
def lighten(clr, f=1 / 3):
    """
    An implementation of Mathematica's Lighter[]
    function for RGB colors
    clr : 3-tuple or list, an RGB color
    f : float, the fraction by which to brighten
    """
    gaps = [f * (1 - val) for val in clr]
    new_clr = [val + gap for gap, val in zip(gaps, clr)]
    return new_clr


def darken(clr, f=1 / 3):
    """
    An implementation of Mathematica's Darker[]
    function for RGB colors
    clr : 3-tuple or list, an RGB color
    f : float, the fraction by which to brighten
    """
    gaps = [f * val for val in clr]
    new_clr = [val - gap for gap, val in zip(gaps, clr)]
    return new_clr


def reset_global_style():
    plt.style.use("default")


def color_ticks(ax, color=None, axis="both", which="both"):
    if color is None:
        color = mpl.rcParams["grid.color"]
    ax.tick_params(color=color, axis=axis, which=which)


# From  https://github.com/williamgilpin/degas/blob/master/degas/degas.py
def lighten_color(color, f=1 / 3):
    """
    An implementation of Mathematica's Lighter[]
    function for RGB colors
    clr : 3-tuple or list, an RGB color
    f : float, the fraction by which to brighten
    """
    gaps = [f * (1 - val) for val in color]
    new_clr = [val + gap for gap, val in zip(gaps, color)]
    return new_clr


def darken_color(color, f=1 / 3):
    """
    An implementation of Mathematica's Darker[]
    function for RGB colors
    clr : 3-tuple or list, an RGB color
    f : float, the fraction by which to brighten
    """
    gaps = [f * val for val in color]
    new_clr = [val - gap for gap, val in zip(gaps, color)]
    return new_clr


def lighten_palette(palette, f=1 / 3):
    return [lighten_color(p, f=f) for p in palette]


def darken_palette(palette, f=1 / 3):
    return [darken_color(p, f=f) for p in palette]
