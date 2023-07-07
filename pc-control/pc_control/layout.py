import pygame

from pc_control.points import StraightPoint, CrossOver, Point
from pc_control.track import Track
from pc_control.signals import Signal
from typing import Tuple


class Layout(pygame.Surface):
    """Draws the bowmont water layout diagram."""

    width = 790
    height = 545

    def __init__(self):
        """Creates all the objects in the layout drawing."""
        super().__init__((Layout.width, Layout.height))

        self.signals = [Signal(self, 10, 10)]

        sw1 = StraightPoint(self, 150, 100, type="right_up")
        sw1_enter, sw1_exit, sw1_diverge = sw1.get_connections()

        sw2 = StraightPoint(self, 450, 100, type="right_up")
        sw2_enter, sw2_exit, sw2_diverge = sw2.get_connections()

        self.points: list[Point] = [sw1, sw2]

        tr1 = Track(self, sw1_enter, sw2_exit)
        self.tracks = [tr1]

    def draw(self, mouse_pos: Tuple[int, int], mouse_up: bool):
        """Iterates through the items and draws them. Calls update_state with the mouse status.

        Args:
            mouse_pos (Tuple[int, int]): Current mouse position?
            mouse_up (bool): Mouse up event?
        """
        self.fill((0, 0, 0))
        pygame.draw.rect(self, (255, 255, 255), self.get_rect(), 1)

        for signal in self.signals:
            signal.update_state(mouse_pos, mouse_up)
            signal.draw()

        for point in self.points:
            point.update_state(mouse_pos, mouse_up)
            point.draw()

        for track in self.tracks:
            track.draw()
