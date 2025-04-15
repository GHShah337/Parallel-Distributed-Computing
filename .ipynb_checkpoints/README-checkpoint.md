
## Student Questions

### Question 1 (10 points)
Explain how the automated maze explorer works.
### Answer:
1) the explorer uses the right-hand rule algorithm, which simulates keeping your right hand on a wall while exploring a maze. The logic is:
   Always try to move right relative to your current direction.
If that’s blocked, try to go straight.
If that’s blocked too, try to go left.
If everything is blocked, turn around and move backward
2)  To avoid getting stuck in cycles (moving back and forth between the same few cells), the explorer tracks its last three moves using a deque: self.move_history = deque(maxlen=3). if all three recent positions are the same, it means the explorer is stuck in a loop, and it triggers backtracking.
3) When stuck, the explorer calls backtrack():
   it walks backward through its past moves, using the find_backtrack_path() function.
   It searches for the last position that had multiple possible paths using count_available_choices().
   Once found, the explorer follows the reversed path back to that point and tries unexplored directions.
   This strategy ensures that the explorer doesn’t stay stuck at dead ends or in cycles, and can eventually explore the entire maze.
4) Statistics matrix(with visualization):
=== Maze Exploration Statistics ===
Total time taken: 42.35 seconds
Total moves made: 1279
Number of backtrack operations: 0
Average moves per second: 30.20
==================================

### Question 2 (30 points)
Modify the main program to run multiple maze explorers simultaneously. This is because we want to find the best route out of the maze.
### Answer:
=== Summary of All Explorers ===
{'Explorer ID': 0, 'Time Taken': 0.0, 'Total Moves': 1279, 'Backtracks': 0, 'Moves/sec': 749338.57}
{'Explorer ID': 1, 'Time Taken': 0.0, 'Total Moves': 1279, 'Backtracks': 0, 'Moves/sec': 1046734.6}
{'Explorer ID': 2, 'Time Taken': 0.0, 'Total Moves': 1279, 'Backtracks': 0, 'Moves/sec': 1013128.39}
{'Explorer ID': 3, 'Time Taken': 0.0, 'Total Moves': 1279, 'Backtracks': 0, 'Moves/sec': 993980.88}

### Question 3 (10 points)
Analyze and compare the performance of different maze explorers on the static maze. Your analysis should:
### Answer:
1) === Summary of All Explorers ===
{'Explorer ID': 0, 'Time Taken': 0.0, 'Total Moves': 1279, 'Backtracks': 0, 'Moves/sec': 749338.57}
{'Explorer ID': 1, 'Time Taken': 0.0, 'Total Moves': 1279, 'Backtracks': 0, 'Moves/sec': 1046734.6}
{'Explorer ID': 2, 'Time Taken': 0.0, 'Total Moves': 1279, 'Backtracks': 0, 'Moves/sec': 1013128.39}
{'Explorer ID': 3, 'Time Taken': 0.0, 'Total Moves': 1279, 'Backtracks': 0, 'Moves/sec': 993980.88}
2) When running multiple explorers on the static maze, I noticed that all explorers solved the maze with the same number of moves (1279), because the maze layout was fixed and the explorer algorithm is deterministic.
3) The number of backtracks was zero in all cases, indicating that the algorithm found a clean path without needing to reverse.
4) The only difference between explorers was the Moves per second (Moves/sec), which varied slightly between processes due to the GPU capabilities and efficiency.
### After improvement to the right hand rule
=== Summary of All Explorers ===
{'Explorer ID': 0, 'Time Taken': 0.0, 'Total Moves': 786, 'Backtracks': 85, 'Moves/sec': 400719.94}
{'Explorer ID': 1, 'Time Taken': 0.0, 'Total Moves': 786, 'Backtracks': 85, 'Moves/sec': 418100.56}
{'Explorer ID': 2, 'Time Taken': 0.0, 'Total Moves': 786, 'Backtracks': 85, 'Moves/sec': 424507.2}
{'Explorer ID': 3, 'Time Taken': 0.0, 'Total Moves': 786, 'Backtracks': 85, 'Moves/sec': 423797.78}


   
### Question 4 (20 points)
Based on your analysis from Question 3, propose and implement enhancements to the maze explorer to overcome its limitations.
### Answer:
***Identified Limitations of the Original (Right-Hand Rule) Explorer***
1) Non-optimal pathfinding:
The right-hand rule is a heuristic method. While it can solve a maze, it doesn’t guarantee the shortest path and often leads to unnecessary detours.
2) Backtracking overhead:
The explorer needs to remember where it’s been and manually backtrack to previous junctions when stuck, which increases move count and runtime.
3) Repetitive behavior:
It may re-explore parts of the maze it has already checked, especially without tracking decision paths effectively.
4) No learning or optimization:
The explorer always follows the same logic and cannot adapt or improve its path based on previous runs.

***Implemented Enhancements (2 Key Improvements)***
1. Path Optimality with A*

We replaced the trial-and-error exploration of the right-hand rule with a heuristic-based search. A* uses a priority queue to always expand the most promising path first, guaranteeing the shortest path in grid-based mazes.

2. No Backtracking Required

The A* algorithm doesn’t need to backtrack manually. It constructs the optimal path from start to goal in a single pass by remembering the parent of each visited cell
***Modified Code***
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

    self.print_statistics(time_taken)
    return time_taken, self.moves

### Question 5 (20 points)
Compare the performance of your enhanced explorer with the original:
### Answer:
***Performance Comparison – Original vs Enhanced Explorer***

| Metric              |Right-Hand Rule Explorer(imp) | A* Explorer          |
|---------------------|--------------------------|----------------------|
| Total Moves         | ~786                     | 128                  |
| Backtracks          | 85                       | 0                    |
| Time Taken          | ~0.01–0.05 sec           | 0.00 sec             |
| Optimal Path        | No                       | Yes                  |
| Deterministic       | Yes                      | Yes                  |
| Repeated Paths      | Yes                      | No                   |

***Trade-Offs and Features – Right-Hand Rule vs A***
### Trade-Offs and Features – Right-Hand Rule vs A*

| Aspect                  | Right-Hand Rule          | A* Algorithm              |
|-------------------------|--------------------------|---------------------------|
| Simplicity              | Very easy to implement   | Slightly more complex     |
| Shortest Path Guarantee | No                       | Yes                       |
| Memory Usage            | Low                      | Moderate                  |
| Backtracking Required   | Yes                      | No                        |
| Exploratory Efficiency  | Poor                     | Excellent                 |
| Suitable for Dynamic Mazes | Good                 | Better for static         |

### Question 6 (10 points)

### Answer: 
Achieve the best result of 128 moves
















