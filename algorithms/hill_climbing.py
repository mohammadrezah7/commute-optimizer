"""
algorithms/hill_climbing.py
Hill Climbing search with sideways move limits and random restarts.
"""

import random
from typing import Tuple
from algorithms.base import LocalSearchSolver
from core.state import State
from core.problem import CommuteProblem
from algorithms.operators import get_neighbors, random_path


class HillClimbingSolver(LocalSearchSolver):
    def __init__(self, problem: CommuteProblem, **kwargs):
        super().__init__(problem, **kwargs)
        self.max_sideways: int = self.params.get("max_sideways", 100)
        self.max_restarts: int = self.params.get("max_restarts", 5)

    def random_start(self) -> State:
        path = random_path(self.problem, self.problem.origin, self.problem.destination, set())
        departure = random.choice(self.problem.get_valid_time_domain())
        return State(tuple(path), departure)

    def solve(self) -> Tuple[State, float]:
        """
        Executes Hill Climbing optimization.

        Guidelines:
        - Search through the neighborhood greedily for candidates that minimize total travel time.
        - Handle flat local maxima / shoulders by allowing up to `max_sideways` non-improving steps.
        - Apply up to `max_restarts` to explore different starting basins.
        - Track the best objective cost seen at each major step in self.history.

        Prohibited:
        - Looping indefinitely on flat plateaus.
        """
        # TODO: Implement Hill Climbing with sideways moves and restarts
        best_state = self.problem.generate_initial_state()
        best_cost = self.problem.evaluate(best_state)
        self.history.append(best_cost)

        for restart in range(self.max_restarts + 1):
            if restart == 0:
                current = best_state
            else:
                current = self.random_start()
            current_cost = self.problem.evaluate(current)
            if current_cost < best_cost:
                best_state = current
                best_cost = current_cost
            sideways = 0

            while True:
                neighbors = get_neighbors(current, self.problem)
                costs = [self.problem.evaluate(n) for n in neighbors]
                lowest = min(costs)

                if lowest < current_cost - 1e-9:
                    sideways = 0
                elif lowest <= current_cost + 1e-9 and sideways < self.max_sideways:
                    sideways += 1
                else:
                    break

                candidates = [n for n, c in zip(neighbors, costs) if c <= lowest + 1e-9]
                current = random.choice(candidates)
                current_cost = self.problem.evaluate(current)
                if current_cost < best_cost:
                    best_state = current
                    best_cost = current_cost
                self.history.append(best_cost)

        return best_state, best_cost