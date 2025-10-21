

# colors
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
GREEN  = (0, 255, 0)
RED    = (255, 0, 0)
ORANGE = (255, 140, 0)
ALICEBLUE  = (120, 200, 255)
BLUEVIOLET = (138, 43, 226)
DEEPSKYBLUE= (0,191,255)



# types of cells
TARGET = 'target'                   # target for pathfinding
OBSTACLE = 'obstacle'               # obstacle for pathfinding
STARTING_POINT = 'starting_point'   # starting point for pathfinding
SEEN_POINT = 'seen_point'           # a temporary seen point cell during pathfinding
WAY_POINT = 'way_point'             # the cell that is part of the final path
EMPTY = 'empty'                     # empty cell

# colors of cells
cell_color = {
    TARGET: RED,
    OBSTACLE: BLACK,
    STARTING_POINT: GREEN,
    EMPTY: ALICEBLUE,
    SEEN_POINT: BLUEVIOLET,
    WAY_POINT: ORANGE
}


# types of pathfining algorithms
A_STAR = "a_star"
DIJKSTRA = "dijkstra"