# utils/plots.py
# ─────────────────────────────────────────────────────────────────────────────
# ALL PLOTTING FUNCTIONS — TSP & Knapsack
# ─────────────────────────────────────────────────────────────────────────────

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

PLOTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

# ── Color palette ────────────────────────────────────────────────────────────
COLORS = {
    "Greedy Det":    "#4a9eff",
    "Greedy NonDet": "#f9a03f",
    "LS First":      "#a259ff",
    "LS Best":       "#ff5c8a",
    "SA":            "#00c49f",
    "Genetic":       "#ff8c42",
}
ALG_ORDER = list(COLORS.keys())


# ════════════════════════════════════════════════════════════════════════════
#  SHARED HELPERS
# ════════════════════════════════════════════════════════════════════════════

def _save(fig, filename):
    path = os.path.join(PLOTS_DIR, filename)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved → plots/{filename}")
    return path


def _bar_comparison(results, title, ylabel, filename, lower_is_better=True):
    """Generic bar chart comparing all algorithms."""
    names  = [k for k in ALG_ORDER if k in results]
    values = [results[k] for k in names]
    best   = min(values) if lower_is_better else max(values)
    colors = [COLORS.get(n, "#888") for n in names]
    edge   = ["gold" if v == best else "none" for v in values]

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(names, values, color=colors, edgecolor=edge, linewidth=2.5, zorder=3)

    # Value labels on bars
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.005,
                f"{val:.1f}" if isinstance(val, float) else str(val),
                ha="center", va="bottom", fontsize=9, fontweight="bold")

    ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_xlabel("Algorithm", fontsize=11)
    ax.yaxis.grid(True, alpha=0.4, zorder=0)
    ax.set_axisbelow(True)

    # Star best
    best_idx = values.index(best)
    ax.get_children()[best_idx].set_edgecolor("gold")

    star = mpatches.Patch(facecolor="gold", edgecolor="gray", label="★ Best")
    ax.legend(handles=[star], fontsize=9)
    fig.tight_layout()
    return _save(fig, filename)


# ════════════════════════════════════════════════════════════════════════════
#  TSP PLOTS
# ════════════════════════════════════════════════════════════════════════════

def _draw_tour(ax, tour, cities, title, color, cost):
    xs = [cities[c][0] for c in tour] + [cities[tour[0]][0]]
    ys = [cities[c][1] for c in tour] + [cities[tour[0]][1]]
    ax.plot(xs, ys, color=color, linewidth=1.2, alpha=0.85, zorder=2)
    ax.scatter([c[0] for c in cities], [c[1] for c in cities],
               s=25, color="black", zorder=3)
    ax.scatter(cities[tour[0]][0], cities[tour[0]][1],
               s=80, color="red", zorder=4, label="Start")
    ax.set_title(f"{title}\ndist = {cost:.1f}", fontsize=9, fontweight="bold")
    ax.axis("off")


def plot_tsp_cities(tsp, filename="tsp_00_cities.png"):
    """Scatter plot of all cities."""
    fig, ax = plt.subplots(figsize=(7, 6))
    xs = [c[0] for c in tsp.cities]
    ys = [c[1] for c in tsp.cities]
    ax.scatter(xs, ys, s=50, color="steelblue", zorder=3)
    for i, (x, y) in enumerate(tsp.cities):
        ax.annotate(str(i+1), (x, y), fontsize=7, ha="center", va="bottom", xytext=(0, 5),
                    textcoords="offset points")
    ax.set_title(f"{tsp.name} — {tsp.n} cities", fontsize=13, fontweight="bold")
    ax.axis("off")
    fig.tight_layout()
    return _save(fig, filename)


def plot_tsp_greedy(tsp, gs_tour, gs_cost, gnd_tour, gnd_cost,
                    filename="tsp_01_greedy.png"):
    """Side-by-side greedy tours."""
    fig, axes = plt.subplots(1, 2, figsize=(13, 6))
    fig.suptitle(f"{tsp.name} — Greedy Construction", fontsize=13, fontweight="bold")
    _draw_tour(axes[0], gs_tour,  tsp.cities, "Greedy Deterministic",    COLORS["Greedy Det"],    gs_cost)
    _draw_tour(axes[1], gnd_tour, tsp.cities, "Greedy Non-Deterministic", COLORS["Greedy NonDet"], gnd_cost)
    fig.tight_layout()
    return _save(fig, filename)


