import pygame
from typing import Tuple
import tomllib
import pygame.gfxdraw
import serial
from pathlib import Path


def get_colours():
    with open(Path(__file__).parent.parent / "settings.toml", "rb") as f:
        return tomllib.load(f)["point_colours"]


def draw_red_cross(surface, center, size):
    color = (255, 0, 0)  # Red color
    x, y = center
    half_size = size // 2

    pygame.draw.line(
        surface,
        color,
        (x - half_size, y - half_size),
        (x + half_size, y + half_size),
        2,
    )
    pygame.draw.line(
        surface,
        color,
        (x - half_size, y + half_size),
        (x + half_size, y - half_size),
        2,
    )


class Point:
    """Parent Point class intended to be overridden.
    Maintains a point state: ahead, diverge, moving_to_ahead, moving_to_diverge.
    Sets fixed track width of 5.
    Draws bounding box and label.
    """

    def __init__(
        self,
        display: pygame.Surface,
        left: int,
        top: int,
        servo_index: int,
        ser: serial.Serial,
        length: int = 50,
        throw: int = 20,
        name: str = "",
        name_pos: str = "bottom",
    ):
        """Sets up the object with key class data.

        Args:
            display (pygame.Surface): Surface to draw the point on.
            left (int): Draw position
            top (int): Draw position
            length (int, optional): Length of point. Defaults to 50.
            throw (int, optional): Width of point throw. Defaults to 20.
            name (str, optional): Label to draw. Defaults to "".
            name_pos (str, optional): 'bottom' or 'top'. Where to draw the label.
        """
        self.left = left
        self.top = top
        self.display = display
        self.length = length
        self.throw = throw
        self.fixed_offset = 10
        self.thickness = 5
        self.colours = get_colours()

        self.line_colour = self.colours["ahead"]

        self.state = "ahead"

        self.name = name

        self.name_pos = name_pos

        # label_font = pygame.font.Font("resources/britrdn_.ttf", 10)
        label_font = pygame.font.SysFont("MS Reference Sans Serif", 14)
        self.label_surface = label_font.render(self.name, True, self.colours["boundary"])

        self.rect = pygame.Rect(0, 0, 0, 0)

        self.ser = ser
        self.servo_index = servo_index

        self.mark_unoccupied = False

    def __eq__(self, other):
        """Override the equality operator to compare Track objects by their id."""
        if isinstance(other, Point):
            return self.name == other.name
        return False

    def check_mouse_click(self, mouse_pos: Tuple[int, int], mouse_up: bool):
        """Called to check if the point has been clicked and update the state if necessary

        Args:
            mouse_pos (Tuple[int, int]): Mouse position
            mouse_up (bool): Mouse up event?
        """
        if self.rect.collidepoint(mouse_pos):  # is the mouse in the bounding rect?
            # mouse is hovering
            if self.state == "ahead" or self.state == "diverge":
                self.line_colour = self.colours["hover"]

            # have we clicked on the point?
            if mouse_up:
                self.ser.write(str.encode(f"p{self.servo_index}\n"))
                self.line_colour = self.colours["moving"]
                match self.state:
                    case "ahead":
                        self.state = "moving_to_diverge"
                    case "diverge":
                        self.state = "moving_to_ahead"
                    case "moving_to_ahead":
                        self.state = "moving_to_diverge"
                    case "moving_to_diverge":
                        self.state = "moving_to_ahead"
        elif self.state == "ahead":
            self.line_colour = self.colours["ahead"]
        elif self.state == "diverge":
            self.line_colour = self.colours["diverge"]

    def set_state(self, state: int):
        """Set the state of the point externally.

        Args:
            state (int): 0 = move_to_ahead, 1 = move_to_diverge
        """
        if state:
            self.state = "moving_to_diverge"
        else:
            self.state = "moving_to_ahead"

    def draw(self):
        """Draw the bounding box and the label"""
        pygame.draw.rect(self.display, self.colours["boundary"], self.rect, 1)

        if self.name_pos == "bottom":
            self.display.blit(
                self.label_surface,
                (
                    self.rect.left + self.rect.width,
                    self.rect.top + self.rect.height - 2,
                ),
            )
        else:
            self.display.blit(
                self.label_surface,
                (self.rect.left + self.rect.width, self.rect.top - 12),
            )


