"""PC Control app top-level"""

import pygame
import pygame.freetype
from pc_control.layout import Layout
import pc_control.serial_comms as serial


def main():
    """Basic pygame setup and main event loop."""

    pygame.display.set_caption("Bowmont Town Layout PC Control")

    pygame.init()
    pygame.font.init()

    width = 600
    height = 400

    # Title font
    title_font = pygame.font.Font("resources/britrdn_.ttf", 39)
    title_surface = title_font.render("Bowmont Town", True, (255, 255, 255))
    sign_outline = pygame.Rect(width / 2 - title_surface.get_width() / 2 - 10, 5, title_surface.get_width() + 20, 40)

    # Set up the display
    screen = pygame.display.set_mode((width, height))

    layout = Layout()
    layout_pos = (5, 50)

    image = pygame.image.load("resources/sign_small.png")
    roundel = pygame.image.load("resources/roundel.png")

    ser = serial.connect()

    running = True

    while running:
        mouse_up = False

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_up = True

        mouse_pos = pygame.mouse.get_pos()

        screen.fill((0, 0, 0))

        # Draw the layout with the mouse position relative to the layout pos.
        layout.draw((mouse_pos[0] - layout_pos[0], mouse_pos[1] - layout_pos[1]), mouse_up)

        # Blit the layout and text
        screen.blit(layout, layout_pos)
        screen.blit(title_surface, (width / 2 - title_surface.get_width() / 2, 7))
        screen.blit(image, (5, 5))
        screen.blit(roundel, (width - 40 - 5, 5))
        pygame.draw.rect(screen, (255, 255, 255), sign_outline, 2)

        serial_read(ser, layout)

        pygame.display.flip()

        pygame.time.wait(10)

    pygame.quit()

def serial_read(ser, layout):
    data = serial.read_data(ser)

    if data:
        for line in data:
            print(line)

if __name__ == "__main__":
    main()
