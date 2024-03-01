import tkinter as tk
import math
import heapq
import time

#function to draw the nodes
def draw_node(event): #called when button is clicked
    x, y = event.x, event.y #gets mouse click coordinates
    overlap = False 
    for node_x, node_y in nodes: #iterate through nodes so there is no overlap, does this by checking the combined nodes radius'
        if (x - node_x) ** 2 + (y - node_y) ** 2 <= (2 * node_radius) ** 2:
            overlap = True #if there is an overlap node wont be placed
            break
    if not overlap: #if no overlap, create a circle at the mouse coordinates with a defined radius
        canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius)
        node_index = len(nodes) #calculate the index of the new node
        canvas.create_text(x, y, text=str(node_index))  #display the index inside the bubble
        nodes.append((x, y))#adds the coordinates to a list of nodes. will be used for calculating path
    print("Nodes:", nodes) 

#function to draw edges
def draw_edge_start(event):#called when button is clicked
    global start_node #defines which node we initally pressed from logic below. gloabl so next function can access.
    x, y = event.x, event.y #gets mouse click coordinates
    min_dist = float('inf') #initializes distance of the edge to positive infinity, as place holder
    closest_node = None #closest node is none initially
    for node_x, node_y in nodes: #iterates over exisitng node positions to find closest to mouse click
        dist = (x - node_x) ** 2 + (y - node_y) ** 2 #calculation for choosing node.
        if dist < min_dist: #check if this distance is less than the current minimum distance of nodes
            min_dist = dist #if it is assign it as closest node
            closest_node = (node_x, node_y)
    start_node = closest_node #assign the starting node as the closest node to button


def draw_edge_end(event):#called when mouse is released
    global start_node
    x, y = event.x, event.y
    min_dist = float('inf')#initializes distance of the edge to positive infinity, as place holder
    closest_node = None
    for node_x, node_y in nodes:#iterates over exisitng node positions to find closest to mouse release
        dist = (x - node_x) ** 2 + (y - node_y) ** 2
        if dist < min_dist:
            min_dist = dist
            closest_node = (node_x, node_y)
            closest_index = nodes.index((node_x, node_y))#gets the index of the discovered node
    end_node = closest_node
    if start_node and end_node and start_node != end_node:#checks if the nodes are not the same, so there are connecting the same node
        edge = (nodes.index(start_node), closest_index)#defines the edge indexes to know which nodes are connected
        if edge not in edges and edge[::-1] not in edges:#checks if nodes are already connected, to avoid repeats
            canvas.create_line(start_node, end_node)#draws line
            edges.append(edge)#adds the edge to the list
        start_node = None
    print("Edges:", edges)


def activate_draw_node():#gui code to define the buttons
    canvas.bind("<Button-1>", draw_node)
    canvas.unbind("<Button-3>")
    draw_node_button.config(relief=tk.SUNKEN)
    draw_edge_button.config(relief=tk.RAISED)
    run_algorithm_button.config(relief=tk.RAISED)


def activate_draw_edge():#gui code to define the buttons
    canvas.bind("<Button-1>", draw_edge_start)
    canvas.bind("<ButtonRelease-1>", draw_edge_end)
    canvas.unbind("<Button-3>")
    draw_edge_button.config(relief=tk.SUNKEN)
    draw_node_button.config(relief=tk.RAISED)
    run_algorithm_button.config(relief=tk.RAISED)


def activate_run_algorithm():#gui code to define the buttons
    canvas.unbind("<Button-1>")
    canvas.unbind("<ButtonRelease-1>")
    run_algorithm_button.config(relief=tk.SUNKEN)
    draw_node_button.config(relief=tk.RAISED)
    draw_edge_button.config(relief=tk.RAISED)
    
    #implement A* algorithm
    print("Running A* algorithm...")
    start_index = 0 #makes the first node placed the starting node
    goal_index = len(nodes) - 1#makes the last node placed the goal node
    path = astar(nodes, edges, start_index, goal_index)#calls the astar function to get the optimal list
    if path:#if path is not empty
        print("Best path found:", path)
        for node_index in path:#iterate throught the node index
            x, y = nodes[node_index]#retrieves coordinates for each node 
            canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, fill="green")#cover the nodes with green for optimal path
            canvas.create_text(x, y, text=str(node_index))  #display the index inside the bubble
            root.update()#updates canvas 
            time.sleep(1)#wait 1 second inbetween coloring green
        
    else:
        print("No path found.")


