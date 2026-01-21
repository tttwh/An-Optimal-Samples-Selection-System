# Project Report
# An Optimal Samples Selection System

---

## Group Information

| Role | Name | Student ID |
|------|------|------------|
| Member 1 | [Name] | [ID] |
| Member 2 | [Name] | [ID] |
| Member 3 | [Name] | [ID] |
| Member 4 | [Name] | [ID] |

**Group Number:** [To be assigned]

**Course:** CS360/SE360 Artificial Intelligence

---

## 1. Introduction

This project implements an **Optimal Samples Selection System** that solves a combinatorial optimization problem arising from group (sample) selection. The goal is to select as few groups as possible while ensuring every required subset is “covered” under a given overlap rule.

The delivered system includes:

- A **core optimization solver** implemented in Python.
- A **desktop GUI** (PyQt5) for parameter input, running the solver, and inspecting results.
- A **SQLite-based persistence layer** to save and manage computed results.

## 2. Problem Definition

Given:

- A total sample pool size `m` (samples labeled `1..m`).
- A chosen set of `n` distinct samples `S` (either selected randomly or entered manually).
- Integers `k, j, s` with constraints `s <= j <= k`, and typical assignment constraints `4 <= k <= 7`, `3 <= s <= 7`.

We must output a collection of **k-groups** (each is a size-`k` subset of `S`) such that:

- For every **j-subset** `T` of `S`, at least one selected k-group `G` satisfies:

  `|T ∩ G| >= s`.

Objective:

- Minimize the number of selected k-groups.

This can be viewed as a **set cover** variant where each k-group “covers” the j-subsets it sufficiently overlaps.

## 3. Mathematical Formulation (ILP)

Let:

- `U` be the set of all j-subsets of `S`. `|U| = C(n, j)`.
- `K` be the set of all candidate k-groups of `S`. `|K| = C(n, k)`.
- `cover(i, g)` be 1 if k-group `g` covers j-subset `i`, i.e., `|i ∩ g| >= s`, otherwise 0.

Decision variables:

- For each candidate k-group `g ∈ K`, define a binary variable `x_g ∈ {0,1}` indicating whether `g` is selected.

Objective:

- Minimize `Σ_{g∈K} x_g`.

Constraints:

- For every `i ∈ U`, ensure it is covered by at least one selected k-group:

  `Σ_{g∈K} cover(i, g) * x_g >= 1`.

This ILP guarantees optimality when solved to optimality.

## 4. System Architecture

Repository modules:

- `main.py`: application entry point.
- `core/solver.py`: optimization solver (ILP + fallbacks).
- `gui/main_window.py`: PyQt5 desktop interface.
- `database/db_manager.py`: SQLite persistence for results.
- `results/`: saved SQLite database files.
- `docs/`: documentation (User Manual, this Project Report).

High-level data flow:

1. User selects parameters (`m, n, k, j, s`) and a sample set `S`.
2. The GUI creates an `OptimalSamplesSolver` with (`n, k, j, s, S`).
3. The solver generates:
   - All j-subsets (`C(n,j)`) and candidate k-groups (`C(n,k)`),
   - A coverage matrix indicating which k-groups cover which j-subsets.
4. An ILP is built and solved (OR-Tools CP-SAT by default).
5. Selected k-groups are displayed and can be saved to SQLite.

## 5. Key Implementation Details

### 5.1 Coverage Matrix Construction

In `core/solver.py`, the solver enumerates:

- `j_subsets = combinations(samples, j)`
- `k_groups  = combinations(samples, k)`

Then for each pair `(j_subset, k_group)`, it checks whether the overlap size is at least `s`.

This creates a boolean matrix of size `C(n,j) × C(n,k)`. While straightforward and reliable, it can grow quickly as `n` increases.

### 5.2 ILP Solving Strategy

The method `solve_ilp()` tries solvers in the following order:

1. **OR-Tools CP-SAT** (preferred; fast and reliable for many instances).
2. **PuLP (CBC)** as a secondary option.
3. A custom **Branch and Bound** fallback.

A 5-minute time limit is set for OR-Tools and PuLP to keep the GUI responsive on larger instances.

### 5.3 GUI Responsiveness

The GUI uses a background thread (`SolverThread`) to run the solver without blocking the main UI thread. This allows the interface to remain responsive while the optimization runs.

### 5.4 Result Persistence (SQLite)

Results are stored as individual SQLite files under `results/` using a naming convention:

`{m}-{n}-{k}-{j}-{s}-{run}-{num_groups}.db`

Each DB contains:

- `metadata`: parameters, selected samples, solve time, method, timestamp, number of groups.
- `groups`: the selected k-groups, stored as JSON arrays.

## 6. Validation and Example

The solver includes a `verify_solution()` routine that checks every j-subset is covered by the selected groups according to the overlap rule.

Example (small instance):

- `n=7, k=4, j=3, s=3`, samples `1..7`
- The implementation can find a feasible/optimal solution and verify it as valid.

Note: Runtime and memory usage grow rapidly with `C(n,j)` and `C(n,k)`. Larger `n` values may require longer solve times, tighter constraints, or additional optimization techniques.

## 7. Limitations and Future Work

- **Scalability**: enumerating all k-groups and all j-subsets can become expensive for larger `n`.
- **Heuristics**: add a fast greedy or local-search heuristic to produce good solutions quickly, then optionally refine with ILP.
- **Model improvements**: symmetry breaking, column generation, or lazy constraint generation could reduce model size.
- **Export**: support exporting results to CSV/JSON and adding a report-friendly output format.
- **Mobile adaptation** (optional): a mobile version is not included in this repository; it can be implemented as an extension.

## 8. Conclusion

This project delivers an end-to-end system that models the optimal sample group selection problem as an ILP and solves it using OR-Tools, while providing a practical GUI and persistent storage for results. The design is modular, making it straightforward to extend with improved solving strategies, richer reporting, or additional platforms.

---

*Document Version: 1.0*

*Last Updated: January 2026*
