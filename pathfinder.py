
from __future__ import annotations
import math
import heapq
import itertools

from cell import Cell
from grid import Grid
from constants import *

from sensor_data import simulate_lidar_scan

class Node:
    def __init__(self, cell: Cell, parent: Node|None = None, 
                 dist:float = float("inf")) -> None:
        self.cell = cell
        self.parent = parent
        self.dist = dist


class Pathfinder:
    def __init__(self, grid: Grid) -> None:
        self.grid = grid
        
        self.G = {cell: Node(cell)
            for row in self.grid.grid for cell in row}
                
        self.queue: list[tuple[float, int, Cell]] = []
        self.visited: set[Cell] = set()
        
        self.counter = itertools.count()  # unique sequence count

        

    def dijkstra(self):
        changed_cells = set()
        current_cell = None
        
        for sp in self.grid.seen_points:
            self.G[sp].dist = 0.0
            heapq.heappush(self.queue, (0, next(self.counter), sp))
        
        while self.queue:
            current_dist, _, current_cell = heapq.heappop(self.queue)
            if current_cell in self.visited:
                continue
            self.visited.add(current_cell)
            
            if current_cell in self.grid.targets:
                print("Target reached!")
                break
            
            adjacent_cells = self.grid.get_adjacent_non_obstacle_cells(current_cell)
            if adjacent_cells is None:
                continue
            
            for adjacent_cell in adjacent_cells:
                if not adjacent_cell:
                    continue                
                                
                weight = adjacent_cell.dist(current_cell)
                distance = self.G[current_cell].dist + weight
                if distance < self.G[adjacent_cell].dist:
                    self.G[adjacent_cell].dist = distance
                    self.G[adjacent_cell].parent = self.G[current_cell]
                    heapq.heappush(self.queue, (distance, next(self.counter), adjacent_cell))
                    
                    self.grid.find_and_change_type_of_cell(adjacent_cell.get_cell_ind(), SEEN_POINT)
                    changed_cells.add(adjacent_cell)
                         
            if changed_cells:
                yield changed_cells, current_cell
                changed_cells = set()
        return changed_cells, current_cell
    
    def a_star(self):
        changed_cells = set()
        current_cell = None
        
        for sp in self.grid.seen_points:
            self.G[sp].dist = 0.0
            heapq.heappush(self.queue, (0, next(self.counter), sp))
        
        while self.queue:
            current_dist, _, current_cell = heapq.heappop(self.queue)
            if current_cell in self.visited:
                continue
            self.visited.add(current_cell)
            
            if current_cell in self.grid.targets:
                print("Target reached!")
                break
            
            adjacent_cells = self.grid.get_adjacent_non_obstacle_cells(current_cell)
            # adjacent_cells_inds = simulate_lidar_scan(self.grid, current_cell.get_cell_ind(), scan_range=3, points_per_rotation=90)[0]
            # adjacent_cells = [self.grid.grid[r][c] for r, c in adjacent_cells_inds]
            
            if adjacent_cells is None:
                continue
            
            for adjacent_cell in adjacent_cells:
                if not adjacent_cell:
                    continue                
                                
                weight = adjacent_cell.dist(current_cell)
                g_cost = self.G[current_cell].dist + weight                
                h_cost = adjacent_cell.dist(self.grid.targets[0])
                f_cost = g_cost + h_cost
                
                if g_cost < self.G[adjacent_cell].dist:
                    self.G[adjacent_cell].dist = g_cost
                    self.G[adjacent_cell].parent = self.G[current_cell]
                    heapq.heappush(self.queue, (f_cost, next(self.counter), adjacent_cell))
                    
                    self.grid.find_and_change_type_of_cell(adjacent_cell.get_cell_ind(), SEEN_POINT)
                    changed_cells.add(adjacent_cell)
                         
            if changed_cells:
                yield changed_cells, current_cell
                changed_cells = set()
        return changed_cells, current_cell
    
    def shortest_path(self, algorithm: str, start_cell: Cell|None = None, end_cell: Cell|None = None, ):
        if algorithm == DIJKSTRA:
            pathfinding_algorithm_gen = self.dijkstra()
        elif algorithm == A_STAR:
            pathfinding_algorithm_gen = self.a_star()
        else:
            pathfinding_algorithm_gen = self.dijkstra()
            
        while pathfinding_algorithm_gen:
            try:
                changed_cells, current_cell = next(pathfinding_algorithm_gen)
                yield changed_cells, current_cell
                changed_cells = set()
            except StopIteration:
                break
        
        changed_cells = set()

        
        path = []
        current_cell = end_cell
        
        while current_cell and current_cell != start_cell:
            path.append(current_cell)
            self.grid.find_and_change_type_of_cell(current_cell.get_cell_ind(), WAY_POINT)
            changed_cells.add(current_cell)
                
            parent = self.G[current_cell].parent
            if parent:
                current_cell = parent.cell
            else:
                current_cell = None
            
            if changed_cells:    
                yield changed_cells, current_cell
                changed_cells = set()
            
        return changed_cells, current_cell
    
    def get_parents(self, cell: Cell) -> list[Cell]:
        parents = []
        current_cell = cell
        while current_cell:
            parents.append(current_cell)
            parent_node = self.G[current_cell].parent
            if parent_node:
                current_cell = parent_node.cell
            else:
                break
        return parents[::-1]  # reverse to get from start to end

    def find(self, algorithm:str):
        if self.grid.seen_points == []:
            self.grid.seen_points = self.grid.starting_points.copy()
        shortest_path_gen = self.shortest_path(algorithm, self.grid.starting_points[0], self.grid.targets[0])
        changed_cells = set()
        current_cell = None
        
        while shortest_path_gen:
            try:
                changed_cells, current_cell = next(shortest_path_gen) 
                if changed_cells and current_cell:
                    yield changed_cells, current_cell
                    changed_cells = set()
            except StopIteration:
                break 
        return

