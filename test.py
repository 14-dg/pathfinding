import pygame
import sys
import heapq

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up display
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
FPS = 30

# Define directions (up, down, left, right, diagonal)
DIRS = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = 0  # Cost from start node to current node
        self.h = 0  # Heuristic (estimated cost from current node to goal node)
        self.f = 0  # Total cost (g + h)
        self.parent = None
        self.walkable = True

    def __lt__(self, other):
        return self.f < other.f


def heuristic(node, goal):
    # Manhattan distance
    return abs(node.x - goal.x) + abs(node.y - goal.y)


def draw_grid(screen):
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (WIDTH, y))


def draw_node(screen, node, color):
    pygame.draw.rect(screen, color, (node.x * CELL_SIZE, node.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def draw_path(screen, path):
    for node in path:
        draw_node(screen, node, BLUE)


def astar(start, goal, grid):
    open_set = []
    closed_set = set()

    heapq.heappush(open_set, start)

    while open_set:
        current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = current.parent
            return path[::-1]

        closed_set.add(current)

        for dir_x, dir_y in DIRS:
            neighbor_x, neighbor_y = current.x + dir_x, current.y + dir_y

            if 0 <= neighbor_x < GRID_WIDTH and 0 <= neighbor_y < GRID_HEIGHT:
                neighbor = grid[neighbor_x][neighbor_y]

                if neighbor.walkable and neighbor not in closed_set:
                    tentative_g = current.g + 1

                    if neighbor not in open_set or tentative_g < neighbor.g:
                        neighbor.g = tentative_g
                        neighbor.h = heuristic(neighbor, goal)
                        neighbor.f = neighbor.g + neighbor.h
                        neighbor.parent = current

                        if neighbor not in open_set:
                            heapq.heappush(open_set, neighbor)

    return None


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("A* Pathfinding Visualization")
    clock = pygame.time.Clock()

    start_node = Node(5, 5)
    goal_node = Node(15, 15)

    grid = [[Node(x, y) for y in range(GRID_HEIGHT)] for x in range(GRID_WIDTH)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)
        draw_grid(screen)

        for row in grid:
            for node in row:
                draw_node(screen, node, WHITE if node.walkable else BLACK)

        path = astar(grid[start_node.x][start_node.y], grid[goal_node.x][goal_node.y], grid)

        if path:
            draw_path(screen, path)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
