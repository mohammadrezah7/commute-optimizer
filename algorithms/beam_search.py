"""
algorithms/beam_search.py
Local Beam Search maintaining K parallel candidate states.
"""

import random
from typing import Tuple
from algorithms.base import LocalSearchSolver
from core.state import State
from core.problem import CommuteProblem
from algorithms.operators import get_neighbors, random_path


class LocalBeamSearchSolver(LocalSearchSolver):
    def __init__(self, problem: CommuteProblem, **kwargs):
        super().__init__(problem, **kwargs)
        self.beam_width: int = self.params.get("beam_width", 5)
        self.max_iterations: int = self.params.get("max_iterations", 150)

    def random_start(self) -> State:
        path = random_path(self.problem, self.problem.origin, self.problem.destination, set())
        departure = random.choice(self.problem.get_valid_time_domain())
        return State(tuple(path), departure)

    def solve(self) -> Tuple[State, float]:
        """
        Executes Local Beam Search.

        Guidelines:
        - Maintain a set of `beam_width` parallel configurations.
        - In each iteration, generate neighbors from all active states in the beam.
        - Pool and rank all generated successors collectively, then retain the top `beam_width` states.
        - Halt when the beam ceases to improve or reaches max_iterations.
        - Record the best cost of the population at each step in self.history.

        Encouraged:
        - Ensuring diversity across states in the beam to prevent collapse into a single redundant path.

        Prohibited:
        - Treating this as K independent, non-communicating searches.
        """
        # TODO: Implement Local Beam Search
        beam = [self.problem.generate_initial_state()]
        while len(beam) < self.beam_width:
            beam.append(self.random_start())

        best_state = min(beam, key=self.problem.evaluate)
        best_cost = self.problem.evaluate(best_state)
        self.history.append(best_cost)

        for _ in range(self.max_iterations):
            pool = []
            for state in beam:
                for neighbor in get_neighbors(state, self.problem):
                    if neighbor not in pool:
                        pool.append(neighbor)

            random.shuffle(pool)
            pool.sort(key=self.problem.evaluate)
            beam = pool[:self.beam_width]

            top_cost = self.problem.evaluate(beam[0])
            if top_cost < best_cost - 1e-9:
                best_state = beam[0]
                best_cost = top_cost
                self.history.append(best_cost)
            else:
                self.history.append(best_cost)
                break

        return best_state, best_cost