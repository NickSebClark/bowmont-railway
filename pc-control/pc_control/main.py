"""PC Control app top-level"""

import pygame
import pygame.freetype
from pc_control.layout import Layout
from pc_control.serial_comms import ZeroWaitSerial, read_connection_settings
from datetime import datetime

def main():
    """Basic pygame setup and main event loop."""
    port, baud = read_connection_settings()
    pygame.display.set_caption(f"Bowmont Town Layout PC Control ({port})")

    pygame.init()
    pygame.font.init()

    width = 600
    height = 458

    # Title font
    title_font = pygame.font.Font("pc-control/resources/britrdn_.ttf", 39)
    title_surface = title_font.render("Bowmont Town", True, (255, 255, 255))
    sign_outline = pygame.Rect(width / 2 - title_surface.get_width() / 2 - 10, 5, title_surface.get_width() + 20, 40)
    
    #Serial Monitor Text
    monitor_font = pygame.font.SysFont("Consolas", 12)
    serial_monitor_buffer = ['']*5

    # Set up the display
    screen = pygame.display.set_mode((width, height))
    
    ser = ZeroWaitSerial(port, baud)

    layout = Layout(ser)
    layout_pos = (5, 50)

    image = pygame.image.load("pc-control/resources/sign_small.png")
    roundel = pygame.image.load("pc-control/resources/roundel.png")

    

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
        screen.blit(title_surface, (width / 2 - title_surface.get_width() / 2, 7))
        screen.blit(image, (5, 5))
        screen.blit(roundel, (width - 40 - 5, 5))
        pygame.draw.rect(screen, (255, 255, 255), sign_outline, 2)


        lines = ser.read_available_lines()
        process_lines(lines, layout, serial_monitor_buffer)
        draw_serial_monitor(monitor_font, serial_monitor_buffer, height, screen)

        pygame.display.flip()

        pygame.time.wait(10)

    pygame.quit()

def draw_serial_monitor(font, buffer, top, screen):
    for index, line in enumerate(buffer):
        #draw to the screen
        rendered_line = font.render(line, True, (255, 255, 255))
        v_pos = top-12*(len(buffer)-index)
        screen.blit(rendered_line, (5, v_pos))


def process_lines(new_lines:list[str], layout:Layout, monitor_buffer:list[str]):

    for line in new_lines:
        monitor_buffer.append(f"{datetime.now().strftime('%H:%M:%S')}: {line}")
        monitor_buffer.pop(0)

        match line[0]:
            case 'S':
                if line[1] == '0' or line[1] == '1':
                    try:
                        states = [int(char) for char in line[1:].strip()]
                        states[7] = int(line[7:9], 2) #convert the sidings into a single number
                        #remove the doubles
                        states.pop(8)
                        states.pop(6)
                        states.pop(3)
                        layout.update_points(states)
                    except Exception as e:
                        print(e)
            case '<':
                pass

if __name__ == "__main__":
    main()
