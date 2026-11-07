"""Compare Robo Router heuristics and draw the best route from each search."""
import argparse
from contextlib import redirect_stdout
import csv
import io
import itertools
import math
import os
from pathlib import Path
import random
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from algorithm2.aco import aco
from algorithm2.alns import alns
from algorithm2.ga import ga
from algorithm2.greedy import run_greedy
from algorithm2.prepare_reduced_graph import prepare_data, generate_graph
from algorithm2.route_evaluation import evaluate_route
from algorithm2.vns import vns
from data_reader import read_data, PointType
from postprocessing.complete_solution import create_complete_sol

BUDGET = 40040
METHODS = ("GREEDY", "ALNS", "VNS", "ACO", "GA")
SEEDS = (11, 22, 33, 44, 55)
CHECKPOINTS = (2040, 10040, BUDGET)
COLORS = dict(zip(METHODS, ("black", "tab:blue", "tab:orange", "tab:green", "tab:red")))


def benchmark(case, seeds_by_method):
    rows, stops, starts = read_data(case)
    depot = starts[0]
    prepare_data(depot, stops, rows)
    graph, costs, paths = generate_graph(depot, stops)
    initial = run_greedy(depot, graph, costs)
    _, baseline_route, baseline = evaluate_route(initial, stops, costs, paths)
    assert sum(point.type == PointType.SAMPLE for point in baseline_route) == len(stops)
    best_routes, summaries, curves = {}, [], {}

    for method, seeds in seeds_by_method.items():
        for seed in seeds:
            random.seed(seed)
            np.random.seed(seed)
            trace = []
            if method == "GREEDY":
                route, score, counts = baseline_route, baseline, [0]
                trace = [baseline]
            elif method == "ALNS":
                with redirect_stdout(io.StringIO()):
                    route, score, _, trend, _ = alns(depot, stops, graph, costs, paths,
                                                     max_evaluations=BUDGET)
                trace = trend[2][1:]
                counts = range(1, BUDGET + 1)
            elif method == "VNS":
                route, score, _ = vns(depot, stops, graph, costs, paths,
                                      max_evaluations=BUDGET, on_evaluation=trace.append)
                counts = range(1, BUDGET + 1)
            elif method == "ACO":
                order, score, _, trend = aco(depot, graph, stops, costs, paths, initial, BUDGET // 20, 20)
                route, verified = create_complete_sol([graph[i] for i in order], costs, paths)
                assert math.isclose(verified, score)
                trace = trend[1]
                counts = range(20, BUDGET + 1, 20)
            else:
                order, score, *_ = ga(costs, initial, stops, paths, (BUDGET - 40) // 20, 40, 0.1,
                                       on_iteration=lambda best, _: trace.append(best))
                route, verified = create_complete_sol(order, costs, paths)
                assert math.isclose(verified, score)
                counts = range(40, BUDGET + 1, 20)

            assert len(counts) == len(trace) and math.isclose(trace[-1], score)
            assert route[0].id == route[-1].id == 0
            order_ids = [point.id for point in route if point.type == PointType.SAMPLE]
            assert sorted(order_ids) == list(range(1, len(graph)))
            reduced_order = [graph[0]] + [graph[i] for i in order_ids]
            assert math.isclose(create_complete_sol(reduced_order, costs, paths)[1], score)
            assert all(a >= b for a, b in itertools.pairwise(trace))
            reduction = 100 * (baseline - score) / baseline
            for checkpoint in CHECKPOINTS:
                checkpoint_cost = baseline if method == "GREEDY" else trace[counts.index(checkpoint)]
                summaries.append((case, method, seed, checkpoint, baseline, checkpoint_cost,
                                  100 * (baseline - checkpoint_cost) / baseline))
            curves[method, seed] = (counts, trace)
            if method not in best_routes or score < best_routes[method][0]:
                best_routes[method] = score, route
            print(case, method, seed, f"{reduction:.2f}%", flush=True)

    return rows, depot, baseline, best_routes, summaries, curves



def save(fig, folder, name):
    for extension in ("svg", "png"):
        fig.savefig(folder / f"{name}.{extension}", dpi=180, facecolor="white")
    plt.close(fig)


def plot_convergence(case, folder, baseline, curves):
    fig, ax = plt.subplots(figsize=(10, 4.7), layout="constrained")
    x = np.arange(0, BUDGET + 1, 20)
    for method in METHODS:
        series = []
        for seed in SEEDS:
            counts, trace = curves[method, seed]
            indices = np.searchsorted(counts, x, side="right") - 1
            scores = np.where(indices >= 0, np.array(trace)[indices], baseline)
            series.append(100 * (baseline - scores) / baseline)
        ax.step(x, np.median(series, axis=0), where="post", label=method,
                color=COLORS[method], linewidth=2)
    ax.set(xlabel="Route evaluations", ylabel="Median best cost reduction (%)")
    ax.axvline(10040, linestyle=":", color="0.45")
    ax.grid(color="0.88", linewidth=.7)
    ax.legend(frameon=True, facecolor="white", edgecolor="none", ncol=5, loc="lower right")
    ax.set_title(f"{case.rsplit('_', 1)[-1]} sampling stops", loc="left")
    save(fig, folder, "method-convergence")


def plot_routes(folder, rows, depot, baseline, routes):
    fig = plt.figure(figsize=(12, 5.35), layout="constrained")
    grid = fig.add_gridspec(2, 6)
    positions = ((0, 0), (0, 2), (0, 4), (1, 1), (1, 3))
    x0, y0 = depot.x, depot.y
    field_points = [point for row in rows for point in (row.a, row.b)]
    route_points = [point for _, route in routes.values() for point in route]
    all_points = field_points + route_points
    limits = []
    for axis, origin in (("x", x0), ("y", y0)):
        offsets = [getattr(point, axis) - origin for point in all_points]
        limits.append((min(offsets), max(offsets)))
    for method, (row_index, col_index) in zip(METHODS, positions):
        ax = fig.add_subplot(grid[row_index, col_index:col_index + 2])
        score, route = routes[method]
        for row in rows:
            ax.plot([row.a.x-x0, row.b.x-x0], [row.a.y-y0, row.b.y-y0], color=".83", linewidth=.55)
        ax.plot([p.x-x0 for p in route], [p.y-y0 for p in route], color=COLORS[method], linewidth=1.15)
        stops = [p for p in route if p.type == PointType.SAMPLE]
        ax.scatter([p.x-x0 for p in stops], [p.y-y0 for p in stops], color="black", s=8, zorder=3)
        ax.scatter(0, 0, facecolor="white", edgecolor="black", marker="D", s=29, zorder=4)
        gain = 100 * (baseline - score) / baseline
        ax.set_title(f"{method}   {score:,.1f}   ({gain:.2f}%)", fontsize=13, pad=5)
        for setter, (low, high) in zip((ax.set_xlim, ax.set_ylim), limits):
            padding = (high - low) * .035
            setter(low - padding, high + padding)
        ax.set_aspect("equal")
        ax.set_axis_off()
    save(fig, folder, "all-routes")


def write_results(folder, summaries, curves):
    with (folder / "checkpoint-results.csv").open("w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(("dataset", "method", "seed", "evaluation_checkpoint",
                         "greedy_cost", "route_cost", "reduction_pct"))
        writer.writerows(summaries)

    with (folder / "convergence.csv").open("w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(("method", "seed", "evaluations", "best_cost"))
        for (method, seed), (counts, trace) in curves.items():
            writer.writerows((method, seed, n, cost) for n, cost in zip(counts, trace))


def read_replay(folder):
    winners = {}
    curves = {}
    with (folder / "checkpoint-results.csv").open(newline="") as file:
        for row in csv.DictReader(file):
            if int(row["evaluation_checkpoint"]) == BUDGET:
                method = row["method"]
                candidate = (float(row["route_cost"]), int(row["seed"]))
                winners[method] = min(candidate, winners.get(method, candidate))
    with (folder / "convergence.csv").open(newline="") as file:
        for row in csv.DictReader(file):
            counts, trace = curves.setdefault((row["method"], int(row["seed"])), ([], []))
            counts.append(int(row["evaluations"]))
            trace.append(float(row["best_cost"]))
    return winners, curves


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("benchmark-output"))
    parser.add_argument("--case", choices=("with_elev_10", "with_elev_50"))
    parser.add_argument("--replay", action="store_true", help="rerun only the winning seeds from existing results")
    args = parser.parse_args()
    output = args.output.resolve()
    os.chdir(ROOT)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12, "text.color": "black"})
    for case in ([args.case] if args.case else ("with_elev_10", "with_elev_50")):
        folder = output / case
        folder.mkdir(parents=True, exist_ok=True)
        if args.replay:
            winners, curves = read_replay(folder)
            selected = {method: (winners[method][1],) for method in METHODS}
            rows, depot, baseline, routes, _, _ = benchmark(case, selected)
            for method in METHODS:
                assert math.isclose(routes[method][0], winners[method][0]), method
        else:
            selected = {method: SEEDS for method in METHODS}
            rows, depot, baseline, routes, summaries, curves = benchmark(case, selected)
            write_results(folder, summaries, curves)
        plot_convergence(case, folder, baseline, curves)
        plot_routes(folder, rows, depot, baseline, routes)


if __name__ == "__main__":
    main()
