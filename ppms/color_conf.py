import matplotlib as mpl
import numpy as np
from typing import Sequence, Optional

def blend_hex(color1: str, color2: str, ratio: float) -> str:
    """
    Linearly interpolate / extrapolate between two hex colours.

    Parameters
    ----------
    color1 : str
        First colour in 6‑digit hex form, e.g. '#AA3377' or 'AA3377'.
    color2 : str
        Second colour in 6‑digit hex form.
    ratio  : float
        Interpolation factor:
            0.0 → returns color1
            1.0 → returns color2
            <0  → extrapolates past color1 (darker than color1 if color2 is lighter)
            >1  → extrapolates past color2

    Returns
    -------
    str
        Hex colour string starting with '#'.
    """
    # strip leading '#' if present
    c1, c2 = color1.lstrip('#'), color2.lstrip('#')
    if len(c1) != 6 or len(c2) != 6:
        raise ValueError("Colours must be 6‑digit hex strings.")

    # convert to integer RGB tuples
    r1, g1, b1 = int(c1[0:2], 16), int(c1[2:4], 16), int(c1[4:6], 16)
    r2, g2, b2 = int(c2[0:2], 16), int(c2[2:4], 16), int(c2[4:6], 16)

    # interpolate / extrapolate
    r = round(r1 + ratio * (r2 - r1))
    g = round(g1 + ratio * (g2 - g1))
    b = round(b1 + ratio * (b2 - b1))

    # keep channel values in valid range
    r, g, b = (max(0, min(255, v)) for v in (r, g, b))

    return f"#{r:02X}{g:02X}{b:02X}"


def three_color_cmap(color1: str,
                     color2: str,
                     color3: str,
                     midpoint: float = 0.5,
                     name: str = "three_step",
                     N: int = 256) -> mpl.colors.Colormap:
    """
    Build a colormap that goes color1 → color2 → color3.

    Parameters
    ----------
    color1, color2, color3 : str
        Hex colour strings ('#RRGGBB' or 'RRGGBB').
    midpoint : float, optional
        Fractional position of color2 (0–1). 0.5 gives symmetric blending.
    name : str, optional
        Internal name for the colormap.
    N : int, optional
        Number of colours sampled in the final map.

    Returns
    -------
    mpl.colors.Colormap
    """
    # (position, colour) pairs; positions must be monotonically increasing
    colors = [(0.0, color1), (midpoint, color2), (1.0, color3)]
    return mpl.colors.LinearSegmentedColormap.from_list(name, colors, N=N)


def multi_color_cmap(colors: Sequence[str],
                     positions: Optional[Sequence[float]] = None,
                     name: str = "multi_step",
                     N: int = 256) -> mpl.colors.Colormap:
    """
    Build a LinearSegmentedColormap that passes through an arbitrary
    sequence of colours.

    Parameters
    ----------
    colors : sequence of str
        Hex colour strings ('#RRGGBB' or 'RRGGBB').
    positions : sequence of float, optional
        Monotonically increasing numbers in [0,1] that set where each
        colour appears. If None, colours are spaced evenly.
    name : str, optional
        Internal name for the colormap.
    N : int, optional
        Number of colour samples in the final map.

    Returns
    -------
    mpl.colors.Colormap
    """
    n = len(colors)
    if n < 2:
        raise ValueError("Need at least two colours for a colormap.")

    if positions is None:
        positions = np.linspace(0, 1, n)
    else:
        if len(positions) != n:
            raise ValueError("`positions` must have the same length as `colors`.")
        if (positions[0] != 0.0) or (positions[-1] != 1.0):
            raise ValueError("First position must be 0 and last must be 1.")
        if any(p_next <= p for p_next, p in zip(positions[1:], positions[:-1])):
            raise ValueError("`positions` must be strictly increasing.")

    # pair each position with its colour
    colour_list = list(zip(positions, colors))
    return mpl.colors.LinearSegmentedColormap.from_list(name, colour_list, N=N)


# custom colormap 
color_low  = blend_hex("#AA3377", "#CCBB44", -0.3) #"#AA3377"   # low‑end colour
color_high  = blend_hex("#AA3377", "#CCBB44", 1.4) #"#CCBB44"   # high‑end colour

# base 2‑colour interpolation
cmap_custom = mpl.colors.LinearSegmentedColormap.from_list(
        "color_custom",      # cmap name
        [color_low, color_high],     # low → high
        N=256                 # no. of interpolated colours
)

# extrapolate: darker purple for values below the displayed range
cmap_custom.set_under("#552255")     # any dark shade you like

colors_custom = cmap_custom(np.linspace(0, 1, 26))


# ------------------ example ------------------
cmap3 = three_color_cmap("#210b21",  # dark purple (low)
                         color_low,  # purple‑pink (mid)
                         color_high,  # yellow‑green (high)
                         midpoint=0.3)  # put colour‑2 at 30 % of the scale

# 26 colours for your line plots (T = 0‥25 K)
colors3 = cmap3(np.linspace(0, 1, 26))



cmap5 = multi_color_cmap(
    colors=["#210b21",     #blend_hex("#AA3377", "#EE6677", -0.9),  
            "#AA3377", 
            "#EE6677",
            "#CCBB44",
            blend_hex("#EE6677", "#CCBB44", 1.4)],  # yellow‑green     (0.7)
    positions=[0.0, 0.3, 0.5, 0.7, 1.0],  # you decide where colours 2 & 3 sit
    name="purple_yellow_light",
    N=256
)

# 26 equally spaced colours for line plots
colors5 = cmap5(np.linspace(0, 1, 26))


if __name__ == "__main__":
    color1 = "#AA3377"  # purple
    color2 = "#CCBB44"  # yellow
    for r in [-1, -0.3, 0, 0.5, 1, 1.4]:
        print(f'{color1}+{color2} ({r:.1f}) = {blend_hex(color1, color2, r)}')
    print(blend_hex("#AA3377", "#EE6677", -0.9))
    print(blend_hex("#EE6677", "#CCBB44", 1.7))
