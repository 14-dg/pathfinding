

# colors
BLACK  = (0, 0, 0)
GRAY   = (128, 128, 128)
WHITE  = (255, 255, 255)
RED    = (255, 0, 0)
GREEN  = (0, 255, 0)
BLUE   = (0, 0, 255)
DARKGREEN = (0, 100, 0)
ORANGE = (255, 140, 0)
ALICEBLUE  = (120, 200, 255)
BLUEVIOLET = (138, 43, 226)
DEEPSKYBLUE= (0,95,127)




# types of cells
# cell types Pathfinding
TARGET = 'target'                           # target for pathfinding
OBSTACLE = 'obstacle'                       # obstacle for pathfinding
STARTING_POINT = 'starting_point'           # starting point for pathfinding
SEEN_POINT = 'seen_point'                   # a temporary seen point cell during pathfinding
CURRENT_PATH_CELL = 'current_path_cell'     # the cell on the way to the current point
WAY_POINT = 'way_point'                     # the cell that is part of the final path
EMPTY = 'empty'                             # empty cell
# cell types LIDAR
EXPECTED_OCCUPIED = 'expected_occupied'     # cell expected to be occupied (for LIDAR)
EXPECTED_FREE = 'expected_free'             # cell expected to be free (for LIDAR
# SLAM cell types
ROVER_POSITION = 'rover_position'           # cell representing the rover's position


# colors of cells
CELL_COLOR = {
    TARGET: RED,
    OBSTACLE: BLACK,
    STARTING_POINT: GREEN,
    EMPTY: ALICEBLUE,
    SEEN_POINT: BLUEVIOLET,
    CURRENT_PATH_CELL: DARKGREEN,
    WAY_POINT: ORANGE,
    EXPECTED_OCCUPIED: GRAY,   
    EXPECTED_FREE: WHITE,       
    ROVER_POSITION: BLUE,
}

# types of grids
MAIN_GRID = "MAIN_GRID"
ROVER_GRID = "ROVER_GRID"
SENSOR_GRID = "SENSOR_GRID"
ROVER_PATHFINDER_GRID = "ROVER_PATHFINDER_GRID"
SECONDARY_GRID = "SECONDARY_GRID"

# types of pathfining algorithms
A_STAR = "a_star"
DIJKSTRA = "dijkstra"