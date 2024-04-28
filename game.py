import pygame
import argparse
from maze import *
from player import *
from enemy import *
from buttons import *
from objects import *
from highscore import *

# initializes pygame module!!
pygame.init()

# important variables
screen_col=(5,5,5) #black
# maze_col=(0,50,0) #dark green
# player_col=(200,0,0) #red
# enemy_col=(150,0,150) #dark blue
text_col=(200,200,200) #white
enter_col=(75,75,75) #grey
sidebar_col=(25,100,225) #violet 

screen_width, screen_height=1080,720
maze_width=720
# IF you change this then make sure to change it over all files!! (@"v")
# or if you change it to say 800,800 then change the factors which decide cellsize, playersize etc.

font = pygame.font.SysFont('Pipe Dream', 48)

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


# Loading images for player, enemies, tiles, walls and sorting them based on theme
green_tile=pygame.image.load("./Images/grass_tile_com.png")
green_upper_wall=pygame.image.load("./Images/wall_horizontal_com.png")
green_side_wall=pygame.image.load("./Images/wall_vertical_com.png")
forest_trap=pygame.image.load("./Images/mystery_forest_trap_com.png")
forest_enemy=pygame.image.load("./Images/forest_enemy_com.png")
forest=[green_tile, green_upper_wall, green_side_wall, forest_enemy, forest_trap]

snow_tile=pygame.image.load("./Images/snow_tile_com.png")
ice_upper_wall=pygame.image.load("./Images/ice_wall_hori_com.png")
ice_side_wall=pygame.image.load("./Images/ice_wall_vert_com.png")
ice_enemy=pygame.image.load("./Images/ice_enemy_com.png")
ice_trap_upper=pygame.image.load("./Images/ice_trap_upper_com.png")
ice_trap_lower=pygame.image.load("./Images/ice_trap_lower_com.png")
snow=[snow_tile, ice_upper_wall, ice_side_wall, ice_enemy, ice_trap_lower]

stone_tile=pygame.image.load("./Images/stone_tile_com.png")
stone_upper_wall=pygame.image.load("./Images/stone_wall_hori_com.png")
stone_side_wall=pygame.image.load("./Images/stone_wall_vert_com.png")
dungeon_enemy=pygame.image.load("./Images/dungeon_enemy_com.png")
scorpion_trap=pygame.image.load("./Images/scorpion_trap_com.png").convert_alpha()
dungeon=[stone_tile, stone_upper_wall, stone_side_wall, dungeon_enemy, scorpion_trap]

parser = argparse.ArgumentParser()
parser.add_argument("--theme",type=str,required=False)
args = parser.parse_args()
theme=forest
if args.theme=="snow":
    theme=snow
if args.theme=="forest":
    theme=forest
if args.theme=="dungeon":
    theme=dungeon    



