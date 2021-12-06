import io

import mplcyberpunk
import numpy as np
from matplotlib import pyplot as plt

from extensions.vaping.monthly_puff_data import MonthlyPuffData

plt.style.use("cyberpunk")


def get_vaping_plot(data: list[MonthlyPuffData]):
    fig, ax = plt.subplots(figsize=(12, 6))

    day_limit = len(data[0].puffs)
    x = list(range(1, day_limit + 1))
    max_y = max([max(puff_data.puffs) for puff_data in data])

    ax.set_xlim([1, data[0].month_days])
    ax.set_ylim([0, max_y + 5])

    for puff_data in data:
        y = puff_data.puffs

        ax.plot(x, y, marker="o")

    mplcyberpunk.add_glow_effects()

    if len(data) == 1:
        np_array = np.array(data[0].puffs)

        z = np.polyfit(x, np_array, 1)
        p = np.poly1d(z)

        line = ax.plot(x, p(x), "--", color="#00ff41")[0]
        make_line_glow(line, ax)

    plt.xticks(range(min(x), max(x) + 1, 1))
    plt.legend([puff_data.username for puff_data in data])

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    return buf


def make_line_glow(line, ax, n_glow_lines=10, diff_linewidth=1.05, alpha_line=0.3):
    """Add a glow effect to the lines in an axis object.

    Each existing line is redrawn several times with increasing width and low alpha to create the glow effect.
    """
    alpha_value = alpha_line / n_glow_lines

    data = line.get_data()
    linewidth = line.get_linewidth()

    try:
        step_type = line.get_drawstyle().split('-')[1]
    except:
        step_type = None

    for n in range(1, n_glow_lines + 1):
        if step_type:
            glow_line, = ax.step(*data)
        else:
            glow_line, = ax.plot(*data)
        glow_line.update_from(
            line)

        glow_line.set_alpha(alpha_value)
        glow_line.set_linewidth(linewidth + (diff_linewidth * n))
        glow_line.is_glow_line = True  # mark the glow lines, to disregard them in the underglow function.
