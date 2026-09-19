from pathlib import Path  # for OS paths and files
from graph_algorithms import *  # for path planning - ie the code from previous labs
from visualize import Animation
import time

def import_instance(filename):
    """ Import a CSV file representing a grid with start and finish positions.
    
    Args:
        filename - a string with the filename of a file in the current directory.
    """
    f = Path(filename)
    if not f.is_file():
        raise BaseException(filename + " does not exist.")
    f = open(filename, 'r')
    # first line: #rows #columns
    data = f.readline().split(',')
    rows = int(data[0])
    columns = int(data[1])
    print("rows: ", rows, "; columns: ", columns)
    grid = []
    start = None
    finish = None
    for r in range(rows):
        line = f.readline().split(',')
        grid.append([])
        for c in range(columns):
            if line[c] == 'X' or line[c] == 'X\n':
                grid[-1].append('X')
            else:
                grid[-1].append(line[c])
                if line[c] == 'F':
                    finish = (r,c)
                elif line[c] == 'S':
                    start = (r,c)
    f.close()
    if start is None or finish is None:
        print("ERROR: start =", start, "; finish =", finish)
        exit(1)
    return grid, start, finish


def runsearch(file):
    grid, start, finish = import_instance(file)

    # Record time taken to create graph
    start_time = time.time()
    graph = Graph() 
    graph.create_from_grid(grid)
    end_time = time.time()
    print(f"Graph creation time: {end_time - start_time:.3f} seconds")

    # Record time taken to find shortest path
    sv = graph.get_vertex_by_label(start)
    fv = graph.get_vertex_by_label(finish)
    start_time = time.time()
    pd = graph.dijkstra(sv)
    end_time = time.time()
    print(f"Time taken to find shortest path using Dijkstra's algorithm: {end_time - start_time:.5f} seconds")
    path, cost = graph.extract_path(pd,finish)
    print("Path:", path, "Cost:", cost)
    print("Path cost:", cost)

    # Compare A* to Dijkstra's algorithm.
    start_time = time.time()
    pd = graph.a_star(sv, fv)
    end_time = time.time()
    path, cost = graph.extract_path(pd,finish)
    print(f"A* time taken: {end_time - start_time:.5f} seconds")
    print("A* path cost:", cost)

    start_time = time.time()
    pd = graph.dijkstra(sv)
    end_time = time.time()
    path, cost = graph.extract_path(pd,finish)
    print(f"Dijkstra's algorithm time taken: {end_time - start_time:.5f} seconds")
    print("Dijkstra's algorithm path cost:", cost)
    print("\n")

    animation = Animation(grid, start, finish, path)
    animation.show()
    

if __name__ == '__main__':
    print("Enter grid CSV file name: ")
    file_name = input()
    runsearch(file_name)
