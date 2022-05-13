import math
import time

# Check if inside board, not in obstacle, not in nodes and not in neighbours
def valid(obstacles, x, y):
    result = (x >= 15) and (x < 615) and (y >= 45) and (y < 645) and ((x,y) not in obstacles) and ((x, y) not in nodes) and ((x, y) not in neighbours)
    return result

# Check if 8 possible neighbours are inside the board and appends them
def node_neighbours(x, y, obstacles):
    global parents
    
    if valid(obstacles, x+15, y):
        neighbours.append((x+15, y))      
        # Add parent
        parents.append([ (x+15,y), (x,y) ])

    if valid(obstacles, x-15, y):
        neighbours.append((x-15, y))
        parents.append([ (x-15, y), (x,y) ])

    if valid(obstacles, x, y+15):
        neighbours.append((x, y+15))
        parents.append([ (x, y+15), (x,y) ])

    if valid(obstacles, x, y-15):
        neighbours.append((x, y-15))
        parents.append([ (x, y-15), (x,y) ])

    if valid(obstacles, x+15, y+15):
        if (x, y+15) not in obstacles and (x+15, y) not in obstacles:
            neighbours.append((x+15, y+15))
            parents.append([ (x+15, y+15), (x,y) ])

    if valid(obstacles, x+15, y-15):
        if (x, y-15) not in obstacles and (x+15, y) not in obstacles:
            neighbours.append((x+15, y-15))
            parents.append([ (x+15, y-15), (x,y) ])

    if valid(obstacles, x-15, y+15):
        if (x, y+15) not in obstacles and (x-15, y) not in obstacles:
            neighbours.append((x-15, y+15))
            parents.append([ (x-15, y+15), (x,y) ])
        
    if valid(obstacles, x-15, y-15):
        if (x, y-15) not in obstacles and (x-15, y) not in obstacles:
            neighbours.append((x-15, y-15))
            parents.append([ (x-15, y-15), (x,y) ])
    

# Neighbours of point_A
def first_neighbours(obstacles, point_A):
    global neighbours
    global nodes
    global parents

    parents.append([point_A,()])

    # Get neighbours of point_A
    x,y = point_A
    node_neighbours(x, y, obstacles)
    nodes.append(point_A)


# Go through all nodes to find new neighbours
def new_neighbours(obstacles):
    global neighbours
    
    neighbours.clear()

    # Get neighbours from nodes
    for node in nodes:
        x,y = node
        node_neighbours(x,y, obstacles)


# Check if found point_B
def found_B(point_B):
    finding = True
    global neighbours

    for n in neighbours:
        if n == point_B:          
            neighbours.remove(n)
            finding = False
    return finding
        
    


# Get center coords of square
def center(x,y):
    return x+7.5, y+7.5


# Distance between two points
def distance(u1,w1,u2,w2):
    return math.sqrt( (u1-u2)**2 + (w1-w2)**2 )


# Path already taken
def g(n, point_A):
    lenght = 0
    x,y = n
    u1,w1 = center(x,y)
    done = False

    while not done:
        # First x,y is parent of n. Then x,y is grandparent of n
        for p in parents:
            if (x,y) == p[0]:
                if (x,y) == point_A:
                    done = True
                else:
                    x,y = p[1] 
        
        u2,w2 = center(x,y)
        lenght += distance(u1,w1,u2,w2)
        u1,w1 = u2,w2
    
    return lenght


# Distance from neighbour to point_B (center of squares)
def h(n, point_B):
    b1,b2 = point_B
    b1,b2 = center(b1,b2)
    x,y = n
    x,y = center(x,y)
    
    return distance(x,y,b1,b2)


# Total value
def f(n, point_A, point_B):
    g_value = g(n, point_A)
    h_value = h(n, point_B)
    return g_value + h_value 


# Updates priority_queue
def add_neighbours(point_A, point_B):
    global priority_queue_coords
    global priority_queue_value

    done1 = True
    new_n = []
    
    # Find new neighbours that are not in priority_queue
    for n in neighbours:
        if n not in priority_queue_coords:
            new_n.append(n)

    # Calculates f(n) and appends accordingly
    for n in new_n:  
        f_value = f(n ,point_A, point_B)
        
        for index,v in enumerate(priority_queue_value):
            if done1:
                if f_value < v:
                    priority_queue_coords.insert(index, n)
                    priority_queue_value.insert(index, f_value)
                    done1 = False

        # Adds to last because it wasn't added yet or because len = 0
        if done1 or len(priority_queue_coords) == 0:
            priority_queue_coords.append(n)
            priority_queue_value.append(f_value)

        # Resets done1
        done1 = True


# Execute priority_queue. Transform neighbours --> nodes
def execute():
    global nodes
    global neighbours
    global priority_queue_coords
    global priority_queue_value

    try:
        lowest_value = priority_queue_value[0]

        for index,v in enumerate(priority_queue_value):
            if v == lowest_value:
                nodes.append(priority_queue_coords[index])
                neighbours.remove(priority_queue_coords[index])
                priority_queue_coords.pop(index)
                priority_queue_value.remove(v)
    except:
        pass

# Only neighbours here. Lowest value f(n) first in queue
priority_queue_coords = [] # coords
priority_queue_value = [] # f(n)

# All neighbours are here
neighbours = []

# All nodes are here
nodes = [] # [ [(neighbour/node) , (parent)], [], ... ]

# All parents and neighbours go here
parents = [] # [ [(coords), (parent)], [], ... ]

# This has to be here (for the "point_A next to point_B" case scenario)
finding_point_B = True

point_A = ()
point_B = ()
obstacles = []

if __name__ == "__main__":

    path = []

    # This is just for testing
    point_A = (30, 60)
    point_B = (585, 615)
    obstacles = [(180, 75), (180, 90), (180, 105), (180, 120), (180, 135), (180, 150), (180, 165), (180, 180), (180, 195), (180, 210), (180, 225), (180, 240), (180, 255)]  
       
    # Initial steps before loop
    first_neighbours(obstacles, point_A)
    finding_point_B = found_B(point_B)

    # Loop
    start = time.perf_counter()

    while finding_point_B:
        # Add neighbours to priority_queue
        add_neighbours(point_A, point_B)

        # Execute priority_queue = neighbours --> nodes
        execute()

        # Go through all nodes to find new neighbours
        new_neighbours(obstacles) # identical to first_neighbours()
        finding_point_B = found_B(point_B)

    end = time.perf_counter()

    done = True
    x,y = point_B
    path.append(point_B)
    while done:
        for p in parents:
            if p[0] == (x,y):
                x,y = p[1]
                path.append((x,y))
                if (x,y) == point_A:
                    done = False
    
    # Found a path
    if not finding_point_B:
        print("Found in", end - start, "seconds.")
        print("Distance of path:", round(g(point_B, point_A),1), "units.")
        print("Path: ", path)

