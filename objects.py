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

image1=pygame.image.load("./Images/Gold_2.png")
image2=pygame.image.load("./Images/Silver_6.png")
# image3=pygame.image.load("./Images/spider_trap_com.png").convert()

class Trap:
    def __init__(self, x, y, size, trap_image):
        self.x, self.y=x, y
        self.rect=pygame.Rect(x, y, size, size)
        self.image=pygame.transform.scale(trap_image, (size, size))

    def location(self, grid):
        w=grid[0][0].width
        return grid[self.y//w][self.x//w]

    def set_traps(n, trap_size, maze1, solution_path, trap_image):
        grid=maze1.grid_cells
        traps=[]
        for i in range(n):
            rand_cell=grid[random.randint(0,len(grid)-1)][random.randint(0,len(grid)-1)]
            while rand_cell in solution_path:
                rand_cell=grid[random.randint(0,len(grid)-1)][random.randint(0,len(grid)-1)]
            rx,ry,w,t=rand_cell.x, rand_cell.y, rand_cell.width, rand_cell.thickness
            trap1=Trap(rx+t, ry+t, trap_size, trap_image)
            traps.append(trap1)
            # pygame.draw.rect(maze_screen, trap_col, trap1.rect)
            maze_screen.blit(trap1.image, (trap1.x, trap1.y))
        return traps
            
class Coin:
    def __init__(self, x, y, size, value) :
        self.x, self.y=x,y
        self.size=size
        # self.rect=pygame.Rect(x, y, size, size)
        self.used=False
        self.value=value
        global image1, image2
        image1=pygame.transform.scale(image1, (size,size))
        image2=pygame.transform.scale(image2, (size,size))
        self.image=image1 if value==10 else image2
    
    def location(self, grid):
        w=grid[0][0].width
        return grid[self.y//w][self.x//w]
    
    def set_coins(n, coin_size, maze1, traps):
        coins=[]
        grid=maze1.grid_cells
        traps_loc=[trap.location(grid) for trap in traps]
        # Free ke coins
        for i in range(n):
            rand_cell=grid[random.randint(0,len(grid)-1)][random.randint(0,len(grid)-1)]
            while rand_cell in traps_loc:
                rand_cell=grid[random.randint(0,len(grid)-1)][random.randint(0,len(grid)-1)]
            rx,ry,w,t=rand_cell.x, rand_cell.y, rand_cell.width, rand_cell.thickness
            v=random.randint(1,2)*5
            coin1=Coin(rx+t, ry+t, coin_size,v)
            coins.append(coin1)
            # pygame.draw.rect(maze_screen, coin_col, coin1.rect)
            maze_screen.blit(coin1.image, (coin1.x+coin1.size//2, coin1.y+coin1.size//2))
    
        # Bonus coins ...trap ke samne
        m=len(traps)
        for i in range(m):
            trap1_loc=traps[i].location(grid)
            rand_cell=random.choice(maze1.check_neighbours_by_walls(trap1_loc, grid))
            rx,ry,w,t=rand_cell.x, rand_cell.y, rand_cell.width, rand_cell.thickness
            v=random.randint(1,2)*5
            coin1=Coin(rx+t, ry+t, coin_size,v)
            coins.append(coin1)
            # pygame.draw.rect(maze_screen, coin_col, coin1.rect)
            maze_screen.blit(coin1.image, (coin1.x+coin1.size//2, coin1.y+coin1.size//2))

        return coins
