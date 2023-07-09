import pygame

from pc_control.points import StraightPoint, CrossOver, Point, Triple
from pc_control.track import Track
from pc_control.signals import Signal
from typing import Tuple
import math


class Layout(pygame.Surface):
    """Draws the bowmont water layout diagram."""

    width = 590
    height = 345

    def __init__(self):
        """Creates all the objects in the layout drawing."""
        super().__init__((Layout.width, Layout.height))

        sw1 = StraightPoint(self, 480, 320, type="right_up", name="SW1")
        sw1_enter, sw1_exit, sw1_diverge = sw1.get_connections()

        sw10 = CrossOver(self, 140, 300, "top_bottom", name="SW10")
        sw10_enter1, sw10_enter2, sw10_exit1, sw10_exit2 = sw10.get_connections()

        sw11 = StraightPoint(self, 20, 230, type="up_right", name="SW11")
        sw11_enter, sw11_exit, sw11_diverge = sw11.get_connections()

        sw12 = StraightPoint(self, 20, 120, type="up_right", name="SW12")
        sw12_enter, sw12_exit, sw12_diverge = sw12.get_connections()

        sw8 = StraightPoint(self, 230, 90, type="right_up", name="SW8")
        sw8_enter, sw8_exit, sw8_diverge = sw8.get_connections()

        sw5 = StraightPoint(self, 310, 110, type="right_up", name="SW5")
        sw5_enter, sw5_exit, sw5_diverge = sw5.get_connections()
        station_signal = Signal(self, 315, 60)

        sw3 = StraightPoint(self, 510, 20, type="right_down", name="SW3")
        sw3_enter, sw3_exit, sw3_diverge = sw3.get_connections()

        sw9 = StraightPoint(self, 140, 180, type="left_down", name="SW9")
        sw9_enter, sw9_exit, sw9_diverge = sw9.get_connections()

        # needs to go the 'other way'
        sw6 = CrossOver(self, 240, 160, "bottom_top", name="SW6")
        sw6_enter1, sw6_enter2, sw6_exit1, sw6_exit2 = sw6.get_connections()

        sw4 = StraightPoint(self, 370, 250, type="right_up", name="SW4")
        sw4_enter, sw4_exit, sw4_diverge = sw4.get_connections()

        sw2 = StraightPoint(self, 440, 230, type="left_up", name="SW2")
        sw2_enter, sw2_exit, sw2_diverge = sw2.get_connections()

        sw7 = Triple(self, 280, 250, name="SW7")
        sw7_enter, sw7_top, sw7_middle, sw7_bottom = sw7.get_connections()

        self.points: list[Point] = [sw1, sw2, sw3, sw4, sw5, sw6, sw7, sw8, sw9, sw10, sw11, sw12]

        tr1 = Track(self, sw1_exit, sw10_exit2)
        tr2 = Track(self, sw10_enter2, sw11_enter, [(sw11_enter[0], sw10_enter2[1])])
        tr3 = Track(self, sw11_exit, sw12_enter)
        tr4 = Track(
            self,
            sw12_diverge,
            (sw12_diverge[0] + 100, sw3_diverge[1]),
            [(sw12_diverge[0], sw3_diverge[1])],
            endstop="vertical",
        )
        tr5 = Track(self, sw12_exit, sw3_exit, [(sw12_exit[0], sw3_exit[1])])
        tr6 = Track(self, sw3_enter, sw1_enter, [(Layout.width - 20, sw3_enter[1]), (Layout.width - 20, sw1_enter[1])])
        tr7 = Track(
            self, sw1_diverge, sw4_enter, [(sw1_diverge[0] - 5, sw1_diverge[1]), (sw4_enter[0] + 5, sw4_enter[1])]
        )
        tr8 = Track(self, sw4_diverge, sw9_diverge, [(sw6_exit2[0], sw9_diverge[1])])
        tr9 = Track(self, sw9_exit, sw6_enter2)
        tr10 = Track(self, sw11_diverge, sw6_enter1, [(sw11_diverge[0], sw6_enter1[1])])
        tr11 = Track(
            self, sw9_enter, sw10_enter1, [(sw9_enter[0] - 50, sw9_enter[1]), (sw9_enter[0] - 50, sw10_enter1[1])]
        )
        tr12 = Track(self, sw10_exit1, sw2_enter, [(sw4_enter[0], sw10_exit1[1])])
        tr13 = Track(
            self, sw2_diverge, sw6_exit2, [(sw2_diverge[0] + 20, sw2_diverge[1]), (sw2_diverge[0] + 20, sw6_exit2[1])]
        )

        self.underpass_bottom = (sw5_enter[0] + 70, sw5_enter[1] + 15)
        self.underpass_top = (sw5_enter[0] + 87, sw5_enter[1] - 15)
        tr14 = Track(self, sw6_exit1, self.underpass_bottom, [(sw5_enter[0] + 40, sw6_exit1[1])])
        tr15 = Track(self, sw3_diverge, self.underpass_top, [(sw3_diverge[0] - 18, sw3_diverge[1])])
        tr16 = Track(self, sw4_exit, sw7_enter)

        slope = Track(self, sw2_exit, sw5_enter, [(sw2_exit[0] + 40, sw2_exit[1]), (sw2_exit[0] + 40, sw5_enter[1])])

        platform_1 = Track(self, sw8_diverge, (sw8_diverge[0] - 110, sw8_diverge[1]), endstop="vertical")
        platform_2 = Track(self, sw8_exit, (sw8_diverge[0] - 110, sw8_exit[1]), endstop="vertical")
        platform_3 = Track(self, sw5_exit, (sw8_diverge[0] - 110, sw5_exit[1]), endstop="vertical")
        platform_stub = Track(self, sw5_diverge, sw8_enter)

        siding_1 = Track(self, sw7_top, (sw7_top[0] - 70, sw7_top[1]), endstop="vertical")
        siding_2 = Track(self, sw7_middle, (sw7_middle[0] - 70, sw7_middle[1]), endstop="vertical")
        siding_3 = Track(self, sw7_bottom, (sw7_bottom[0] - 70, sw7_bottom[1]), endstop="vertical")

        self.tracks = [
            tr1,
            tr2,
            tr3,
            tr4,
            tr5,
            tr6,
            tr7,
            tr8,
            tr9,
            tr10,
            tr11,
            tr12,
            tr13,
            tr14,
            tr15,
            tr16,
            slope,
            platform_1,
            platform_2,
            platform_3,
            platform_stub,
            siding_1,
            siding_2,
            siding_3,
        ]

        self.signals = [station_signal]

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

        # line to show raised section
        pygame.draw.lines(
            self, (125, 125, 125), False, [(342, 0), (342, 135), (120, 135), (120, Layout.height)], width=2
        )

        "bridge"

        pygame.draw.lines(
            self,
            (255, 255, 255),
            False,
            [
                (self.underpass_bottom[0] - 17, self.underpass_bottom[1] - 2),
                (self.underpass_bottom[0] - 12, self.underpass_bottom[1] - 7),
                (self.underpass_bottom[0] + 28, self.underpass_bottom[1] - 7),
                (self.underpass_bottom[0] + 33, self.underpass_bottom[1] - 2),
            ],
        )

        pygame.draw.lines(
            self,
            (255, 255, 255),
            False,
            [
                (self.underpass_bottom[0] - 17, self.underpass_bottom[1] - 29),
                (self.underpass_bottom[0] - 12, self.underpass_bottom[1] - 24),
                (self.underpass_bottom[0] + 28, self.underpass_bottom[1] - 24),
                (self.underpass_bottom[0] + 33, self.underpass_bottom[1] - 29),
            ],
        )
