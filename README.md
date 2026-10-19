# Multi-Objective UAV Fleet Trajectory Strategy Engine

An AI-driven Strategy Engine designed using a custom **Genetic Algorithm (GA)** to solve a multi-objective path optimization problem for a fleet of three Unmanned Aerial Vehicles (UAVs) navigating a hazardous disaster sector.

## System Design Overview
- **Grid Environment:** A 100x100 matrix containing Normal Space, No-Fly Obstacles, High-Priority Disaster Zones, and Environmental Hazards.
- **Hybrid Chromosome:** Real-valued spatial waypoints combined with continuous velocity curves and a binary active-scanning sensor profile.
- **Fitness Evaluation:** Multi-objective equation maximizing area coverage while applying exponential penalties for energy over-expenditure, flight time, and hard constraint no-fly violations.

## Installation & Setup
1. Clone this repository:
   ```bash
   git clone https://github.com/muhammad-ahmad08/ai-assignment-2.git
   cd ai-assignment-2
   ```
2. Set up a virtual environment and install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Execute the simulation framework:
   ```bash
   python3 main.py
   ```
