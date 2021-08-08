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
        return self.color == WHITE
    
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
        self.color = WHITE  # change to more visible color later

    # Define the methods to draw the nodes on screen
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

    def updateNeighbors(self, grid):
        pass

    def __lt__(self, other):  # Less than operator for comparisons of tiles
        return False

# Heuristic(h) for calculations of 2 points(p1 & p2)
def h(p1, p2): 
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

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
    startPos = None
    endPos = None

    run = True
    started = False

    while run:
        for event in pygame.event.get():  # Loop through events and check them
            if event.type == pygame.QUIT:
                run = False
            if started:
                continue
            if pygame.mouse.get_pressed()[0]: # Check for LMB press
                pos = pygame.mouse.get_pos()
                row, col = getClickedPos(pos, ROWS, width)
                node = grid[row][col]
                
                if not start:
                    start = node
                    start.makeStart()
                elif not end:
                    end = node
                    end.makeEnd()
                elif node != start and node != end:
                    node.makeBarrier

            elif pygame.mouse.get_pressed()[2]: # RMB
                pass
    pygame.quit()

main(window, WIDTH)
