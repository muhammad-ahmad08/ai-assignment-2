# Main script to run the simulation

from src.grid import DisasterGrid

def main():
    # 1. Initialize a 100x100 environment
    grid = DisasterGrid(width=100, height=100)
    
    # 2. Add static No-Fly zones (e.g., skyscrapers or restricted zones)
    grid.add_no_fly_zone(top_left_x=20, top_left_y=30, width=15, height=25)
    grid.add_no_fly_zone(top_left_x=65, top_left_y=70, width=20, height=15)
    
    # 3. Add environmental hazard pockets (e.g., high-wind zones)
    grid.add_hazard_zone(top_left_x=45, top_left_y=10, width=30, height=20)
    
    # 4. Drop some high-priority target spots (disaster hot-spots)
    grid.add_priority_target(x=15, y=85, radius=3)
    grid.add_priority_target(x=80, y=25, radius=4)
    grid.add_priority_target(x=50, y=55, radius=3)
    
    # 5. Display the map to make sure everything rendered beautifully
    print("Grid generation complete! Displaying physical space map...")
    grid.visualize_grid()

if __name__ == "__main__":
    main()
