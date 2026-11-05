"""
algorithms/genetic_algorithm.py
Population-based optimization using selection, recombination, and mutation.
"""

import random
from typing import Tuple
from algorithms.base import LocalSearchSolver
from core.state import State
from core.problem import CommuteProblem
from algorithms.operators import get_neighbors, crossover, random_path


class GeneticAlgorithmSolver(LocalSearchSolver):
    def __init__(self, problem: CommuteProblem, **kwargs):
        super().__init__(problem, **kwargs)
        self.population_size: int = self.params.get("population_size", 30)
        self.generations: int = self.params.get("generations", 100)
        self.crossover_rate: float = self.params.get("crossover_rate", 0.8)
        self.mutation_rate: float = self.params.get("mutation_rate", 0.2)
        self.elitism: int = self.params.get("elitism", 2)

    def random_start(self) -> State:
        path = random_path(self.problem, self.problem.origin, self.problem.destination, set())
        departure = random.choice(self.problem.get_valid_time_domain())
        return State(tuple(path), departure)

    def tournament(self, population, costs) -> State:
        best = random.randrange(len(population))
        for _ in range(2):
            other = random.randrange(len(population))
            if costs[other] < costs[best]:
                best = other
        return population[best]

    def solve(self) -> Tuple[State, float]:
        """
        Executes Genetic Algorithm optimization.

        Guidelines:
        - Initialize a population of valid candidate solutions.
        - Design a fitness metric suitable for minimizing commute travel time (lower cost -> higher fitness).
        - Use selection operators (such as tournament or roulette selection) to pick parents.
        - Pair parents to produce offspring via `crossover()`, and apply stochastic mutation.
        - Preserve the top candidates across generations if using elitism.
        - Track best population performance per generation in self.history.

        Encouraged:
        - Experimenting with population size, selection pressure, and operator rates to balance exploration vs. exploitation.
        """
        # TODO: Implement Genetic Algorithm
        population = [self.problem.generate_initial_state()]
        while len(population) < self.population_size:
            population.append(self.random_start())

        best_state = min(population, key=self.problem.evaluate)
        best_cost = self.problem.evaluate(best_state)
        self.history.append(best_cost)

        for _ in range(self.generations):
            population.sort(key=self.problem.evaluate)
            costs = [self.problem.evaluate(state) for state in population]

            next_population = population[:self.elitism]
            while len(next_population) < self.population_size:
                parent1 = self.tournament(population, costs)
                parent2 = self.tournament(population, costs)

                if random.random() < self.crossover_rate:
                    child = crossover(parent1, parent2, self.problem)
                else:
                    child = parent1

                if random.random() < self.mutation_rate:
                    child = random.choice(get_neighbors(child, self.problem))

                next_population.append(child)

            population = next_population

            top = min(population, key=self.problem.evaluate)
            top_cost = self.problem.evaluate(top)
            if top_cost < best_cost - 1e-9:
                best_state = top
                best_cost = top_cost
            self.history.append(best_cost)

        return best_state, best_cost