class StraightPoint(Point):
    """
    Basic straight point with a single throw.
    types:
    left_up
    left_down
    right_up
    right_down
    up_right
    up_left
    down_right
    down_left

    possible states: ahead, diverge, moving_to_ahead, moving_to_diverge
    """

    def __init__(
        self,
        display: pygame.surface,
        left: int,
        top: int,
        servo_index: int,
        ser: serial.Serial,
        type: str = "left_up",
        length: int = 50,
        throw: int = 20,
        name: str = "",
        name_pos: str = "bottom",
    ):
        """Sets up the object.

        Args:
            display (pygame.surface): Surface to draw on
            left (int): Draw position of point start.
            top (int): Draw position of point start.
            type (str, optional): Point type. Describes which direction to draw and throw.
                                  Possible types: left_up, left_down, right_up, right_down, up_right, up_left, down_right, down_left.
                                  Defaults to "left_up".
            length (int, optional): Length of point. Defaults to 50.
            throw (int, optional): Distance to throw. Defaults to 20.
            name (str, optional): Label to draw. Defaults to "".
            name_pos (str, optional): 'bottom' or 'top'. Where to draw the label.
        """
        super().__init__(display, left, top, servo_index, ser, length, throw, name, name_pos)

        self.line_start = (left, top)

        self.type = type

        match type:
            case "left_up":
                self.increment = -1
                self.box_top = top - self.fixed_offset - throw
                self.box_left = left
                self.box_width = self.length + 1
                self.box_height = self.throw + 2 * self.fixed_offset
                self.line_end = [left + self.length, top]
                self.end_pos_index = 1
                self.ahead_pos = top
                self.diverge_pos = top - self.throw
                self.diverge_coord = [self.line_end[0], self.diverge_pos]
                self.ahead_coord = [self.line_end[0], self.ahead_pos]
            case "left_down":
                self.increment = 1
                self.box_top = top - self.fixed_offset
                self.box_left = left
                self.box_width = self.length + 1
                self.box_height = self.throw + 2 * self.fixed_offset
                self.line_end = [left + self.length, top]
                self.end_pos_index = 1
                self.ahead_pos = top
                self.diverge_pos = top + self.throw
                self.diverge_coord = [self.line_end[0], self.diverge_pos]
                self.ahead_coord = [self.line_end[0], self.ahead_pos]
            case "right_up":
                self.increment = -1
                self.box_top = top - self.fixed_offset - throw
                self.box_left = left - self.length
                self.box_width = self.length + 1
                self.box_height = self.throw + 2 * self.fixed_offset
                self.line_end = [left - self.length, top]
                self.end_pos_index = 1
                self.ahead_pos = top
                self.diverge_pos = top - self.throw
                self.diverge_coord = [self.line_end[0], self.diverge_pos]
                self.ahead_coord = [self.line_end[0], self.ahead_pos]
            case "right_down":
                self.increment = 1
                self.box_top = top - self.fixed_offset
                self.box_left = left - self.length
                self.box_width = self.length + 1
                self.box_height = self.throw + 2 * self.fixed_offset
                self.line_end = [left - self.length, top]
                self.end_pos_index = 1
                self.ahead_pos = top
                self.diverge_pos = top + self.throw
                self.diverge_coord = [self.line_end[0], self.diverge_pos]
                self.ahead_coord = [self.line_end[0], self.ahead_pos]
            case "up_right":
                self.increment = 1
                self.box_top = top - self.length
                self.box_left = left - self.fixed_offset
                self.box_width = throw + 2 * self.fixed_offset
                self.box_height = self.length + 1
                self.line_end = [left, top - self.length]
                self.end_pos_index = 0
                self.ahead_pos = left
                self.diverge_pos = left + self.throw
                self.diverge_coord = [self.diverge_pos, self.line_end[1]]
                self.ahead_coord = [self.ahead_pos, self.line_end[1]]
            case "up_left":
                self.increment = -1
                self.box_top = top - self.length
                self.box_left = left - self.throw - self.fixed_offset
                self.box_width = throw + 2 * self.fixed_offset
                self.box_height = self.length + 1
                self.line_end = [left, top - self.length]
                self.end_pos_index = 0
                self.ahead_pos = left
                self.diverge_pos = left - self.throw
                self.diverge_coord = [self.diverge_pos, self.line_end[1]]
                self.ahead_coord = [self.ahead_pos, self.line_end[1]]
            case "down_right":
                self.increment = 1
                self.box_top = top
                self.box_left = left - self.fixed_offset
                self.box_width = throw + 2 * self.fixed_offset
                self.box_height = self.length + 1
                self.line_end = [left, top + self.length]
                self.end_pos_index = 0
                self.ahead_pos = left
                self.diverge_pos = left + self.throw
                self.diverge_coord = [self.diverge_pos, self.line_end[1]]
                self.ahead_coord = [self.ahead_pos, self.line_end[1]]
            case "down_left":
                self.increment = -1
                self.box_top = top
                self.box_left = left - self.throw - self.fixed_offset
                self.box_width = throw + 2 * self.fixed_offset
                self.box_height = self.length + 1
                self.line_end = [left, top + self.length]
                self.end_pos_index = 0
                self.ahead_pos = left
                self.diverge_pos = left - self.throw
                self.diverge_coord = [self.diverge_pos, self.line_end[1]]
                self.ahead_coord = [self.ahead_pos, self.line_end[1]]

        self.rect = pygame.Rect(self.box_left, self.box_top, self.box_width, self.box_height)

    def get_connections(
        self,
    ) -> Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]:
        return self.line_start, self.line_end.copy(), self.diverge_coord

    def set_tracks(self, enter, exit, diverge):
        self.enter = enter
        self.exit = exit
        self.diverge = diverge

    def get_connected_tracks(self):
        match self.state:
            case "ahead":
                return self.enter, self.exit
            case "diverge":
                return self.enter, self.diverge
            case "moving_to_ahead":
                return self.enter, self.diverge
            case "moving_to_diverge":
                return self.enter, self.exit

    def draw(self):
        """Draw the point. Increment the position if moving."""

        match self.state:
            case "moving_to_ahead":
                if self.line_end[self.end_pos_index] == self.ahead_pos:
                    self.state = "ahead"
                else:
                    self.line_end[self.end_pos_index] -= self.increment

            case "moving_to_diverge":
                if self.line_end[self.end_pos_index] == self.diverge_pos:
                    self.state = "diverge"
                else:
                    self.line_end[self.end_pos_index] += self.increment

        # pygame.draw.line(self.display, self.line_colour, self.line_start, self.line_end, self.thickness)

        if self.type in ["left_up", "left_down", "right_up", "right_down"]:
            points = [
                (self.line_start[0], self.line_start[1] - 2),
                (self.line_start[0], self.line_start[1] + 2),
                (self.line_end[0], self.line_end[1] + 2),
                (self.line_end[0], self.line_end[1] - 2),
            ]
        else:
            points = [
                (self.line_start[0] - 2, self.line_start[1]),
                (self.line_start[0] + 2, self.line_start[1]),
                (self.line_end[0] + 2, self.line_end[1]),
                (self.line_end[0] - 2, self.line_end[1]),
            ]

        pygame.gfxdraw.filled_polygon(self.display, points, self.line_colour)
        pygame.gfxdraw.aapolygon(self.display, points, self.line_colour)

        if self.mark_unoccupied:
            if self.state == "ahead":
                draw_red_cross(self.display, self.diverge_coord, 10)
            elif self.state == "diverge":
                draw_red_cross(self.display, self.ahead_coord, 10)

        super().draw()


