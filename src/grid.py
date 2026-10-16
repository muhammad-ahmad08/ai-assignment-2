# Handles the 2D map, hazards, and no-fly zones

import numpy as np
import matplotlib.pyplot as plt


class DisasterGrid:
    def __init__(self, width=100, height=100):
        """Initializes a uniform 2D grid matrix for UAV simulation."""
        self.width = width
        self.height = height

        # State representations
        self.NORMAL = 0
        self.NO_FLY = 1
        self.PRIORITY = 2
        self.HAZARD = 3

        # Create a clean matrix filled with zeros
        self.matrix = np.zeros((self.height, self.width), dtype=int)

    def add_no_fly_zone(self, top_left_x, top_left_y, width, height):
        """Places a rectangular block representing a building or restricted airspace."""
        self.matrix[top_left_y: top_left_y + height, top_left_x: top_left_x + width] = self.NO_FLY

    def add_hazard_zone(self, top_left_x, top_left_y, width, height):
        """Places a rectangular block representing wind/radiation pockets."""
        self.matrix[top_left_y: top_left_y + height, top_left_x: top_left_x + width] = self.HAZARD

    def add_priority_target(self, x, y, radius=2):
        """Places a specific point of interest (e.g., trapped victims) with a small radius."""
        for i in range(max(0, x - radius), min(self.width, x + radius + 1)):
            for j in range(max(0, y - radius), min(self.height, y + radius + 1)):
                # Only overwrite normal cells so we don't accidentally erase a No-Fly building
                if self.matrix[j, i] == self.NORMAL:
                    self.matrix[j, i] = self.PRIORITY

    def is_valid_coordinate(self, x, y):
        """Checks if a coordinate is within bounds and not a No-Fly zone."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.matrix[y, x] != self.NO_FLY
        return False

    def visualize_grid(self):
        """Plots the current grid status using Matplotlib."""
        plt.figure(figsize=(8, 8))

        # Define a custom discrete color map: Normal(White), No-Fly(Red), Priority(Green), Hazard(Orange)
        from matplotlib.colors import ListedColormap
        cmap = ListedColormap(['#FFFFFF', '#D32F2F', '#388E3C', '#F57C00'])

        plt.imshow(self.matrix, cmap=cmap, origin='lower')
        plt.colorbar(ticks=[0, 1, 2, 3], label="Cell Status (0: Normal, 1: No-Fly, 2: Priority, 3: Hazard)")
        plt.title("Disaster Surveillance Sector Grid")
        plt.xlabel("X Coordinates")
        plt.ylabel("Y Coordinates")
        plt.grid(True, which='both', color='gray', linestyle='-', linewidth=0.5, alpha=0.3)
        plt.show()
