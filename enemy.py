import pygame
from maze import *

pygame.init()

# screen=pygame.display.set_mode((screen_width, screen_height))

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


    def set_enemies(n, enemy_size, maze1, solution_path):
        try:
            grid=maze1.grid_cells
            enemies=dict()
            for i in range(n):
                rand_cell=grid[random.randint(0,len(grid)-1)][random.randint(0,len(grid)-1)]
                while rand_cell in solution_path:
                    rand_cell=grid[random.randint(0,len(grid)-1)][random.randint(0,len(grid)-1)]
                rx,ry,w,t=rand_cell.x, rand_cell.y, rand_cell.width, rand_cell.thickness
                enemy1 = Enemy(rx+t, ry+t, enemy_size)

                loc=grid[ry//w][rx//w]
                close_neighbours=maze1.check_neighbours_by_walls(loc,grid,grid[0][0])
                for nr in close_neighbours:
                    if nr in solution_path:
                        close_neighbours.remove(nr)
                far_neighbours={nr : maze1.check_neighbours_by_walls(nr,grid,loc) for nr in close_neighbours}
                for nr_key in far_neighbours.keys():
                    for nr in far_neighbours[nr_key]:
                        if nr in solution_path:
                            far_neighbours[nr_key].remove(nr)

                cell1=loc
                cell2=random.choice(close_neighbours)
                cell3=random.choice(far_neighbours[cell2])

                cells=[cell1, cell2, cell3]
                enemies[enemy1]=cells
            return enemies
        except: 
            print("calling set_enemies again")
            return Enemy.set_enemies(n, enemy_size, maze1, solution_path)
                
