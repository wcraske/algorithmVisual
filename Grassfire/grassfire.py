from collections import deque

class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, u, v):
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []
        self.graph[u].append(v)

    def grassfire(self, startNode):
        visited = {}
        distance = {}
        predecessor = {}

        for node in self.graph:
            visited[node] = False
            distance[node] = int(-1)
            predecessor[node] = None


        arr = deque([startNode])
        visited[startNode] = True
        distance[startNode] = 0

        while arr:
            current_node = arr.popleft()
            
            for n in self.graph.get(current_node, []):
                if not visited[n]:
                    visited[n] = True
                    arr.append(n)
                    distance[n] = distance[current_node] + 1
                    predecessor[n] = current_node                    

        for x in distance:
            if distance[x] == -1:
                distance[x] = "Not possible to reach from start node"
        
        return distance, predecessor

    def reconstruct_path(self, startNode, goalNode, predecessor):
        path = []
        current_node = goalNode
        while current_node is not None:
            path.append(current_node)
            current_node = predecessor[current_node]
        path.reverse()
        if path[0] == startNode:
            return path
        else:
            return "No path from start node to goal node!"

if __name__ == "__main__":
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
        graph.add_edge(vertex1, vertex2)
        num = num - 1
    startNode = 0
    distances = graph.grassfire(startNode)
    dis = distances[0]
    predes = distances[1]
    print("Distances from start node", startNode, ":", dis) 
    goalNode = int(input("Enter in the goal vertex number: "))
    path = graph.reconstruct_path(startNode, goalNode, predes)
    print("Path from start node", startNode, "to node", goalNode, ":", path)