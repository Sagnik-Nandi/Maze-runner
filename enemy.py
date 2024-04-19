import pygame
from maze import *

pygame.init()

screen=pygame.display.set_mode((screen_width, screen_height))

class Enemy:
    # everything other than move function will be same as player class
    def __init__(self, x, y, size) :
        self.x, self.y=x,y
        self.width=size
        self.height=size

    def location(self, grid):
        w=grid[0][0].width
        return grid[self.y//w][self.x//w]
    
    def move(self, tocell, maze_col, enemy_col):
        rect1=pygame.Rect(self.x, self.y, self.width, self.height)
        t=tocell.thickness 
        self.x, self.y=tocell.x+t, tocell.y+t
        rect2=pygame.Rect(self.x, self.y, self.width, self.height)

        if rect1 != rect2:
            screen.fill(maze_col, rect1)
            pygame.draw.rect(screen, enemy_col, rect2)


        
            