def manhattan_distance(node1, node2):#gets manhattan distance as used for path cost value
    return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])


def euclidean_distance(node1, node2):#gets euclidean distance as used for heuristic cost value
    return math.sqrt((node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2)



def astar(nodes, edges, start, goal):
    potential_nodes = [(0, start)] #priority queue as a heap for potential nodes, starting with first node
    previous = {} #keeps track of optimal path
    g_value = {i: float('inf') for i in range(len(nodes))} #cheapest path cost so far. all nodes contain positive infinity until they are branched
    g_value[start] = 0 #start with inital node as value 0
    f_value = {i: float('inf') for i in range(len(nodes))} #estimated path cost so far. all nodes contain positive infinity until they are branched
    f_value[start] = heuristic(nodes[start], nodes[goal])# to calculate f value, call heurisitc with the start and goal node

    while potential_nodes:#while potential nodes is not empty
        current_f, current = heapq.heappop(potential_nodes) #pops node with lowest f value from the potential nodes, this node will now be explored
        if current == goal:#base case, if the current node is the goal node, reconstruct the path.
            return reconstruct_path(previous, current)
        
        canvas.create_oval(nodes[current][0] - node_radius, nodes[current][1] - node_radius, nodes[current][0] + node_radius, nodes[current][1] + node_radius, fill="yellow")#make the explored nodes yellow
        
        root.update()#updates canvas and sleeps
        time.sleep(1)
        #exploration of nodes
        for neighbor in get_neighbors(edges, current):#iterates over neighbours of the current node
            potential_g_value = g_value[current] + distance(nodes[current], nodes[neighbor])#calculate the potential gvalue for each of the neighbours
            if potential_g_value < g_value[neighbor]:#if it is lower than other neighbours, update all values for optimal path
                previous[neighbor] = current
                g_value[neighbor] = potential_g_value
                f_value[neighbor] = g_value[neighbor] + heuristic(nodes[neighbor], nodes[goal])
                heapq.heappush(potential_nodes, (f_value[neighbor], neighbor))#push the neighbour node onto the potential nodes with the updated value.
    
    return None


def reconstruct_path(previous, current):#function to map the current
    total_path = [current]#starts list with the goal node
    while current in previous:#whbile theres a node in previous, update current node to the node before, and insert it into the total path at the beginning
        current = previous[current]
        total_path.insert(0, current)
    return total_path


def get_neighbors(edges, node):#function to get neighbouring nodes
    neighbors = []
    for edge in edges:#iterate through the edges and checks the edge is connected to the current node and appends the node it is connected to 
        if edge[0] == node:
            neighbors.append(edge[1])
        elif edge[1] == node:
            neighbors.append(edge[0])
    return neighbors


def distance(node1, node2):#helper function for euclidean
    return manhattan_distance(node1, node2)


def heuristic(node1, node2):#helper function for heurstic
    return euclidean_distance(node1, node2)

#initalizing the window
root = tk.Tk()
root.title("Graph Editor")
root.geometry("800x600")

#creates buttons
button_frame = tk.Frame(root)
button_frame.pack(side="top", fill="x")

draw_node_button = tk.Button(button_frame, text="Draw Node", command=activate_draw_node, relief=tk.RAISED)
draw_node_button.pack(side="left", padx=5, pady=5)

draw_edge_button = tk.Button(button_frame, text="Draw Edge", command=activate_draw_edge, relief=tk.RAISED)
draw_edge_button.pack(side="left", padx=5, pady=5)

run_algorithm_button = tk.Button(button_frame, text="Run Algorithm", command=activate_run_algorithm, relief=tk.RAISED)
run_algorithm_button.pack(side="left", padx=5, pady=5)

#create canvas
canvas = tk.Canvas(root, bg="white")
canvas.pack(fill="both", expand=True)


#node values
nodes = []
node_radius = 30
start_node = None
#edges list
edges = []

root.mainloop()