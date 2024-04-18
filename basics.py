import pygame

#initializes pygame module!!
pygame.init()

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Let's make a game!")

x=40
y=40
w=30
h=30
vel=5
clock=pygame.time.Clock()

run=True
while run:
    clock.tick(300)
    pygame.time.delay(50) #this is required for moving with keys unless those keys are seen as an event

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

    screen.fill((0,0,0)) #after each frame screen is updated to blank.. so as to create moving effect.. otherwise it will create overlapping rectangles without any moving effect
    pygame.draw.rect(screen, (0,255,0), (x,y,w,h))
    pygame.display.update()
