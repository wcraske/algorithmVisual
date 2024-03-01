import tkinter as tk
import math
import heapq
import time

def draw_node(event):
    x, y = event.x, event.y
    overlap = False
    for node_x, node_y in nodes:
        if (x - node_x) ** 2 + (y - node_y) ** 2 <= (2 * node_radius) ** 2:
            overlap = True
            break
    if not overlap:
        canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius)
        node_index = len(nodes) #calculate the index of the node
        canvas.create_text(x, y, text=str(node_index))  #display the index inside the bubble
        nodes.append((x, y))
    print("Nodes:", nodes)


def draw_edge_start(event):
    global start_node
    x, y = event.x, event.y
    min_dist = float('inf')
    closest_node = None
    for node_x, node_y in nodes:
        dist = (x - node_x) ** 2 + (y - node_y) ** 2
        if dist < min_dist:
            min_dist = dist
            closest_node = (node_x, node_y)
    start_node = closest_node


def draw_edge_end(event):
    global start_node
    x, y = event.x, event.y
    min_dist = float('inf')
    closest_node = None
    for node_x, node_y in nodes:
        dist = (x - node_x) ** 2 + (y - node_y) ** 2
        if dist < min_dist:
            min_dist = dist
            closest_node = (node_x, node_y)
            closest_index = nodes.index((node_x, node_y))
    end_node = closest_node
    if start_node and end_node and start_node != end_node:
        edge = (nodes.index(start_node), closest_index)
        if edge not in edges and edge[::-1] not in edges:
            canvas.create_line(start_node, end_node)
            edges.append(edge)
        start_node = None
    print("Edges:", edges)


def activate_draw_node():
    canvas.bind("<Button-1>", draw_node)
    canvas.unbind("<Button-3>")
    draw_node_button.config(relief=tk.SUNKEN)
    draw_edge_button.config(relief=tk.RAISED)
    run_algorithm_button.config(relief=tk.RAISED)


def activate_draw_edge():
    canvas.bind("<Button-1>", draw_edge_start)
    canvas.bind("<ButtonRelease-1>", draw_edge_end)
    canvas.unbind("<Button-3>")
    draw_edge_button.config(relief=tk.SUNKEN)
    draw_node_button.config(relief=tk.RAISED)
    run_algorithm_button.config(relief=tk.RAISED)


def activate_run_algorithm():
    canvas.unbind("<Button-1>")
    canvas.unbind("<ButtonRelease-1>")
    run_algorithm_button.config(relief=tk.SUNKEN)
    draw_node_button.config(relief=tk.RAISED)
    draw_edge_button.config(relief=tk.RAISED)
    
    #implement A* algorithm
    print("Running A* algorithm...")
    start_index = 0
    goal_index = len(nodes) - 1
    path = astar(nodes, edges, start_index, goal_index)
    if path:
        print("Best path found:", path)
        for node_index in path:
            x, y = nodes[node_index]
            canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, fill="green")
            canvas.create_text(x, y, text=str(node_index))  #display the index inside the bubble
            root.update()
            time.sleep(1)
        
    else:
        print("No path found.")


def manhattan_distance(node1, node2):
    return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])


def euclidean_distance(node1, node2):
    return math.sqrt((node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2)


def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.insert(0, current)
    return total_path


def astar(nodes, edges, start, goal):
    open_set = [(0, start)] #priority queue as a heap for potential nodes
    came_from = {} #keeps track of optimal path
    g_score = {i: float('inf') for i in range(len(nodes))} #cheapest path cost so far
    g_score[start] = 0
    f_score = {i: float('inf') for i in range(len(nodes))} #estimated path cost so afar
    f_score[start] = heuristic(nodes[start], nodes[goal])

    while open_set:
        current_f, current = heapq.heappop(open_set)
        if current == goal:
            return reconstruct_path(came_from, current)
        
        canvas.create_oval(nodes[current][0] - node_radius, nodes[current][1] - node_radius, nodes[current][0] + node_radius, nodes[current][1] + node_radius, fill="yellow")
        root.update()
        time.sleep(1)
        
        for neighbor in get_neighbors(edges, current):
            tentative_g_score = g_score[current] + distance(nodes[current], nodes[neighbor])
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(nodes[neighbor], nodes[goal])
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return None


def get_neighbors(edges, node):
    neighbors = []
    for edge in edges:
        if edge[0] == node:
            neighbors.append(edge[1])
        elif edge[1] == node:
            neighbors.append(edge[0])
    return neighbors


def distance(node1, node2):
    return euclidean_distance(node1, node2)


def heuristic(node1, node2):
    return euclidean_distance(node1, node2)


root = tk.Tk()
root.title("Graph Editor")
root.geometry("800x600")

button_frame = tk.Frame(root)
button_frame.pack(side="top", fill="x")

draw_node_button = tk.Button(button_frame, text="Draw Node", command=activate_draw_node, relief=tk.RAISED)
draw_node_button.pack(side="left", padx=5, pady=5)

draw_edge_button = tk.Button(button_frame, text="Draw Edge", command=activate_draw_edge, relief=tk.RAISED)
draw_edge_button.pack(side="left", padx=5, pady=5)

run_algorithm_button = tk.Button(button_frame, text="Run Algorithm", command=activate_run_algorithm, relief=tk.RAISED)
run_algorithm_button.pack(side="left", padx=5, pady=5)

canvas = tk.Canvas(root, bg="white")
canvas.pack(fill="both", expand=True)

nodes = []
node_radius = 30
start_node = None

edges = []

root.mainloop()
