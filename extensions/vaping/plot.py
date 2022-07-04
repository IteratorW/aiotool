import io

import mplcyberpunk
import numpy as np
from matplotlib import pyplot as plt, patches

from extensions.vaping.monthly_puff_data import MonthlyPuffData

plt.style.use("aiotool.mplstyle")


def get_vaping_plot_year(data: list[int]) -> io.BytesIO:
    fig, ax = plt.subplots(figsize=(12, 6))

    max_y = max(data)
    x = list(range(1, len(data) + 1))

    ax.set_xlim([1, 12])
    ax.set_ylim([0, max_y + 250])

    line = ax.plot(x, data, marker="o")[0]

    make_line_glow(line, ax, n_glow_lines=15, diff_linewidth=2.0)
    mplcyberpunk.add_underglow(ax)

    plt.xticks(range(min(x), max(x) + 1, 1))
    plt.yticks(np.arange(0, max_y + 15, 500))

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    return buf


def get_vaping_plot_month(data: list[MonthlyPuffData], global_chart=False) -> io.BytesIO:
    # TODO probably requires a fucking refactor

    fig, ax = plt.subplots(figsize=(12, 6))

    day_limit = len(data[0].puffs)
    x = list(range(1, day_limit + 1))
    max_y = max([max(puff_data.puffs) for puff_data in data])

    ax.set_xlim([1, data[0].month_days])
    ax.set_ylim([0, max_y + 15])

    for puff_data in data:
        y = puff_data.puffs

        line = ax.plot(x, y, marker="o")[0]

        make_line_glow(line, ax, n_glow_lines=15, diff_linewidth=2.0)
        mplcyberpunk.add_underglow(ax)

    if not global_chart:
        np_array = np.array(data[0].puffs)

        z = np.polyfit(x, np_array, 1)
        p = np.poly1d(z)

        line = ax.plot(x, p(x), "--", color="#00ff41")[0]
        make_line_glow(line, ax)

        max_x = data[0].puffs.index(max_y)

        line2 = ax.plot(x, [max_y] * len(x), ":", color="#F5D300")[0]
        make_line_glow(line2, ax)

        ax.annotate("Больше всего затяжек!", xy=(max_x + 1.5, max_y + 5), color="#F5D300")

    plt.xticks(range(min(x), max(x) + 1, 1))
    plt.yticks(np.arange(0, max_y + 15, 45))
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
