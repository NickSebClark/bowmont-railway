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
screen = pygame.display.set_mode((600, 600))

layout = pygame.Surface((400,400))

layout_pos = (100,0)

# Set up the line
line_color = (255, 255, 255)
line_start = (50, 200)
line_end = (150, 250)
line_width = 5

points = [points.BasicPoint(layout, 50,100, type="right_up"), 
          points.BasicPoint(layout, 00,200, type="right_down"),
          points.BasicPoint(layout, 50,175, type="up_right"),
          points.BasicPoint(layout, 200,175, type="up_left"),
          points.BasicPoint(layout, 50,250, type="down_right"),
          points.BasicPoint(layout, 200,250, type="down_left"),
          points.BasicPoint(layout, 200,100, type="left_up"),
          points.BasicPoint(layout, 200,200, type="left_down")]

sections = [Section(layout, (100, 100), (300,100)),
        Section(layout, (100, 200), (300,200))]

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

    mouse_pos = (mouse_pos[0] - layout_pos[0], mouse_pos[1] - layout_pos[1])

    for point in points:
        point.update_state(mouse_pos, mouse_up)
    
    mouse_up = False

    # Draw the line
    screen.fill((0, 0, 0))
    layout.fill((0,0,0))

    for point in points:
        point.draw()

    for section in sections:
        section.draw()

    screen.blit(layout, layout_pos)

    pygame.display.flip()

    pygame.time.wait(10)

pygame.quit()