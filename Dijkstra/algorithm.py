import heapq
import networkx as nx


def distance_calculator(G, start):
    queue = []  # priority queue to store entries in the form: (distance, node)
    heapq.heappush(queue, (0, start))  # add start node to the queue

    # initialize the distance from start to all other nodes as infinity
    distance = {node: float("inf") for node in G.nodes}
    distance[start] = 0  # set the distance from start to start as 0

    # iterate through the priority queue
    while queue:
        current_distance, current_node = heapq.heappop(queue) # pop the node with the smallest distance

        # if the distance is already larger than the current distance, skip
        if current_distance > distance[current_node]:   
            continue
        # iterate through all neighbors of the current node
        for neighbor, weight in G[current_node].items():
            # calculate the distance from start to the neighbor through the current node
            distance_through_current = current_distance + weight["weight"]
            # if the distance is smaller than the current distance, update the distance and add the neighbor to the queue
            if distance_through_current < distance[neighbor]:
                distance[neighbor] = distance_through_current
                heapq.heappush(queue, (distance_through_current, neighbor))

    # return the distance from start to all other nodes
    return distance

