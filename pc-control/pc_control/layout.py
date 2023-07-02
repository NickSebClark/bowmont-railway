import pygame

from pc_control.points import BasicPoint
from pc_control.track import Track

class Layout(pygame.Surface):

    width = 400
    height = 400

    def __init__(self):

        super().__init__((Layout.width,Layout.height))

        self.points = [BasicPoint(self, 50,100, type="right_up"), 
                       BasicPoint(self, 00,200, type="right_down"),
                       BasicPoint(self, 50,175, type="up_right"),
                       BasicPoint(self, 200,175, type="up_left"),
                       BasicPoint(self, 50,250, type="down_right"),
                       BasicPoint(self, 200,250, type="down_left"),
                       BasicPoint(self, 200,100, type="left_up"),
                       BasicPoint(self, 200,200, type="left_down")]

        self.sections = [Track(self, [[(100, 100), (150,100)],
                                      [(150, 98), (150,127)],
                                      [(150, 125), (125,125)]
                                      ])]

    def draw(self, mouse_pos, mouse_up):
        self.fill((0,0,0))
        pygame.draw.rect(self, (255,255,255), self.get_rect(), 1)

        for point in self.points:
            point.update_state(mouse_pos, mouse_up)
        
        for point in self.points:
            point.draw()

        for section in self.sections:
            section.draw()