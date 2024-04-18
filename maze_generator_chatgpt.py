import random

# Constants for maze symbols
WALL = '#'
EMPTY = ' '
START = 'S'
END = 'E'
PATH = '.'

# Directions: Up, Down, Left, Right
directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

def generate_maze(width, height):
    maze = [[WALL] * width for _ in range(height)]
    return maze

def is_valid_move(maze, x, y, width, height):
    return 0 <= x < width and 0 <= y < height and maze[y][x] == WALL

def depth_first_search(maze, x, y, end_x, end_y, width, height, visited):
    if x == end_x and y == end_y:
        return True

    visited.add((x, y))

    random.shuffle(directions)
    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if (new_x, new_y) not in visited and is_valid_move(maze, new_x, new_y, width, height):
            maze[new_y][new_x] = EMPTY
            if depth_first_search(maze, new_x, new_y, end_x, end_y, width, height, visited):
                return True

    return False
def generate_path(maze, start_x, start_y, end_x, end_y, width, height):
    maze[start_y][start_x] = START
    maze[end_y][end_x] = END

    visited = set()

    def dfs(x, y):
        if x == end_x and y == end_y:
            return True

        visited.add((x, y))

        random.shuffle(directions)
        for dx, dy, direction in directions:
            new_x, new_y = x + dx, y + dy
            if (new_x, new_y) not in visited and is_valid_move(maze, new_x, new_y, width, height):
                maze[new_y][new_x] = direction
                if dfs(new_x, new_y):
                    return True

        return False

    if dfs(start_x, start_y):
        with open('path.txt', 'w') as file:
            for y in range(height):
                for x in range(width):
                    if maze[y][x] in ['U', 'D', 'L', 'R']:
                        file.write(maze[y][x])
                    else:
                        file.write(EMPTY)
                file.write('\n')
    else:
        print("Path not found.")

# Directions: Up, Down, Left, Right
directions = [(0, -1, 'U'), (0, 1, 'D'), (-1, 0, 'L'), (1, 0, 'R')]

def generate_random_maze(width, height):
    start_x, start_y = random.randint(0, width - 1), random.randint(0, height - 1)
    end_x, end_y = random.randint(0, width - 1), random.randint(0, height - 1)

    maze = generate_maze(width, height)
    generate_path(maze, start_x, start_y, end_x, end_y, width, height)

    return maze

def print_maze(maze):
    for row in maze:
        print(''.join(row))

def main():
    num_levels = 3
    width, height = 10, 10

    for level in range(1, num_levels + 1):
        print(f"Level {level}:")
        maze = generate_random_maze(width, height)
        print_maze(maze)
        print()

if __name__ == "__main__":
    main()
