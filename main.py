# Main script to run the simulation

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from src.grid import DisasterGrid
from src.drone import FleetChromosome

def main():
    # 1. Setup our grid environment from Step-2
    grid = DisasterGrid(width=100, height=100)
    grid.add_no_fly_zone(20, 30, 15, 25)
    grid.add_no_fly_zone(65, 70, 20, 15)
    grid.add_hazard_zone(45, 10, 30, 20)
    grid.add_priority_target(15, 85, radius=3)
    grid.add_priority_target(80, 25, radius=4)
    grid.add_priority_target(50, 55, radius=3)
    
    # 2. Instantiate an initial candidate solution (A random chromosome representing 3 drones)
    fleet_solution = FleetChromosome(num_drones=3, num_waypoints=12, grid_width=100, grid_height=100)
    
    # 3. Setup Plotting
    plt.figure(figsize=(9, 9))
    cmap = ListedColormap(['#FFFFFF', '#D32F2F', '#388E3C', '#F57C00'])
    plt.imshow(grid.matrix, cmap=cmap, origin='lower', alpha=0.8)
    
    # Define colors for different drones in the fleet
    drone_colors = ['#1E88E5', '#D81B60', '#8E24AA']
    
    # 4. Plot each drone's waypoint path onto the matrix
    for idx, drone in enumerate(fleet_solution.drones):
        x_coords = drone.waypoints[:, 0]
        y_coords = drone.waypoints[:, 1]
        
        # Plot lines connecting waypoints
        plt.plot(x_coords, y_coords, color=drone_colors[idx], marker='o', linewidth=2, label=f"Drone {idx+1} Path")
        # Mark the start position
        plt.scatter(x_coords[0], y_coords[0], color='black', s=100, zorder=5)
        
    plt.title("Initial Random Flight Trajectories of Drone Fleet")
    plt.xlabel("X Coordinates")
    plt.ylabel("Y Coordinates")
    plt.legend()
    plt.grid(True, alpha=0.2)
    plt.show()

    # Print out a slice of internal chromosome data to verify structural health
    sample_drone = fleet_solution.drones[0]
    print("--- Drone 1 Chromosome Segment Data ---")
    print(f"Waypoints Shape: {sample_drone.waypoints.shape}")
    print(f"First Waypoint Coordinate: {sample_drone.waypoints[0]}")
    print(f"Speed Vector: {sample_drone.speeds[:3]}...")
    print(f"Sensor States Vector: {sample_drone.sensors[:3]}...")

if __name__ == "__main__":
    main()
