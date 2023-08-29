import pygame
from typing import Tuple
import pygame.gfxdraw


class Track:
    """Draw track. Uses aapolygons. Fixed width of 4 pixels."""

    def __init__(
        self,
        display: pygame.surface,
        start: Tuple[int, int],
        end: Tuple[int, int],
        corners: list[Tuple[int, int]] = [],
        endstop: str = "None",
    ):
        """Setup a section of track

        Args:
            display (pygame.surface): Surface to draw on
            start (Tuple[int,int]): beginning of track
            stop (Tuple[int,int]): end of track
            corners (list[Tuple[int,int]]): any additional corners
            endstop (str, optional): horizontal or vertical. Defaults to "None".
        """
        self.display = display
        self.vertices = [start] + corners + [end]
        self.line_colour = (255, 255, 255)
        self.endstop = endstop

    def draw(self):
        """Draw the sections to the display and add the endstop if one is specified."""
        # pygame.draw.lines(self.display, self.line_colour, False, self.vertices, self.width)

        for i in range(len(self.vertices) - 1):
            line_start = self.vertices[i]
            line_end = self.vertices[i + 1]


            if line_start[0] != line_end[0] and line_start[1] != line_end[1]: #diagonal line
                points = [
                    (line_start[0] - 3, line_start[1]),
                    (line_start[0] + 2, line_start[1]),
                    (line_end[0] + 3, line_end[1]),
                    (line_end[0] - 2, line_end[1]),
                ]
            elif line_start[0] != line_end[0]: # horizontal line
                points = [
                    (line_start[0], line_start[1] - 2),
                    (line_start[0], line_start[1] + 2),
                    (line_end[0], line_end[1] + 2),
                    (line_end[0], line_end[1] - 2),
                ]
            else: # vertical line
                points = [
                    (line_start[0] - 2, line_start[1]),
                    (line_start[0] + 2, line_start[1]),
                    (line_end[0] + 2, line_end[1]),
                    (line_end[0] - 2, line_end[1]),
                ]

            pygame.gfxdraw.filled_polygon(self.display, points, self.line_colour)
            pygame.gfxdraw.aapolygon(self.display, points, self.line_colour)

            #if there is more than one section, draw a circle at the start of subsequent sections to round the corners.
            if i>0:
                pygame.gfxdraw.filled_circle(self.display, line_start[0], line_start[1], 2, self.line_colour)
                pygame.gfxdraw.aacircle(self.display, line_start[0], line_start[1], 2, self.line_colour)


        

        end_point = self.vertices[-1]

        if self.endstop == "vertical":
            pygame.draw.line(
                self.display,
                self.line_colour,
                (end_point[0], end_point[1] - 5),
                (end_point[0], end_point[1] + 5),
                4,
            )
        elif self.endstop == "horizontal":
            pygame.draw.line(
                self.display,
                self.line_colour,
                (end_point[0] - 5, end_point[1]),
                (end_point[0] + 5, end_point[1]),
                4,
            )
