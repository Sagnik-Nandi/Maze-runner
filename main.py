import pygame
from maze import *
from player import *
from enemy import *
from buttons import *
from objects import *

# initializes pygame module!!
pygame.init()

# important variables
screen_col=(5,5,5) #black
maze_col=(0,50,0) #dark green
player_col=(200,0,0) #red
enemy_col=(150,0,150) #dark blue
text_col=(200,200,200) #white
sidebar_col=(25,100,225) #violet 

screen_width, screen_height=1080,720
maze_width=720
# IF you change this then make sure to change it over all files!! (@"v")
# or if you change it to say 800,800 then change the factors which decide cellsize, playersize etc.

font = pygame.font.SysFont('Pipe Dream', 48)

# opening the game window
screen = pygame.display.set_mode((screen_width, screen_height))
# main_screen = pygame.Surface((screen_width, screen_height))
pygame.display.set_caption("Let's make a game!")

clock=pygame.time.Clock()


# plays music 
total_music=2
music_index=1
pygame.mixer.init()
pygame.mixer.music.load(f"./Music/theme_{music_index}.mp3")
pygame.mixer.music.play(-1)



#creating buttons and menu at the start of game
def menu():
    # print("menu function is called")
    screen.fill(screen_col)
    start_btn=Buttons(2, "Start")
    options_btn=Buttons(3, "Options")
    quit_btn=Buttons(4, "Quit ?")
    change_music=Buttons(2,"Change music")
    mute=Buttons(3,"Stop music")
    back=Buttons(4,"Back")
    
    started=False
    while not started :
        welcome=font.render("Hello Player, Welcome to Maze Runner",False, text_col)
        screen.blit(welcome, ((screen_width-welcome.get_width())//2, screen_height//6))
        start_btn.draw_button()
        options_btn.draw_button()
        quit_btn.draw_button()
        pygame.display.update()
        # draw button needs to be inside loop as it detects the button click ...Oofff
        # update is needed for rendering text 

        for event in pygame.event.get():
            if event.type == pygame.QUIT or quit_btn.clicked :
                pygame.quit()
                quit()
            if options_btn.clicked :
                #very buggy performance (T^T )
                #finally mila bug \(^v^)/
                selected=False      
                screen.fill(screen_col)
                while not selected:
                    settings=font.render("Settings",True,text_col)
                    screen.blit(settings, ((screen_width-settings.get_width())//2, screen_height//6))
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
                        if back.clicked :
                            screen.fill(screen_col)
                            selected=True
                            back.clicked=False
                            options_btn.clicked=False
                            break
            elif start_btn.clicked :
                started=True
                start_btn.clicked=False
      

    #choose difficulty levels
    screen.fill(screen_col)
    easy=Buttons(2, "Easy")
    medium=Buttons(3, "Medium")
    hard=Buttons(4, "Hard")

    level_chosen=False
    while not level_chosen:
        difficulty=font.render("Choose a difficulty Level",True,text_col)
        screen.blit(difficulty, ((screen_width-difficulty.get_width())//2, screen_height//6))
        easy.draw_button()
        medium.draw_button()
        hard.draw_button()
        pygame.display.update()

        global level, timer, cell_size, cell_wall_thickness, player_size, visibility

        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                pygame.quit()
                quit()
            if easy.clicked :
                level=1
                timer=20
                visibility=2/3
                cell_size=maze_width//8
                cell_wall_thickness=cell_size//5
                player_size=maze_width//12
                level_chosen=True

            if medium.clicked :
                level=2
                timer=30
                visibility=3/5
                cell_size=maze_width//10
                cell_wall_thickness=cell_size//5
                player_size=maze_width//15
                level_chosen=True

            if hard.clicked :
                level=3
                timer=45
                visibility=1/2
                cell_size=maze_width//12
                cell_wall_thickness=cell_size//5
                player_size=maze_width//18
                level_chosen=True

def setup(menu_required=True):
    # print("setup called")
    global maze1, grid, player1, player_rect, enemies, traps, coins
    # global level, cell_size, cell_wall_thickness, player1 # became global from previous function
    if menu_required :
        menu()
    
    # Setting up the maze
    maze_screen.fill(maze_col,(0,0,maze_width,screen_height))
    maze1=Maze(maze_width, screen_height, cell_size, cell_wall_thickness)
    grid=maze1.generate_maze(level)
    solution_path, directed_path=maze1.generate_solution()
    # for p in solution_path :
    #     print(p)
    #     new_rect=pygame.Rect(p.x+p.thickness,p.y+p.thickness,player_size, player_size)
    #     pygame.draw.rect(screen,(125,50,0),new_rect)
    #     pygame.display.update()
    print(directed_path)

    first_cell=grid[0][0]
    x1, y1 = first_cell.x, first_cell.y
    for row in grid:
        for cell in row:
            cell.draw_walls(maze_col)

    screen.blit(maze_screen, (0,0))

    # Creating objects
    traps=Trap.set_traps(2*level, player_size, maze1, solution_path)
    coins=Coin.set_coins(3*level, player_size, maze1, traps)

    # Creating enemy
    enemies=Enemy.set_enemies(2*level, player_size, maze1, solution_path)

    # Creating player
    player1 = Player(x1+cell_wall_thickness,y1+cell_wall_thickness,player_size)
    Player.draw(player1, player_col)

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

    play_again=Buttons(4.5,"Play Again")
    menu_btn=Buttons(5.25,"Menu")

    # Main game loop
    over=False
    score=0
    scored=False
    win=False
    move=True
    while True:
        clock.tick(10) #sets frames per second(FPS) ...dunno why but menu btn is glitching at high fps
        # pygame.time.delay(100) #this is required for moving with keys unless those keys are seen as an event
        
        screen.fill((0,0,0), (0,0,maze_width, screen_height))

        # Setting up the camera ......finally !!! (ง⩾◡⩽)ง
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
            move=player1.move("left", grid, maze_col, player_col)
            
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) :
            move=player1.move("right", grid, maze_col, player_col)
            
        if (keys[pygame.K_UP] or keys[pygame.K_w]) :
            move=player1.move("up", grid, maze_col, player_col)
            
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) :
            move=player1.move("down", grid, maze_col, player_col)


        # Checking for events like timeover or quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #for closing window (otherwise won't close)
                pygame.quit()
                quit()
            if event.type == pygame.USEREVENT : 
                # print("Userevent")
                over=True
                print("time out")
        
            # use pygame.key.set_repeat(200) for repeating key action while keydown
            # if event.type == pygame.KEYDOWN :
            #     if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            #         player1.move("left", grid, maze_col, player_col)
            #     if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            #         player1.move("right", grid, maze_col, player_col)
            #     if event.key == pygame.K_UP or event.key == pygame.K_w:
            #         player1.move("up", grid, maze_col, player_col)
            #     if event.key == pygame.K_DOWN or event.key == pygame.K_s:
            #         player1.move("down", grid, maze_col, player_col)


        if not move and not over : win=True
           
        if not over and not win:
            # moving enemies and checkking collision with player
            # v sets direction of motion

            for enemy,cells in enemies.items() :
                # print(enemy.x, enemy.y, cells)
                loc_p=player1.location(grid)
                loc_now=enemy.location(grid)
                if loc_p==loc_now:
                    over=True
                    print("hit an enemy")
                if loc_now==cells[0] :
                    enemy.move(cells[1],maze_col, enemy_col)
                    # print("moved from 0 to 1")
                    v=1
                elif loc_now==cells[2] :
                    # if loc_p==loc_now:
                    #     over=True
                    enemy.move(cells[1],maze_col, enemy_col)
                    # print("moved from 2 to 1")
                    v=-1
                elif loc_now==cells[1] :
                    # if loc_p==loc_now:
                    #     over=True
                    if v==1: 
                        enemy.move(cells[2],maze_col, enemy_col)
                        # print("moved from 1 to 2")
                    else:
                        enemy.move(cells[0],maze_col, enemy_col)
                        # print("moved from 1 to 0")
                
            # checking for objects interaction with player
            for trap in traps:
                if player1.location(grid)==trap.location(grid):
                    over=True
                    print("hit a trap")

            if scored==True:
                scored=False

            for coin in coins:
                if player1.location(grid)==coin.location(grid) and not coin.used:
                    coin.used=True
                    score+=coin.value
                    scored=True

            # displaying time, score and instructions
            screen.fill(sidebar_col,(maze_width,0,(screen_width-maze_width),screen_height))
            time_elapsed=(pygame.time.get_ticks()-start_ticks)//1000
            time_remaining=timer-time_elapsed
            minutes, seconds=time_remaining//60, time_remaining%60

            line1=font.render("Use arrow keys",True,text_col)
            line2=font.render("Or WASD",True,text_col)
            line3=font.render("To move",True,text_col)
            line4=font.render("Scores", True, text_col)
            score_col=(0,250,0) if scored else (0,200,0)
            line5=font.render(f"{score}", True, score_col)
            line6=font.render("Time remaining",True,text_col)
            time_col=(125,25,0) if time_remaining<=10 else (125,125,0)
            time_display=font.render(f"{minutes:02}:{seconds:02}",True,time_col) 
            lines=[line1, line2, line3, line4, line5, line6, time_display] 
            for i in range(len(lines)):
                posx=(maze_width+screen_width-lines[i].get_width())//2
                posy=(i+1)*screen_height//9 if i<3 else (i+2)*screen_height//9
                screen.blit(lines[i],(posx,posy))

        # Gameover or you win screen
        else:    
            screen.fill(screen_col)
            if over and not win:
                # gameover=font.render("Game Over", True, text_col)
                # screen.blit(gameover, ((screen_width-gameover.get_width())//2, screen_height//3))
                image=pygame.image.load("./Images/Game over.png")
                image=pygame.transform.scale(image, (screen_width//2, screen_height//2))
                screen.blit(image, (screen_width//4, screen_height//12))
           
            else: 
                # print("you won")
                image=pygame.image.load("./Images/You win!.webp").convert_alpha()
                image=pygame.transform.scale(image, (screen_width//2, screen_height//2))
                screen.blit(image, (screen_width//4, screen_height//12))
            
            # Display score
            score_display=font.render(f"You scored {score}", True, text_col)
            screen.blit(score_display, ((screen_width-score_display.get_width())//2, 7*screen_height//12))

            # Play again and menu button
            play_again.draw_button()
            menu_btn.draw_button()
            if play_again.clicked :
                # over=False
                # play_again.clicked=False #they might be unnecessary because each time a new function is called sonvariables are redefined from scratch
                setup(menu_required=False)
                gameloop()
            if menu_btn.clicked :
                # menu_btn.clicked=False
                setup()
                gameloop()

        
        pygame.display.update()
        

# Calling the real function (@*v*)
setup()
gameloop()