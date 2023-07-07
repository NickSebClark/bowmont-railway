import pygame
from typing import Tuple


class Track:
    def __init__(
        self,
        display: pygame.surface,
        sections: list[Tuple[Tuple[int, int], Tuple[int, int]]],
        width: int = 5,
        endstop: str = "None",
    ):
        """Setup a section of track

        Args:
            display (pygame.surface): Surface to draw on
            sections (list[Tuple[Tuple[int, int], Tuple[int, int]]]): Each element in the outer list represents a line section.
                                                                     This is comprised of two, two element tuples which are the start end end point of the line.
            width (int, optional): Line width. Defaults to 5.
            endstop (str, optional): horizontal or vertical. Defaults to "None".
        """
        self.display = display
        self.sections = sections
        self.line_colour = (255, 255, 255)
        self.width = width
        self.endstop = endstop

    def draw(self):
        for section in self.sections:
            pygame.draw.line(self.display, self.line_colour, section[0], section[1], self.width)

            end_point = self.sections[-1][1]

        if self.endstop == "vertical":
            pygame.draw.line(
                self.display,
                self.line_colour,
                (end_point[0], end_point[1] - 5),
                (end_point[0], end_point[1] + 5),
                self.width,
            )
        elif self.endstop == "horizontal":
            pygame.draw.line(
                self.display,
                self.line_colour,
                (end_point[0] - 5, end_point[1]),
                (end_point[0] + 5, end_point[1]),
                self.width,
            )
