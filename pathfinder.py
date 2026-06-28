"""
Pfadfindungsalgorithmen (A* und Dijkstra) als schrittweise Generatoren.
"""

from __future__ import annotations
import heapq
import itertools
import logging
from typing import Generator, Tuple, Set, Optional, Callable

from cell import Cell
from grid import Grid
from constants import *

logger = logging.getLogger(__name__)


class Pathfinder:
    def __init__(self, grid: Grid) -> None:
        self.grid = grid
        self._came_from: dict[Cell, Cell | None] = {}

    # -------------------------------------------------------------------------
    #  Allgemeine Suche (Generator)
    # -------------------------------------------------------------------------
    def _search(
        self,
        start_cells: set[Cell],
        end_cell: Cell,
        heuristic: Callable[[Cell, Cell], float],
    ) -> Generator[Tuple[Set[Cell], Cell | None], None, None]:
        came_from: dict[Cell, Cell | None] = {}
        g_score: dict[Cell, float] = {cell: float('inf') for row in self.grid.grid for cell in row}
        queue: list[tuple[float, int, Cell]] = []
        visited: set[Cell] = set()
        counter = itertools.count()

        for start in start_cells:
            g_score[start] = 0.0
            heapq.heappush(queue, (heuristic(start, end_cell), next(counter), start))
            came_from[start] = None

        changed: set[Cell] = set()
        current: Cell | None = None

        while queue:
            _, _, current = heapq.heappop(queue)
            if current in visited:
                continue
            visited.add(current)

            if current in self.grid.targets:
                logger.debug("Ziel erreicht.")
                break

            neighbours = self.grid.get_adjacent_non_obstacle_cells(current)
            if not neighbours:
                continue

            for nxt in neighbours:
                weight = nxt.dist(current)
                tentative_g = g_score[current] + weight
                if tentative_g < g_score[nxt]:
                    g_score[nxt] = tentative_g
                    came_from[nxt] = current
                    f = tentative_g + heuristic(nxt, end_cell)
                    heapq.heappush(queue, (f, next(counter), nxt))
                    result = self.grid.find_and_change_type_of_cell(nxt.get_cell_ind(), SEEN_POINT)
                    if result:
                        changed.update(result)

            self._came_from = came_from  # ← jetzt aktuell, damit get_parents funktioniert

            if changed:
                yield changed, current
                changed = set()

        self._came_from = came_from
        if changed:
            yield changed, current

    # -------------------------------------------------------------------------
    #  Konkrete Algorithmen
    # -------------------------------------------------------------------------
    def dijkstra(self, start_cells: set[Cell], end_cell: Cell) -> Generator[Tuple[Set[Cell], Cell | None], None, None]:
        return self._search(start_cells, end_cell, lambda a, b: 0.0)

    def a_star(self, start_cells: set[Cell], end_cell: Cell) -> Generator[Tuple[Set[Cell], Cell | None], None, None]:
        return self._search(start_cells, end_cell, lambda a, b: a.dist(b))

    # -------------------------------------------------------------------------
    #  Hauptmethode
    # -------------------------------------------------------------------------
    def find(self, algorithm: str) -> Generator[Tuple[Set[Cell], Cell | None], None, None]:
        if self.grid.seen_points:
            start_cells = set(self.grid.seen_points)
        else:
            start_cells = set(self.grid.starting_points)

        if not start_cells or not self.grid.targets:
            logger.error("Keine Start- oder Zielzelle vorhanden.")
            return

        end_cell = next(iter(self.grid.targets))
        start_cell = next(iter(start_cells))

        search_gen = self.a_star(start_cells, end_cell) if algorithm == A_STAR else self.dijkstra(start_cells, end_cell)

        for changed, current in search_gen:
            yield changed, current

        path = []
        cur = end_cell
        while cur is not None and cur != start_cell:
            path.append(cur)
            self.grid.find_and_change_type_of_cell(cur.get_cell_ind(), WAY_POINT)
            cur = self._came_from.get(cur)

        if path:
            yield set(path), end_cell

    def get_parents(self, cell: Cell) -> list[Cell]:
        parents = []
        cur = cell
        while cur is not None:
            parents.append(cur)
            cur = self._came_from.get(cur)
        parents.reverse()
        return parents


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    g = Grid(10, 10)
    g.find_and_change_type_of_cell((1, 1), STARTING_POINT)
    g.find_and_change_type_of_cell((8, 8), TARGET)
    g.find_and_change_type_of_cell((5, 5), OBSTACLE)
    pf = Pathfinder(g)
    gen = pf.find(A_STAR)
    try:
        while True:
            changed, current = next(gen)
            print(f"Changed: {len(changed)} cells, current: {current}")
    except StopIteration:
        pass
    print("Pathfinder test completed.")