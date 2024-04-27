import pygame

# initializes pygame module!!
pygame.init()

# important variables
screen_width, screen_height=1080,720
button_width, button_height=screen_width//4, screen_height//20
button_x, button_y=(screen_width-button_width)//2, screen_height//6
screen=pygame.display.set_mode((screen_width, screen_height))

font_btn=pygame.font.SysFont('AwmU Slant Demo', 36)

#Class for buttons
class Buttons:

    button_col=(255, 50, 0) #red
    click_col=(255, 0, 100) #magenta
    hover_col=(175, 0, 0) #dark red
    text_col=(200,200,200) #white

    #the usual constructor
    def __init__(self, index, text):
        self.text=text
        self.index=index
        self.rect=pygame.Rect(button_x, int(button_y*self.index) , button_width, button_height)
        self.clicked=False

    #drawing the button rectangle
    def draw_button(self, surface=screen):
        # pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))

        #changing style of buttons with mouse activity
        cursor=pygame.mouse.get_pos()

        if self.rect.collidepoint(cursor):
            # print("Mouse inside ", self)
            if pygame.mouse.get_pressed()[0]==1: #left click
                self.clicked=True
                # print(self.text,"was clicked")
                pygame.draw.rect(surface, self.click_col, self.rect)
            elif pygame.mouse.get_pressed()[0]==0 and self.clicked==True:
                self.clicked=False
            else:
                pygame.draw.rect(surface, self.hover_col, self.rect)
        else:
            pygame.draw.rect(surface, self.button_col, self.rect)
        
        text=font_btn.render(self.text,True,self.text_col)
        text_width=text.get_width()
        text_height=text.get_height()
        surface.blit(text, (button_x + (button_width-text_width)//2 , int(button_y*self.index) + (button_height-text_height)//2))

        pygame.display.update()
        
        


    
