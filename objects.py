import pygame
from maze import *

pygame.init()

screen_width, screen_height=1080,720 
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Let's make a game!")
clock=pygame.time.Clock()

trap_col=(225, 125, 0)

class Trap:
    def __init__(self, x, y, size):
        self.x, self.y=x, y
        self.rect=pygame.Rect(x, y, size, size)

    def location(self, grid):
        w=grid[0][0].width
        return grid[self.y//w][self.x//w]

    def set_traps(trap_size, maze1, solution_path):
        grid=maze1.grid_cells
        traps=[]
        for i in range(2):
            rand_cell=grid[random.randint(0,len(grid)-1)][random.randint(0,len(grid)-1)]
            while rand_cell in solution_path:
                rand_cell=grid[random.randint(0,len(grid)-1)][random.randint(0,len(grid)-1)]
            rx,ry,w,t=rand_cell.x, rand_cell.y, rand_cell.width, rand_cell.thickness
            trap1=Trap(rx+t, ry+t, trap_size)
            pygame.draw.rect(screen, trap_col, trap1.rect)
            traps.append(trap1)
        return traps
            
class Coin:
    def __init__(self, x, y, size) :
        pass