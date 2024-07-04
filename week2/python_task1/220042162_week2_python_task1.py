# 220042162 week2 python task1 graph trversal in shortest path
# I'll use Dijkstra's algorithm for this
# [please place an input.txt file next to it]


import sys
from heapq import heapify, heappush


def dijkstra(graph, start, end):
    start = str(start)
    end = str(end)
    n = len(graph)

    # create container for vertex data
    vertex_data = {}
    for vertex in graph:
        vertex_data[vertex] = {"dist": float("inf"), "prev": []}

    vertex_data[start]["dist"] = 0
    visited = []
    current = start

    # traverse the graph
    for i in range(n - 1):
        if current not in visited:
            visited.append(current)
            min_heap = []

            # traverse the neighbors
            for j in graph[current]:
                if j not in visited:
                    distance = vertex_data[current]["dist"] + graph[current][j]
                    # check if neighbor j has shorter distance
                    if distance < vertex_data[j]["dist"]:
                        vertex_data[j]["dist"] = distance
                        vertex_data[j]["prev"] = vertex_data[current]["prev"] + list(
                            current
                        )
                    heappush(min_heap, (vertex_data[j]["dist"], j))

        heapify(min_heap)
        current = min_heap[0][1]

    path = vertex_data[end]["prev"] + list(end)

    if vertex_data[end]["dist"] == float("inf"):
        return -1, []
    else:
        return vertex_data[end]["dist"], path


def main():
    input = None

    try:
        with open("input.txt", "r") as file:
            input = file.readlines()
    except FileNotFoundError as _:
        print("input.txt not found")
        sys.exit(1)

    first_line = input[0].strip().split()
    n = int(first_line[0])
    e = int(first_line[1])

    edges = []
    for line in input[1 : e + 1]:
        line = line.strip().split()
        values = []
        for value in line:
            values.append(value)

        edge = tuple(values)
        edges.append(edge)

    # create the graph dictionary
    graph = {}
    for i in range(1, n + 1):
        graph[str(i)] = {}

    for s, d, v in edges:
        graph[s][d] = int(v)
        graph[d][s] = int(v)

    start = 1
    end = n

    distance, path = dijkstra(graph, start, end)

    if distance == -1:
        print(-1)
    else:
        for i in path:
            print(i + " ", end="")


if __name__ == "__main__":
    main()
