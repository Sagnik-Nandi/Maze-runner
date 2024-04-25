import pygame

#initializes pygame module!!
pygame.init()

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Let's make a game!")
clock=pygame.time.Clock()

player_rect=pygame.Rect(0,0,400,400)

image=pygame.image.load("./Images/StartScreen.png")
image=pygame.transform.scale(image, (800,800))
sub_image=image.subsurface(player_rect)
screen.blit(sub_image, player_rect.topleft)
pygame.display.update()

x=40
y=40
w=30
h=30
player1=pygame.draw.rect(screen, (0,255,0), (x,y,w,h))
vel=5

run=True
while run:
    clock.tick(300)
    pygame.time.delay(50) #this is required for moving with keys unless those keys are seen as an event
    screen.fill((0,0,0), player1) #after each frame screen is updated to blank.. so as to create moving effect.. otherwise it will create overlapping rectangles without any moving effect
    screen.fill((0,0,0), player_rect)

    # Setting up the camera
    if player_rect.centerx>player1.x>200:
        player_rect.centerx=player1.x
    if player_rect.centerx<player1.x<600:
        player_rect.centerx=player1.x
    if player_rect.centery>player1.y and player_rect.top>0:
        player_rect.centery=player1.y    
    if player_rect.centery<player1.y and player_rect.bottom<800:
        player_rect.centery=player1.y


    sub_image=image.subsurface(player_rect)
    screen.blit(sub_image, player_rect.topleft)

    # camera=image.subsurface(player_rect)
    # camera.unlock()
    # screen.blit(camera, player_rect.topleft)


    # Watch for keyboard and mouse events.
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #for closing window (otherwise won't close)
            run=False
    
    keys = pygame.key.get_pressed() #returns an array

    if keys[pygame.K_LEFT] and x>=vel:
        x-=vel
    if keys[pygame.K_RIGHT] and x<=800-w-vel:
        x+=vel
    if keys[pygame.K_UP] and y>=vel:
        y-=vel
    if keys[pygame.K_DOWN] and y<=800-h-vel:
        y+=vel

    player1=pygame.draw.rect(screen, (0,255,0), (x,y,w,h))
    pygame.display.update()