def plot_tsp_local_search(tsp, initial_tour, initial_cost,
                          fi_tour, fi_cost, bi_tour, bi_cost,
                          filename="tsp_02_local_search.png"):
    """Three tours: initial, first improvement, best improvement."""
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle(f"{tsp.name} — Local Search (2-opt)", fontsize=13, fontweight="bold")
    _draw_tour(axes[0], initial_tour, tsp.cities, "Initial (Greedy)",      "#aaa",              initial_cost)
    _draw_tour(axes[1], fi_tour,      tsp.cities, "First Improvement",     COLORS["LS First"],  fi_cost)
    _draw_tour(axes[2], bi_tour,      tsp.cities, "Best Improvement",      COLORS["LS Best"],   bi_cost)
    fig.tight_layout()
    return _save(fig, filename)


def plot_tsp_sa(tsp, sa_tour, sa_cost, sa_history,
                filename="tsp_03_simulated_annealing.png"):
    """SA: convergence curve + final tour."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(f"{tsp.name} — Simulated Annealing", fontsize=13, fontweight="bold")

    # Convergence
    temps  = [h[0] for h in sa_history]
    costs  = [h[1] for h in sa_history]
    ax = axes[0]
    ax.plot(costs, color=COLORS["SA"], linewidth=1.2, alpha=0.8)
    ax.set_xlabel("Iteration", fontsize=10)
    ax.set_ylabel("Tour Cost", fontsize=10)
    ax.set_title("Convergence Curve", fontsize=10, fontweight="bold")
    ax.yaxis.grid(True, alpha=0.3)

    # Temperature on secondary axis
    ax2 = ax.twinx()
    ax2.plot(temps, color="orange", linewidth=0.8, alpha=0.5, linestyle="--")
    ax2.set_ylabel("Temperature", fontsize=9, color="orange")
    ax2.tick_params(axis="y", colors="orange")

    # Final tour
    _draw_tour(axes[1], sa_tour, tsp.cities, f"Best Tour  dist={sa_cost:.1f}", COLORS["SA"], sa_cost)
    fig.tight_layout()
    return _save(fig, filename)


def plot_tsp_ga(tsp, ga_tour, ga_cost, ga_history,
                filename="tsp_04_genetic.png"):
    """GA: convergence + final tour."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(f"{tsp.name} — Genetic Algorithm", fontsize=13, fontweight="bold")

    axes[0].plot(ga_history, color=COLORS["Genetic"], linewidth=1.5)
    axes[0].set_xlabel("Generation", fontsize=10)
    axes[0].set_ylabel("Best Tour Cost", fontsize=10)
    axes[0].set_title("Convergence Curve", fontsize=10, fontweight="bold")
    axes[0].yaxis.grid(True, alpha=0.3)

    _draw_tour(axes[1], ga_tour, tsp.cities, f"Best Tour  dist={ga_cost:.1f}", COLORS["Genetic"], ga_cost)
    fig.tight_layout()
    return _save(fig, filename)


def plot_tsp_all_tours(tsp, tours_dict, filename="tsp_05_all_tours.png"):
    """
    Grid of all 6 algorithm tours.
    tours_dict = {name: (tour, cost)}
    """
    items = [(k, tours_dict[k]) for k in ALG_ORDER if k in tours_dict]
    n = len(items)
    cols = 3
    rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(15, 5*rows))
    axes = axes.flatten()
    fig.suptitle(f"{tsp.name} — All Algorithm Tours", fontsize=14, fontweight="bold")
    for idx, (name, (tour, cost)) in enumerate(items):
        _draw_tour(axes[idx], tour, tsp.cities, name, COLORS.get(name, "#888"), cost)
    for idx in range(len(items), len(axes)):
        axes[idx].axis("off")
    fig.tight_layout()
    return _save(fig, filename)


