"""PC Control app top-level"""

import pygame
from pc_control.layout import Layout


def main():
    """Basic pygame setup and main event loop."""

    pygame.init()
    pygame.font.init()

    # Title font
    title_font = pygame.font.SysFont("Calibri", 45)
    title_surface = title_font.render("BOWMONT RAILWAY", True, (255, 255, 255))
    sign_outline = pygame.Rect(74, 5, 389, 40)

    # Set up the display
    screen = pygame.display.set_mode((800, 600))

    layout = Layout()
    layout_pos = (5, 50)

    image = pygame.image.load("resources/sign_small.png")

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
        screen.blit(title_surface, (78, 5))
        screen.blit(image, (5, 5))
        pygame.draw.rect(screen, (255, 255, 255), sign_outline, 2)

        pygame.display.flip()

        pygame.time.wait(10)

    pygame.quit()


if __name__ == "__main__":
    main()
