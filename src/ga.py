# The core Genetic Algorithm loop (selection, crossover, mutation)

import random
import numpy as np
from src.drone import FleetChromosome

class GeneticAlgorithmEngine:
    def __init__(self, grid, evaluator, pop_size=50, mutation_rate=0.15, tournament_size=4):
        self.grid = grid
        self.evaluator = evaluator
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        
        # Initialize an initial randomized population pool
        self.population = [FleetChromosome(num_drones=3, num_waypoints=12, 
                                            grid_width=grid.width, grid_height=grid.height) 
                           for _ in range(self.pop_size)]
        self.evaluate_population()

    def evaluate_population(self):
        """Scores every individual within the current population pool."""
        for individual in self.population:
            self.evaluator.evaluate_fleet(individual, self.grid)

    def selection_tournament(self):
        """Selects the strongest individual from a random sample pool."""
        tournament_pool = random.sample(self.population, self.tournament_size)
        best_individual = max(tournament_pool, key=lambda ind: ind.fitness)
        return best_individual.copy()

    def crossover(self, parent1, parent2):
        """
        Performs structural crossover by swapping flight segment data 
        between matching drone profiles.
        """
        child1 = parent1.copy()
        child2 = parent2.copy()
        
        for d_idx in range(parent1.num_drones):
            if random.random() < 0.7:  # 70% Crossover rate
                # Select a split index along the waypoint sequence length
                num_wps = parent1.drones[d_idx].num_waypoints
                split = random.randint(1, num_wps - 2)
                
                # Swap Waypoint Coordinates
                child1.drones[d_idx].waypoints[split:] = parent2.drones[d_idx].waypoints[split:]
                child2.drones[d_idx].waypoints[split:] = parent1.drones[d_idx].waypoints[split:]
                
                # Swap Speed vectors
                child1.drones[d_idx].speeds[split:] = parent2.drones[d_idx].speeds[split:]
                child2.drones[d_idx].speeds[split:] = parent1.drones[d_idx].speeds[split:]
                
                # Swap Sensor tracking profiles
                child1.drones[d_idx].sensors[split:] = parent2.drones[d_idx].sensors[split:]
                child2.drones[d_idx].sensors[split:] = parent1.drones[d_idx].sensors[split:]
                
        return child1, child2

    def mutate(self, chromosome):
        """Applies spatial and parameter mutation based on the mutation rate."""
        for drone in chromosome.drones:
            for i in range(drone.num_waypoints):
                if random.random() < self.mutation_rate:
                    # 1. Spatial Mutation: Nudge X,Y coordinates slightly via Gaussian distribution
                    nudge_x = np.random.normal(0, 4.0)
                    nudge_y = np.random.normal(0, 4.0)
                    
                    drone.waypoints[i, 0] = np.clip(drone.waypoints[i, 0] + nudge_x, 0, drone.grid_width - 1)
                    drone.waypoints[i, 1] = np.clip(drone.waypoints[i, 1] + nudge_y, 0, drone.grid_height - 1)
                    
                    # 2. Speed Mutation: Alter velocity metrics slightly
                    drone.speeds[i] = np.clip(drone.speeds[i] + np.random.normal(0, 0.5), 1.0, 5.0)
                    
                    # 3. Sensor Mutation: Flip binary activation profile
                    drone.sensors[i] = 1 - drone.sensors[i]

    def evolve_one_generation(self):
        """Executes a full cycle generation shift (Selection -> Crossover -> Mutation)."""
        new_population = []
        
        # Elitism: Preserve the single best solution from the previous generation
        best_of_all = max(self.population, key=lambda ind: ind.fitness)
        new_population.append(best_of_all.copy())
        
        while len(new_population) < self.pop_size:
            # Selection
            p1 = self.selection_tournament()
            p2 = self.selection_tournament()
            
            # Crossover
            c1, c2 = self.crossover(p1, p2)
            
            # Mutation
            self.mutate(c1)
            self.mutate(c2)
            
            new_population.append(c1)
            if len(new_population) < self.pop_size:
                new_population.append(c2)
                
        self.population = new_population
        self.evaluate_population()