def plot_tsp_summary(results, filename="tsp_06_summary.png"):
    return _bar_comparison(results, "TSP — Algorithm Comparison (Tour Cost)",
                           "Tour Cost", filename, lower_is_better=True)


# ════════════════════════════════════════════════════════════════════════════
#  KNAPSACK PLOTS
# ════════════════════════════════════════════════════════════════════════════

def plot_knapsack_instance(knapsack, filename="ks_00_instance.png"):
    """Scatter plot: weight vs value for all items, size = ratio."""
    fig, ax = plt.subplots(figsize=(8, 6))
    ws = [knapsack.weight(i) for i in range(knapsack.n)]
    vs = [knapsack.value(i)  for i in range(knapsack.n)]
    rs = [knapsack.ratio(i)  for i in range(knapsack.n)]
    sc = ax.scatter(ws, vs, c=rs, cmap="RdYlGn", s=120, edgecolors="gray",
                    linewidth=0.5, zorder=3)
    plt.colorbar(sc, ax=ax, label="Value/Weight Ratio")
    for i, (w, v) in enumerate(zip(ws, vs)):
        ax.annotate(str(i), (w, v), fontsize=7, ha="center", va="bottom",
                    xytext=(0, 4), textcoords="offset points")
    ax.axhline(y=0, color="gray", linewidth=0.5)
    ax.set_xlabel("Weight", fontsize=11)
    ax.set_ylabel("Value",  fontsize=11)
    ax.set_title(f"{knapsack.name} — Items (color = v/w ratio)\nCapacity = {knapsack.capacity}",
                 fontsize=12, fontweight="bold")
    ax.yaxis.grid(True, alpha=0.3)
    fig.tight_layout()
    return _save(fig, filename)


