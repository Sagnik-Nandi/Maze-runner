import pygame
from maze import *

pygame.init()

# screen_width, screen_height=1080,720 
# screen = pygame.display.set_mode((screen_width, screen_height))
# pygame.display.set_caption("Let's make a game!")
# clock=pygame.time.Clock()

trap_col=(225, 125, 0)
coin_col=(125, 50, 0)
# coin_10_col=(250,200,0)

class Trap:
    def __init__(self, x, y, size):
        self.x, self.y=x, y
        self.rect=pygame.Rect(x, y, size, size)

    def location(self, grid):
        w=grid[0][0].width
        return grid[self.y//w][self.x//w]

    def set_traps(n, trap_size, maze1, solution_path):
        grid=maze1.grid_cells
        traps=[]
        for i in range(n):
            rand_cell=grid[random.randint(0,len(grid)-1)][random.randint(0,len(grid)-1)]
            while rand_cell in solution_path:
                rand_cell=grid[random.randint(0,len(grid)-1)][random.randint(0,len(grid)-1)]
            rx,ry,w,t=rand_cell.x, rand_cell.y, rand_cell.width, rand_cell.thickness
            trap1=Trap(rx+t, ry+t, trap_size)
            pygame.draw.rect(maze_screen, trap_col, trap1.rect)
            traps.append(trap1)
        return traps
            
class Coin:
    def __init__(self, x, y, size, value) :
        self.x, self.y=x,y
        self.rect=pygame.Rect(x, y, size, size)
        self.used=False
        self.value=value
    
    def location(self, grid):
        w=grid[0][0].width
        return grid[self.y//w][self.x//w]
    
    def set_coins(n, coin_size, maze1, traps):
        coins=[]
        grid=maze1.grid_cells
        # Free ke coins
        for i in range(n):
            rand_cell=grid[random.randint(0,len(grid)-1)][random.randint(0,len(grid)-1)]
            rx,ry,w,t=rand_cell.x, rand_cell.y, rand_cell.width, rand_cell.thickness
            v=random.randint(1,2)*5
            # coin_col=coin_5_col if v==5 else coin_10_col
            coin1=Coin(rx+t, ry+t, coin_size,v)
            coins.append(coin1)
            pygame.draw.rect(maze_screen, coin_col, coin1.rect)
    
        # Bonus coins ...trap ke samne
        m=len(traps)
        for i in range(m):
            trap1_loc=traps[i].location(grid)
            rand_cell=random.choice(maze1.check_neighbours_by_walls(trap1_loc, grid))
            rx,ry,w,t=rand_cell.x, rand_cell.y, rand_cell.width, rand_cell.thickness
            v=random.randint(1,2)*5
            coin1=Coin(rx+t, ry+t, coin_size,v)
            coins.append(coin1)
            pygame.draw.rect(maze_screen, coin_col, coin1.rect)

        return coins
