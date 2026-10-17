# Main script to run the simulation

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
    
    print("Beginning Evolution Framework Pipeline...")
    
    for gen in range(1, generations + 1):
        ga_engine.evolve_one_generation()
        
        # Extract performance monitoring statistics
        best_ind = max(ga_engine.population, key=lambda ind: ind.fitness)
        avg_fitness = sum(ind.fitness for ind in ga_engine.population) / len(ga_engine.population)
        
        if gen == 1 or gen % 10 == 0:
            print(f"Generation {gen:02d} -> Best Fitness Score: {best_ind.fitness:.2f} | Average Population Fitness: {avg_fitness:.2f}")

    print("Evolution complete! Initial engine loops are functioning successfully.")

if __name__ == "__main__":
    main()