class CrossOver(Point):
    """Cross over point type. Single click to change point from ahead to cross-over"""

    def __init__(
        self,
        display: pygame.surface,
        left: int,
        top: int,
        servo_index: int,
        ser: serial.Serial,
        type: str,
        length: int = 50,
        throw: int = 20,
        name: str = "",
        name_pos: str = "bottom",
    ):
        """Setup the point object.

        Args:
            display (pygame.surface): Display to draw on.
            left (int): Draw position of point start.
            top (int): Draw position of point start.
            type (str): which direction to move the point top_bottom or bottom_top
            length (int, optional): Length of point. Defaults to 50.
            throw (int, optional): Width of throw. Defaults to 20.
            name (str, optional): Label to draw. Defaults to "".
            name_pos (str, optional): 'bottom' or 'top'. Where to draw the label.
        """

        super().__init__(display, left, top, servo_index, ser, length, throw, name, name_pos)

        self.line1_start = [left, top]
        self.line2_start = [left, top + throw]
        self.line1_end = [left + length, top]
        self.line2_end = [left + length, top + throw]

        self.top_enter_pos = self.line1_start.copy()
        self.top_exit_pos = self.line1_end.copy()
        self.bottom_enter_pos = self.line2_start.copy()
        self.bottom_exit_pos = self.line2_end.copy()

        self.type = type

        self.rect = pygame.Rect(left, top - self.fixed_offset, length + 1, throw + 2 * self.fixed_offset)

        self.conflict = None

    def mark_conflict(self, track):
        match track:
            case self.top_enter:
                self.conflict = self.top_enter_pos
            case self.top_exit:
                self.conflict = self.top_exit_pos
            case self.bottom_enter:
                self.conflict = self.bottom_enter_pos
            case self.bottom_exit:
                self.conflict = self.bottom_exit_pos

    def get_connections(self):
        return (
            self.line1_start.copy(),
            self.line2_start.copy(),
            self.line1_end.copy(),
            self.line2_end.copy(),
        )

    def set_tracks(self, top_enter, top_exit, bottom_enter, bottom_exit):
        self.top_enter = top_enter
        self.top_exit = top_exit
        self.bottom_enter = bottom_enter
        self.bottom_exit = bottom_exit

    def get_connected_tracks(self):
        match self.state:
            case "ahead":
                return [
                    (self.top_enter, self.top_exit),
                    (self.bottom_enter, self.bottom_exit),
                ]
            case "diverge":
                if self.type == "top_bottom":
                    return self.top_enter, self.bottom_exit
                else:
                    return self.bottom_enter, self.top_exit
            case "moving_to_ahead":
                if self.type == "top_bottom":
                    return self.top_enter, self.bottom_exit
                else:
                    return self.bottom_enter, self.top_exit
            case "moving_to_diverge":
                return [
                    (self.top_enter, self.top_exit),
                    (self.bottom_enter, self.bottom_exit),
                ]

    def draw(self):
        """Draw the point. Increment the position if moving."""
        match self.state:
            case "moving_to_ahead":
                if self.type == "top_bottom":
                    if self.line1_end[1] == self.top:
                        self.state = "ahead"
                    else:
                        self.line1_end[1] -= 1
                        self.line2_start[1] += 1
                else:
                    if self.line1_start[1] == self.top:
                        self.state = "ahead"
                    else:
                        self.line1_start[1] -= 1
                        self.line2_end[1] += 1
            case "moving_to_diverge":
                if self.type == "top_bottom":
                    if self.line1_end[1] == self.top + self.throw:
                        self.state = "diverge"
                    else:
                        self.line1_end[1] += 1
                        self.line2_start[1] -= 1
                else:
                    if self.line1_start[1] == self.top + self.throw:
                        self.state = "diverge"
                    else:
                        self.line1_start[1] += 1
                        self.line2_end[1] -= 1

        points1 = [
            (self.line1_start[0], self.line1_start[1] - 2),
            (self.line1_start[0], self.line1_start[1] + 2),
            (self.line1_end[0], self.line1_end[1] + 2),
            (self.line1_end[0], self.line1_end[1] - 2),
        ]
        pygame.gfxdraw.filled_polygon(self.display, points1, self.line_colour)
        pygame.gfxdraw.aapolygon(self.display, points1, self.line_colour)

        points2 = [
            (self.line2_start[0], self.line2_start[1] - 2),
            (self.line2_start[0], self.line2_start[1] + 2),
            (self.line2_end[0], self.line2_end[1] + 2),
            (self.line2_end[0], self.line2_end[1] - 2),
        ]
        pygame.gfxdraw.filled_polygon(self.display, points2, self.line_colour)
        pygame.gfxdraw.aapolygon(self.display, points2, self.line_colour)

        if self.conflict:
            draw_red_cross(self.display, self.conflict, 10)

        super().draw()


