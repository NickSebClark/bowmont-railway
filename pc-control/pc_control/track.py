import pygame
from typing import Tuple
import pygame.gfxdraw
import tomllib
from pathlib import Path


def get_colours():
    with open(Path(__file__).parent.parent / "settings.toml", "rb") as f:
        return tomllib.load(f)["track_colours"]


class Track:
    """Draw track. Uses aapolygons. Fixed width of 4 pixels."""

    id_counter = 1

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
        self.endstop = endstop
        self.click_buffer = 5  # how much margin around the line for clicking
        self.id = Track.id_counter
        Track.id_counter += 1

        font = pygame.font.Font(None, 18)  # Use default font and size 36
        self.label = font.render(str(self.id), True, (255, 255, 255))  # Render the ID as text
        self.in_route = False
        self.connections = []

        colours = get_colours()
        self.route_colour = colours["route_colour"]
        self.base_colour = colours["base_colour"]
        self.highlight_colour = colours["highlight_colour"]

    def __eq__(self, other):
        """Override the equality operator to compare Track objects by their id."""
        if isinstance(other, Track):
            return self.id == other.id
        return False

    def draw(self, mouse_pos: Tuple[int, int]):
        """Draw the sections to the display and add the endstop if one is specified."""
        # pygame.draw.lines(self.display, self.line_colour, False, self.vertices, self.width)

        self.hover = False

        for i in range(len(self.vertices) - 1):
            line_start = self.vertices[i]
            line_end = self.vertices[i + 1]

            if line_start[0] != line_end[0] and line_start[1] != line_end[1]:  # diagonal line
                points = [
                    (line_start[0] - 3, line_start[1]),
                    (line_start[0] + 3, line_start[1]),
                    (line_end[0] + 3, line_end[1]),
                    (line_end[0] - 3, line_end[1]),
                ]
            elif line_start[0] != line_end[0]:  # horizontal line
                points = [
                    (line_start[0], line_start[1] - 2),
                    (line_start[0], line_start[1] + 2),
                    (line_end[0], line_end[1] + 2),
                    (line_end[0], line_end[1] - 2),
                ]
            else:  # vertical line
                points = [
                    (line_start[0] - 2, line_start[1]),
                    (line_start[0] + 2, line_start[1]),
                    (line_end[0] + 2, line_end[1]),
                    (line_end[0] - 2, line_end[1]),
                ]

            # Extracting the x and y coordinates
            x_coords = [point[0] for point in points]
            y_coords = [point[1] for point in points]

            # Finding the minimum and maximum coordinates
            min_x = min(x_coords) - self.click_buffer
            max_x = max(x_coords) + self.click_buffer
            min_y = min(y_coords) - self.click_buffer
            max_y = max(y_coords) + self.click_buffer

            # Calculating the width and height
            width = max_x - min_x
            height = max_y - min_y

            # Creating the Rect object
            rect = pygame.Rect(min_x, min_y, width, height)

            if self.in_route:
                colour = self.route_colour
            else:
                colour = self.base_colour

            if rect.collidepoint(mouse_pos):
                self.hover = True

            pygame.gfxdraw.filled_polygon(self.display, points, colour)
            pygame.gfxdraw.aapolygon(self.display, points, colour)

            # if there is more than one section, draw a circle at the start of subsequent sections to round the corners.
            if i > 0:
                pygame.gfxdraw.filled_circle(self.display, line_start[0], line_start[1], 2, colour)
                pygame.gfxdraw.aacircle(self.display, line_start[0], line_start[1], 2, colour)

        end_point = self.vertices[-1]

        if self.endstop == "vertical":
            pygame.draw.line(
                self.display,
                colour,
                (end_point[0], end_point[1] - 5),
                (end_point[0], end_point[1] + 5),
                4,
            )
        elif self.endstop == "horizontal":
            pygame.draw.line(
                self.display,
                colour,
                (end_point[0] - 5, end_point[1]),
                (end_point[0] + 5, end_point[1]),
                4,
            )

        # self.display.blit(
        #     self.label, (self.vertices[0][0] + 10, self.vertices[0][1] - 10)
        # )  # Blit the text surface onto the display
