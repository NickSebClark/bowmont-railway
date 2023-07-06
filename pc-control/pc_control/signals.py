import pygame
import pygame.gfxdraw
from typing import Tuple


class Signal:
    """2 aspect signal.
    Maintains state of either 'stop' or 'proceed'.
    The colour of the lights is set by the state.
    """

    def __init__(self, display: pygame.Surface, left: int, top: int):
        """Sets up object.

        Args:
            display (pygame.Surface): Surface to draw the point on.
            left (int): Top left corner
            top (int): Top left corner
        """
        self.left = left
        self.top = top
        self.display = display
        self.width = 22
        self.height = 40
        self.light_radius = 5

        self.outline_colour = (255, 255, 255)

        self.red_aspect_illuminated_colour = (255, 0, 0)
        self.red_aspect_dimmed_colour = (75, 0, 0)
        self.red_aspect_colour = self.red_aspect_illuminated_colour

        self.green_aspect_illuminated_colour = (0, 255, 0)
        self.green_aspect_dimmed_colour = (0, 60, 0)
        self.green_aspect_colour = self.green_aspect_dimmed_colour

        self.rect = pygame.Rect(left, top, self.width, self.height)

        self.state = "stop"

    def update_state(self, mouse_pos: Tuple[int, int], mouse_up: bool):
        """Updates the state of the signal if it is clicked

        Args:
            mouse_pos (Tuple[int, int]): Mouse position.
            mouse_up (bool): Mouse up event?
        """
        if self.rect.collidepoint(mouse_pos):
            if mouse_up:
                if self.state == "stop":
                    self.red_aspect_colour = self.red_aspect_dimmed_colour
                    self.green_aspect_colour = self.green_aspect_illuminated_colour
                    self.state = "proceed"
                elif self.state == "proceed":
                    self.red_aspect_colour = self.red_aspect_illuminated_colour
                    self.green_aspect_colour = self.green_aspect_dimmed_colour
                    self.state = "stop"

    def draw(self):
        """Draw the boundary and the lights."""
        pygame.draw.rect(self.display, (255, 255, 255), self.rect, 1, border_radius=8)

        # draw red circle
        pygame.gfxdraw.aacircle(
            self.display, int(self.left + self.width / 2), int(self.top + 12), self.light_radius, self.red_aspect_colour
        )
        pygame.gfxdraw.filled_circle(
            self.display, int(self.left + self.width / 2), int(self.top + 12), self.light_radius, self.red_aspect_colour
        )

        # draw green circle
        pygame.gfxdraw.aacircle(
            self.display,
            int(self.left + self.width / 2),
            int(self.top + self.height - 12),
            self.light_radius,
            self.green_aspect_colour,
        )
        pygame.gfxdraw.filled_circle(
            self.display,
            int(self.left + self.width / 2),
            int(self.top + self.height - 12),
            self.light_radius,
            self.green_aspect_colour,
        )
