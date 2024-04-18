import pygame

class Camera:
    camera_width, camera_height=360,360

    #constructor with margin data
    def __init__(self):
        self.camera = pygame.display.set_mode((self.camera_width, self.camera_height))
        self.x, self.y=0,0
        self.right_margin=0.7
        self.left_margin=0.2
        self.up_margin=0.2
        self.down_margin=0.7

    def follow(self, rect):
        x, y=rect.topleft[0], rect.topleft[1]
        if x>self.x+self.camera_width*self.right_margin :
            self.x=x
        if x<self.x+self.camera_width*self.left_margin :
            self.x=x
        if y>self.y+self.camera_height*self.down_margin :
            self.y=y
        if y<self.y+self.camera_height*self.up_margin :
            self.y=y

        