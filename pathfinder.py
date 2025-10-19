
from __future__ import annotations
import math

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
            cost=cell.dist(self.grid.starting_points[0]))
            for row in self.grid.grid for cell in row}
                
        self.queue: list[tuple[float, Cell]] = []
        self.visited: set[Cell] = set()
        

    def dijkstra(self) -> set[Cell]:#tuple[dict[Cell, Node], set[Cell]]:
        changed_cells = set()
        
        for sp in self.grid.seen_points:
            self.G[sp].dist = 0.0
            self.queue.append((0, sp))
        
        while self.queue:
            current_dist, current_cell = self.queue.pop(0)
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
                distance = current_dist + weight
                if distance < self.G[adjacent_cell].dist:
                    self.G[adjacent_cell].dist = distance
                    self.G[adjacent_cell].parent = self.G[current_cell]
                    self.queue.append((distance, adjacent_cell))
                    self.queue.sort(key=lambda n: n[0])  # Sort queue by distance
                    
                    self.grid.find_and_change_type_of_cell((adjacent_cell.x, adjacent_cell.y), SEEN_POINT)
                    changed_cells.add(adjacent_cell)
                            
        return changed_cells
    
    def shortest_path(self, start_cell: Cell|None = None, end_cell: Cell|None = None) -> set[Cell]:
        changed_cells = self.dijkstra()
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
            # for neighbor in self.grid.get_adjacent_cells(current_cell):
                           
                
                
            #     weight = self.G[neighbor].cost if neighbor else float("inf")
            #     if self.G[neighbor] and self.G[neighbor].parent == self.G[current_cell]:
                
                
                
            #     if neighbor and dist[neighbor].dist + current_cell.dist == dist[current_cell].dist:
            #         current_cell = neighbor
            #         break
        
        return changed_cells
    
    def a_star(self):
        pass
    
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


    def find(self):
        if self.grid.seen_points == []:
            self.grid.seen_points = self.grid.starting_points.copy()
        
        return self.shortest_path(self.grid.starting_points[0], self.grid.targets[0])