class Triple(Point):
    def __init__(
        self,
        display: pygame.surface,
        left: int,
        top: int,
        servo_index: int,
        ser: serial.Serial,
        length: int = 50,
        throw: int = 20,
        name: str = "",
    ):
        super().__init__(display, left, top, servo_index, ser, length, throw, name)

        self.rect = pygame.Rect(
            left - length,
            top - throw - self.fixed_offset,
            length + 1,
            2 * throw + 2 * self.fixed_offset,
        )

        self.enter = (left, top)
        self.road_1 = (left - length, top - throw)
        self.road_2 = (left - length, top)
        self.road_3 = (left - length, top + throw)

        self.line_end = [self.road_2[0], self.road_2[1]]

        self.state = "road_2"

        self.conflict = None

    def set_tracks(self, enter, road_1, road_2, road_3):
        self.enter_track = enter
        self.road_1_track = road_1
        self.road_2_track = road_2
        self.road_3_track = road_3

    def mark_conflict(self, track):
        match track:
            case self.road_1_track:
                self.conflict = self.road_1
            case self.road_2_track:
                self.conflict = self.road_2
            case self.road_3_track:
                self.conflict = self.road_3

    def get_connected_tracks(self):
        match self.state:
            case "road_1":
                return self.enter_track, self.road_1_track
            case "road_2":
                return self.enter_track, self.road_2_track
            case "road_3":
                return self.enter_track, self.road_3_track
            case "moving_to_road_1":
                return self.enter_track, self.road_1_track
            case "moving_to_road_2":
                return self.enter_track, self.road_2_track
            case "moving_to_road_3":
                return self.enter_track, self.road_3_track

    def set_state(self, state: int):
        match state:
            case 0:
                self.state = "moving_to_road_1"
            case 1:
                self.state = "moving_to_road_2"
            case 2:
                self.state = "moving_to_road_3"

    def check_mouse_click(self, mouse_pos: Tuple[int, int], mouse_up: bool):
        """Called to check if the point has been clicked and update the state if necessary

        Args:
            mouse_pos (Tuple[int, int]): Mouse position
            mouse_up (bool): Mouse up event?
        """
        if self.rect.collidepoint(mouse_pos):  # is the mouse in the bounding rect?
            # mouse is hovering
            if self.state in ["road_1", "road_2", "road_3"]:
                self.line_colour = self.colours["hover"]

            # have we clicked on the point?
            if mouse_up:
                self.line_colour = self.colours["moving"]
                match self.state:
                    case "road_1":
                        self.state = "moving_to_road_2"
                    case "road_2":
                        self.state = "moving_to_road_3"
                    case "road_3":
                        self.state = "moving_to_road_1"
                    case "moving_to_road_2":
                        self.state = "moving_to_road_3"
                    case "moving_to_road_3":
                        self.state = "moving_to_road_1"
                    case "moving_to_road_1":
                        self.state = "moving_to_road_2"
        elif self.state == "road_2":
            self.line_colour = self.colours["ahead"]
        elif self.state == "road_1" or self.state == "road_3":
            self.line_colour = self.colours["diverge"]

    def get_connections(self):
        return self.enter, self.road_1, self.road_2, self.road_3

    def draw(self):
        match self.state:
            case "moving_to_road_1":
                if self.line_end[1] == self.road_1[1]:
                    self.state = "road_1"
                elif self.line_end[1] > self.road_1[1]:
                    self.line_end[1] -= 1
                else:
                    self.line_end[1] += 1
            case "moving_to_road_2":
                if self.line_end[1] == self.road_2[1]:
                    self.state = "road_2"
                elif self.line_end[1] > self.road_2[1]:
                    self.line_end[1] -= 1
                else:
                    self.line_end[1] += 1
            case "moving_to_road_3":
                if self.line_end[1] == self.road_3[1]:
                    self.state = "road_3"
                elif self.line_end[1] > self.road_3[1]:
                    self.line_end[1] -= 1
                else:
                    self.line_end[1] += 1

        points = [
            (self.enter[0], self.enter[1] - 2),
            (self.enter[0], self.enter[1] + 2),
            (self.line_end[0], self.line_end[1] + 2),
            (self.line_end[0], self.line_end[1] - 2),
        ]

        pygame.gfxdraw.filled_polygon(self.display, points, self.line_colour)
        pygame.gfxdraw.aapolygon(self.display, points, self.line_colour)
        pygame.draw.rect(self.display, self.colours["boundary"], self.rect, 1)

        if self.conflict:
            draw_red_cross(self.display, self.conflict, 10)

        self.display.blit(
            self.label_surface,
            (self.rect.left + self.rect.width, self.rect.top + self.rect.height),
        )
