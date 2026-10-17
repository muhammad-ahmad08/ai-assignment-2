from src.grid import DisasterGrid
from src.drone import FleetChromosome
from src.fitness import EvaluationEngine

def main():
    # 1. Construct physical world
    grid = DisasterGrid(100, 100)
    grid.add_no_fly_zone(20, 30, 15, 25)
    grid.add_no_fly_zone(65, 70, 20, 15)
    grid.add_hazard_zone(45, 10, 30, 20)
    grid.add_priority_target(15, 85, radius=5)
    grid.add_priority_target(80, 25, radius=5)
    grid.add_priority_target(50, 55, radius=5)
    
    # 2. Build Evaluation Engine 
    evaluator = EvaluationEngine(max_battery=600.0)
    
    print("Testing Strategy Fitness Calculations...")
    
    # Generate 3 distinct sample configurations to compare scores
    for test_idx in range(1, 4):
        candidate = FleetChromosome(num_drones=3, num_waypoints=10, grid_width=100, grid_height=100)
        score = evaluator.evaluate_fleet(candidate, grid)
        print(f"Candidate Fleet Config #{test_idx} Calculated Fitness Score: {score:.2f}")

if __name__ == "__main__":
    main()
