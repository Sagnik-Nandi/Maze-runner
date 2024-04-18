import pygame
from maze import *
from player import *
from buttons import *

# initializes pygame module!!
pygame.init()

# important variables
screen_col=(200,25,0) #red
maze_col=(0,50,0) #dark green
player_col=(200,0,0) #red
text_col=(200,200,200) #white
screen_width, screen_height=720,720
# IF you change this then make sure to change it over all files!!
# or if you change it to say 800,800 then change the factors which decide cellsize, playersize etc.

font = pygame.font.SysFont('Lucida Calligraphy', 24)

# opening the game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Let's make a game!")

clock=pygame.time.Clock()


# plays music 
total_music=2
music_index=1
pygame.mixer.init()
pygame.mixer.music.load(f"./Music/theme_{music_index}.mp3")
pygame.mixer.music.play(-1)



#creating buttons and menu at the start of game
screen.fill(screen_col)
start_btn=Buttons(2, "Start")
options_btn=Buttons(3, "Options")
quit_btn=Buttons(4, "Quit ?")
change_music=Buttons(2,"Change music")
mute=Buttons(3,"Stop music")
back=Buttons(4,"Back")

started=False
while not started :
    welcome=font.render("Hello Player, Welcome to MAZER",True, text_col)
    screen.blit(welcome, ((screen_width-welcome.get_width())//2, screen_height//5))
    start_btn.draw_button()
    options_btn.draw_button()
    quit_btn.draw_button()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or quit_btn.clicked :
            pygame.quit()
            quit()
        if options_btn.clicked :
            #very buggy performance
            #finally mila (T^T )
            selected=False      
            screen.fill(screen_col)
            while not selected:
                settings=font.render("Settings",True,text_col)
                screen.blit(settings, ((screen_width-settings.get_width())//2, screen_height//5))
                change_music.draw_button()
                mute.draw_button()
                back.draw_button()
                pygame.display.update()
                # print("control at loop 3")
                # print("selected",selected)
                # print("options_btn.clicked",options_btn.clicked)

                for event in pygame.event.get():
                    # print("control at loop 4")
                    # print("event",event)
                    # print("selected",selected)
                    # print("options_btn.clicked",options_btn.clicked)
                    if event.type == pygame.QUIT :
                        pygame.quit()
                        quit()
                    if change_music.clicked :
                        pygame.mixer.music.unload()
                        music_index=music_index%total_music + 1
                        pygame.mixer.music.load(f"./Music/theme_{music_index}.mp3")
                        pygame.mixer.music.play(-1)
                    if mute.clicked :
                        if mute.text=="Stop music":
                            pygame.mixer.music.pause()
                            mute.text="Resume music"
                            screen.fill(screen_col)
                            mute.draw_button()
                        elif mute.text=="Resume music":
                            pygame.mixer.music.unpause()
                            mute.text="Stop music"
                            screen.fill(screen_col)
                            mute.draw_button()
                    if back.clicked :
                        screen.fill(screen_col)
                        # print("back.clicked")
                        selected=True
                        options_btn.clicked=False
                        back.clicked=False
                        break
        elif start_btn.clicked :
            started=True
            # print("Start.clicked")
        


#choose difficulty levels
screen.fill(screen_col)
easy=Buttons(2, "Easy")
medium=Buttons(3, "Medium")
hard=Buttons(4, "Hard")

level_chosen=False
while not level_chosen:
    difficulty=font.render("Choose a difficulty Level",False,text_col)
    screen.blit(difficulty, ((screen_width-difficulty.get_width())//2, screen_height//5))
    easy.draw_button()
    medium.draw_button()
    hard.draw_button()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            pygame.quit()
            quit()
        if easy.clicked :
            level=1
            cell_size=screen_width//18
            cell_wall_thickness=cell_size//5
            player_size=screen_width//27 
            level_chosen=True

        if medium.clicked :
            level=2
            cell_size=screen_width//20
            cell_wall_thickness=cell_size//5
            player_size=screen_width//30
            level_chosen=True

        if hard.clicked :
            level=3
            cell_size=screen_width//24
            cell_wall_thickness=cell_size//5
            player_size=screen_width//36
            level_chosen=True



# Setting up the maze
screen.fill(maze_col)
maze1=Maze(screen_width, screen_height, cell_size, cell_wall_thickness)
grid=maze1.generate_maze(level)
first_cell=grid[0][0]
x1, y1 = first_cell.x, first_cell.y
for row in grid:
    for cell in row:
        cell.draw_walls()


# Creating player
player1 = Player(x1+cell_wall_thickness,y1+cell_wall_thickness,player_size)
Player.draw(player1, player_col)


# Setting timer and formatting its text
timer = 60
pygame.time.set_timer(pygame.USEREVENT, timer*1000) # unit is milisecond
start_ticks=pygame.time.get_ticks()



# Main game loop
pygame.key.set_repeat(200) #for repeating key action while keydown
over=False
while True:
    clock.tick(10) #sets frames per second(FPS)
    # pygame.time.delay(100) #this is required for moving with keys unless those keys are seen as an event

    keys = pygame.key.get_pressed() #returns an array

    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) :
        player1.move("left", grid, maze_col, player_col)
        
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) :
        player1.move("right", grid, maze_col, player_col)
        
    if (keys[pygame.K_UP] or keys[pygame.K_w]) :
        player1.move("up", grid, maze_col, player_col)
        
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) :
        player1.move("down", grid, maze_col, player_col)

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #for closing window (otherwise won't close)
            pygame.quit()
            quit()
        # if event.type == pygame.KEYDOWN :
        #     if event.key == pygame.K_LEFT or event.key == pygame.K_a:
        #         player1.move("left", grid, maze_col, player_col)
        #     if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        #         player1.move("right", grid, maze_col, player_col)
        #     if event.key == pygame.K_UP or event.key == pygame.K_w:
        #         player1.move("up", grid, maze_col, player_col)
        #     if event.key == pygame.K_DOWN or event.key == pygame.K_s:
        #         player1.move("down", grid, maze_col, player_col)
        if event.type == pygame.USEREVENT : 
            over=True

    # displaying time
    time_elapsed=(pygame.time.get_ticks()-start_ticks)//1000
    time_remaining=timer-time_elapsed
    minutes, seconds=time_remaining//60, time_remaining%60

    if not over :
        time_display=font.render(f"{minutes:02}:{seconds:02}",True,text_col)
        screen.blit(time_display,(screen_width-time_display.get_width(),0))
    else:    
        screen.fill(screen_col)
        gameover=font.render("Game Over", True, text_col)
        screen.blit(gameover, ((screen_width-gameover.get_width())//2, (screen_height-gameover.get_height())//2))
    
    pygame.display.update()
    