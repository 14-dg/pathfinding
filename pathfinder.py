
from __future__ import annotations
import math
import heapq
import itertools

from cell import Cell
from grid import Grid
from constants import *

class Node:
    def __init__(self, cell: Cell, parent: Node|None = None, 
                 cost:float = 1.0, dist:float = float("inf")) -> None:
        self.cell = cell
        self.parent = parent
        self.cost = cost
        self.dist = dist


class Pathfinder:
    def __init__(self, grid: Grid) -> None:
        self.grid = grid
        
        self.G = {cell: Node(cell, 
            cost=cell.w+cell.h)
            for row in self.grid.grid for cell in row}
                
        self.queue: list[tuple[float, int, Cell]] = []
        self.visited: set[Cell] = set()
        
        self.counter = itertools.count()  # unique sequence count

        

    def dijkstra(self):#tuple[dict[Cell, Node], set[Cell]]:
        changed_cells = set()
        
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
                                
                weight = self.G[adjacent_cell].cost
                distance = self.G[current_cell].dist + weight
                if distance < self.G[adjacent_cell].dist:
                    self.G[adjacent_cell].dist = distance
                    self.G[adjacent_cell].parent = self.G[current_cell]
                    heapq.heappush(self.queue, (distance, next(self.counter), adjacent_cell))
                    
                    self.grid.find_and_change_type_of_cell((adjacent_cell.x, adjacent_cell.y), SEEN_POINT)
                    changed_cells.add(adjacent_cell)
                         
            if changed_cells:
                yield changed_cells
                changed_cells = set()
        return changed_cells
    
    def a_star(self, start_cell: Cell | None = None, end_cell: Cell | None = None):
        yield set()
    
    def shortest_path(self, algorithm: str, start_cell: Cell|None = None, end_cell: Cell|None = None, ):
        if algorithm == DIJKSTRA:
            pathfinding_algorithm_gen = self.dijkstra()
        elif algorithm == A_STAR:
            pathfinding_algorithm_gen = self.a_star()
        else:
            pathfinding_algorithm_gen = self.dijkstra()
            
        while pathfinding_algorithm_gen:
            try:
                changed_cells = next(pathfinding_algorithm_gen)
                yield changed_cells
                changed_cells = set()
            except StopIteration:
                break
        
        changed_cells = set()

        
        path = []
        current_cell = end_cell
        
        while current_cell and current_cell != start_cell:
            path.append(current_cell)
            self.grid.find_and_change_type_of_cell((current_cell.x, current_cell.y), WAY_POINT)
            changed_cells.add(current_cell)
                
            parent = self.G[current_cell].parent
            if parent:
                current_cell = parent.cell
            else:
                current_cell = None
            
            if changed_cells:    
                yield changed_cells
                changed_cells = set()
            
        return changed_cells
    
    def breadth_first_search(self):
        changed_cells = []
        
        # sps = self.grid.seen_points.copy()
        # for sp_c in sps:
        #     adjacent_cells = self.grid.get_adjacent_cells(sp_c)
        #     for a_c in adjacent_cells:
        #         if a_c:
        #             cells = self.grid.find_and_change_type_of_cell((a_c.x, a_c.y), SEEN_POINT)
        #             if cells:
        #                 changed_cells.extend(cells)
        return changed_cells


    def find(self, algorithm:str):
        if self.grid.seen_points == []:
            self.grid.seen_points = self.grid.starting_points.copy()
        shortest_path_gen = self.shortest_path(algorithm, self.grid.starting_points[0], self.grid.targets[0])
        changed_cells = set()
        
        while shortest_path_gen:
            try:
                changed_cells = next(shortest_path_gen) 
                if changed_cells:
                    yield changed_cells
                    changed_cells = set()
            except StopIteration:
                break 
        return

