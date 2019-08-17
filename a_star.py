import heapq
from PIL import Image, ImageDraw

BOARD       = "boards/board-2-2.txt"

B_WALKABLE  = "."
B_WALL      = "#"
B_WATER     = "w"
B_MOUNTAIN  = "m"
B_FOREST    = "f"
B_GRASSLAND = "g"
B_ROAD      = "r"
B_START     = "A"
B_GOAL      = "B"

# Nodes are positions on the board
class Node:
    def __init__(self, position, parent=None, char=None):
        self.position = position
        self.parent = parent
        self.char = char
        
        self.g = 0
        self.h = 0

        self.fill, self.cost = self.setFillAndCost()

    # Check if nodes position equals another nodes position. Used when checking if a node is in fringeList or closedList
    def __eq__(self, other):
        return self.position == other.position
    
    # Finds the node with the lowest f value. Used by the heap
    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)

    def setFillAndCost(self):
        if(self.char == B_WALKABLE):
            return "white", 1
        elif(self.char == B_WALL):
            return (70,70,70), 0
        elif(self.char == B_WATER):
            return (67,110,238), 100
        elif(self.char == B_MOUNTAIN):
            return (150,150,150), 50
        elif(self.char == B_FOREST):
            return (35,142,35), 10
        elif(self.char == B_GRASSLAND):
            return (50,205,50), 5
        elif(self.char == B_ROAD):
            return (133,94,66), 1
        elif(self.char == B_START):
            return "red", 0
        elif(self.char == B_GOAL):
            return (0,255,0), 1
        else:
            return None, 0

# Calculate h (heuristic)
def heuristic(node, goal):
    (x1, y1) = node.position
    (x2, y2) = goal.position
    # Manhattan calculation
    return abs(x1 - x2) + abs(y1 - y2)

# Convert a text file to an array
def fileToArray(filename):
    array = []
    
    with open(filename) as f:
        for line in f.read().splitlines():
            array.append(list(line))
    
    return array

# Visualize the solution graphically
def drawSolution(array, node):
    img = Image.new("RGB", (20 * len(array[0])+1, 20 * len(array)+1), color="white")
    draw = ImageDraw.Draw(img)
    
    (x, y) = node.position

    # For loop for writing all the squares (water, mountain, ..)
    for i in range(len(array)):
        for j in range(len(array[i])):
            this = array[i][j]

            draw.rectangle(((j*20), (i*20), (j*20)+20, (i*20)+20), fill=this.fill, outline=(54,54,54))
    
    # Draw the solution. Starting at the goal node
    while node:
        (x, y) = node.position
        draw.ellipse(((x*20)+8, (y*20)+8, (x*20)+12, (y*20)+12), fill=(48,48,48))
        # Set current nodes parent as next node to draw
        node = node.parent
    
    img.show()

# Check if a position is inside the board
def positionInsideArray(array, x, y):
    if(x >= 0 and y >= 0 and y < len(array) and x < len(array[0])):
        return True

    return False

# Check if new node position is walkable
def isWalkable(array, node):
    (x, y) = node.position
    
    if(array[y][x].char == B_WALL):
        return False

    return True

def AStar(start, goal, array):    
    fringeList = [] # The open list containing all nodes that are to be visited
                    # Using a heap to always have the node with lowest f value at index 0
    closedList = [] # Contains all visited nodes
    
    start = array[start[1]][start[0]]
    goal = array[goal[1]][goal[0]]

    start.h = heuristic(start, goal)

    # Pushing the startnode into the heap    
    heapq.heappush(fringeList, start)
    
    # Right, bottom, left, top
    neighbors = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    
    while fringeList:
        # Get the node at index 0 in fringeList, which has the lowest f value
        current = heapq.heappop(fringeList)
        
        closedList.append(current)
        
        # Found solution. Draw it by using function above
        if(current == goal):
            drawSolution(array, current)
            return True
        
        # For each possible neighbor
        for neighbor in neighbors:
            (x, y) = current.position
            # Using values from the neighbors array to find neighbors in the 4 directions
            x += neighbor[0]
            y += neighbor[1]

            # Checking if neighbors position is possible
            if(positionInsideArray(array, x, y) == False):
                continue
            
            neighborNode = array[y][x]
            
            # If neighbor is already visited, skip to next neighbor
            if neighborNode in closedList:
                continue

            # Set the g cost to current nodes value + the cost of the neighbor
            g = current.g + neighborNode.cost

            # If node isn't already in fringeList, add it to fringeList
            if neighborNode not in fringeList and isWalkable(array, neighborNode):
                neighborNode.g = g
                neighborNode.h = heuristic(neighborNode, goal)
                neighborNode.parent = current
                heapq.heappush(fringeList, neighborNode)
            # If current nodes g value is higher than the neighbors, skip to next neighbor
            elif g >= neighborNode.g:
                continue

            # Update neighors g, h and parent
            neighborNode.g = g
            neighborNode.h = heuristic(neighborNode, goal)
            neighborNode.parent = current
            
    if(not fringeList):
        print('No solution')

if __name__ == "__main__":
    array = fileToArray(BOARD)

    for i in range(len(array)):
        for j in range(len(array[i])):
            if(array[i][j] == B_START):
                start = (j, i)
            elif(array[i][j] == B_GOAL):
                goal = (j, i)

            # Converting all array elements into Nodes
            array[i][j] = Node((j, i), None, array[i][j])

    AStar(start, goal, array)
