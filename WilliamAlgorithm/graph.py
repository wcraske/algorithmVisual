import tkinter as tk
import math

def draw_node(event):
    x, y = event.x, event.y
    #check if the new circle will overlap with any existing circles
    overlap = False
    for node_x, node_y in nodes:
        if (x - node_x) ** 2 + (y - node_y) ** 2 <= (2 * node_radius) ** 2:  #check if distance <= sum of radius
            overlap = True
            break
    #draw the circle only if there is no overlap
    if not overlap:
        canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius)
        nodes.append((x, y))
    print("Nodes:", nodes)  #print nodes list after drawing a node


def draw_edge_start(event):
    global start_node
    x, y = event.x, event.y
    #find the node closest to the click
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
    #find the node closest to the click
    min_dist = float('inf')
    closest_node = None
    for node_x, node_y in nodes:
        dist = (x - node_x) ** 2 + (y - node_y) ** 2
        if dist < min_dist:
            min_dist = dist
            closest_node = (node_x, node_y)
            closest_index = nodes.index((node_x, node_y))
    end_node = closest_node
    #draw the edge between the nodes
    if start_node and end_node and start_node != end_node:  #make sure start node and end node are different
        edge = (nodes.index(start_node), closest_index)
        #check if the edge already exists in the list
        if edge not in edges and edge[::-1] not in edges:
            canvas.create_line(start_node, end_node)
            edges.append(edge)  #add edge to the list
        start_node = None
    print("Edges:", edges)  #print edges list after drawing an edge


def activate_draw_node():
    canvas.bind("<Button-1>", draw_node)
    canvas.unbind("<Button-3>")  #deactivate draw_edge
    draw_node_button.config(relief=tk.SUNKEN)
    draw_edge_button.config(relief=tk.RAISED)
    run_algorithm_button.config(relief=tk.RAISED)  #reactivate run_algorithm_button


def activate_draw_edge():
    canvas.bind("<Button-1>", draw_edge_start)
    canvas.bind("<ButtonRelease-1>", draw_edge_end)
    canvas.unbind("<Button-3>")  #deactivate draw_node
    draw_edge_button.config(relief=tk.SUNKEN)
    draw_node_button.config(relief=tk.RAISED)
    run_algorithm_button.config(relief=tk.RAISED)  #reactivate run_algorithm_button


def activate_run_algorithm():
    canvas.unbind("<Button-1>")  #deactivate draw_node
    canvas.unbind("<ButtonRelease-1>")  #deactivate draw_edge
    run_algorithm_button.config(relief=tk.SUNKEN)
    draw_node_button.config(relief=tk.RAISED)
    draw_edge_button.config(relief=tk.RAISED)
    print("Euclidean Distances:")
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            dist = euclidean_distance(nodes[i], nodes[j])
            print(f"Node {i+1} to Node {j+1}: {dist}")

    print("\nManhattan Distances:")
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            dist = manhattan_distance(nodes[i], nodes[j])
            print(f"Node {i+1} to Node {j+1}: {dist}")


def manhattan_distance(node1, node2):
    return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])


def euclidean_distance(node1, node2):
    return math.sqrt((node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2)


#create main window
root = tk.Tk()
root.title("Graph Editor")
root.geometry("800x600")

#create frame for buttons
button_frame = tk.Frame(root)
button_frame.pack(side="top", fill="x")

#create draw node button
draw_node_button = tk.Button(button_frame, text="Draw Node", command=activate_draw_node, relief=tk.RAISED)
draw_node_button.pack(side="left", padx=5, pady=5)

#create draw edge button
draw_edge_button = tk.Button(button_frame, text="Draw Edge", command=activate_draw_edge, relief=tk.RAISED)
draw_edge_button.pack(side="left", padx=5, pady=5)

#create run algorithm button
run_algorithm_button = tk.Button(button_frame, text="Run Algorithm", command=activate_run_algorithm, relief=tk.RAISED)
run_algorithm_button.pack(side="left", padx=5, pady=5)

#create canvas
canvas = tk.Canvas(root, bg="white")
canvas.pack(fill="both", expand=True)

#node aspects
nodes = []
node_radius = 30
start_node = None

#edge aspects
edges = []

root.mainloop()
