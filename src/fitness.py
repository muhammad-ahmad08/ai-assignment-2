# This handles the geometric tracing of lines across your matrix cells and outputs the strategic score.

import numpy as np

class EvaluationEngine:
    def __init__(self, max_battery=500.0):
        self.max_battery = max_battery
        
        # Optimization Weights (Tweak these for your report analysis!)
        self.W_COVERAGE = 15.0      # Heavy reward for visiting disaster targets
        self.W_ENERGY = 0.5         # Penalty weight for burning power
        self.W_TIME = 0.2           # Penalty weight for long flight periods
        self.HARD_PENALTY = -5000.0 # Death penalty for rule breakers

    def calculate_distance(self, p1, p2):
        return np.linalg.norm(p1 - p2)

    def check_line_collision(self, p1, p2, grid):
        """
        Approximates a line trajectory between waypoints using step samples 
        to verify if the drone crosses a No-Fly or Hazard Zone.
        """
        dist = self.calculate_distance(p1, p2)
        steps = max(int(dist * 2), 2)  # Sample every half-cell
        
        has_collision = False
        hazard_cells_crossed = 0
        
        x_vals = np.linspace(p1[0], p2[0], steps)
        y_vals = np.linspace(p1[1], p2[1], steps)
        
        for x, y in zip(x_vals, y_vals):
            grid_x = int(np.clip(x, 0, grid.width - 1))
            grid_y = int(np.clip(y, 0, grid.height - 1))
            
            cell_type = grid.matrix[grid_y, grid_x]
            if cell_type == grid.NO_FLY:
                has_collision = True
            elif cell_type == grid.HAZARD:
                hazard_cells_crossed += 1
                
        return has_collision, hazard_cells_crossed

    def evaluate_fleet(self, chromosome, grid):
        """
        Calculates total multi-objective fitness for the whole fleet.
        """
        total_coverage_score = 0.0
        total_energy_spent = 0.0
        total_flight_time = 0.0
        rule_violations = 0
        
        # Track which unique priority cells are seen across the whole fleet to avoid double counting
        visited_priority_cells = set()

        for drone in chromosome.drones:
            drone_energy = 0.0
            drone_time = 0.0
            
            for i in range(len(drone.waypoints) - 1):
                p1 = drone.waypoints[i]
                p2 = drone.waypoints[i+1]
                v = drone.speeds[i]
                sensor_on = drone.sensors[i]
                
                # Spatial calculations
                d = self.calculate_distance(p1, p2)
                
                # Check terrain constraints via the line sampling method
                hit_nofly, hazard_count = self.check_line_collision(p1, p2, grid)
                if hit_nofly:
                    rule_violations += 1
                
                # 1. Calculate Energy Expenditure Model
                base_drag = 1.0
                speed_modifier = 0.1 * (v ** 2)  # Faster speed builds exponential drain
                hazard_modifier = 2.5 if hazard_count > 0 else 1.0
                sensor_drain = 1.5 if sensor_on == 1 else 0.2
                
                segment_energy = d * (base_drag + speed_modifier) * hazard_modifier + (sensor_drain * d)
                drone_energy += segment_energy
                
                # 2. Flight Time Model (Time = Distance / Speed)
                drone_time += (d / v)
                
                # 3. Handle Sensor Scanning and Coverage Metrics
                if sensor_on == 1:
                    # Collect cells along the path that are Priority fields
                    steps = max(int(d), 2)
                    x_vals = np.linspace(p1[0], p2[0], steps)
                    y_vals = np.linspace(p1[1], p2[1], steps)
                    for x, y in zip(x_vals, y_vals):
                        gx, gy = int(np.clip(x, 0, grid.width - 1)), int(np.clip(y, 0, grid.height - 1))
                        if grid.matrix[gy, gx] == grid.PRIORITY:
                            visited_priority_cells.add((gx, gy))

            # Hard Constraint: Battery capacity exceeded?
            if drone_energy > self.max_battery:
                rule_violations += 1
                
            total_energy_spent += drone_energy
            total_flight_time += drone_time

        # Compute raw objective components
        total_coverage_score = len(visited_priority_cells) * self.W_COVERAGE
        energy_penalty = total_energy_spent * self.W_ENERGY
        time_penalty = total_flight_time * self.W_TIME
        constraint_penalty = rule_violations * self.HARD_PENALTY
        
        # Final Unified Multi-Objective Score
        fitness_score = total_coverage_score - (energy_penalty + time_penalty) + constraint_penalty
        
        # Prevent the GA from getting broken by hyper-negative values
        chromosome.fitness = max(fitness_score, -99999.0)
        return chromosome.fitness
