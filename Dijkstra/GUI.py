import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import networkx as nx
from algorithm import distance_calculator
import numpy as np

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
    G.add_edge("h", "e", weight=0.5)

    elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > 5]
    esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] <= 5]

    pos = nx.circular_layout(G, scale=1, center=(0, 0))
  # positions for all nodes

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
    pos = nx.circular_layout(G, scale=1, center=(0, 0))

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


def onRunAlgorithm(G):
    # Assuming 'a' is the source and 'f' is the target for the demonstration
    source = 'b'
    target = 'e'
    
    # Run Dijkstra's algorithm to find the shortest path
    shortest_path = nx.dijkstra_path(G, source=source, target=target, weight='weight')
    # Convert the result into a string to display
    result_text = "Result: " + " -> ".join(shortest_path)
    
    # Update the result label
    result.config(text=result_text)

    # Highlight the shortest path in the graph
    highlightPath(G, shortest_path)
    

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



# Result
result_frame = tk.Frame(m)
result = tk.Label(result_frame, text="", font=("Arial", 16))
result.pack(side="bottom")
result_frame.pack(side="top", fill="x")

# Buttons
button_frame = tk.Frame(m)

draw = tk.Button(button_frame, text="Draw Graph", command=onDrawGraph)
draw.grid(row=0, column=0)  # Place button in the middle column
run = tk.Button(button_frame, text="Run Algorithm", command=lambda: onRunAlgorithm(drawGraph(fig)))
run.grid(row=0, column=1)

button_frame.pack(side="top")


# Tool bar
toolbar_frame = tk.Frame(m)
toolbar = NavigationToolbar2Tk(canvas, toolbar_frame, pack_toolbar=False)
toolbar.update()
toolbar.pack(anchor = "sw", fill = tk.X)
toolbar_frame.pack(side="top", fill="x")




m.mainloop()