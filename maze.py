import pygame
import random

#initializes pygame module!!
pygame.init()

screen_width, screen_height=720,720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Let's make a game!")
clock=pygame.time.Clock()


class Cell:
    #constructor for class cell (also note: __*__ makes * a public attribute.. by default any attribute is private)
    def __init__(self, x, y, width, thickness, color=(225,225,25)): 
        self.x, self.y = x, y       #components of a cell
        self.width=width
        self.thickness=thickness
        self.color=color
        self.visited=False
        self.walls={'Up':True, 'Down':True, 'Left':True, 'Right':True}

    #draws walls around a cell
    def draw_walls(self):
        w,x,y=self.width, self.x, self.y
        # print("draw_walls is called")
        if self.walls['Up']:
            pygame.draw.line(screen,self.color, (x,y),(x+w,y), self.thickness)
        if self.walls['Down']:
            pygame.draw.line(screen,self.color, (x,y+w),(x+w,y+w), self.thickness)
        if self.walls['Left']:
            pygame.draw.line(screen,self.color, (x,y),(x,y+w), self.thickness)
        if self.walls['Right']:
            pygame.draw.line(screen,self.color, (x+w,y),(x+w,y+w), self.thickness)
        pygame.display.update()

    #checks top, bottom, left, right for unvisited cell and returns cell with coordinates of unvisited cells otherwise False
    def check_neighbours(self, xdim, ydim, grid_cells):
        w, x, y =self.width, self.x, self.y
        neighbours=[]
        if y>=w :
            up = grid_cells[(y//w)-1][x//w]
            if not up.visited:
                neighbours.append(up)
        if y<ydim-w:
            down = grid_cells[(y//w)+1][x//w]
            if not down.visited:
                neighbours.append(down)
        if x>=w :
            left = grid_cells[y//w][(x//w)-1]
            if not left.visited:
                neighbours.append(left)
        if x<xdim-w :
            right = grid_cells[y//w][(x//w)+1]
            if not right.visited:
                neighbours.append(right)
        return random.choice(neighbours) if neighbours else False


class Maze:
    def __init__(self, xdim, ydim, width, thickness):
        self.xdim, self.ydim=xdim, ydim
        self.width=width
        self.thickness=thickness
        self.grid_cells=[[Cell(col,row,self.width, self.thickness) for col in range(0,self.xdim,self.width)] for row in range(0,self.ydim,self.width) ]
    
    #remove walls... used in the algorithm for generating maze
    def remove_walls(self, current_cell, next_cell):
        c,n =current_cell, next_cell
        if c.x<n.x and c.y==n.y: #right neighbour
            c.walls['Right']=False
            n.walls['Left']=False

        if c.x>n.x and c.y==n.y: #left neighbour
            c.walls['Left']=False
            n.walls['Right']=False

        if c.x==n.x and c.y>n.y: #top neighbour
            c.walls['Up']=False
            n.walls['Down']=False

        if c.x==n.x and c.y<n.y: #bottom neighbour
            c.walls['Down']=False
            n.walls['Up']=False

    #generates maze and returns a list/grid of cells
    #DFS algorithm is used with backtracing the cells it has visited
    def generate_maze(self, level):
        # print("Now generating maze")
        current_cell = self.grid_cells[0][0]
        array = []
        count = 1

        length=len(self.grid_cells)
        while count != length*length:
            current_cell.visited = True
            next_cell = current_cell.check_neighbours(self.xdim, self.ydim, self.grid_cells)

            if next_cell:
                next_cell.visited = True
                count += 1
                array.append(current_cell) #array keeps track of cells which are visited but its neighbours not fully explored
                self.remove_walls(current_cell, next_cell)
                # print(current_cell.walls)
                # print(next_cell.walls)
                current_cell = next_cell
            elif array:                     #all neighbours visited
                current_cell = array.pop()
        
        # to drop some random walls based on level of difficulty
        drop=(3-level)
        for i in range(0,drop*length):
            j=i//drop
            k=random.randint(0,length-1)
            random_walls=self.grid_cells[j][k].walls

            if j!=0 and random_walls['Up'] :
                neighbouring_walls=self.grid_cells[j-1][k].walls
                random_walls['Up']=False
                neighbouring_walls['Down']=False
                continue

            if k!=0 and random_walls['Left']:
                neighbouring_walls=self.grid_cells[j][k-1].walls
                random_walls['Left']=False
                neighbouring_walls['Right']=False
                continue

            if j!=length-1 and random_walls['Down'] :
                neighbouring_walls=self.grid_cells[j+1][k].walls
                random_walls['Down']=False
                neighbouring_walls['Up']=False
                continue

            if k!=length-1 and random_walls['Right']:
                neighbouring_walls=self.grid_cells[j][k+1].walls
                random_walls['Right']=False
                neighbouring_walls['Left']=False
                continue

        return self.grid_cells
