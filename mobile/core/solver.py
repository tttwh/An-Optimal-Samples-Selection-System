"""core.solver

Optimal Samples Selection Solver.

Problem (informal):
Given a selected sample set S of size n, choose as few k-groups (size-k subsets of S)
as possible such that every j-subset T of S is "covered" by at least one chosen
k-group G with |T ∩ G| >= s.

This can be formulated as a set cover ILP and solved with OR-Tools (preferred)
or PuLP. If those solvers are unavailable, we fall back to an exact branch-and-
bound search.

Note: The search space grows quickly with n; practical instances on mobile
should use small n.
"""

from __future__ import annotations

from itertools import combinations
from typing import List, Tuple, Set, Optional, Callable
import time


class OptimalSamplesSolver:
    """Solver for the Optimal Samples Selection Problem."""

    def __init__(self, n: int, k: int, j: int, s: int, samples: List[int]):
        self.n = n
        self.k = k
        self.j = j
        self.s = s
        self.samples = sorted(samples)

        self._validate_parameters()

        # All j-subsets must be covered; all k-groups are candidate sets.
        self.j_subsets = list(combinations(self.samples, j))
        self.k_groups = list(combinations(self.samples, k))

        # Coverage relations.
        # subset_to_groups[i] = list of group indices that cover j-subset i
        # group_to_subsets[g] = set of j-subset indices covered by group g
        self.subset_to_groups, self.group_to_subsets = self._build_cover_relations()

    def _validate_parameters(self) -> None:
        if not (4 <= self.k <= 7):
            raise ValueError(f"k must be between 4 and 7, got {self.k}")
        if not (3 <= self.s <= 7):
            raise ValueError(f"s must be between 3 and 7, got {self.s}")
        if not (self.s <= self.j <= self.k):
            raise ValueError(f"Must have s <= j <= k, got s={self.s}, j={self.j}, k={self.k}")
        if len(self.samples) != self.n:
            raise ValueError(f"Expected {self.n} samples, got {len(self.samples)}")

    def _build_cover_relations(self) -> Tuple[List[List[int]], List[Set[int]]]:
        subset_to_groups: List[List[int]] = [[] for _ in range(len(self.j_subsets))]
        group_to_subsets: List[Set[int]] = [set() for _ in range(len(self.k_groups))]

        for i, j_subset in enumerate(self.j_subsets):
            j_set = set(j_subset)
            for g, k_group in enumerate(self.k_groups):
                # k,j are small (<=7), set intersection is fine here.
                if len(j_set.intersection(k_group)) >= self.s:
                    subset_to_groups[i].append(g)
                    group_to_subsets[g].add(i)

        # Early infeasibility check.
        for i, groups in enumerate(subset_to_groups):
            if not groups:
                raise ValueError(f"j-subset {i} cannot be covered by any k-group")

        return subset_to_groups, group_to_subsets

    def solve_ilp(
        self,
        progress_callback: Optional[Callable[[int, int, int], None]] = None,
        time_limit_seconds: float = 300.0,
        prefer_ortools: bool = True,
        allow_pulp: bool = True,
    ) -> Tuple[List[Tuple], float, str]:
        """Solve the instance.

        Returns:
            (selected_groups, solve_time, method_used)

        Method selection:
        - If prefer_ortools is True, try OR-Tools CP-SAT.
        - Otherwise, or if OR-Tools is unavailable, try PuLP.
        - Otherwise fall back to an exact Branch and Bound search.

        If time_limit_seconds is exceeded in the fallback search, a TimeoutError
        is raised.
        """

        start_time = time.time()

        if prefer_ortools:
            try:
                result = self._solve_with_ortools(time_limit_seconds=time_limit_seconds)
                method = "OR-Tools CP-SAT"
                return result, time.time() - start_time, method
            except ImportError:
                pass

        if allow_pulp:
            try:
                result = self._solve_with_pulp(time_limit_seconds=time_limit_seconds)
                method = "PuLP CBC"
                return result, time.time() - start_time, method
            except ImportError:
                pass

        # Exact fallback.
        result = self._solve_branch_and_bound(progress_callback=progress_callback, time_limit_seconds=time_limit_seconds)
        method = "Branch and Bound (Exact)"
        return result, time.time() - start_time, method

    def _solve_with_ortools(self, time_limit_seconds: float = 300.0) -> List[Tuple]:
        from ortools.sat.python import cp_model

        model = cp_model.CpModel()
        num_groups = len(self.k_groups)

        x = [model.NewBoolVar(f"x_{g}") for g in range(num_groups)]

        for i, covering_group_ids in enumerate(self.subset_to_groups):
            model.Add(sum(x[g] for g in covering_group_ids) >= 1)

        model.Minimize(sum(x))

        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = float(time_limit_seconds)

        status = solver.Solve(model)
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return [self.k_groups[g] for g in range(num_groups) if solver.Value(x[g]) == 1]
        raise RuntimeError("No solution found")

    def _solve_with_pulp(self, time_limit_seconds: float = 300.0) -> List[Tuple]:
        import pulp

        num_groups = len(self.k_groups)

        prob = pulp.LpProblem("OptimalSamplesSelection", pulp.LpMinimize)
        x = [pulp.LpVariable(f"x_{g}", cat="Binary") for g in range(num_groups)]

        prob += pulp.lpSum(x)

        for i, covering_group_ids in enumerate(self.subset_to_groups):
            prob += pulp.lpSum(x[g] for g in covering_group_ids) >= 1

        prob.solve(pulp.PULP_CBC_CMD(msg=0, timeLimit=float(time_limit_seconds)))

        if prob.status == pulp.LpStatusOptimal:
            return [self.k_groups[g] for g in range(num_groups) if pulp.value(x[g]) == 1]
        raise RuntimeError("No solution found")

    def _greedy_feasible_solution(self) -> List[int]:
        """Return a feasible solution (list of group indices) using a greedy heuristic."""
        uncovered: Set[int] = set(range(len(self.j_subsets)))
        selected: List[int] = []

        while uncovered:
            # Pick a most constrained subset, then choose a group that covers the most uncovered.
            target = min(uncovered, key=lambda i: len(self.subset_to_groups[i]))
            best_g = None
            best_gain = -1
            for g in self.subset_to_groups[target]:
                gain = len(self.group_to_subsets[g].intersection(uncovered))
                if gain > best_gain:
                    best_gain = gain
                    best_g = g

            if best_g is None or best_gain <= 0:
                # Should not happen due to infeasibility check in _build_cover_relations.
                raise RuntimeError("Failed to construct a feasible solution")

            selected.append(best_g)
            uncovered.difference_update(self.group_to_subsets[best_g])

        return selected

    def _solve_branch_and_bound(
        self,
        progress_callback: Optional[Callable[[int, int, int], None]] = None,
        time_limit_seconds: float = 300.0,
    ) -> List[Tuple]:
        """Exact Branch and Bound fallback.

        This method is used when ILP solvers are unavailable (e.g., mobile builds).
        It is guaranteed optimal if it finishes before time_limit_seconds.
        """

        start = time.time()
        num_subsets = len(self.j_subsets)

        # Initial upper bound from a greedy feasible solution.
        best_solution = self._greedy_feasible_solution()
        best_size = len(best_solution)

        global_max_cover = max((len(s) for s in self.group_to_subsets), default=0)
        if global_max_cover <= 0:
            raise RuntimeError("No solution found")

        def lower_bound(uncovered: Set[int]) -> int:
            # Safe (possibly loose) bound: each group can cover at most global_max_cover subsets.
            # Using a larger denominator makes the bound smaller => never overestimates.
            return (len(uncovered) + global_max_cover - 1) // global_max_cover

        def branch(selected: List[int], uncovered: Set[int], depth: int) -> None:
            nonlocal best_solution, best_size

            if time.time() - start > time_limit_seconds:
                raise TimeoutError(f"Branch and bound exceeded time limit ({time_limit_seconds}s)")

            if not uncovered:
                if len(selected) < best_size:
                    best_solution = selected.copy()
                    best_size = len(selected)
                return

            # Basic pruning.
            if len(selected) >= best_size:
                return

            if len(selected) + lower_bound(uncovered) >= best_size:
                return

            # Choose a most constrained uncovered subset.
            target = min(uncovered, key=lambda i: len(self.subset_to_groups[i]))

            # Try groups that cover target, best-first by gain.
            candidates = list(self.subset_to_groups[target])
            candidates.sort(key=lambda g: len(self.group_to_subsets[g].intersection(uncovered)), reverse=True)

            for g in candidates:
                gain = self.group_to_subsets[g].intersection(uncovered)
                if not gain:
                    continue

                new_uncovered = uncovered.difference(gain)
                branch(selected + [g], new_uncovered, depth + 1)

                if progress_callback and depth == 0:
                    progress_callback(depth, len(selected) + 1, best_size)

        uncovered0: Set[int] = set(range(num_subsets))
        branch([], uncovered0, 0)

        return [self.k_groups[g] for g in best_solution]

    def verify_solution(self, selected_groups: List[Tuple]) -> bool:
        for j_subset in self.j_subsets:
            j_set = set(j_subset)
            if not any(len(j_set.intersection(k_group)) >= self.s for k_group in selected_groups):
                return False
        return True

    def get_statistics(self) -> dict:
        return {
            "n": self.n,
            "k": self.k,
            "j": self.j,
            "s": self.s,
            "num_j_subsets": len(self.j_subsets),
            "num_k_groups": len(self.k_groups),
            "samples": self.samples,
        }
