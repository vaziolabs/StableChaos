import pygame


sanitize = lambda t: t % 360

class Mouse:
    def __init__(self):
        self.x, self.y = pygame.mouse.get_pos()
        self.p_x, self.p_y = pygame.mouse.get_pos()
        self.dx, self.dy = 0, 0
        self.speed = 0.1
    
    def dxy(self):
        self.dx = self.x - self.p_x
        self.dy = self.y - self.p_y
        self.p_x, self.p_y = self.x, self.y
        return self.dx, self.dy
        

class Camera:
    def __init__(self, position):
        self.mouse = Mouse()
        self.x, self.y, self.z = position       # Current Position
        self.lookat = (0, 0, 0)                 # Current Looking Position in Degrees
        self.p_x, self.p_y, self.p_z = position # Previous Position
        self.mouse_speed = 0.1
        self.zoom = 1.0
        self.max_zoom = 3.6

    def look(self, x, y, z):
        