
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
   
















