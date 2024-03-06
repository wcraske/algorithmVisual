import heapq
import time
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import networkx as nx
from algorithm import reconstruct_path

# Create a weighted graph function
def drawGraph(fig):
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
    G.add_edge("h", "f", weight=1)
    G.add_edge("h", "d", weight=0.5)
    G.add_edge("h", "c", weight=0.5)

    elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > 5]
    esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] <= 5]

    pos = nx.spring_layout(G, seed=7, k = 0.5)  # positions for all nodes
 

    fig.clf()
    ax = fig.add_subplot(111)
    

    # Drawing the graph
    nx.draw_networkx_nodes(G, pos, node_size=700, ax=ax)
    nx.draw_networkx_edges(G, pos, edgelist=elarge, width=3, ax=ax)
    nx.draw_networkx_edges( G, pos, edgelist=esmall, width=3, alpha=0.5, edge_color="b", style="solid", ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif", ax=ax)
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels, ax=ax)
    ax.margins(0.08)
    ax.axis("off")

    # Update canvas
    canvas.draw()

    return G


def onDrawGraph():
    drawGraph(fig)

def highlightPath(G, path):
    # Clear and redraw the graph with the path highlighted
    fig.clf()
    ax = fig.add_subplot(111)
    
    # Draw the whole graph as before
    pos = nx.spring_layout(G, seed=7, k = 0.5)  # positions for all nodes - seed for reproducibility

    nx.draw_networkx_nodes(G, pos, node_size=700, ax=ax) # nodes
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif", ax=ax) # node labels
    nx.draw_networkx_edges(G, pos, edgelist=G.edges, width=4, alpha=0.5, edge_color="grey", style="solid", ax=ax) # edges


    # Draw the shortest path with a different color and style
    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='red', node_size=500, ax=ax)
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2, ax=ax)
    
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif", ax=ax)
    ax.margins(0.08)
    ax.axis("off")
    
    # Update canvas
    canvas.draw()

def updateGraph(G, current_node, distance):
    # Clear and redraw the graph with the current node highlighted
    fig.clf()
    ax = fig.add_subplot(111)
    
    # Draw the whole graph as before
    pos = nx.spring_layout(G, seed=7, k = 0.5)  # positions for all nodes - seed for reproducibility

    nx.draw_networkx_nodes(G, pos, node_size=700, ax=ax) # nodes
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif", ax=ax) # node labels
    nx.draw_networkx_edges(G, pos, edgelist=G.edges, width=4, alpha=0.5, edge_color="grey", style="solid", ax=ax) # edges

    # draw the visited nodes with a different color
    visited_nodes = [node for node in distance if distance[node] != float("inf")]
    nx.draw_networkx_nodes(G, pos, nodelist=visited_nodes, node_color='green', node_size=500, ax=ax)

    # Draw the current node with a different color
    nx.draw_networkx_nodes(G, pos, nodelist=[current_node], node_color='red', node_size=500, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif", ax=ax)
    ax.margins(0.08)
    ax.axis("off")
    
    # Update canvas
    canvas.draw()

def onRunAlgorithmStep(G, start, goal, queue, distance, predecessor, current_node=None):
    if not queue:
        # Algorithm finished, trace and highlight the shortest path
        shortest_path = reconstruct_path(predecessor, start, goal)
        result_text = "Result: " + " -> ".join(shortest_path)
        result.config(text=result_text, fg="green")
        highlightPath(G, shortest_path)
        return

    if current_node:
        # Process current node, update graph visualization
        updateGraph(G, current_node, distance)
        m.update()  # Make sure the update is reflected in the GUI
        time.sleep(0.5)  # Delay to allow observation, adjust as needed

    # Proceed with algorithm, schedule next step
    current_distance, current_node = heapq.heappop(queue)
    if current_distance <= distance[current_node]:
        for neighbor, weight in G[current_node].items():
            distance_through_current = current_distance + weight["weight"]
            if distance_through_current < distance[neighbor]:
                distance[neighbor] = distance_through_current
                predecessor[neighbor] = current_node
                heapq.heappush(queue, (distance_through_current, neighbor))
    m.after(1000, lambda: onRunAlgorithmStep(G, start, goal, queue, distance, predecessor, current_node))

def onRunAlgorithm(G, start, goal):
    if start == "" or goal == "":
        result.config(text="Please enter start and goal nodes", fg="red")
        return

    # Initialize algorithm state
    queue = [(0, start)]
    distance = {node: float("inf") for node in G.nodes}
    distance[start] = 0
    predecessor = {node: None for node in G.nodes}

    # Start step-by-step execution
    onRunAlgorithmStep(G, start, goal, queue, distance, predecessor)

    

# Tkinter GUI initialization
m = tk.Tk()
m.title('Dijkstra Algorithm')
m.geometry('800x600')

# Tkinter application

# Title frame
title_frame = tk.Frame(m)
label = tk.Label(title_frame, text="Dijkstra's Algorithm", font=("Arial", 20))
label.pack()
title_frame.pack(side="top", fill="x")

#Canvas
canvas_frame = tk.Frame(m)
fig = plt.Figure(figsize=(5, 4))
canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()
canvas_widget.config(highlightthickness=2, highlightbackground="black")
canvas_frame.pack(side="top", fill="both", expand=True)

#input frame
start_node = tk.StringVar()
goal_node = tk.StringVar()

input_frame = tk.Frame(m)
input_frame.pack(side="top", fill="x")
start = tk.Label(input_frame, text="Start Node: ", font=("Arial", 14))
start_entry = tk.Entry(input_frame, font=("Arial", 14), textvariable=start_node)
start.grid(row=0, column=0)
start_entry.grid(row=0, column=1)
goal = tk.Label(input_frame, text="Goal Node: ", font=("Arial", 14))
goal_entry = tk.Entry(input_frame, font=("Arial", 14), textvariable=goal_node)
goal.grid(row=0, column=2)
goal_entry.grid(row=0, column=3)


# Result
result_frame = tk.Frame(m)
result = tk.Label(result_frame, text="", font=("Arial", 16))
result.pack(side="bottom")
result_frame.pack(side="top", fill="x")

# Buttons
button_frame = tk.Frame(m)

draw = tk.Button(button_frame, text="Draw Graph", command=onDrawGraph)
draw.grid(row=0, column=0)  # Place button in the middle column
run = tk.Button(button_frame, text="Run Algorithm", command=lambda: onRunAlgorithm(drawGraph(fig), start_node.get(), goal_node.get()))
run.grid(row=0, column=1)

button_frame.pack(side="top")


# Tool bar
toolbar_frame = tk.Frame(m)
toolbar = NavigationToolbar2Tk(canvas, toolbar_frame, pack_toolbar=False)
toolbar.update()
toolbar.pack(anchor = "sw", fill = tk.X)
toolbar_frame.pack(side="top", fill="x")




m.mainloop()