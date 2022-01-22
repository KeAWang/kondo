import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import font_manager


def make_subplots(
    ncols=1, nrows=1, w=4, h_to_w=1 / 1.618, wspace=None, hspace=None, **subplots_kwargs
):
    box_aspect = h_to_w
    h = box_aspect * w
    fig, axes = plt.subplots(
        figsize=(ncols * w, nrows * h),
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
