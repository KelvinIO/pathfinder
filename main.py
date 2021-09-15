import pygame
import math
from queue import PriorityQueue

# Set the window to be 800 pixels by 800 pixels
WIDTH = 800
HEIGHT = 800
window = pygame.display.set_mode((WIDTH, HEIGHT))  

# Display the window
pygame.display.set_caption("Pathfinder")

# Define colors for grid coloring using RGB format
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0) # Start position
PURPLE = (255, 0, 255) # End position
RED = (255, 0, 0) # Already visited
GREEN = (0, 255, 0) # Available path 
WHITE = (255, 255, 255) # Unvisited node
BLACK = (0, 0, 0)  # Roadblock

# For A*
# Create grid tiles class to hold values for the algorithm
class Node:
    def __init__(self, row, col, width, height, totalRows): # width can be used here instead of height as we're working with squares
        self.row = row                                      # however for the sake of readability/proper naming conventions and future iterations
        self.col = col                                      # I have used height.
        self.x = row * width
        self.y = col * height
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.height = height
        self.totalRows = totalRows

    def getPosition(self):
        return self.row, self.col
    
    # Check to see if a tile has been visited
    def nodeIsClosed(self):
        return self.color == RED

    def nodeIsOpen(self):
        return self.color == GREEN

    def nodeIsBarrier(self):
        return self.color == BLACK

    def nodeIsStart(self):
        return self.color == YELLOW

    def nodeIsEnd(self):
        return self.color == PURPLE

    def reset(self):
        self.color = WHITE
    
    # Now we define methods to assign/make the colors
    def makeClosed(self):
        self.color = RED

    def makeOpen(self):
        self.color = GREEN

    def makeBarrier(self):
        self.color = BLACK

    def makeStart(self):
        self.color = YELLOW

    def makeEnd(self):
        self.color = PURPLE

    def makePath(self):
        self.color = BLUE  

# Define the methods to draw the nodes on screen
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

    def updateNeighbors(self, grid):
        self.neighbors = [] # Create a list of neighbors
        
        # Check if we can check our neighbors below(for out of bounds errors) and check if the neighboring nodes are barriers
        if self.row < self.totalRows - 1 and not grid[self.row + 1][self.col].nodeIsBarrier():  #DOWN
            self.neighbors.append(grid[self.row + 1][self.col])
        # Check if we have room above the current node
        if self.row > 0 and not grid[self.row - 1][self.col].nodeIsBarrier():   #UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col > 0 and not grid[self.row][self.col - 1].nodeIsBarrier():  #LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

        if self.col < self.totalRows - 1 and not grid[self.row][self.col + 1].nodeIsBarrier():  #RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

    def __lt__(self, other):  # Less than operator for comparisons of tiles
        return False

# Heuristic[h(n)] cost for calculations of 2 points(p1 & p2)
def h(p1, p2): 
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def remakePath(prevNode, current, draw):
    while current in prevNode:
        current = prevNode[current]
        current.makePath()
        draw()

# A-Star Algorithm 
def astar(draw, grid, start, end):
    count = 0
    openSet = PriorityQueue()
    openSet.put((0, count, start)) # Initialize the open set with our F(n), a count for tiebreaker purposes and start node
    prevNode = {}

    # Intilize g(n) and f(n) as infinity for all nodes except start to calculate path costs
    gScore = {node: float("inf") for row in grid for node in row} 
    gScore[start] = 0
    fScore = {node: float("inf") for row in grid for node in row} 
    fScore[start] = h(start.getPosition(), end.getPosition())
    
    # Keep track of items in priority queue using a hash
    openSetHash = {start}

    while not openSet.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.key == pygame.K_q:
                pygame.quit()

        current = openSet.get()[2] # Current node we're evaluating
        openSetHash.remove(current)

        if current == end:
            remakePath(prevNode, end, draw)
            # Reset the colors of start and end nodes
            start.makeStart()
            end.makeEnd()
            return True # we found the path!
        
        # Evaluate f/g scores of the current and neighbor nodes
        for neighbor in current.neighbors:
            tempGscore = gScore[current] + 1

            if tempGscore < gScore[neighbor]: # Update pathing if a better path is found
                prevNode[neighbor] = current
                gScore[neighbor] = tempGscore
                fScore[neighbor] = tempGscore + h(neighbor.getPosition(), end.getPosition())

                if neighbor not in openSetHash:
                    count += 1
                    openSet.put((fScore[neighbor], count, neighbor))
                    openSetHash.add(neighbor)
                    neighbor.makeOpen()
        draw()

        if current != start: # If the current node is not the start node...
            current.makeClosed() # Make it closed as we've already considered it's f/g/h scores in the prev for loop
    return False

# Make the grid
def makeGrid(rows, width):
    grid = []
    gap = width // rows # Use integer division to calculate width of tiles
    
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            tile = Node(i, j, gap, gap, rows)
            grid[i].append(tile)
 
    return grid

def drawGridlines(window, rows, width):
    gap = width // rows
    
    # Draw gridlines
    for i in range(rows):
        pygame.draw.line(window, RED, (0, i*gap), (width, i*gap))
        for j in range(rows):
            pygame.draw.line(window, RED, (j*gap, 0), (j*gap, width))

def drawGrid(window, grid, rows, width):
    window.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(window)

    drawGridlines(window, rows, width)
    pygame.display.update()

def getClickedPos(pos, rows, width):
    gap = width // rows
    x, y = pos

    row = x // gap
    col = y // gap

    return row, col

def main(window, width):
    ROWS = 20
    grid = makeGrid(ROWS, width)
    
    # Some helper variables to keep track of program state
    start = None
    end = None

    run = True
    started = False

    while run:
        drawGrid(window, grid, ROWS, WIDTH)
        for event in pygame.event.get():  # Loop through events and check them
            if event.type == pygame.QUIT:
                run = False
            if started:
                continue
            if pygame.mouse.get_pressed()[0]: # Check for LMB press
                pos = pygame.mouse.get_pos()
                row, col = getClickedPos(pos, ROWS, width)
                node = grid[row][col]

                if not start and node != end:
                    start = node
                    start.makeStart()
                elif not end and node != start:
                    end = node
                    end.makeEnd()
                elif node != end and node != start:
                    node.makeBarrier()

            elif pygame.mouse.get_pressed()[2]: # RMB
                pos = pygame.mouse.get_pos()
                row, col = getClickedPos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()

                if node == start:
                    start = None
                elif node == end:
                    end = None
            # Configure keybindings
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for node in row:
                            node.updateNeighbors(grid)

                    astar(lambda: drawGrid(window, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c: # Reset the grid
                    start = None
                    end = None
                    grid = makeGrid(ROWS, width)

    pygame.quit()

main(window, WIDTH)
