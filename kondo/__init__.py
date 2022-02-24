import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.axes
import numpy as np
from contextlib import contextmanager
from matplotlib import font_manager
from matplotlib.artist import ArtistInspector
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


@contextmanager
def plt_breakpoint():
    """
    Type `u` three times to go to code wrapped in this context manager.
    Then manipulate the plot via pdb as you please
    To finish, type `c` to continue execution, or `q` to quit the process.

    Example usage:
    ```
    x, y = expensive_function()
    with plt_breakpoint():
        fig, ax = plt.subplots()
        ax.plot(x, y)
    ```

    This code is equivalent to manually entering
    ```
    x, y = expensive_function()
    with plt.ion():
        fig, ax = plt.subplots()
        ax.plot(x, y)
        breakpoint()
    ```
    but packaged as one single context manager.

    After interactive mode, you can get the properties of your figure and axes via
    ```
    fig_prop = plt.getp(fig)
    ax_prop = plt.getp(ax)
    ```
    and save them if you wish.

    """
    with plt.ion():
        try:
            yield
        finally:
            breakpoint()


def getp(obj, property=None, all=False):
    """
    Like plt.getp, but actually returns the dictionary of properties that are settable

    TODO: plt.setp doesn't work properly. Example:
    ```
    x = np.linspace(0, 2*np.pi)
    y = np.sin(x)

    fig, ax = plt.subplots()
    ax.plot(x, y)
    old = getp(ax)

    plt.setp(ax, **old)
    # This will result in a figure that looks different from before, even though we're using the same properties
    # Somehow, the ybounds change
    ```
    To get around this, we need to explicitly set xbound, ybound, xlim, ylim after
    plt.setp if we're setting properties of Axes
    """
    if property is not None:
        return plt.getp(property)
    insp = ArtistInspector(obj)
    setable_props = set(insp.get_setters())
    props = insp.properties()
    if all:
        return props
    props = {k: v for k, v in props.items() if k in setable_props}
    return props


PALETTES = {
    "tianyi": np.array(
        [
            "#1d437d",
            "#ee442f",
            "#0099ad",
            "#dec923",
            "#a95aa1",
            "#f78f1e",
            "#ccbe9f",
            "#29562a",
            "#99cc83",
        ]
    ),
    "bmh": np.array(
        [
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
        ]
    ),
    "solarized-light": np.array(
        [
            "#268BD2",
            "#2AA198",
            "#859900",
            "#B58900",
            "#CB4B16",
            "#DC322F",
            "#D33682",
            "#6C71C4",
        ]
    ),
    "fivethirtyeight": np.array(
        [
            "#008fd5",
            "#fc4f30",
            "#e5ae38",
            "#6d904f",
            "#8b8b8b",
            "#810f7c",
        ]
    ),
    "ggplot": np.array(
        [
            "#E24A33",
            "#348ABD",
            "#988ED5",
            "#777777",
            "#FBC15E",
            "#8EBA42",
            "#FFB5B8",
        ]
    ),
    "degas-high-contrast": np.array(
        [
            [0.372549, 0.596078, 1],
            [1.0, 0.3882, 0.2784],
            [0.20784314, 0.67843137, 0.6],
            [0.59607843, 0.25882353, 0.89019608],
            [0.803922, 0.0627451, 0.462745],
            [0.917647, 0.682353, 0.105882],
            [0.7, 0.7, 0.7],
        ]
    ),
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
