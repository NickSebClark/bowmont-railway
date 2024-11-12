import pygame

from pc_control.points import StraightPoint, CrossOver, Point, Triple
from pc_control.track import Track
from pc_control.signals import Signal
from typing import Tuple
import math
import serial


class Layout(pygame.Surface):
    """Draws the bowmont water layout diagram."""

    width = 590
    height = 345

    def __init__(self, ser: serial.Serial):
        """Creates all the objects in the layout drawing."""
        super().__init__((Layout.width, Layout.height))

        sw_0 = StraightPoint(self, 20, 120, 0, ser, type="up_right", name="SW0")
        sw_0_enter, sw_0_exit, sw_0_diverge = sw_0.get_connections()

        sw_1 = StraightPoint(self, 20, 230, 1, ser, type="up_right", name="SW1")
        sw_1_enter, sw_1_exit, sw_1_diverge = sw_1.get_connections()

        sw_2 = StraightPoint(self, 140, 180, 2, ser, type="left_down", name="SW2")
        sw_2_enter, sw_2_exit, sw_2_diverge = sw_2.get_connections()

        sw_3 = CrossOver(self, 140, 300, 3, ser, "top_bottom", name="SW3")
        sw_3_enter1, sw_3_enter2, sw_3_exit1, sw10_exit2 = sw_3.get_connections()

        sw_4 = StraightPoint(self, 230, 90, 5, ser, type="right_up", name="SW4", name_pos="top")
        sw_4_enter, sw_4_exit, sw_4_diverge = sw_4.get_connections()

        sw_5 = Triple(self, 280, 250, 6, ser, name="SW5")
        sw_5_enter, sw_5_top, sw_5_middle, sw_5_bottom = sw_5.get_connections()

        sw_6 = CrossOver(self, 240, 160, 8, ser, "bottom_top", name="SW6", name_pos="top")
        sw_6_enter1, sw_6_enter2, sw_6_exit1, sw6_exit2 = sw_6.get_connections()

        sw_7 = StraightPoint(self, 310, 110, 10, ser, type="right_up", name="SW7")
        sw_7_enter, sw_7_exit, sw_7_diverge = sw_7.get_connections()
        station_signal = Signal(self, 315, 60)

        sw_8 = StraightPoint(self, 370, 250, 11, ser, type="right_up", name="SW8", name_pos="top")
        sw_8_enter, sw_8_exit, sw_8_diverge = sw_8.get_connections()

        sw_9 = StraightPoint(self, 510, 20, 12, ser, type="right_down", name="SW9")
        sw_9_enter, sw_9_exit, sw_9_diverge = sw_9.get_connections()

        sw_10 = StraightPoint(self, 480, 320, 13, ser, type="right_up", name="SW10")
        sw_10_enter, sw_10_exit, sw_10_diverge = sw_10.get_connections()

        sw_11 = StraightPoint(self, 440, 230, 14, ser, type="left_up", name="SW11")
        sw_11_enter, sw_11_exit, sw_11_diverge = sw_11.get_connections()

        self.points: list[Point] = [
            sw_0,
            sw_1,
            sw_2,
            sw_3,
            sw_4,
            sw_5,
            sw_6,
            sw_7,
            sw_8,
            sw_9,
            sw_10,
            sw_11,
        ]

        tr1 = Track(self, sw_10_exit, sw10_exit2)
        tr2 = Track(self, sw_3_enter2, sw_1_enter, [(sw_1_enter[0], sw_3_enter2[1])])
        tr3 = Track(self, sw_1_exit, sw_0_enter)
        tr4 = Track(
            self,
            sw_0_diverge,
            (sw_0_diverge[0] + 100, sw_9_diverge[1]),
            [(sw_0_diverge[0], sw_9_diverge[1])],
            endstop="vertical",
        )
        tr5 = Track(self, sw_0_exit, sw_9_exit, [(sw_0_exit[0], sw_9_exit[1])])
        tr6 = Track(
            self,
            sw_9_enter,
            sw_10_enter,
            [(Layout.width - 20, sw_9_enter[1]), (Layout.width - 20, sw_10_enter[1])],
        )
        tr7 = Track(
            self,
            sw_10_diverge,
            sw_8_enter,
            [
                (sw_10_diverge[0] - 5, sw_10_diverge[1]),
                (sw_8_enter[0] + 5, sw_8_enter[1]),
            ],
        )
        tr8 = Track(
            self,
            sw_8_diverge,
            sw_2_diverge,
            [
                (sw_8_diverge[0] - 5, sw_8_diverge[1]),
                (sw6_exit2[0] - 5, sw_2_diverge[1]),
            ],
        )
        tr9 = Track(self, sw_2_exit, sw_6_enter2)
        tr10 = Track(self, sw_1_diverge, sw_6_enter1, [(sw_1_diverge[0], sw_6_enter1[1])])
        tr11 = Track(
            self,
            sw_2_enter,
            sw_3_enter1,
            [(sw_2_enter[0] - 50, sw_2_enter[1]), (sw_2_enter[0] - 50, sw_3_enter1[1])],
        )
        tr12 = Track(
            self,
            sw_3_exit1,
            sw_11_enter,
            [(sw_8_enter[0] - 5, sw_3_exit1[1]), (sw_11_enter[0] - 5, sw_11_enter[1])],
        )
        tr13 = Track(
            self,
            sw_11_diverge,
            sw6_exit2,
            [
                (sw_11_diverge[0] + 20, sw_11_diverge[1]),
                (sw_11_diverge[0] + 20, sw6_exit2[1]),
            ],
        )

        self.underpass_bottom = (sw_7_enter[0] + 75, sw_7_enter[1] + 15)
        self.underpass_top = (self.underpass_bottom[0], sw_7_enter[1] - 15)
        tr14 = Track(
            self,
            sw_6_exit1,
            self.underpass_bottom,
            [
                (sw_7_enter[0] + 47, sw_6_exit1[1]),
                (self.underpass_bottom[0], self.underpass_bottom[1] + 7),
            ],
        )
        # little bit to make it line up neatly
        tr14_b = Track(
            self,
            (self.underpass_bottom[0] + 1, self.underpass_bottom[1] + 7),
            (self.underpass_bottom[0] + 1, self.underpass_bottom[1]),
        )
        tr15 = Track(
            self,
            sw_9_diverge,
            self.underpass_top,
            [
                (sw_9_diverge[0] - 27, sw_9_diverge[1]),
                (self.underpass_top[0], self.underpass_top[1] - 7),
            ],
        )
        # little bit to make it line up neatly
        tr15_b = Track(
            self,
            (self.underpass_top[0] - 1, self.underpass_top[1] - 7),
            (self.underpass_top[0] - 1, self.underpass_top[1]),
        )

        tr16 = Track(self, sw_8_exit, sw_5_enter)

        slope = Track(
            self,
            sw_11_exit,
            sw_7_enter,
            [(sw_11_exit[0] + 40, sw_11_exit[1]), (sw_11_exit[0] + 40, sw_7_enter[1])],
        )

        platform_1 = Track(
            self,
            sw_4_diverge,
            (sw_4_diverge[0] - 110, sw_4_diverge[1]),
            endstop="vertical",
        )
        platform_2 = Track(self, sw_4_exit, (sw_4_diverge[0] - 110, sw_4_exit[1]), endstop="vertical")
        platform_3 = Track(self, sw_7_exit, (sw_4_diverge[0] - 110, sw_7_exit[1]), endstop="vertical")
        platform_stub = Track(self, sw_7_diverge, sw_4_enter)

        siding_1 = Track(self, sw_5_top, (sw_5_top[0] - 70, sw_5_top[1]), endstop="vertical")
        siding_2 = Track(self, sw_5_middle, (sw_5_middle[0] - 70, sw_5_middle[1]), endstop="vertical")
        siding_3 = Track(self, sw_5_bottom, (sw_5_bottom[0] - 70, sw_5_bottom[1]), endstop="vertical")

        tr1.connections = [sw_10, sw_3]
        tr2.connections = [sw_3, sw_1]
        tr3.connections = [sw_1, sw_0]
        tr4.connections = [sw_0]
        tr5.connections = [sw_0, sw_9]
        tr6.connections = [sw_9, sw_10]
        tr7.connections = [sw_10, sw_8]
        tr8.connections = [sw_8, sw_2]
        tr9.connections = [sw_2, sw_6]
        tr10.connections = [sw_1, sw_6]
        tr11.connections = [sw_2, sw_3]
        tr12.connections = [sw_3, sw_11]
        tr13.connections = [sw_11, sw_6]
        tr14.connections = [sw_6, tr14_b]
        tr14_b.connections = [tr14, tr15_b]
        tr15.connections = [sw_9, tr15_b]
        tr15_b.connections = [tr15, tr14_b]
        tr16.connections = [sw_8, sw_5]
        slope.connections = [sw_11, sw_7]
        platform_1.connections = [sw_4]
        platform_2.connections = [sw_4]
        platform_3.connections = [sw_7]
        platform_stub.connections = [sw_7, sw_4]
        siding_1.connections = [sw_5]
        siding_2.connections = [sw_5]
        siding_3.connections = [sw_5]

        sw_0.set_tracks(tr3, tr5, tr4)
        sw_1.set_tracks(tr2, tr3, tr10)
        sw_2.set_tracks(tr11, tr9, tr8)
        sw_3.set_tracks(tr11, tr12, tr2, tr1)
        sw_4.set_tracks(platform_stub, platform_2, platform_1)
        sw_5.set_tracks(tr16, siding_1, siding_2, siding_3)
        sw_6.set_tracks(tr10, tr14, tr9, tr13)
        sw_7.set_tracks(slope, platform_3, platform_stub)
        sw_8.set_tracks(tr7, tr16, tr8)
        sw_9.set_tracks(tr6, tr5, tr15)
        sw_10.set_tracks(tr6, tr1, tr7)
        sw_11.set_tracks(tr12, slope, tr13)

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
            tr14_b,
            tr15,
            tr15_b,
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

        self.crossovers = [sw_3, sw_6]

        self.signals = [station_signal]

    def update_points(self, states: list[int]):
        for i, state in enumerate(states):
            self.points[i].set_state(state)

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

        for track in self.tracks:
            track.draw(mouse_pos)

        for point in self.points:
            point.check_mouse_click(mouse_pos, mouse_up)
            point.draw()

        # line to show raised section
        pygame.draw.lines(
            self,
            (125, 125, 125),
            False,
            [(342, 0), (342, 135), (120, 135), (120, Layout.height)],
            width=2,
        )

        "bridge"

        pygame.draw.lines(
            self,
            (255, 255, 255),
            False,
            [
                (self.underpass_bottom[0] - 17, self.underpass_bottom[1] - 2),
                (self.underpass_bottom[0] - 12, self.underpass_bottom[1] - 7),
                (self.underpass_bottom[0] + 12, self.underpass_bottom[1] - 7),
                (self.underpass_bottom[0] + 17, self.underpass_bottom[1] - 2),
            ],
        )

        pygame.draw.lines(
            self,
            (255, 255, 255),
            False,
            [
                (self.underpass_bottom[0] - 17, self.underpass_bottom[1] - 29),
                (self.underpass_bottom[0] - 12, self.underpass_bottom[1] - 24),
                (self.underpass_bottom[0] + 12, self.underpass_bottom[1] - 24),
                (self.underpass_bottom[0] + 17, self.underpass_bottom[1] - 29),
            ],
        )

        route_start = None
        for track in self.tracks:
            track.in_route = False
            if track.hover:
                route_start = track

        for switch in self.points:
            switch.mark_unoccupied = False

        for crossover in self.crossovers:
            crossover.conflict = None

        if route_start:
            # list of tuples containing the connection as a tuple
            connections = [(connection, route_start) for connection in route_start.connections]
            route_start.in_route = True
            route = [route_start]

            # while there are still connections to check
            while connections:
                # get the last connection - we add connections to the end
                next_connection = connections.pop(0)

                if isinstance(next_connection[0], Track):
                    # add it to the route
                    if not next_connection[0].in_route:
                        next_connection[0].in_route = True
                        # add the next connections to the list of connections to check
                        connections += [
                            (connection, next_connection[0]) for connection in next_connection[0].connections
                        ]
                        route += [next_connection]
                elif isinstance(next_connection[0], StraightPoint):

                    switch_connections = next_connection[0].get_connected_tracks()

                    if switch_connections[0] == next_connection[1]:
                        connections.append([switch_connections[1], next_connection[0]])
                    elif switch_connections[1] == next_connection[1]:
                        connections.append([switch_connections[0], next_connection[0]])
                    else:
                        next_connection[0].mark_unoccupied = True  # switch not set for route

                    route += [next_connection]

                elif isinstance(next_connection[0], CrossOver):
                    switch_connections = next_connection[0].get_connected_tracks()

                    # Do we have two pairs to handle?
                    if next_connection[0].state == "ahead" or next_connection[0].state == "moving_to_diverge":
                        for connection_pair in switch_connections:
                            if connection_pair[0] == next_connection[1]:
                                connections.append([connection_pair[1], next_connection[0]])
                            elif connection_pair[1] == next_connection[1]:
                                connections.append([connection_pair[0], next_connection[0]])
                    else:  # switch is in the crossover position so only one pair of connections.
                        if switch_connections[0] == next_connection[1]:
                            connections.append([switch_connections[1], next_connection[0]])
                        elif switch_connections[1] == next_connection[1]:
                            connections.append([switch_connections[0], next_connection[0]])
                        else:
                            # set the cross at the incomming route position.
                            next_connection[0].mark_conflict(next_connection[1])
