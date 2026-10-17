# Main script to run the simulation

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from src.grid import DisasterGrid
from src.fitness import EvaluationEngine
from src.ga import GeneticAlgorithmEngine

def main():
    # 1. Initialize environment properties
    grid = DisasterGrid(100, 100)
    grid.add_no_fly_zone(20, 30, 15, 25)
    grid.add_no_fly_zone(65, 70, 20, 15)
    grid.add_hazard_zone(45, 10, 30, 20)
    grid.add_priority_target(15, 85, radius=4)
    grid.add_priority_target(80, 25, radius=4)
    grid.add_priority_target(50, 55, radius=4)
    
    # 2. Define operational metrics
    evaluator = EvaluationEngine(max_battery=700.0)
    
    # 3. Start Genetic Algorithm Engine
    generations = 50
    ga_engine = GeneticAlgorithmEngine(grid, evaluator, pop_size=40, mutation_rate=0.2)
    
    # Lists to store metrics for visualization
    best_history = []
    avg_history = []
    
    print("Beginning Evolution Framework Pipeline...")
    
    for gen in range(1, generations + 1):
        ga_engine.evolve_one_generation()
        
        # Calculate statistics
        best_ind = max(ga_engine.population, key=lambda ind: ind.fitness)
        avg_fitness = sum(ind.fitness for ind in ga_engine.population) / len(ga_engine.population)
        
        # Save history data
        best_history.append(best_ind.fitness)
        avg_history.append(avg_fitness)
        
        if gen == 1 or gen % 10 == 0:
            print(f"Generation {gen:02d} -> Best Fitness Score: {best_ind.fitness:.2f} | Average Population Fitness: {avg_fitness:.2f}")

    print("\nEvolution complete! Generating output visualizations...")

    # ==========================================
    # PLOT 1: FITNESS CONVERGENCE CURVE
    # ==========================================
    plt.figure(figsize=(10, 5))
    plt.plot(range(1, generations + 1), best_history, label='Best Fitness', color='#388E3C', linewidth=2.5)
    plt.plot(range(1, generations + 1), avg_history, label='Average Fitness', color='#1E88E5', linestyle='--', linewidth=1.5)
    plt.title('Genetic Algorithm Convergence Curve')
    plt.xlabel('Generations')
    plt.ylabel('Fitness Score')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig('fitness_convergence.png', dpi=300)
    print("-> Saved: fitness_convergence.png")
    plt.show()

    # ==========================================
    # PLOT 2: FINAL EVOLVED FLIGHT PATH MAP
    # ==========================================
    plt.figure(figsize=(9, 9))
    # Map colors: White (Normal), Red (No-Fly), Green (Priority Target), Orange (Hazard)
    cmap = ListedColormap(['#FFFFFF', '#D32F2F', '#388E3C', '#F57C00'])
    plt.imshow(grid.matrix, cmap=cmap, origin='lower', alpha=0.8)
    
    # Get the ultimate winner configuration from the final population
    best_overall_fleet = max(ga_engine.population, key=lambda ind: ind.fitness)
    drone_colors = ['#0D47A1', '#C2185B', '#4A148C'] # High contrast paths
    
    for idx, drone in enumerate(best_overall_fleet.drones):
        x_coords = drone.waypoints[:, 0]
        y_coords = drone.waypoints[:, 1]
        
        # Plot path lines
        plt.plot(x_coords, y_coords, color=drone_colors[idx], marker='o', markersize=6, linewidth=2, label=f"UAV {idx+1} Path")
        # Distinct star marker for start position
        plt.scatter(x_coords[0], y_coords[0], color='black', marker='*', s=150, zorder=5)

    plt.title(f"Optimized UAV Fleet Deployment Map (Fitness: {best_overall_fleet.fitness:.2f})")
    plt.xlabel("Grid X Coordinates")
    plt.ylabel("Grid Y Coordinates")
    plt.legend()
    plt.grid(True, alpha=0.15)
    plt.savefig('evolved_uav_paths.png', dpi=300)
    print("-> Saved: evolved_uav_paths.png")
    plt.show()

if __name__ == "__main__":
    main()
