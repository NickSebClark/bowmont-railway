import pygame

point_colour = (255, 255, 255)

class BasicPoint():
    def __init__(self, left, top, display):
        self.left = left
        self.top = top
        self.display = display
        self.width = 50
        self.height = 50
        self.fixed_offset = 10
        self.rect = pygame.Rect(left, top, self.width, self.height)
        
        self.offset = 0

        self.hover_colour = (0, 255, 0)
        self.moving_colour = (255, 0, 0)
        self.line_colour = (255, 255, 255)

        self.line_start = (left, top+self.fixed_offset)
        self.line_end = [left+self.width-1, top+self.fixed_offset]

        self.pos1_vpos = top+self.fixed_offset
        self.pos2_vpos = top+self.height - self.fixed_offset

        # possible states: pos1, pos2, moving_to_pos1, moving_to_pos2
        self.state = "pos1"

    def update_state(self, mouse_pos, mouse_up):
        if self.rect.collidepoint(mouse_pos):
            
            if self.state == "pos1":
                self.line_colour = self.hover_colour

            if mouse_up:
                self.line_colour = self.moving_colour
                match self.state:
                    case "pos1":
                        self.state = "moving_to_pos2"
                    case "pos2":
                        self.state = "moving_to_pos1"
                    case "moving_to_pos1":
                        self.state = "moving_to_pos2"
                    case "moving_to_pos2":
                        self.state = "moving_to_pos1"
        else:
            self.line_colour =(255, 255, 255)

    def draw(self):
        #pygame.draw.rect(self.display, (255, 0, 0), self.rect)

        match self.state:
            case "moving_to_pos1":
                self.line_end[1] -= 1
                if self.line_end[1] == self.pos1_vpos:
                    self.state = "pos1"
                    self.line_colour = (255, 255, 255)
            case "moving_to_pos2":
                self.line_end[1] += 1 
                if self.line_end[1] == self.pos2_vpos:
                    self.state = "pos2"
                    self.line_colour = (255, 255, 255)

        pygame.draw.line(self.display, self.line_colour, self.line_start, self.line_end, 5)



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


points = [BasicPoint(100,100,screen)]

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
    # Create a Rect object at position (100, 100) with width 50 and height 50

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


    for point in points:
        point.draw()

    pygame.display.flip()

    pygame.time.wait(10)

pygame.quit()