def grassfire(graph, start_node):
    visited = {}
    distance = {}

    for node in graph:
        visited[node] = False
        distance[node] = int(-1)

    arr = {}
    arr.append(start_node)
    distance[start_node] = 0




