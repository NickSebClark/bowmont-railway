import pygame

class Track():
    def __init__(self, display, sections, width =5):
        self.display = display
        self.sections = sections
        self.line_colour = (255,255,255)
        self.width = width
    
    def draw(self):
        for section in self.sections:
            pygame.draw.line(self.display, self.line_colour, section[0], section[1], self.width)