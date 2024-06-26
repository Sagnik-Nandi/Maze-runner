import pygame
import random

#initializes pygame module!!
pygame.init()

screen_width, screen_height=1080,720
maze_width=720
maze_screen = pygame.Surface((screen_width, screen_height))
pygame.display.set_caption("Let's make a game!")
clock=pygame.time.Clock()


class Cell:
    #constructor for class cell (also note: __*__ makes * a public attribute.. by default any attribute is private)
    def __init__(self, x, y, width, thickness, color=(225,225,25)): 
        self.x, self.y = x, y       
        self.width=width
        self.thickness=thickness
        self.color=color
        self.visited=False
        self.walls={'Up':True, 'Down':True, 'Left':True, 'Right':True}

    def __str__(self) :
        return str((self.x,self.y))
        

    #draws walls around a cell
    def draw_walls(self, tile, up_wall, left_wall):
        w,x,y,t=self.width, self.x, self.y, self.thickness
        
        #scales the images a snecessary
        up_wall=pygame.transform.scale(up_wall, (w, t))
        left_wall=pygame.transform.scale(left_wall, (t, w))
        tile=pygame.transform.scale(tile, (w, w))

        maze_screen.blit(tile, (x,y))
        if self.walls['Up']:
            maze_screen.blit(up_wall, (x, y))
        if self.walls['Down']:
            maze_screen.blit(up_wall, (x, y+w-t))
        if self.walls['Left']:
            maze_screen.blit(left_wall, (x, y))
        if self.walls['Right']:
            maze_screen.blit(left_wall, (x+w-t, y))
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
    # The ususal constructor
    # It depends on the class cell also
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
    #DFS algorithm is used with recursively backtracking the cells it has visited
    def generate_maze(self, level):
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
                current_cell = next_cell
            elif array:                     #all neighbours visited
                current_cell = array.pop()
        
        # to drop some random walls based on level of difficulty (╯⇀◡↼）╯︵ ┻━┻
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



    # check walls between neighbours
    def check_neighbours_by_walls(self,c,grid, skip=None):
        walls=c.walls
        w,x,y=c.width,c.x,c.y
        neighbours=[]
        if not walls["Up"] and y>=w: # if up_neighbour is accessible
            up=grid[y//w-1][x//w]
            neighbours.append(up)
        if not walls["Down"] and y<self.ydim-w: # if down_neighbour is accessible
            down=grid[y//w+1][x//w]
            neighbours.append(down)
        if not walls["Left"] and x>=w: # if left_neighbour is accessible
            left=grid[y//w][x//w-1]
            neighbours.append(left)
        if not walls["Right"] and x<self.xdim-w: # if right_neighbour is accessible
            right=grid[y//w][x//w+1]
            neighbours.append(right)
            
        if skip in neighbours: # optional argument.. if you want to ignore a particular cell out of neighbours.. used in set_enemies function
            neighbours.remove(skip)
        return neighbours


    # using DFS again to solve maze
    # tried using recursion but maximum recursion deppth was exceeded
    def generate_solution(self):
        path={}
        visited=set()
        stack=[self.grid_cells[0][0]]
        n=len(self.grid_cells)

        while stack : # stack is a record for the unvisited cells
            c=stack.pop() # last element in stack
            if c.x+c.y==2*(n-1) : #goal found
                break
            if c not in visited :
                visited.add(c)
                neighbours=self.check_neighbours_by_walls(c, self.grid_cells)
                for nr in neighbours :
                    if nr not in visited :
                        stack.append(nr)
                        path[nr]=c 
                        # path dictionary stores parent cell of each neighbour..so that it can backtrace via path to reach start
            # elif c visited, do nothing  
              
        # reconstructing the path
        c=self.grid_cells[n-1][n-1]
        d=c #just initializing
        directed_path=[] 
        solution_path_proper=[c]
        while c != self.grid_cells[0][0] :
            d=path[c] # d is the parent 
            solution_path_proper.append(d)
            if d.x<c.x:
                directed_path.append("R") 
            if d.x>c.x:
                directed_path.append("L")
            if d.y>c.y:
                directed_path.append("U")  
            if d.y<c.y:
                directed_path.append("D")
                # recall we will actually backtrack
            c=d 
            # updating current cell

        solution_path_proper.append(d) 
        solution_path_proper.reverse()
        directed_path.reverse()

        # writing directed path in a file path.txt
        file=open("path.txt", 'w')
        for directions in directed_path:
            file.write(f"{directions}, ")
        file.close()

        return solution_path_proper,directed_path
    # solution path stores a sequence of cells which lead to the goal
    # directed path is a sequence of left, right, up, down directions, which again lead us to the goal