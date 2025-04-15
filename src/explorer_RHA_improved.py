"""
Maze Explorer module that implements automated maze solving with enhanced memory and smart backtracking.
"""

import time
import pygame
from typing import Tuple, List
from collections import deque
from .constants import BLUE, WHITE, CELL_SIZE, WINDOW_SIZE

class Explorer:
    def __init__(self, maze, visualize: bool = False):
        self.maze = maze
        self.x, self.y = maze.start_pos
        self.direction = (1, 0)
        self.moves = []
        self.start_time = None
        self.end_time = None
        self.visualize = visualize
        self.move_history = deque(maxlen=3)
        self.backtracking = False
        self.backtrack_path = []
        self.backtrack_count = 0
        self.direction_memory = {}  # memory of directions tried from each cell

        if visualize:
            pygame.init()
            self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
            pygame.display.set_caption("Maze Explorer - Automated Solving")
            self.clock = pygame.time.Clock()

    def turn_right(self):
        x, y = self.direction
        self.direction = (-y, x)

    def turn_left(self):
        x, y = self.direction
        self.direction = (y, -x)

    def can_move_forward(self) -> bool:
        dx, dy = self.direction
        new_x, new_y = self.x + dx, self.y + dy
        return (0 <= new_x < self.maze.width and 
                0 <= new_y < self.maze.height and 
                self.maze.grid[new_y][new_x] == 0)

    def move_forward(self):
        dx, dy = self.direction
        self.x += dx
        self.y += dy
        current_move = (self.x, self.y)
        self.moves.append(current_move)
        self.move_history.append(current_move)
        if self.visualize:
            self.draw_state()

    def is_stuck(self) -> bool:
        if len(self.move_history) < 3:
            return False
        return (self.move_history[0] == self.move_history[1] == self.move_history[2])

    def backtrack(self) -> bool:
        while self.path:
            prev = self.path.pop()
            self.x, self.y = prev
            if self.get_untried_directions((self.x, self.y)):
                return True
        return False

    def get_untried_directions(self, pos):
        if pos not in self.direction_memory:
            self.direction_memory[pos] = set()

        tried = self.direction_memory[pos]
        untried = []

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = pos[0] + dx, pos[1] + dy
            if (0 <= nx < self.maze.width and
                0 <= ny < self.maze.height and
                self.maze.grid[ny][nx] == 0 and
                (nx, ny) not in self.visited and
                (dx, dy) not in tried):
                untried.append((dx, dy))

        return untried

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
        print(f"Number of backtrack operations: {self.backtrack_count}")
        print(f"Average moves per second: {len(self.moves)/time_taken:.2f}")
        print("==================================\n")

    def solve(self):
        self.start_time = time.time()
        self.visited = set()
        self.path = [(self.x, self.y)]
        self.moves = []
        self.backtrack_count = 0

        while (self.x, self.y) != self.maze.end_pos:
            pos = (self.x, self.y)
            self.visited.add(pos)

            if pos not in self.direction_memory:
                self.direction_memory[pos] = set()
            moved = False

            for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                direction = (dx, dy)
                nx, ny = self.x + dx, self.y + dy
                if direction in self.direction_memory[pos]:
                    continue
                if (0 <= nx < self.maze.width and
                    0 <= ny < self.maze.height and
                    self.maze.grid[ny][nx] == 0 and
                    (nx, ny) not in self.visited):
                    self.x, self.y = nx, ny
                    self.path.append((self.x, self.y))
                    self.moves.append((self.x, self.y))
                    self.direction_memory[pos].add(direction)
                    moved = True
                    if self.visualize:
                        self.draw_state()
                    break
                else:
                    self.direction_memory[pos].add(direction)

            if not moved:
                if not self.backtrack():
                    break
                self.backtrack_count += 1

        self.end_time = time.time()
        time_taken = self.end_time - self.start_time

        if self.visualize:
            pygame.time.wait(2000)
            pygame.quit()

        self.print_statistics(time_taken)
        return time_taken, self.moves
