

import heapq
import networkx as nx
# import matplotlib.pyplot as plt

# Create a weighted graph
G = nx.Graph()

G.add_edge("a", "b", weight=6)
G.add_edge("a", "c", weight=2)
G.add_edge("c", "d", weight=1)
G.add_edge("c", "e", weight=7)
G.add_edge("c", "f", weight=9)
G.add_edge("a", "d", weight=3)
G.add_edge("b", "g", weight=4)
G.add_edge("g", "c", weight=5)
G.add_edge("b", "d", weight=1)


def distance_calculator(G, start):
    queue = []  # priority queue to store entries in the form: (distance, node)
    heapq.heappush(queue, (0, start))  # add start node to the queue

    # initialize the distance from start to all other nodes as infinity
    distance = {node: float("inf") for node in G.nodes}
    distance[start] = 0


    while queue:
        current_distance, current_node = heapq.heappop(queue)

        # if the distance is already larger than the current distance, skip
        if current_distance > distance[current_node]:   
            continue
        # iterate through all neighbors of the current node
        for neighbor, weight in G[current_node].items():
            distance_through_current = current_distance + weight["weight"]
            if distance_through_current < distance[neighbor]:
                distance[neighbor] = distance_through_current
                heapq.heappush(queue, (distance_through_current, neighbor))

    return distance

print(distance_calculator(G, "a"))