from mpi4py import MPI
import argparse
from src.maze import create_maze
from src.explorer import Explorer

def run_explorer(rank, width, height, maze_type):
    maze = create_maze(width, height, maze_type)
    explorer = Explorer(maze, visualize=False)
    time_taken, moves = explorer.solve()
    stats = {
        "Explorer ID": rank,
        "Time Taken": round(time_taken, 2),
        "Total Moves": len(moves),
        "Backtracks": explorer.backtrack_count,
        "Moves/sec": round(len(moves) / time_taken, 2) if time_taken > 0 else 0
    }
    return stats

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="MPI Maze Explorer")
    parser.add_argument("--type", choices=["random", "static"], default="random",
                        help="Maze type: 'random' (default) or 'static'")
    parser.add_argument("--width", type=int, default=30,
                        help="Maze width (only applies to random maze)")
    parser.add_argument("--height", type=int, default=30,
                        help="Maze height (only applies to random maze)")
    args = parser.parse_args()

    # MPI setup
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Adjust behavior for static maze
    width = args.width
    height = args.height
    if args.type == "static":
        if rank == 0:
            print("[Info] Static maze selected — ignoring width and height values.")
        width = 0
        height = 0

    if rank == 0:
        print(f"[Master] Running {size} explorers")
        print(f"Maze Type: {args.type}")
        if args.type == "random":
            print(f"Maze Size: {args.width} x {args.height}")
        print()

    # Run the explorer for this process
    result = run_explorer(rank, args.width, args.height, args.type)

    # Gather and print results
    results = comm.gather(result, root=0)

    if rank == 0:
        print("=== Summary of All Explorers ===")
        for res in results:
            print(res)
        best = min(results, key=lambda r: r["Total Moves"])
        print("\n=== Best Explorer ===")
        print(best)

if __name__ == "__main__":
    main()
