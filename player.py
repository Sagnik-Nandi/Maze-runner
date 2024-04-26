import pygame
from maze import *

#initializes pygame module!!
pygame.init()

# screen_width, screen_height=1080,720 (since we are importing from maze this line is not required)
# screen = pygame.display.set_mode((screen_width, screen_height))
# pygame.display.set_caption("Let's make a game!")
# clock=pygame.time.Clock()


class Player:
    def __init__(self,x,y,size):
        self.x, self.y = x, y
        self.width=size
        self.height=size
        image=pygame.image.load("./Images/hero_player_com.png")
        self.image=pygame.transform.scale(image, (self.width, self.height))

    # draws player rectangle
    def draw(self, player_col):
        # pygame.draw.rect(maze_screen,player_col, (self.x, self.y, self.width, self.height))
        maze_screen.blit(self.image, (self.x,self.y))

    # check current cell of the player
    def location(self, grid):
        w=grid[0][0].width
        return grid[self.y//w][self.x//w]
            

    # moves the player
    def move(self,event,grid,maze_col, player_col):
        
        rect1=pygame.Rect(self.x, self.y, self.width, self.height)
        loc=self.location(grid)
        tile=pygame.image.load("./Images/grass_tile_com.png")
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

            self.draw(player_col)
            if rect1 != rect2 : 
                # maze_screen.fill(maze_col, rect1) #fills old rectangle with black to create moving effect instead of dragging 
                maze_screen.blit(tile, (rect1.x, rect1.y))
    
            return True
        # new_rect=pygame.Rect(self.x, self.y, self.width, self.height)
        # print("Removed rect", rect.center)
        # print("now rect at", new_rect.center)


