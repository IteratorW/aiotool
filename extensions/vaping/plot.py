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

    plt.xticks(range(min(x), max(x) + 1, 1))
    plt.legend([puff_data.username for puff_data in data])

    mplcyberpunk.add_glow_effects()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    return buf
