import pygame
from pc_control import points

point_colour = (255, 255, 255)


class Section():
    def __init__(self, display, start, end):
        self.display = display
        self.start = start
        self.end = end
        self.line_colour = (255,255,255)
    
    def draw(self):
        pygame.draw.line(self.display, self.line_colour, self.start, self.end, 5)


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


points = [points.BasicPoint(screen, 100,100, type="ru"), 
          points.BasicPoint(screen, 100,200, type="rd"),
          points.BasicPoint(screen, 300,100, type="lu"),
          points.BasicPoint(screen, 300,200, type="ld")]

sections = [Section(screen, (100, 100), (300,100)),
        Section(screen, (100, 200), (300,200))]

# Start the game loop
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

    for point in points:
        point.update_state(mouse_pos, mouse_up)
    
    mouse_up = False

    # Draw the line
    screen.fill((0, 0, 0))

    for point in points:
        point.draw()

    for section in sections:
        section.draw()

    pygame.display.flip()

    pygame.time.wait(10)

pygame.quit()