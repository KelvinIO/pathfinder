import pygame
import math
from queue import PriorityQueue

# Set the window to be 800 pixels by 800 pixels
window = pygame.display.set_mode((800, 800))  

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
    
    # Now we define methods to assign hte colors
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

    # Draw the nodes on screen
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

    def updateNeighbors(self, grid):
        pass

    def __lt__(self, other):
        return False
