import pygame

pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([500, 500])

# Set up the initial line position
line_start = (0, 0)
line_end = (250, 250)

# Draw an anti-aliased line
pygame.draw.aaline(screen, (255, 255, 255), line_start, line_end)

# Update the screen
pygame.display.flip()

# Run until the user asks to quit
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Move the line to the mouse position
            line_start = event.pos
            line_end = (line_end[0] + event.pos[0], line_end[1] + event.pos[1])
            # Redraw the line
            screen.fill((0, 0, 0))
            pygame.draw.aaline(screen, (255, 255, 255), line_start, line_end)
            pygame.display.flip()

# Quit pygame properly
pygame.quit()