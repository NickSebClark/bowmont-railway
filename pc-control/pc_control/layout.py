import pygame

from pc_control.points import StraightPoint, CrossOver, Point
from pc_control.track import Track
from pc_control.signals import Signal
from typing import Tuple


class Layout(pygame.Surface):
    """Draws the bowmont water layout diagram."""

    width = 590
    height = 345

    def __init__(self):
        """Creates all the objects in the layout drawing."""
        super().__init__((Layout.width, Layout.height))

        self.signals = [Signal(self, 10, 10)]

        sw1 = StraightPoint(self, 470, 300, type="right_up", name="SW1")
        sw1_enter, sw1_exit, sw1_diverge = sw1.get_connections()

        sw10 = CrossOver(self, 150, 280, name="SW10")
        sw10_enter1, sw10_enter2, sw10_exit1, sw10_exit2 = sw10.get_connections()

        sw11 = StraightPoint(self, 50, 230, type="up_right", name="SW11")
        sw11_enter, sw11_exit, sw11_diverge = sw11.get_connections()

        sw12 = StraightPoint(self, 50, 100, type="up_right", name="SW12")
        sw12_enter, sw12_exit, sw12_diverge = sw12.get_connections()

        sw8 = StraightPoint(self, 260, 90, type="right_up", name="SW8")
        sw8_enter, sw8_exit, sw8_diverge = sw8.get_connections()

        sw5 = StraightPoint(self, 340, 110, type="right_up", name="SW5")
        sw5_enter, sw5_exit, sw5_diverge = sw5.get_connections()

        sw3 = StraightPoint(self, 480, 20, type="right_down", name="SW3")
        sw3_enter, sw3_exit, sw3_diverge = sw3.get_connections()

        sw9 = StraightPoint(self, 150, 180, type="left_down", name="SW9")
        sw9_enter, sw9_exit, sw9_diverge = sw9.get_connections()

        sw6 = StraightPoint(self, 300, 160, type="right_down", name="SW6")
        sw6_enter, sw6_exit, sw6_diverge = sw6.get_connections()

        sw4 = StraightPoint(self, 370, 220, type="right_up", name="SW4")
        sw4_enter, sw4_exit, sw4_diverge = sw4.get_connections()

        sw2 = StraightPoint(self, 460, 230, type="left_up", name="SW2")
        sw2_enter, sw2_exit, sw2_diverge = sw6.get_connections()

        self.points: list[Point] = [sw1, sw2, sw3, sw4, sw5, sw6, sw8, sw9, sw10, sw11, sw12]

        tr1 = Track(self, sw1_exit, sw10_exit2)
        tr2 = Track(self, sw10_enter2, sw11_enter, [(sw11_enter[0], sw10_enter2[1])])
        self.tracks = [tr1, tr2]

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
