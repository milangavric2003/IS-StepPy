from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Callable

from core.grid import Grid
from core.path import Path


@dataclass(slots=True)
class Agent:
    name: str

    def find_path(self, grid: Grid, start: tuple[int, int], goal: tuple[int, int]) -> Path:
        raise NotImplementedError


class ExampleAgent(Agent):

    def __init__(self):
        super().__init__("Example")

    def find_path(self, grid: Grid, start: tuple[int, int], goal: tuple[int, int]) -> Path:
        nodes = [start]
        while nodes[-1] != goal:
            r, c = nodes[-1]
            neighbors = grid.neighbors4(r, c)

            min_dist = min(grid.manhattan(t.pos, goal) for t in neighbors)
            best_tiles = [
                tile for tile in neighbors
                if grid.manhattan(tile.pos, goal) == min_dist
            ]
            best_tile = best_tiles[random.randint(0, len(best_tiles) - 1)]

            nodes.append(best_tile.pos)

        return Path(nodes)


class DFSAgent(Agent):

    def __init__(self):
        super().__init__("DFS")

    def find_path(self, grid: Grid, start: tuple[int, int], goal: tuple[int, int]) -> Path:
        # raise NotImplementedError
        # nodes = [start]
        # seen = set([start])
        # while nodes[-1] != goal:
        #     r, c = nodes[-1]
        #
        #     neighbors = grid.neighbors4(r, c)
        #
        #     to_add = []
        #     for x in neighbors:
        #         if x.pos not in seen:
        #             to_add.append(x)
        #
        #     if not to_add:
        #         nodes.pop()
        #         continue
        #
        #     direction_order = {
        #         (0, 1): 0,  # istok
        #         (1, 0): 1,  # jug
        #         (0, -1): 2,  # zapad
        #         (-1, 0): 3  # sever
        #     }
        #
        #     to_add.sort(key=lambda t: (t.cost, direction_order[(t.pos[0] - r, t.pos[1] - c)]))
        #     nodes.append(to_add[0].pos)
        #     seen.add(to_add[0].pos)
        #
        # return Path(nodes)

        # nodes = [start]
        # visited = set([start])
        #
        # while nodes:
        #     r, c = nodes[-1]
        #
        #     if (r, c) == goal:
        #         return Path(nodes)
        #
        #     neighbors = grid.neighbors4(r, c)
        #
        #     # filtriraj neposjećene
        #     to_add = []
        #     for t in neighbors:
        #         if t.pos not in visited:
        #             to_add.append(t)
        #
        #     if not to_add:
        #         # nema gde dalje → backtracking (DFS!)
        #         nodes.pop()
        #         continue
        #
        #     # sortiranje:
        #     # 1) cost rastuće
        #     # 2) smer: E, S, W, N
        #     direction_order = {
        #         (0, 1): 0,  # istok
        #         (1, 0): 1,  # jug
        #         (0, -1): 2,  # zapad
        #         (-1, 0): 3  # sever
        #     }
        #
        #     to_add.sort(
        #         key=lambda t: (
        #             t.cost,
        #             direction_order[(t.pos[0] - r, t.pos[1] - c)]
        #         ),
        #         reverse=True  # reverse jer je DFS (stek)
        #     )
        #
        #     next_tile = to_add.pop()
        #     nodes.append(next_tile.pos)
        #     visited.add(next_tile.pos)
        #
        # return Path([])

        nodes = [start]
        seen = {start}
        while nodes[-1] != goal:
            r, c = nodes[-1]
            neighbors = grid.neighbors4(r, c)

            best_tiles = [
                tile for tile in neighbors
                if tile.pos not in seen
            ]
            if not best_tiles:
                nodes.pop()
                continue

            direction_order = {
                (0, 1): 0,  # istok
                (1, 0): 1,  # jug
                (0, -1): 2,  # zapad
                (-1, 0): 3  # sever
            }

            best_tile = sorted(
                best_tiles,
                key=lambda t: (
                    t.cost, direction_order[(t.pos[0] - r, t.pos[1] - c)]
                )
            )[0]

            nodes.append(best_tile.pos)
            seen.add(best_tile.pos)

        return Path(nodes)


class BranchAndBoundAgent(Agent):

    def __init__(self):
        super().__init__("BranchAndBound")

    def find_path(self, grid: Grid, start: tuple[int, int], goal: tuple[int, int]) -> Path:
        # raise NotImplementedError
        nodes: list[list[tuple[int, int]]] = [start]
        seen = {start}
        while nodes[-1] != goal:
            r, c = nodes[-1]
            neighbors = grid.neighbors4(r, c)

            best_tiles = [
                tile for tile in neighbors
                if tile.pos not in seen
            ]
            if not best_tiles:
                nodes.pop()
                continue

            direction_order = {
                (0, 1): 0,  # istok
                (1, 0): 1,  # jug
                (0, -1): 2,  # zapad
                (-1, 0): 3  # sever
            }

            best_tile = sorted(
                best_tiles,
                key=lambda t: (
                    t.cost, direction_order[(t.pos[0] - r, t.pos[1] - c)]
                )
            )[0]

            nodes.append(best_tile.pos)
            seen.add(best_tile.pos)

        return Path(nodes)

class AStar(Agent):

    def __init__(self):
        super().__init__("AStar")

    def find_path(self, grid: Grid, start: tuple[int, int], goal: tuple[int, int]) -> Path:
        raise NotImplementedError


AGENTS: dict[str, Callable[[], Agent]] = {
    "Example": ExampleAgent,
    "DFS": DFSAgent,
    "BranchAndBound": BranchAndBoundAgent,
    "AStar": AStar
}


def create_agent(name: str) -> Agent:
    if name not in AGENTS:
        raise ValueError(f"Unknown agent '{name}'. Available: {', '.join(AGENTS.keys())}")
    return AGENTS[name]()
