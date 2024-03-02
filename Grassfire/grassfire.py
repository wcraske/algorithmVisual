def grassfire(graph, start_node):
    visited = {}
    distance = {}

    for node in graph:
        visited[node] = False
        distance[node] = int(-1)

    arr = {}
    arr.append(start_node)
    distance[start_node] = 0

    while arr:
        current_node = arr.popleft()
        visited[current_node] = True
        
        for n in graph.get(current_node, []):
            if not visited[n]:
                arr.append[n]
                visited[n] = True
                distance[n] = distance[current_node] + 1

    for x in distance:
        if distance[x] == -1:
            distance[x] = "Not possible to reach from start node"
    
    return distance




