# Defines the Drone and Chromosome structures

import numpy as np
import random

class DroneGene:
    def __init__(self, num_waypoints=10, grid_width=100, grid_height=100):
        """
        Represents the flight data ('DNA') for a single UAV.
        """
        self.num_waypoints = num_waypoints
        self.grid_width = grid_width
        self.grid_height = grid_height
        
        # 1. Waypoints: Multi-segment real-valued spatial coordinates (X, Y)
        # Starting from a random point or a home base (e.g., 0,0)
        self.waypoints = np.zeros((num_waypoints, 2), dtype=float)
        self.initialize_random_path()
        
        # 2. Speeds: Float array matching transitions (e.g., speed between 1.0 and 5.0 m/s)
        self.speeds = np.random.uniform(1.0, 5.0, size=num_waypoints)
        
        # 3. Sensor Profile: Binary string (1 = Sensor Active, 0 = Power Saving)
        self.sensors = np.random.randint(0, 2, size=num_waypoints)

    def initialize_random_path(self):
        """Generates a random path within grid constraints."""
        current_x = random.uniform(0, self.grid_width - 1)
        current_y = random.uniform(0, self.grid_height - 1)
        self.waypoints[0] = [current_x, current_y]
        
        for i in range(1, self.num_waypoints):
            # Drones move relative to their last location to keep paths physically plausible
            max_step = 15.0 
            dx = random.uniform(-max_step, max_step)
            dy = random.uniform(-max_step, max_step)
            
            next_x = np.clip(current_x + dx, 0, self.grid_width - 1)
            next_y = np.clip(current_y + dy, 0, self.grid_height - 1)
            
            self.waypoints[i] = [next_x, next_y]
            current_x, current_y = next_x, next_y


class FleetChromosome:
    def __init__(self, num_drones=3, num_waypoints=10, grid_width=100, grid_height=100):
        """
        A complete candidate solution containing data for the whole fleet of UAVs.
        """
        self.num_drones = num_drones
        self.drones = [DroneGene(num_waypoints, grid_width, grid_height) for _ in range(num_drones)]
        self.fitness = 0.0  # Will be calculated and set during Step 4

    def copy(self):
        """Creates a deep copy of the chromosome for genetic operations."""
        duplicate = FleetChromosome(self.num_drones, self.drones[0].num_waypoints, 
                                     self.drones[0].grid_width, self.drones[0].grid_height)
        for i in range(self.num_drones):
            duplicate.drones[i].waypoints = np.copy(self.drones[i].waypoints)
            duplicate.drones[i].speeds = np.copy(self.drones[i].speeds)
            duplicate.drones[i].sensors = np.copy(self.drones[i].sensors)
        duplicate.fitness = self.fitness
        return duplicate
