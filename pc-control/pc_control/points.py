import pygame


class BasicPoint():
    def __init__(self, display, left, top, type="lu", width=50, height=20):
        self.left = left
        self.top = top
        self.display = display
        self.width = width
        self.height = height
        self.fixed_offset = 10
    
        self.hover_colour = (235, 52, 61)
        self.moving_colour = (235, 216, 52)
        self.pos1_colour = (55, 235, 52)
        self.pos2_colour = (52, 140, 235)
        self.boundary_colour = (255,255,255)

        self.line_colour = self.pos1_colour

        self.pos1_vpos = top
        self.pos2_vpos = top+self.height

        match type:
            case "lu":
                self.increment = -1
                self.pos2_vpos = top-self.height
                box_top = top-self.fixed_offset-height
                box_left = left
                self.line_start = (left, top)
                self.line_end = [left+self.width, top]
            case "ld":
                self.increment = 1
                self.pos2_vpos = top+self.height
                box_top = top-self.fixed_offset
                box_left = left
                self.line_start = (left, top)
                self.line_end = [left+self.width, top]
            case "ru":
                self.increment = -1
                self.pos2_vpos = top-self.height
                box_top = top-self.fixed_offset-height
                box_left = left-self.width
                self.line_start = (left, top)
                self.line_end = [left-self.width, top]
            case "rd":
                self.increment = 1
                self.pos2_vpos = top+self.height
                box_top = top-self.fixed_offset
                box_left = left-self.width
                self.line_start = (left, top)
                self.line_end = [left-self.width, top]

        self.rect = pygame.Rect(box_left, box_top, self.width+1, self.height+2*self.fixed_offset)

        # possible states: pos1, pos2, moving_to_pos1, moving_to_pos2
        self.state = "pos1"

    def update_state(self, mouse_pos, mouse_up):
        if self.rect.collidepoint(mouse_pos):
            
            if self.state == "pos1" or self.state == "pos2":
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
        elif self.state == "pos1":
            self.line_colour = self.pos1_colour
        elif self.state == "pos2":
            self.line_colour = self.pos2_colour


    def draw(self):
        #pygame.draw.rect(self.display, (255, 0, 0), self.rect)

        match self.state:
            case "moving_to_pos1":
                self.line_end[1] -= self.increment
                if self.line_end[1] == self.pos1_vpos:
                    self.state = "pos1"
            case "moving_to_pos2":
                self.line_end[1] += self.increment
                if self.line_end[1] == self.pos2_vpos:
                    self.state = "pos2"

        pygame.draw.line(self.display, self.line_colour, self.line_start, self.line_end, 5)
        pygame.draw.rect(self.display, self.boundary_colour, self.rect, 1)
