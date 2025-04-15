"""
Main entry point for the maze runner game.
"""

import argparse
import multiprocessing
from src.game import run_game
from src.explorer import Explorer
from src.maze import create_maze

def run_explorer_instance(explorer_id, width, height, maze_type):
    maze = create_maze(width, height, maze_type)
    explorer = Explorer(maze, visualize=False)
    time_taken, moves = explorer.solve()
    return {
        "Explorer ID": explorer_id,
        "Time Taken": round(time_taken, 2),
        "Total Moves": len(moves),
        "Backtracks": explorer.backtrack_count,
        "Moves/sec": round(len(moves) / time_taken, 2) if time_taken > 0 else 0
    }

def run_parallel_explorers(count, width, height, maze_type):
    with multiprocessing.Pool(processes=count) as pool:
        args = [(i, width, height, maze_type) for i in range(count)]
        results = pool.starmap(run_explorer_instance, args)

    print("\n=== Summary of All Explorers ===")
    for result in results:
        print(result)

    best = min(results, key=lambda r: r["Total Moves"])
    print("\n=== Best Explorer ===")
    print(best)

def main():
    parser = argparse.ArgumentParser(description="Maze Runner Game")
    parser.add_argument("--type", choices=["random", "static"], default="random",
                        help="Type of maze to generate (random or static)")
    parser.add_argument("--width", type=int, default=30,
                        help="Width of the maze (default: 30, ignored for static mazes)")
    parser.add_argument("--height", type=int, default=30,
                        help="Height of the maze (default: 30, ignored for static mazes)")
    parser.add_argument("--auto", action="store_true",
                        help="Run automated maze exploration")
    parser.add_argument("--visualize", action="store_true",
                        help="Visualize the automated exploration in real-time")
    parser.add_argument("--parallel", type=int, default=0,
                        help="Run multiple explorers in parallel (number of explorers)")

    args = parser.parse_args()

    if args.parallel > 0:
        run_parallel_explorers(args.parallel, args.width, args.height, args.type)
    elif args.auto:
        maze = create_maze(args.width, args.height, args.type)
        explorer = Explorer(maze, visualize=args.visualize)
        time_taken, moves = explorer.solve()
        print(f"Maze solved in {time_taken:.2f} seconds")
        print(f"Number of moves: {len(moves)}")
        if args.type == "static":
            print("Note: Width and height arguments were ignored for the static maze")
    else:
        run_game(maze_type=args.type, width=args.width, height=args.height)

if __name__ == "__main__":
    main()
