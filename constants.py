"""
Zentrale Konstanten für das Pathfinding-Projekt.
"""

# --- Pygame-Farben -----------------------------------------------------------
BLACK         = (0, 0, 0)
GRAY          = (128, 128, 128)
WHITE         = (255, 255, 255)
RED           = (255, 0, 0)
GREEN         = (0, 255, 0)
BLUE          = (0, 0, 255)
DARKGREEN     = (0, 100, 0)
ORANGE        = (255, 140, 0)
ALICEBLUE     = (120, 200, 255)
BLUEVIOLET    = (138, 43, 226)
DEEPSKYBLUE   = (0, 95, 127)

# --- Zelltypen ---------------------------------------------------------------
# Pfadsuche
TARGET              = 'target'
OBSTACLE            = 'obstacle'
STARTING_POINT      = 'starting_point'
SEEN_POINT          = 'seen_point'
CURRENT_PATH_CELL   = 'current_path_cell'
WAY_POINT           = 'way_point'
EMPTY               = 'empty'

# LIDAR
EXPECTED_OCCUPIED   = 'expected_occupied'
EXPECTED_FREE       = 'expected_free'

# SLAM
ROVER_POSITION      = 'rover_position'

# --- Farbzuordnung -----------------------------------------------------------
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

# --- Gittertypen -------------------------------------------------------------
MAIN_GRID                 = "MAIN_GRID"
ROVER_GRID                = "ROVER_GRID"
SENSOR_GRID               = "SENSOR_GRID"
ROVER_PATHFINDER_GRID     = "ROVER_PATHFINDER_GRID"
SECONDARY_GRID            = "SECONDARY_GRID"

# --- Pfadfindungsalgorithmen -------------------------------------------------
A_STAR      = "a_star"
DIJKSTRA    = "dijkstra"

# --- Anwendungskonfiguration -------------------------------------------------
PATHFINDING_BATCH_SIZE = 20          # Anzahl Schritte pro Timer-Tick
TIMER_INTERVAL_MS      = 10          # Timer-Intervall in Millisekunden
FPS                    = 100         # Maximale Bildwiederholrate

# --- Labyrinth-Generierung ---------------------------------------------------
MAZE_EMPTY_PROBABILITY        = 75   # Wahrscheinlichkeit für leere Zelle in %
MAZE_TARGET_ROW_FACTOR        = 0.1
MAZE_TARGET_COL_FACTOR        = 0.1
MAZE_START_ROW_FACTOR         = 0.9
MAZE_START_COL_FACTOR         = 0.9