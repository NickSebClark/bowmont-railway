import pygame
from pc_control.layout import Layout

pygame.init()
pygame.font.init()

title_font = pygame.font.SysFont('Calibri', 30)
title_surface = title_font.render('Bowmont Railway', True, (255, 255, 255))

# Set up the display
screen = pygame.display.set_mode((800, 600))

layout = Layout()

layout_pos = (100,100)

running = True
mouse_up = False

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_up = True

    mouse_pos = pygame.mouse.get_pos()

    screen.fill((0, 0, 0))

    layout.draw((mouse_pos[0] - layout_pos[0], mouse_pos[1] - layout_pos[1]), mouse_up)

    mouse_up = False

    screen.blit(layout, layout_pos)
    screen.blit(title_surface, (0,0))

    pygame.display.flip()

    pygame.time.wait(10)

pygame.quit()