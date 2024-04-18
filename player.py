import pygame
from maze import *

#initializes pygame module!!
pygame.init()

screen_width, screen_height=1080,720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Let's make a game!")
clock=pygame.time.Clock()


class Player:
    def __init__(self,x,y,size):
        self.x, self.y = x, y
        self.width=size
        self.height=size

    # draws player rectangle
    def draw(self, player_col):
        pygame.draw.rect(screen,player_col, (self.x, self.y, self.width, self.height))

        
        #create a rectangle so that part of the screen is visible to the player
        #...cannot create in any way

        # rect=pygame.Rect(0,0,screen_width//2, screen_height//2)
        # if self.x>rect.centerx :
        #     rect.centerx=self.x
        # if self.y>rect.centery :
        #     rect.centery=self.y
        # pygame.draw.rect(screen,(0,255,0), rect, 2)

        # pygame.display.update()

        # rect_surface=pygame.Surface((rect.width, rect.height))
        # screen.blit(rect_surface, rect.topleft)
        # screen_copy=pygame.Surface.copy(screen)
        # screen_black=screen.fill((0,0,0))
        # screen.blit(screen_black, rect)


    # check current cell of the player
    def location(self, grid):
        w=grid[0][0].width
        return grid[self.y//w][self.x//w]

    # moves the player
    def move(self,event,grid,maze_col, player_col):
        # cell1=self.location()
        step=grid[0][0].width

        rect1=pygame.Rect(self.x, self.y, self.width, self.height)
        loc=self.location(grid)

        # check if player has reached goal
        if loc.x//step + loc.y//step == 2*(len(grid)-1):
            return False
        else :
            if event=="left" and not loc.walls["Left"]:
                self.x-=step
            if event=="right" and not loc.walls["Right"]:
                self.x+=step
            if event=="up" and not loc.walls["Up"]:
                self.y-=step
            if event=="down" and not loc.walls["Down"]:
                self.y+=step

            rect2=pygame.Rect(self.x, self.y, self.width, self.height)

            self.draw(player_col)
            if rect1 != rect2 : 
                screen.fill(maze_col, rect1) #fills old rectangle with black to create moving effect instead of dragging 
    
            return True
        # new_rect=pygame.Rect(self.x, self.y, self.width, self.height)
        # print("Removed rect", rect.center)
        # print("now rect at", new_rect.center)