def plot_knapsack_greedy(knapsack, gs_sel, gs_val, gnd_sel, gnd_val,
                         filename="ks_01_greedy.png"):
    """Bar chart of item values, highlighting selected items for each greedy."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(f"{knapsack.name} — Greedy Construction", fontsize=13, fontweight="bold")

    for ax, sel, val, label, color in [
        (axes[0], gs_sel,  gs_val,  "Greedy Deterministic",    COLORS["Greedy Det"]),
        (axes[1], gnd_sel, gnd_val, "Greedy Non-Deterministic", COLORS["Greedy NonDet"]),
    ]:
        sel_set = set(sel)
        bar_colors = [color if i in sel_set else "#ddd" for i in range(knapsack.n)]
        bars = ax.bar(range(knapsack.n), [knapsack.value(i) for i in range(knapsack.n)],
                      color=bar_colors, edgecolor="gray", linewidth=0.4, zorder=3)
        tw = sum(knapsack.weight(i) for i in sel)
        ax.set_title(f"{label}\nValue={val}  Weight={tw}/{knapsack.capacity}", fontsize=10, fontweight="bold")
        ax.set_xlabel("Item index", fontsize=9)
        ax.set_ylabel("Item value", fontsize=9)
        ax.yaxis.grid(True, alpha=0.3)
        selected_patch = mpatches.Patch(color=color, label="Selected")
        ax.legend(handles=[selected_patch], fontsize=8)
    fig.tight_layout()
    return _save(fig, filename)


def plot_knapsack_local_search(knapsack, init_sel, init_val,
                                fi_sel, fi_val, bi_sel, bi_val,
                                filename="ks_02_local_search.png"):
    """3 subplots showing selected items before and after local search."""
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle(f"{knapsack.name} — Local Search", fontsize=13, fontweight="bold")

    for ax, sel, val, label, color in [
        (axes[0], init_sel, init_val, "Initial (Greedy)", "#aaa"),
        (axes[1], fi_sel,   fi_val,   "First Improvement", COLORS["LS First"]),
        (axes[2], bi_sel,   bi_val,   "Best Improvement",  COLORS["LS Best"]),
    ]:
        sel_set = set(sel)
        bar_colors = [color if i in sel_set else "#eee" for i in range(knapsack.n)]
        ax.bar(range(knapsack.n), [knapsack.value(i) for i in range(knapsack.n)],
               color=bar_colors, edgecolor="gray", linewidth=0.3, zorder=3)
        tw = sum(knapsack.weight(i) for i in sel)
        ax.set_title(f"{label}\nValue={val}  Weight={tw}/{knapsack.capacity}", fontsize=9, fontweight="bold")
        ax.set_xlabel("Item index", fontsize=8)
        ax.set_ylabel("Value", fontsize=8)
        ax.yaxis.grid(True, alpha=0.3)
    fig.tight_layout()
    return _save(fig, filename)


def plot_knapsack_sa(knapsack, sa_sel, sa_val, sa_history,
                     filename="ks_03_simulated_annealing.png"):
    """SA convergence + selected items."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(f"{knapsack.name} — Simulated Annealing", fontsize=13, fontweight="bold")

    temps  = [h[0] for h in sa_history]
    values = [h[1] for h in sa_history]
    ax = axes[0]
    ax.plot(values, color=COLORS["SA"], linewidth=1.2, alpha=0.8)
    ax.set_xlabel("Iteration", fontsize=10)
    ax.set_ylabel("Total Value", fontsize=10)
    ax.set_title("Convergence Curve", fontsize=10, fontweight="bold")
    ax.yaxis.grid(True, alpha=0.3)
    ax2 = ax.twinx()
    ax2.plot(temps, color="orange", linewidth=0.8, alpha=0.5, linestyle="--")
    ax2.set_ylabel("Temperature", fontsize=9, color="orange")
    ax2.tick_params(axis="y", colors="orange")

    sel_set = set(sa_sel)
    bar_colors = [COLORS["SA"] if i in sel_set else "#eee" for i in range(knapsack.n)]
    tw = sum(knapsack.weight(i) for i in sa_sel)
    axes[1].bar(range(knapsack.n), [knapsack.value(i) for i in range(knapsack.n)],
                color=bar_colors, edgecolor="gray", linewidth=0.3, zorder=3)
    axes[1].set_title(f"Best Selection\nValue={sa_val}  Weight={tw}/{knapsack.capacity}",
                      fontsize=10, fontweight="bold")
    axes[1].set_xlabel("Item index", fontsize=9)
    axes[1].set_ylabel("Value", fontsize=9)
    axes[1].yaxis.grid(True, alpha=0.3)
    fig.tight_layout()
    return _save(fig, filename)


