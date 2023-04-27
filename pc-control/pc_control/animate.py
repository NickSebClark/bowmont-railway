import pygame

pygame.init()

# Set up the display
screen = pygame.display.set_mode((400, 400))

# Set up the line
line_color = (255, 255, 255)
line_start = (50, 200)
line_end = (150, 250)
line_width = 5

# Set up the animation
animation_speed = 2
animation_direction = 1

# Start the game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if rect.collidepoint(mouse_pos):
                print("mouse up")

    # Create a Rect object at position (100, 100) with width 50 and height 50
    rect = pygame.Rect(100, 100, 50, 50)

    # Draw a red rectangle using the Rect object


    # Update the line position
    line_start = (line_start[0] + animation_speed * animation_direction, line_start[1])
    line_end = (line_end[0] + animation_speed * animation_direction, line_end[1])

    

    # Reverse direction if we hit an edge
    if line_start[0] < 0 or line_end[0] > screen.get_width():
        animation_direction *= -1

    # Draw the line
    screen.fill((0, 0, 0))
    pygame.draw.line(screen, line_color, line_start, line_end, line_width)

    pygame.draw.rect(screen, (255, 0, 0), rect)


    pygame.display.flip()

    pygame.time.wait(10)

pygame.quit()