import pygame

from pc_control.points import StraightPoint, CrossOver
from pc_control.track import Track
from pc_control.signals import Signal

class Layout(pygame.Surface):

    width = 400
    height = 400

    def __init__(self):

        super().__init__((Layout.width,Layout.height))

        self.points = [StraightPoint(self, 50,100, type="right_up"), 
                       StraightPoint(self, 00,200, type="right_down"),
                       StraightPoint(self, 50,175, type="up_right"),
                       StraightPoint(self, 200,175, type="up_left"),
                       StraightPoint(self, 50,250, type="down_right"),
                       StraightPoint(self, 200,250, type="down_left"),
                       StraightPoint(self, 200,100, type="left_up"),
                       StraightPoint(self, 200,200, type="left_down"),
                       CrossOver(self,75,320)]
        
        self.signals = [Signal(self, 10, 10)]

        self.sections = [Track(self, [[(100, 100), (150,100)],
                                      [(150, 98), (150,127)],
                                      [(150, 125), (125,125)]
                                      ])]

    def draw(self, mouse_pos, mouse_up):
        self.fill((0,0,0))
        pygame.draw.rect(self, (255,255,255), self.get_rect(), 1)

        for signal in self.signals:
            signal.update_state(mouse_pos, mouse_up)
            signal.draw()

        for point in self.points:
            point.update_state(mouse_pos, mouse_up)
            point.draw()

        for section in self.sections:
            section.draw()