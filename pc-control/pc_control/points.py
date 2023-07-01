import pygame


class BasicPoint():
    """
    types:
    left_up
    left_down
    right_up
    right_down
    up_right
    up_left
    down_right
    down_left
    """
    def __init__(self, display, left, top, type="left_up", length=50, throw=20):
        self.left = left
        self.top = top
        self.display = display
        self.length = length
        self.throw = throw
        self.fixed_offset = 10
    
        self.hover_colour = (235, 52, 61)
        self.moving_colour = (235, 216, 52)
        self.ahead_colour = (55, 235, 52)
        self.diverge_colour = (52, 140, 235)
        self.boundary_colour = (255,255,255)

        self.line_colour = self.ahead_colour

        self.line_start = (left, top)

        match type:
            case "left_up":
                self.increment = -1
                box_top = top-self.fixed_offset-throw
                box_left = left
                box_width = self.length+1
                box_height = self.throw+2*self.fixed_offset
                self.line_end = [left+self.length, top]
                self.end_pos_index = 1
                self.ahead_pos = top
                self.diverge_vpos = top-self.throw        
            case "left_down":
                self.increment = 1
                box_top = top-self.fixed_offset
                box_left = left
                box_width = self.length+1
                box_height = self.throw+2*self.fixed_offset
                self.line_end = [left+self.length, top]
                self.end_pos_index = 1
                self.ahead_pos = top
                self.diverge_vpos = top+self.throw
            case "right_up":
                self.increment = -1
                box_top = top-self.fixed_offset-throw
                box_left = left-self.length
                box_width = self.length+1
                box_height = self.throw+2*self.fixed_offset
                self.line_end = [left-self.length, top]
                self.end_pos_index = 1
                self.ahead_pos = top
                self.diverge_vpos = top-self.throw
            case "right_down":
                self.increment = 1
                box_top = top-self.fixed_offset
                box_left = left-self.length
                box_width = self.length+1
                box_height = self.throw+2*self.fixed_offset
                self.line_end = [left-self.length, top]
                self.end_pos_index = 1
                self.ahead_pos = top
                self.diverge_vpos = top+self.throw
            case "up_right":
                self.increment = 1
                box_top = top-self.length
                box_left = left-self.fixed_offset
                box_width = throw+2*self.fixed_offset
                box_height = self.length+1
                self.line_end = [left, top-self.length]
                self.end_pos_index = 0
                self.ahead_pos = left
                self.diverge_vpos = left+self.throw
            case "up_left":
                self.increment = -1
                box_top = top-self.length
                box_left = left-self.throw-self.fixed_offset
                box_width = throw+2*self.fixed_offset
                box_height = self.length+1
                self.line_end = [left, top-self.length]
                self.end_pos_index = 0
                self.ahead_pos = left
                self.diverge_vpos = left-self.throw                
            case "down_right":
                self.increment = 1
                box_top = top
                box_left = left-self.fixed_offset
                box_width = throw+2*self.fixed_offset
                box_height = self.length+1
                self.line_end = [left, top+self.length]
                self.end_pos_index = 0
                self.ahead_pos = left
                self.diverge_vpos = left+self.throw
            case "down_left":
                self.increment = -1
                box_top = top
                box_left = left-self.throw-self.fixed_offset
                box_width = throw+2*self.fixed_offset
                box_height = self.length+1
                self.line_end = [left, top+self.length]
                self.end_pos_index = 0
                self.ahead_pos = left
                self.diverge_vpos = left-self.throw

        self.rect = pygame.Rect(box_left, box_top, box_width, box_height)

        # possible states: pos1, pos2, moving_to_pos1, moving_to_pos2
        self.state = "ahead"

    def update_state(self, mouse_pos, mouse_up):
        if self.rect.collidepoint(mouse_pos):
            
            if self.state == "ahead" or self.state == "diverge":
                self.line_colour = self.hover_colour

            if mouse_up:
                self.line_colour = self.moving_colour
                match self.state:
                    case "ahead":
                        self.state = "moving_to_diverge"
                    case "diverge":
                        self.state = "moving_to_ahead"
                    case "moving_to_ahead":
                        self.state = "moving_to_diverge"
                    case "moving_to_diverge":
                        self.state = "moving_to_ahead"
        elif self.state == "ahead":
            self.line_colour = self.ahead_colour
        elif self.state == "diverge":
            self.line_colour = self.diverge_colour


    def draw(self):
        #pygame.draw.rect(self.display, (255, 0, 0), self.rect)

        match self.state:
            case "moving_to_ahead":
                self.line_end[self.end_pos_index] -= self.increment
                if self.line_end[self.end_pos_index] == self.ahead_pos:
                    self.state = "ahead"
            case "moving_to_diverge":
                self.line_end[self.end_pos_index] += self.increment
                if self.line_end[self.end_pos_index] == self.diverge_vpos:
                    self.state = "diverge"

        pygame.draw.line(self.display, self.line_colour, self.line_start, self.line_end, 5)
        pygame.draw.rect(self.display, self.boundary_colour, self.rect, 1)
