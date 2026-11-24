"""Regenerate the slides' figures with Matplotlib and partition_tree.skpro."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import pandas as pd
from partition_tree.skpro import PartitionForestRegressor, PartitionTreeRegressor


FIGURES = Path(__file__).with_name("figures")
INK, TEAL, RUST = "#213b40", "#006d68", "#b74d26"
PAPER = "#fbfaf6"
plt.rcParams.update({
    "font.size": 14, "text.color": INK, "axes.labelcolor": INK,
    "axes.edgecolor": "#81928f", "xtick.color": INK, "ytick.color": INK,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": PAPER, "axes.facecolor": PAPER,
    "svg.fonttype": "none", "svg.hashsalt": "partition-tree",
})


def probability_space():
    fig = plt.figure(figsize=(8.8, 5.3))
    grid = fig.add_axes([.04, .26, .42, .70], aspect="equal")
    grid.set(xlim=(0, 4), ylim=(0, 4))
    grid.set_axis_off()
    tiles = []
    for row in range(4):
        for col in range(4):
            tile = Rectangle((col, 3-row), 1, 1, facecolor="#eaf0ec", edgecolor="#79908a")
            tiles.append(grid.add_patch(tile))
    grid.plot(.65, 3.24, "o", color=INK, ms=5)
    grid.text(.73, 3.24, r"$\omega$", va="center")
    fig.text(.51, .83, r"$\Omega$   All points in the square", fontsize=17)
    fig.text(.51, .73, r"$\omega$   One outcome")
    fig.savefig(FIGURES / "sample-space.svg", metadata={"Date": None})

    masses = np.array([10] + [5]*9 + [4]*5 + [25])
    assert len(masses) == len(tiles) and masses.sum() == 100
    colors = ["#eaf0ec"] * len(tiles)
    for index, name, color in [(0, "A", "#85c3b3"), (15, "B", "#ecb390")]:
        colors[index] = color
        tile = tiles[index]
        tile.set_facecolor(color)
        grid.text(tile.get_x() + .45, tile.get_y() + .62, f"${name}$", fontsize=17,
                  ha="center", va="center")
    fig.text(.51, .58, r"$\mathcal{F}$   All unions of tiles", fontsize=17)
    fig.text(.51, .51, "Each tile is an atom.")
    fig.text(.51, .43, r"$E = A \cup B \in \mathcal{F}$")
    fig.savefig(FIGURES / "measurable-event.svg", metadata={"Date": None})

    ruler = fig.add_axes([.04, .12, .92, .068])
    edges = np.r_[0, masses.cumsum()] / 100
    ruler.barh(.5, np.diff(edges), left=edges[:-1], height=1, color=colors,
               edgecolor="#79908a", linewidth=.8)
    for index, name in [(0, "A"), (15, "B")]:
        ruler.text((edges[index] + edges[index+1])/2, .5, f"${name}$", ha="center", va="center")
    ruler.set(xlim=(0, 1), ylim=(0, 1), yticks=[], xticks=[0, .10, .75, 1],
              xticklabels=["0", "0.10", "0.75", "1"])
    fig.text(.51, .28, r"$P(E) = 0.10 + 0.25 = \mathbf{0.35}$", fontsize=17)
    fig.savefig(FIGURES / "probability-measure.svg", metadata={"Date": None})
    plt.close(fig)
    tree_over_tiles(colors)


def tree_over_tiles(tile_colors):
    fig = plt.figure(figsize=(8.8, 5.3))
    ax = fig.add_axes([.02, .09, .96, .87], aspect="equal")
    ax.set_axis_off()

    def project(col, row, height=0):
        return col + .52 * row, height - .43 * row

    for index, color in enumerate(tile_colors):
        row, col = divmod(index, 4)
        corners = [project(col + dx, row + dy) for dx, dy in [(0, 0), (1, 0), (1, 1), (0, 1)]]
        ax.fill(*zip(*corners), facecolor=color, edgecolor="#79908a", linewidth=.9)

    def draw_node(region, depth=0):
        rows, cols = np.divmod(region, 4)
        node = project(cols.mean() + .5, rows.mean() + .5, (4 - depth) * .79)
        color = "#849893"
        if region.size == 16:
            color = INK
        elif 0 in region:
            color = TEAL
        elif 15 in region:
            color = RUST
        ax.plot(*node, "o", ms=8 - .7 * depth, color=color, mec=PAPER, mew=.7, zorder=4)
        if region.size > 1:
            for child in np.split(region, 2, axis=1 - depth % 2):
                end, branch_color = draw_node(child, depth + 1)
                highlighted = branch_color in (TEAL, RUST)
                ax.plot(*zip(node, end), color=branch_color, lw=2.5 if highlighted else 1.3,
                        zorder=3 if highlighted else 2)
        return node, color

    root, _ = draw_node(np.arange(16).reshape(4, 4))
    ax.annotate(r"$\Omega$", root, xytext=(0, 8), textcoords="offset points", ha="center", fontsize=17)
    for row, col, label in [(0, 0, "$A$"), (3, 3, "$B$")]:
        ax.text(*project(col + .49, row + .80), label, ha="center", va="center", fontsize=14)
    ax.set(xlim=(-.15, 6.23), ylim=(-1.78, 2.72))
    fig.text(.5, .035, "Each leaf corresponds to one tile.", ha="center", fontsize=16)
    fig.savefig(FIGURES / "tree-over-tiles.svg", metadata={"Date": None})
    plt.close(fig)


def worked_example():
    x = np.array([.06, .08, .12, .16, .20, .23, .27, .30, .34, .38, .41, .46,
                  .54, .59, .65, .72, .77, .83, .89, .94])
    y = np.array([3.6, .25, 3.2, 3.7, 3.4, 3.1, .75, 3.9, 3.5, .5, 3.8, 3.3,
                  .8, .3, 1.4, .6, 1.8, .9, .4, 1.2])
    left = x <= .5
    mean = y[left].mean()
    assert left.sum() == 12 and (left & (y > 3)).sum() == 9 and mean == 2.75

    for stage in ["leaf", "mean", "split", "projections", "point", "slice"]:
        fig, ax = plt.subplots(figsize=(6.4, 4))
        fig.subplots_adjust(left=.10, right=.95, bottom=.18, top=.94)
        ax.set(xlim=(0, 1), ylim=(0, 4), xlabel="Covariate x", ylabel="Outcome y",
               xticks=[0, .25, .5, .75, 1], yticks=[0, 1, 2, 3, 4])
        ax.axvline(.5, color=INK, lw=1.4)
        if stage in ["leaf", "mean"]:
            ax.axvspan(0, .5, color="#e4edeb", zorder=0)
        else:
            ax.axhspan(0, 3, xmin=0, xmax=.5, color="#eaf2ee")
            ax.axhspan(3, 4, xmin=0, xmax=.5, color="#7fbfb0")
            ax.axvspan(.5, 1, color="#d0e4dc")
            ax.hlines(3, 0, .5, color=TEAL, lw=2)
        ax.scatter(x, y, s=48, color=INK, edgecolor=PAPER, linewidth=.8, zorder=3)
        if stage == "projections":
            fig.subplots_adjust(top=.82)
            for label, cx, cy in [(r"$A_1$", .05, 3.26), (r"$A_2$", .25, 1.5),
                                  (r"$A_3$", .75, 2.3)]:
                ax.text(cx, cy, label, ha="center", va="center", fontsize=16)
            ax.plot([0, .5], [4.15, 4.15], "|-", color=RUST, lw=2, ms=9, clip_on=False)
            ax.text(.25, 4.28, r"$A_X = [0, 0.5]$", ha="center", color=RUST)
            ax.plot([.53, .53], [3, 4], "_-", color=RUST, lw=2, ms=9, clip_on=False)
            ax.text(.56, 3.5, r"$A_Y = (3, 4]$", va="center", color=RUST)
        if stage == "mean":
            ax.hlines(mean, 0, .5, color=RUST, lw=2, linestyle="--")
            ax.text(.04, mean-.14, "mean = 2.75", va="top", color=RUST, weight="bold")
        if stage == "point":
            ax.scatter([.25], [3.5], marker="D", s=110, color=RUST,
                       edgecolor=PAPER, linewidth=1.2, zorder=4)
        if stage == "slice":
            ax.axvline(.25, color=RUST, lw=3, linestyle="--")
        fig.savefig(FIGURES / f"{stage}.svg", metadata={"Date": None})
        plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.4, 2.2))
    fig.subplots_adjust(left=.15, right=.96, bottom=.32, top=.94)
    ax.bar([0, 3], [1/12, 3/4], width=[3, 1], align="edge",
           color=["#eaf2ee", "#7fbfb0"], edgecolor=TEAL)
    ax.set(xlim=(0, 4), ylim=(0, .85), xlabel="Outcome y", ylabel="Density",
           xticks=[0, 1, 2, 3, 4], yticks=[1/12, 3/4], yticklabels=["1/12", "3/4"])
    fig.savefig(FIGURES / "histogram.svg", metadata={"Date": None})
    plt.close(fig)


def prediction_example(dataset):
    rng = np.random.default_rng(42)
    x = rng.uniform(0, 1, 2400)
    noise = rng.standard_normal(len(x))
    if dataset == "spread":
        y = np.where(x < .5, .25, .8) * noise
    else:
        upper = rng.random(len(x)) < np.where(x < .5, .2, .8)
        y = np.where(upper, 1.1, -1.1) + .26 * noise

    query = pd.DataFrame({"x": [.25, .75]})
    settings = dict(max_leaves=45, min_samples_xy=16, min_volume_fraction=.04,
                    loss="conditional_log_loss", random_state=42)
    models = [
        ("Partition Tree", PartitionTreeRegressor(**settings), RUST),
        ("Partition Forest", PartitionForestRegressor(n_estimators=50, **settings), TEAL),
    ]
    fig, (sample, *slices) = plt.subplots(1, 3, figsize=(13.6, 4.45))
    fig.subplots_adjust(left=.06, right=.99, top=.85, bottom=.25, wspace=.36)
    sample.scatter(x, y, s=7, color=TEAL, alpha=.28, linewidths=0)
    for value in query.x:
        sample.axvline(value, color=INK, ls=":", lw=1.7)
    sample.set(title="Training observations", xlabel="Covariate x", ylabel="Outcome y",
               xlim=(0, 1), xticks=[0, .25, .5, .75, 1])
    for label, model, color in models:
        model.fit(pd.DataFrame({"x": x}), pd.DataFrame({"y": y}))
        dist = model.predict_proba(query)
        for ax, intervals, heights in zip(slices, dist.intervals, dist.pdf_values):
            lows, highs = np.asarray(intervals).T
            assert np.allclose(lows[1:], highs[:-1])
            area = np.dot(highs - lows, heights)
            assert area > 0
            ax.stairs(heights / area, np.r_[lows, highs[-1]],
                      color=color, lw=2, label=label)
    grid = np.linspace(-2.5, 2.5, 601)
    for ax, value in zip(slices, query.x):
        if dataset == "spread":
            truth = normal_pdf(grid, 0, .25 if value < .5 else .8)
        else:
            p = .2 if value < .5 else .8
            truth = (1-p)*normal_pdf(grid, -1.1, .26) + p*normal_pdf(grid, 1.1, .26)
        ax.plot(grid, truth, ls="--", lw=1.6, color=INK, label="Generating density")
        ax.set(title=f"Prediction at x = {value:.2f}", xlabel="Outcome y",
               xlim=(-2.5, 2.5), xticks=[-2, -1, 0, 1, 2])
    slices[0].set_ylabel("Conditional density")
    ymax = max(ax.get_ylim()[1] for ax in slices)
    for ax in slices:
        ax.set_ylim(0, ymax)
    fig.legend(*slices[0].get_legend_handles_labels(), loc="lower center",
               ncol=3, frameon=False)
    fig.savefig(FIGURES / f"{dataset}.png", dpi=160)
    plt.close(fig)


def normal_pdf(y, mean, sd):
    return np.exp(-.5 * ((y - mean) / sd)**2) / (sd * np.sqrt(2 * np.pi))


if __name__ == "__main__":
    FIGURES.mkdir(exist_ok=True)
    probability_space()
    worked_example()
    prediction_example("spread")
    prediction_example("modes")