# User name entry
def enter():
    screen.fill(screen_col)
    global user_name, skipped

    enter_msg=font.render("Hello Player, Welcome to Maze Runner",True, text_col)
    name_msg=font.render("Please enter your name", True, text_col)
    enter_btn=Buttons(4, "Enter")
    skip_btn=Buttons(5, "Skip")
    user_name=""

    entered=False
    while not entered :
        # Displays the user entry screen
        screen.blit(enter_msg, ((screen_width-enter_msg.get_width())//2, screen_height//6))
        if len(user_name)==0: screen.blit(name_msg, ((screen_width-name_msg.get_width())//2, 2*screen_height//6)) 
        enter_btn.draw_button()
        skip_btn.draw_button()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if enter_btn.clicked and len(user_name):
                entered=True
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_BACKSPACE :
                    if len(user_name):
                        user_name=user_name[:-1]
                elif event.key==pygame.K_RETURN :
                    if len(user_name):
                        entered=True
                else:
                    if len(user_name)<18:
                        user_name+=event.unicode
            if skip_btn.clicked:
                user_name="Player"
                entered=True
        
        # Displays the name entered
        name_box=pygame.draw.rect(screen, enter_col, ((screen_width-name_msg.get_width())//2, screen_height//2, name_msg.get_width(), screen_height//10))
        name_text=font.render(user_name, True, text_col)
        screen.blit(name_text, ((screen_width-name_text.get_width())//2, name_box.top+name_box.h//6))
        pygame.display.update()

# To confirm before quitting
def quit_confirm():
    screen.fill(screen_col)
    ask=font.render("You really want to quit?", True, text_col)
    screen.blit(ask, ((screen.get_width()-ask.get_width())//2, screen.get_height()//4))
    yes_btn=Buttons(2.5, "Yes")
    no_btn=Buttons(3.5, "No")

    selected=False
    while not selected:
        # Display screen asking for confirming quit
        yes_btn.draw_button()
        no_btn.draw_button()
        for event in pygame.event.get():
            if event.type==pygame.QUIT or yes_btn.clicked:
                pygame.quit()
                quit()
            if no_btn.clicked:
                screen.fill(screen_col)
                selected=True
                no_btn.clicked=False


# Creating buttons and menu at the start of game
def menu():
    screen.fill(screen_col)
    start_btn=Buttons(2, "Start")
    options_btn=Buttons(3, "Options")
    quit_btn=Buttons(4, "Quit ?")
    change_music=Buttons(2,"Change music")
    mute=Buttons(3,"Stop music")
    leaderboard=Buttons(4, "Leaderboard")
    back=Buttons(5,"Back")
    i=1
    
    started=False
    while not started :
        # Display Menu screen
        welcome=font.render(f"Hello {user_name}, Ready for an Adventure?",True, text_col)
        screen.blit(welcome, ((screen_width-welcome.get_width())//2, screen_height//6))
        start_btn.draw_button()
        options_btn.draw_button()
        quit_btn.draw_button()
        pygame.display.update()
        # draw button needs to be inside loop as it detects the button click ...
        # update is needed for rendering text 

        for event in pygame.event.get():
            if event.type == pygame.QUIT: #for closing window (otherwise won't close)
                pygame.quit()
                quit()
            if quit_btn.clicked:
                quit_confirm()
                quit_btn.clicked=False
            if options_btn.clicked :
                #very buggy performance 乁( ͡ಥᨓ ͡ಥ)ㄏ
                #finally mila bug \(^v^)/ 
                selected=False      
                screen.fill(screen_col)
                while not selected:
                    # Display options screen
                    settings=font.render("Settings",True,text_col)
                    screen.blit(settings, ((screen_width-settings.get_width())//2, screen_height//6))
                    change_music.draw_button()
                    mute.draw_button()
                    leaderboard.draw_button()
                    back.draw_button()
                    pygame.display.update()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT :
                            pygame.quit()
                            quit()
                        if change_music.clicked :
                            global music_index,total_music
                            pygame.mixer.music.unload()
                            music_index=music_index%total_music + 1
                            pygame.mixer.music.load(f"./Music/theme_{music_index}.mp3")
                            pygame.mixer.music.play(-1)
                        if mute.clicked :
                            if mute.text=="Stop music":
                                pygame.mixer.music.pause()
                                mute.text="Play music"
                                screen.fill(screen_col)
                                mute.draw_button()
                            elif mute.text=="Play music":
                                pygame.mixer.music.unpause()
                                mute.text="Stop music"
                                screen.fill(screen_col)
                                mute.draw_button()
                        if leaderboard.clicked:
                            display_hiscore(i)
                            leaderboard.clicked=False
                            i=i%3+1
                        if back.clicked :
                            # Back to menu
                            screen.fill(screen_col)
                            selected=True
                            back.clicked=False
                            options_btn.clicked=False
                            break
            elif start_btn.clicked :
                started=True
                start_btn.clicked=False
      

    #choose difficulty levels and setting related parameters
    screen.fill(screen_col)
    easy=Buttons(2, "Easy")
    medium=Buttons(3, "Medium")
    hard=Buttons(4, "Hard")

    level_chosen=False
    while not level_chosen:
        # Displaying hardness choosing
        difficulty=font.render("Choose a difficulty Level",True,text_col)
        screen.blit(difficulty, ((screen_width-difficulty.get_width())//2, screen_height//6))
        easy.draw_button()
        medium.draw_button()
        hard.draw_button()
        pygame.display.update()

        # defining them global to access them from other functions also
        global level, timer, cell_size, cell_wall_thickness, player_size, visibility

        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                pygame.quit()
                quit()
            if easy.clicked :
                level=1
                timer=45
                visibility=2/3
                cell_size=maze_width//8
                cell_wall_thickness=cell_size//5
                player_size=maze_width//12
                level_chosen=True

            if medium.clicked :
                level=2
                timer=60
                visibility=3/5
                cell_size=maze_width//10
                cell_wall_thickness=cell_size//5
                player_size=maze_width//15
                level_chosen=True

            if hard.clicked :
                level=3
                timer=90
                visibility=1/2
                cell_size=maze_width//12
                cell_wall_thickness=cell_size//5
                player_size=maze_width//18
                level_chosen=True


# Loading maze and other elements
def setup(menu_required=True):
    # defining them global to access them from other functions also
    global maze1, grid, player1, player_rect, enemies, traps, coins
    if menu_required :
        menu()
    
    # Setting up the maze and generating its solution path
    # maze_screen.fill(maze_col,(0,0,maze_width,screen_height))
    tile,up_wall,side_wall=theme[0], theme[1], theme[2]
    maze1=Maze(maze_width, screen_height, cell_size, cell_wall_thickness)
    grid=maze1.generate_maze(level)
    solution_path, directed_path=maze1.generate_solution()
    # for p in solution_path :
    #     print(p)
    #     new_rect=pygame.Rect(p.x+p.thickness,p.y+p.thickness,player_size, player_size)
    #     pygame.draw.rect(screen,(125,50,0),new_rect)
    #     pygame.display.update()
    print(directed_path)

    # Drawing the maze
    first_cell=grid[0][0] # used as a reference for creating player
    x1, y1 = first_cell.x, first_cell.y
    for row in grid:
        for cell in row:
            cell.draw_walls(tile, up_wall, side_wall)
    
    screen.blit(maze_screen, (0,0))

    # Adding finishing point
    n=maze_width//cell_size
    last_cell=grid[n-1][n-1]
    xn,yn,t=last_cell.x, last_cell.y, last_cell.thickness
    flag=pygame.image.load("./Images/palace_full_com.png")
    flag=pygame.transform.scale(flag,(player_size, player_size))
    maze_screen.blit(flag, (xn+t, yn+t))

    # Creating objects
    traps=Trap.set_traps(2*level, player_size, maze1, solution_path, theme[-1])
    coins=Coin.set_coins(3*level, player_size//2, maze1, traps)

    # Creating enemy
    enemies=Enemy.set_enemies(2*level, player_size, maze1, solution_path, theme[3])

    # Creating player
    player1 = Player(x1+cell_wall_thickness,y1+cell_wall_thickness,player_size)
    Player.draw(player1)

    # Creating subsurface
    v_width, v_height=int(maze_width*visibility), int(screen_height*visibility)
    player_rect=pygame.Rect(0,0,v_width, v_height)
    half_screen=maze_screen.subsurface(player_rect)
    screen.blit(half_screen, player_rect.topleft)





def gameloop():
    # Setting timer and formatting its text
    global timer
    pygame.time.set_timer(pygame.USEREVENT, timer*1000) # unit is milisecond
    start_ticks=pygame.time.get_ticks()

    # Designing health bar and play_again button after game
    health_bar=pygame.Rect(maze_width+(screen_width-maze_width)//8,screen_height//8,3*(screen_width-maze_width)//4, screen_height//12)
    red_bar=pygame.Rect(health_bar.x, health_bar.y, health_bar.w, health_bar.h)
    play_again=Buttons(4.5,"Play Again")
    menu_btn=Buttons(5.25,"Menu")

    # Main game loop annnnnnd some more variables
    score=0
    health=1
    enemy_v=1
    trap_t=1
    scored=False
    over=False
    win=False
    move=True
    updated=False
    while True: 
        clock.tick(10) #sets frames per second(FPS)
        
        screen.fill((0,0,0), (0,0,maze_width, screen_height))

        # Setting up the camera, it follows the player unless it hits boundary of maze_screen
        #......finally !!! (ง⩾◡⩽)ง
        if player_rect.centerx>player1.x:
            if player1.x>player_rect.w//2:
                player_rect.centerx=player1.x
            else:
                player_rect.left=0
        if player_rect.centerx<player1.x:
            if player1.x<maze_width-(player_rect.w//2):
                player_rect.centerx=player1.x
            else:
                player_rect.right=maze_width
        if player_rect.centery>player1.y:
            if player1.y>player_rect.h//2:
                player_rect.centery=player1.y    
            else:
                player_rect.top=0
        if player_rect.centery<player1.y:
            if player1.y<screen_height-(player_rect.h//2):
                player_rect.centery=player1.y
            else:
                player_rect.bottom=screen_height

        half_screen=maze_screen.subsurface(player_rect)
        screen.blit(half_screen, player_rect.topleft)


        # Keyboard inputs for navigating player
        keys = pygame.key.get_pressed() #returns an array

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) :
            move=player1.move("left", grid, theme[0]) # move is a boolean which stores if player has reached goal or not
            
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) :
            move=player1.move("right", grid, theme[0])
            
        if (keys[pygame.K_UP] or keys[pygame.K_w]) :
            move=player1.move("up", grid, theme[0])
            
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) :
            move=player1.move("down", grid, theme[0])
            # move is False when player has reached the goal


        # Checking for events like timeover or quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #for closing window (otherwise won't close)
                pygame.quit()
                quit()
            if event.type == pygame.USEREVENT : 
                over=True
                print("time out")
        
            
        if not move and not over : win=True
           
        if not over and not win:
            if health<=0.1:
                over=True
            
            
            # moving enemies and checkking collision with player
            # v sets direction of motion

            for enemy,cells in enemies.items() :
                loc_p=player1.location(grid)
                loc_now=enemy.location(grid)
                if enemy_v==1 and loc_p==loc_now:
                    # over=True
                    health-=0.2
                    print("hit an enemy")
                    health_bar.w -= 2*red_bar.w//10
                if enemy_v==1 and loc_now==cells[0] :
                    enemy.move(cells[1], theme[0])
                    v=1
                elif enemy_v==1 and loc_now==cells[2] :
                    enemy.move(cells[1], theme[0])
                    v=-1
                elif enemy_v==1 and loc_now==cells[1] :
                    if v==1: 
                        enemy.move(cells[2], theme[0])
                    else:
                        enemy.move(cells[0], theme[0])
            enemy_v=enemy_v%3+1 # controls speed of enemy
                
            # checking for traps interaction with player
            for trap in traps:
                if trap_t==1 and player1.location(grid)==trap.location(grid):
                    # over=True
                    health-=0.1
                    print("hit a trap")
                    health_bar.w -= red_bar.w//10
                maze_screen.blit(trap.image, (trap.x, trap.y))
            player1.draw()
            trap_t=trap_t%3+1 # checks duration of interaction

            # adding score
            if scored==True:
                scored=False

            #checks for collecting coins
            for coin in coins:
                if player1.location(grid)==coin.location(grid) and not coin.used:
                    coin.used=True
                    score+=coin.value
                    scored=True

            # displaying time, score and health on sidebar
            screen.fill(sidebar_col,(maze_width,0,(screen_width-maze_width),screen_height))
            time_elapsed=(pygame.time.get_ticks()-start_ticks)//1000
            time_remaining=timer-time_elapsed
            minutes, seconds=time_remaining//60, time_remaining%60

            # line1=font.render("Use arrow keys",True,text_col)
            # line2=font.render("Or WASD",True,text_col)
            # line3=font.render("To move",True,text_col)
            line4=font.render("Scores", True, text_col)
            score_col=(0,250,0) if scored else (0,200,0)
            line5=font.render(f"{score}", True, score_col)
            line6=font.render("Time remaining",True,text_col)
            time_col=(125,25,0) if time_remaining<=10 else (125,125,0)
            line7=font.render(f"{minutes:02}:{seconds:02}",True,time_col)
            lines=[line4, line5, line6, line7] # removed line1, line2, line3
            for i in range(len(lines)):
                posx=(maze_width+screen_width-lines[i].get_width())//2
                # posy=(i+1)*screen_height//10 if i<3 else (i+2)*screen_height//10
                posy=(i+5)*screen_height//10
                screen.blit(lines[i],(posx,posy))
            pygame.draw.rect(screen, (255,0,0), red_bar, border_radius=red_bar.h//2)
            pygame.draw.rect(screen,(0,255,0), health_bar, border_radius=health_bar.h//2)

        # Gameover or you win screen
        else:    
            screen.fill(screen_col)
            if over and not win:
                image=pygame.image.load("./Images/Game over.png")
                image=pygame.transform.scale(image, (screen_width//2, screen_height//2))
                screen.blit(image, (screen_width//4, screen_height//12))
           
            else: 
                image=pygame.image.load("./Images/You win!.webp").convert_alpha()
                image=pygame.transform.scale(image, (screen_width//2, screen_height//2))
                screen.blit(image, (screen_width//4, screen_height//12))
            
            # Display score
            score_display=font.render(f"You scored {score}", True, text_col)
            screen.blit(score_display, ((screen_width-score_display.get_width())//2, 7*screen_height//12))

            if not updated:
                update_hiscore(user_name, score, level)
                updated=True

            # Play again and menu button 
            # Tapping play_again recursively calls the setup and gameloop, bypassing menu
            play_again.draw_button()
            menu_btn.draw_button()
            if play_again.clicked :
                setup(menu_required=False)
                gameloop()
            if menu_btn.clicked :
                setup()
                gameloop()

        
        pygame.display.update()
        

# Calling the real functions ヽ(^ ε ^)ﾉ
enter()
setup()
gameloop()