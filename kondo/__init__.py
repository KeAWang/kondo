import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.axes
import numpy as np
from matplotlib import font_manager
from os.path import join, dirname, realpath


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


def use_style(style=None):
    """Some of the tick properties cannot be set using ``plt.style.use``."""
    styles = [COMMON] if style is None else [COMMON, style + ".mplstyle"]
    plt.style.use(join(STYLE_DIR, s) for s in styles)


def reset_global_style():
    plt.style.use("default")


def color_ticks(ax, color=None, axis="both", which="both"):
    if color is None:
        color = mpl.rcParams["grid.color"]
    ax.tick_params(color=color, axis=axis, which=which)


# From  https://github.com/williamgilpin/degas/blob/master/degas/degas.py
def lighter_color(color, f=1 / 3):
    """
    An implementation of Mathematica's Lighter[]
    function for RGB colors
    clr : 3-tuple or list, an RGB color
    f : float, the fraction by which to brighten
    """
    gaps = [f * (1 - val) for val in color]
    new_clr = [val + gap for gap, val in zip(gaps, color)]
    return new_clr


def darker_color(color, f=1 / 3):
    """
    An implementation of Mathematica's Darker[]
    function for RGB colors
    clr : 3-tuple or list, an RGB color
    f : float, the fraction by which to brighten
    """
    gaps = [f * val for val in color]
    new_clr = [val - gap for gap, val in zip(gaps, color)]
    return new_clr


def lighter_palette(palette, f=1 / 3):
    return [lighter_color(p, f=f) for p in palette]


def darker_palette(palette, f=1 / 3):
    return [darker_color(p, f=f) for p in palette]