def plot_knapsack_ga(knapsack, ga_sel, ga_val, ga_history,
                     filename="ks_04_genetic.png"):
    """GA convergence + selected items."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(f"{knapsack.name} — Genetic Algorithm", fontsize=13, fontweight="bold")

    axes[0].plot(ga_history, color=COLORS["Genetic"], linewidth=1.5)
    axes[0].set_xlabel("Generation", fontsize=10)
    axes[0].set_ylabel("Best Value", fontsize=10)
    axes[0].set_title("Convergence Curve", fontsize=10, fontweight="bold")
    axes[0].yaxis.grid(True, alpha=0.3)

    sel_set = set(ga_sel)
    bar_colors = [COLORS["Genetic"] if i in sel_set else "#eee" for i in range(knapsack.n)]
    tw = sum(knapsack.weight(i) for i in ga_sel)
    axes[1].bar(range(knapsack.n), [knapsack.value(i) for i in range(knapsack.n)],
                color=bar_colors, edgecolor="gray", linewidth=0.3, zorder=3)
    axes[1].set_title(f"Best Selection\nValue={ga_val}  Weight={tw}/{knapsack.capacity}",
                      fontsize=10, fontweight="bold")
    axes[1].set_xlabel("Item index", fontsize=9)
    axes[1].set_ylabel("Value", fontsize=9)
    axes[1].yaxis.grid(True, alpha=0.3)
    fig.tight_layout()
    return _save(fig, filename)


def plot_knapsack_summary(results, filename="ks_05_summary.png"):
    return _bar_comparison(results, "Knapsack — Algorithm Comparison (Total Value)",
                           "Total Value", filename, lower_is_better=False)


def plot_knapsack_weight_vs_value(knapsack, results_detail, filename="ks_06_weight_value.png"):
    """
    Scatter: weight used vs value obtained per algorithm.
    Uses jitter to separate overlapping points, and a table below.
    results_detail = {name: (value, weight)}
    """
    import random as _rnd
    _rnd.seed(0)

    fig, (ax, ax_tbl) = plt.subplots(2, 1, figsize=(9, 9),
                                      gridspec_kw={"height_ratios": [3, 1]})
    fig.suptitle(f"{knapsack.name} — Weight vs Value per Algorithm",
                 fontsize=13, fontweight="bold")

    # Offsets for label placement to avoid overlap
    label_offsets = {
        "Greedy Det":    (-60, -14),
        "Greedy NonDet": (-70,   8),
        "LS First":      (  6,   6),
        "LS Best":       (  6, -14),
        "SA":            (  6,   6),
        "Genetic":       (  6, -14),
    }

    plotted = {}  # track (wt, val) already plotted to jitter duplicates
    for name, (val, wt) in results_detail.items():
        color = COLORS.get(name, "#888")
        # small jitter if same coords as a previous point
        jx, jy = 0, 0
        for pw, pv in plotted.values():
            if abs(wt - pw) < 0.5 and abs(val - pv) < 0.5:
                jx = _rnd.uniform(-0.3, 0.3)
                jy = _rnd.uniform(-0.5, 0.5)
                break
        plotted[name] = (wt + jx, val + jy)
        ax.scatter(wt + jx, val + jy, s=220, color=color, edgecolors="white",
                   linewidth=1.8, zorder=4, label=name)
        ox, oy = label_offsets.get(name, (6, 6))
        ax.annotate(name, (wt + jx, val + jy), fontsize=9, fontweight="bold",
                    color=color, xytext=(ox, oy), textcoords="offset points")

    ax.axvline(x=knapsack.capacity, color="red", linestyle="--", linewidth=1.5,
               label=f"Capacity = {knapsack.capacity}", alpha=0.7)
    ax.set_xlabel("Total Weight Used", fontsize=11)
    ax.set_ylabel("Total Value Obtained", fontsize=11)
    ax.yaxis.grid(True, alpha=0.3)
    ax.xaxis.grid(True, alpha=0.3)

    # Add margin so labels don't get clipped
    all_wts = [wt for (_, wt) in results_detail.values()]
    all_vals = [val for (val, _) in results_detail.values()]
    ax.set_xlim(min(all_wts) - 5, max(max(all_wts), knapsack.capacity) + 8)
    ax.set_ylim(min(all_vals) - 10, max(all_vals) + 15)

    # ── Summary table below the plot ──────────────────────────────────────
    ax_tbl.axis("off")
    col_labels = ["Algorithm", "Value", "Weight Used", "Capacity Used %"]
    rows = []
    best_val = max(v for (v, _) in results_detail.values())
    for name in ALG_ORDER:
        if name not in results_detail:
            continue
        val, wt = results_detail[name]
        pct = f"{100*wt/knapsack.capacity:.1f}%"
        star = " ★" if val == best_val else ""
        rows.append([f"{name}{star}", str(val), str(wt), pct])

    tbl = ax_tbl.table(cellText=rows, colLabels=col_labels,
                       loc="center", cellLoc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(10)
    tbl.scale(1, 1.6)
    # Color header
    for j in range(len(col_labels)):
        tbl[0, j].set_facecolor("#333333")
        tbl[0, j].set_text_props(color="white", fontweight="bold")
    # Color best rows
    for i, name in enumerate([n for n in ALG_ORDER if n in results_detail], start=1):
        val, _ = results_detail[name]
        if val == best_val:
            for j in range(len(col_labels)):
                tbl[i, j].set_facecolor("#fff3cd")

    fig.tight_layout()
    return _save(fig, filename)
