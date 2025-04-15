"""
Maze Explorer module that implements automated maze solving using A* algorithm.
"""

import time
import pygame
import heapq
from typing import Tuple, List
from collections import deque
from .constants import BLUE, WHITE, CELL_SIZE, WINDOW_SIZE

class Explorer:
    def __init__(self, maze, visualize: bool = False):
        self.maze = maze
        self.x, self.y = maze.start_pos
        self.moves = []
        self.start_time = None
        self.end_time = None
        self.visualize = visualize
        self.backtrack_count = 0  # Added for compatibility with stats

        if visualize:
            pygame.init()
            self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
            pygame.display.set_caption("Maze Explorer - A* Solver")
            self.clock = pygame.time.Clock()

    def draw_state(self):
        self.screen.fill(WHITE)
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if self.maze.grid[y][x] == 1:
                    pygame.draw.rect(self.screen, (0, 0, 0),
                                     (x * CELL_SIZE, y * CELL_SIZE,
                                      CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, (0, 255, 0),
                         (self.maze.start_pos[0] * CELL_SIZE,
                          self.maze.start_pos[1] * CELL_SIZE,
                          CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, (255, 0, 0),
                         (self.maze.end_pos[0] * CELL_SIZE,
                          self.maze.end_pos[1] * CELL_SIZE,
                          CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, BLUE,
                         (self.x * CELL_SIZE, self.y * CELL_SIZE,
                          CELL_SIZE, CELL_SIZE))
        pygame.display.flip()
        self.clock.tick(30)

    def print_statistics(self, time_taken: float):
        print("\n=== Maze Exploration Statistics ===")
        print(f"Total time taken: {time_taken:.2f} seconds")
        print(f"Total moves made: {len(self.moves)}")
        print(f"Backtracks: {self.backtrack_count}")
        print(f"Average moves per second: {len(self.moves)/time_taken:.2f}")
        print("==================================\n")

    def solve(self):
        self.start_time = time.time()

        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        start = (self.x, self.y)
        goal = self.maze.end_pos

        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start, goal)}
        visited = set()

        while open_set:
            _, current = heapq.heappop(open_set)
            if current == goal:
                break

            visited.add(current)

            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                neighbor = (current[0] + dx, current[1] + dy)
                x, y = neighbor
                if (0 <= x < self.maze.width and
                    0 <= y < self.maze.height and
                    self.maze.grid[y][x] == 0):

                    tentative_g_score = g_score[current] + 1
                    if neighbor in visited and tentative_g_score >= g_score.get(neighbor, float('inf')):
                        continue

                    if tentative_g_score < g_score.get(neighbor, float('inf')):
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        self.moves = []
        current = goal
        while current != start:
            self.moves.append(current)
            current = came_from[current]
        self.moves.append(start)
        self.moves.reverse()

        self.end_time = time.time()
        time_taken = self.end_time - self.start_time

        if self.visualize:
            self.draw_state()
            pygame.time.wait(2000)
            pygame.quit()

        self.print_statistics(time_taken)
        return time_taken, self.moves
