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

    def reconstruct_path(self, startNode, goalNode, predecessor):
        path = []
        current_node = goalNode
        while current_node is not False:
            path.append(current_node)
            current_node = predecessor[current_node]
        path.reverse()
        if path[0] == startNode:
            return path
        else:
            return "No path from start node to goal node!"

graph = Graph()
print("\n")
print("Welcome to the Grassfire Algorithm Implementation on a Graph Data Structure!")
print("Important Info: The start node is always 0!")
print("\n")
num = int(input("Enter in the number of edges in the graph: "))
print("\n")
while num > 0:
    vertex1 = int(input("Enter in the first vertex of the edge: "))
    vertex2 = int(input("Enter in the second vertex of the edge: "))
    print("\n")
    graph.addEdge(vertex1, vertex2)
    num = num - 1
startNode = 0
distances = graph.grassfire(startNode)
dis = distances[0]
predes = distances[1]
print("Distances from start node", startNode, ":", dis) 
goalNode = int(input("Enter in the goal vertex number: "))
path = graph.reconstruct_path(startNode, goalNode, predes)
print("Path from start node", startNode, "to node", goalNode, ":", path)