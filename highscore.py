import pygame
from buttons import *

pygame.init()

def update_hiscore(user_name, score, level):
    levels=["easy", "medium", "hard"]
    file=open(f"./highscores/{levels[level-1]}.txt", 'r')
    scores=[]
    users=[]
    total=-1
    for line in file.readlines():
        # ignoring the first line using total = -1
        if total !=-1:
            score_here = line.split(",")
            scores.append(score_here[0])
            users.append(score_here[1][:-1])
        total=total+1

    if total>5:
        total=5
    file.close()

    # now updating part
    if total<5:
        file=open(f"./highscores/{levels[level-1]}.txt", 'w')
        index_add=0
        for i in range(total):
            if score<=int(scores[i]):
                index_add=index_add+1
                continue
            break
        file.write('This file stores 5 highest scores\n')
        for i in range(index_add):
            file.write(f'{scores[i]},{users[i]}\n')
        file.write(f'{score},{user_name}\n')
        for i in range(index_add,total):
            file.write(f'{scores[i]},{users[i]}\n')
        file.close()
    else:
        index_add=0
        for i in range(total):
            if score<=int(scores[i]):
                index_add=index_add+1
                continue
            break
        if(index_add<5):
            file=open(f"./highscores/{levels[level-1]}.txt", 'w')
            file.write('This file stores 5 highest scores\n')
            for i in range(index_add):
                file.write(f'{scores[i]},{users[i]}\n')
            file.write(f'{score},{user_name}\n')
            for i in range(index_add,total-1):
                file.write(f'{scores[i]},{users[i]}\n')
            file.close()



def display_hiscore(level):
    font=pygame.font.SysFont('GAMERIA', 48)
    font2=pygame.font.SysFont('GAMERIA', 36)
    back=Buttons(5,"Back")

    levels=["easy", "medium", "hard"]
    ranklist=dict()
    file=open(f"./highscores/{levels[level-1]}.txt", "r")
    i=-1
    for line in file.readlines():
        if i !=-1:
            line1=line.split(",")
            score1=line1[0]
            user1=line1[1][:-1]
            ranklist[user1]=score1
        i=i+1
    file.close()

    display=True
    while display:
        screen.fill((0,0,0))
        leaderboard=font.render("Leaderboard", True, (150,50,0))
        screen.blit(leaderboard, ((screen_width-leaderboard.get_width())//2, screen_height//6))
        level_dis=font.render(f"{levels[level-1]}", True, (150,50,0))
        screen.blit(level_dis, ((screen_width-level_dis.get_width())//2, 2*screen_height//6))
        i=1
        for users,scores in ranklist.items():
            score_col=(255,200,0) if i==1 else (50,250,0)
            name=font2.render(users, True, score_col) 
            screen.blit(name, (screen_width//6, (i+4)*screen_height//12))
            score=font2.render(scores, True, score_col)
            screen.blit(score, (4*screen_width//6, (i+4)*screen_height//12))
            i=i+1
        back.draw_button()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if back.clicked:
                screen.fill((0,0,0))
                display=False

        pygame.display.update()
