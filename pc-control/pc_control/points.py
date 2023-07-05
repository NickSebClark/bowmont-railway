import pygame
import json

def get_colours():
    with open('settings.json') as settings:
        return json.load(settings)["point_colours"]
    
class Point():

    def __init__(self, display, left, top, length=50, throw=20):
        self.left = left
        self.top = top
        self.display = display
        self.length = length
        self.throw = throw
        self.fixed_offset = 10
        self.thickness = 5
        self.colours = get_colours()

        self.line_colour = self.colours['ahead']

        self.state = "ahead"

        self.rect = pygame.Rect(0,0,0,0)
    
    def update_state(self, mouse_pos, mouse_up):
            if self.rect.collidepoint(mouse_pos):
                
                if self.state == "ahead" or self.state == "diverge":
                    self.line_colour = self.colours['hover']

                if mouse_up:
                    self.line_colour = self.colours['moving']
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
                self.line_colour = self.colours['ahead']
            elif self.state == "diverge":
                self.line_colour = self.colours['diverge']

class StraightPoint(Point):
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

    possible states: ahead, diverge, moving_to_ahead, moving_to_diverge
    """
    def __init__(self, display, left, top, type="left_up", length=50, throw=20):

        super().__init__(display, left, top, length, throw)

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

        pygame.draw.line(self.display, self.line_colour, self.line_start, self.line_end, self.thickness)
        pygame.draw.rect(self.display, self.colours['boundary'], self.rect, 1)

class CrossOver(Point):

    def __init__(self, display, left, top,length=50, throw=20):
        super().__init__(display, left,top, length, throw)

        self.line1_start = [left, top]
        self.line2_start = [left, top+throw]
        self.line1_end = [left+length, top]
        self.line2_end = [left+length, top+throw]

        self.rect = pygame.Rect(left, top-self.fixed_offset, length+1, throw + 2*self.fixed_offset)

    def draw(self):

        match self.state:
            case "moving_to_ahead":
                self.line1_end[1] -= 1
                self.line2_start[1] += 1
                if self.line1_end[1] == self.top:
                    self.state = "ahead"
            case "moving_to_diverge":
                self.line1_end[1] += 1
                self.line2_start[1] -= 1
                if self.line1_end[1] == self.top+self.throw:
                    self.state = "diverge"

        pygame.draw.line(self.display, self.line_colour, self.line1_start, self.line1_end, self.thickness)
        pygame.draw.line(self.display, self.line_colour, self.line2_start, self.line2_end, self.thickness)

        pygame.draw.rect(self.display, self.colours['boundary'], self.rect, 1)
