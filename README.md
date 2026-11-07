# Robo Router

Robo Router plans soil-sampling routes for agricultural robots. The work comes from Stanislav Čeman's research internship at the BioSense Institute in the context of the EU Horizon 2020 [FlexiGroBots blueberry pilot](https://flexigrobots-h2020.eu/pilot-3-blueberries).

The nearest-neighbor greedy route supplies the benchmark baseline. The four search implementations share the route evaluator, which accounts for movement and turn penalties.

| Method | Implementation |
| --- | --- |
| Genetic algorithm (GA) | [ga.py](algorithm2/ga.py) combines route segments and mutates stop orders, starting from variations of the greedy route. |
| Ant colony optimization (ACO) | [aco.py](algorithm2/aco.py) builds routes using edge cost and pheromone and reinforces the strongest tours. |
| Variable neighborhood search (VNS) | [vns.py](algorithm2/vns.py) switches among neighborhoods of segment reversals with a fixed depot. |
| Adaptive large neighborhood search (ALNS) | [alns.py](algorithm2/alns.py) adapts operator weights and uses a cooling schedule to accept some higher-cost moves. |

## Benchmark

Run from the repository root with Python 3.10 or later.

```sh
python -m pip install numpy pandas matplotlib
python benchmarks/compare.py
```

The benchmark runs each search with five fixed seeds and about 40,000 route evaluations per run. It writes checkpoint results, convergence traces and maps to `benchmark-output/`. Use `--case with_elev_10` or `--case with_elev_50` for a single instance.

- **10 stops** · [Results](benchmarks/results/with_elev_10/checkpoint-results.csv) · [Convergence](benchmarks/results/with_elev_10/method-convergence.svg) · [All five routes](benchmarks/results/with_elev_10/all-routes.svg)
- **50 stops** · [Results](benchmarks/results/with_elev_50/checkpoint-results.csv) · [Convergence](benchmarks/results/with_elev_50/method-convergence.svg) · [All five routes](benchmarks/results/with_elev_50/all-routes.svg)
- [Portfolio presentation](benchmarks/Robo-Router-Portfolio.pptx)

The benchmark uses the supplied datasets. The presentation credits the FlexiGroBots field and greenhouse photos in the slide notes.
