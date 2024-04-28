import pygame
from maze import *

#initializes pygame module!!
pygame.init()


class Player:
    def __init__(self,x,y,size):
        self.x, self.y = x, y
        self.width=size
        self.height=size
        image_left=pygame.image.load("./Images/hero_player_com.png")
        image_right=pygame.image.load("./Images/hero_player_com1.png")
        self.image_left=pygame.transform.scale(image_left, (self.width, self.height))
        self.image_right=pygame.transform.scale(image_right, (self.width, self.height))
        self.facing="right"

    # draws player rectangle
    def draw(self):
        if self.facing=="left":
            maze_screen.blit(self.image_left, (self.x,self.y))
        else:
            maze_screen.blit(self.image_right, (self.x,self.y))

    # check current cell of the player
    def location(self, grid):
        w=grid[0][0].width
        return grid[self.y//w][self.x//w]
            

    # moves the player
    def move(self,event,grid, tile):
        
        rect1=pygame.Rect(self.x, self.y, self.width, self.height)
        loc=self.location(grid)
        tile=pygame.transform.scale(tile, (self.width, self.width))
        step=grid[0][0].width

        # check if player has reached goal
        if loc.x//step + loc.y//step == 2*(len(grid)-1):
            return False
        else :
            if event=="left" and not loc.walls["Left"]:
                self.x-=step
            if event=="right" and not loc.walls["Right"]:
                self.x+=step
            if event=="up" and not loc.walls["Up"] :
                self.y-=step
            if event=="down" and not loc.walls["Down"] :
                self.y+=step

            rect2=pygame.Rect(self.x, self.y, self.width, self.height)

            if event=="left" or event=="down":
                self.facing="left"
                self.draw()
            else:
                self.facing="right"
                self.draw()

            if rect1 != rect2 : 
                maze_screen.blit(tile, (rect1.x, rect1.y))
    
            return True


