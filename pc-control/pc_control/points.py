import pygame
import json
from typing import Tuple
import tomllib


def get_colours():
    with open("settings.toml", "rb") as f:
        return tomllib.load(f)["point_colours"]


class Point:
    """Parent Point class intended to be overridden.
    Maintains a point state: ahead, diverge, moving_to_ahead, moving_to_diverge.
    """

    def __init__(self, display: pygame.Surface, left: int, top: int, length: int = 50, throw: int = 20, name: str = ""):
        """Sets up the object with key class data.

        Args:
            display (pygame.Surface): Surface to draw the point on.
            left (int): Draw position
            top (int): Draw position
            length (int, optional): Length of point. Defaults to 50.
            throw (int, optional): Width of point throw. Defaults to 20.
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

        # label_font = pygame.font.Font("resources/britrdn_.ttf", 10)
        label_font = pygame.font.SysFont("MS Reference Sans Serif", 10)
        self.label_surface = label_font.render(self.name, True, self.colours["boundary"])

        self.rect = pygame.Rect(0, 0, 0, 0)

    def update_state(self, mouse_pos: Tuple[int, int], mouse_up: bool):
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

    def draw(self):
        pass


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
        type: str = "left_up",
        length: int = 50,
        throw: int = 20,
        name: str = "",
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
        """
        super().__init__(display, left, top, length, throw, name)

        self.line_start = (left, top)

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

        self.rect = pygame.Rect(self.box_left, self.box_top, self.box_width, self.box_height)

    def get_connections(self) -> Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]:
        return self.line_start, self.line_end.copy(), self.diverge_coord

    def draw(self):
        """Draw the point. Increment the position if moving."""

        match self.state:
            case "moving_to_ahead":
                self.line_end[self.end_pos_index] -= self.increment
                if self.line_end[self.end_pos_index] == self.ahead_pos:
                    self.state = "ahead"
            case "moving_to_diverge":
                self.line_end[self.end_pos_index] += self.increment
                if self.line_end[self.end_pos_index] == self.diverge_pos:
                    self.state = "diverge"

        pygame.draw.line(self.display, self.line_colour, self.line_start, self.line_end, self.thickness)
        pygame.draw.rect(self.display, self.colours["boundary"], self.rect, 1)

        self.display.blit(self.label_surface, (self.box_left + self.box_width, self.box_top + self.box_height))


class CrossOver(Point):
    """Cross over point type. Single click to change point from ahead to cross-over"""

    def __init__(self, display: pygame.surface, left: int, top: int, length: int = 50, throw: int = 20, name: str = ""):
        """Setup the point object.

        Args:
            display (pygame.surface): Display to draw on.
            left (int): Draw position of point start.
            top (int): Draw position of point start.
            length (int, optional): Length of point. Defaults to 50.
            throw (int, optional): Width of throw. Defaults to 20.
        """

        super().__init__(display, left, top, length, throw, name)

        self.line1_start = [left, top]
        self.line2_start = [left, top + throw]
        self.line1_end = [left + length, top]
        self.line2_end = [left + length, top + throw]

        self.rect = pygame.Rect(left, top - self.fixed_offset, length + 1, throw + 2 * self.fixed_offset)

    def get_connections(self):
        return self.line1_start.copy(), self.line2_start.copy(), self.line1_end.copy(), self.line2_end.copy()

    def draw(self):
        """Draw the point. Increment the position if moving."""
        match self.state:
            case "moving_to_ahead":
                self.line1_end[1] -= 1
                self.line2_start[1] += 1
                if self.line1_end[1] == self.top:
                    self.state = "ahead"
            case "moving_to_diverge":
                self.line1_end[1] += 1
                self.line2_start[1] -= 1
                if self.line1_end[1] == self.top + self.throw:
                    self.state = "diverge"

        pygame.draw.line(self.display, self.line_colour, self.line1_start, self.line1_end, self.thickness)
        pygame.draw.line(self.display, self.line_colour, self.line2_start, self.line2_end, self.thickness)

        pygame.draw.rect(self.display, self.colours["boundary"], self.rect, 1)

        self.display.blit(self.label_surface, (self.rect.left + self.rect.width, self.rect.top + self.rect.height))
