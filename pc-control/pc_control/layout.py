import pygame

from pc_control.points import StraightPoint, CrossOver, Point, Triple
from pc_control.track import Track
from pc_control.signals import Signal
from typing import Tuple
import serial


class Layout(pygame.Surface):
    """Draws the bowmont water layout diagram."""

    width = 1270
    height = 670

    def __init__(self, ser: serial.Serial):
        """Creates all the objects in the layout drawing."""
        super().__init__((Layout.width, Layout.height))

        sw_0 = StraightPoint(self, 40, 240, 0, ser, type="up_right", name="SW0")
        sw_0_enter, sw_0_exit, sw_0_diverge = sw_0.get_connections()

        sw_1 = StraightPoint(self, 40, 460, 1, ser, type="up_right", name="SW1")
        sw_1_enter, sw_1_exit, sw_1_diverge = sw_1.get_connections()

        sw_2 = StraightPoint(self, 280, 360, 2, ser, type="left_down", name="SW2")
        sw_2_enter, sw_2_exit, sw_2_diverge = sw_2.get_connections()

        sw_3 = CrossOver(self, 280, 600, 3, ser, "top_bottom", name="SW3")
        sw_3_enter1, sw_3_enter2, sw_3_exit1, sw10_exit2 = sw_3.get_connections()

        sw_4 = StraightPoint(self, 460, 180, 5, ser, type="right_up", name="SW4", name_pos="top")
        sw_4_enter, sw_4_exit, sw_4_diverge = sw_4.get_connections()

        sw_5 = Triple(self, 560, 500, 6, ser, name="SW5")
        sw_5_enter, sw_5_top, sw_5_middle, sw_5_bottom = sw_5.get_connections()

        sw_6 = CrossOver(self, 480, 320, 8, ser, "bottom_top", name="SW6", name_pos="top")
        sw_6_enter1, sw_6_enter2, sw_6_exit1, sw6_exit2 = sw_6.get_connections()

        sw_7 = StraightPoint(self, 620, 220, 10, ser, type="right_up", name="SW7")
        sw_7_enter, sw_7_exit, sw_7_diverge = sw_7.get_connections()
        station_signal = Signal(self, 315, 60)

        sw_8 = StraightPoint(self, 740, 500, 11, ser, type="right_up", name="SW8", name_pos="top")
        sw_8_enter, sw_8_exit, sw_8_diverge = sw_8.get_connections()

        sw_9 = StraightPoint(self, 1020, 40, 12, ser, type="right_down", name="SW9")
        sw_9_enter, sw_9_exit, sw_9_diverge = sw_9.get_connections()

        sw_10 = StraightPoint(self, 960, 640, 13, ser, type="right_up", name="SW10")
        sw_10_enter, sw_10_exit, sw_10_diverge = sw_10.get_connections()

        sw_11 = StraightPoint(self, 880, 460, 14, ser, type="left_up", name="SW11")
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
            [(sw_2_enter[0] - 120, sw_2_enter[1]), (sw_2_enter[0] - 120, sw_3_enter1[1])],
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
                (sw_11_diverge[0] + 40, sw_11_diverge[1]),
                (sw_11_diverge[0] + 40, sw6_exit2[1]),
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
            [(sw_11_exit[0] + 100, sw_11_exit[1]), (sw_11_exit[0] + 100, sw_7_enter[1])],
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

        self.triple = sw_5

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
            [(650, 0), (650, 270), (200, 270), (200, Layout.height)],
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

        self.highlight_route()

    def highlight_route(self):
        """Check if any tracks are being hovered over then start a route traversal from that track."""

        # Clear the route status for all the tracks. If hovering, this is the route start.
        route_start = None
        for track in self.tracks:
            track.in_route = False
            if track.hover:
                route_start = track

        # Switches have flags to mark red crosses when routes enter switches set against them. Clear these flags.
        for switch in self.points:
            switch.mark_unoccupied = False

        for crossover in self.crossovers:
            crossover.conflict = None

        self.triple.conflict = None

        if route_start:
            traverse_route(route_start)


def traverse_route(route_start: Track):
    """Traverse the route from the route start. Set the flag in the contained tracks to indicate they are in the route."""

    # Find the connections for the route start. Build a list of 2 element tuples. Each tuple describes a connection.
    connections_to_process = [(connection, route_start) for connection in route_start.connections]
    route_start.in_route = True
    route = [route_start]

    # while there are still connections in the route
    while connections_to_process:
        # get the last connection - we add connections to the end
        connection = connections_to_process.pop(0)

        if isinstance(connection[0], Track):
            # add it to the route
            if not connection[0].in_route:
                connection[0].in_route = True
                # get the connections to this track and add them to the connections to process
                connections_to_process += [
                    (track_connection, connection[0]) for track_connection in connection[0].connections
                ]
                route += [connection]
        elif isinstance(connection[0], StraightPoint):

            switch_connections = connection[0].get_connected_tracks()

            # We check if the switch reports that it is set to the track connected to it. If so add the track the other side of the switch to process.
            if switch_connections[0] == connection[1]:
                connections_to_process.append([switch_connections[1], connection[0]])
            elif switch_connections[1] == connection[1]:
                connections_to_process.append([switch_connections[0], connection[0]])
            else:
                connection[0].mark_unoccupied = True  # switch not set for route so set the flag to mark the red cross

        elif isinstance(connection[0], CrossOver):
            switch_connections = connection[0].get_connected_tracks()

            # Is the crossover set or do we have two pairs of connections to handle?
            if connection[0].state == "ahead" or connection[0].state == "moving_to_diverge":
                for connection_pair in switch_connections:
                    if connection_pair[0] == connection[1]:
                        connections_to_process.append([connection_pair[1], connection[0]])
                    elif connection_pair[1] == connection[1]:
                        connections_to_process.append([connection_pair[0], connection[0]])
            else:  # switch is in the crossover position so only one pair of connections.
                if switch_connections[0] == connection[1]:
                    connections_to_process.append([switch_connections[1], connection[0]])
                elif switch_connections[1] == connection[1]:
                    connections_to_process.append([switch_connections[0], connection[0]])
                else:
                    # set the cross at track which is not connected through the switch
                    connection[0].mark_conflict(connection[1])

        elif isinstance(connection[0], Triple):

            switch_connections = connection[0].get_connected_tracks()

            if switch_connections[0] == connection[1]:
                connections_to_process.append([switch_connections[1], connection[0]])
            elif switch_connections[1] == connection[1]:
                connections_to_process.append([switch_connections[0], connection[0]])
            else:
                connection[0].mark_conflict(connection[1])
