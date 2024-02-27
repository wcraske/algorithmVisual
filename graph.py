import tkinter as tk

def draw_node():
    print("Draw Node button clicked")

def draw_edge():
    print("Draw Edge button clicked")

# Create main window
root = tk.Tk()
root.title("Graph Editor")

# Set window size
root.geometry("800x600")

# Create frame for buttons
button_frame = tk.Frame(root)
button_frame.pack(side="top", fill="x")

# Create Draw Node button
draw_node_button = tk.Button(button_frame, text="Draw Node", command=draw_node)
draw_node_button.pack(side="left", padx=5, pady=5)

# Create Draw Edge button
draw_edge_button = tk.Button(button_frame, text="Draw Edge", command=draw_edge)
draw_edge_button.pack(side="left", padx=5, pady=5)

# Start the GUI event loop
root.mainloop()