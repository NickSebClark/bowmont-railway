"""PC Control app top-level"""

from pathlib import Path
import sys
import pygame
import pygame.freetype

from pc_control.layout import Layout
from pc_control.serial_comms import ZeroWaitSerial, read_connection_settings, DummySerial
from datetime import datetime
from pygame_widgets.button import Button
import pygame_widgets
from serial import SerialException

resources = Path(__file__).parent / "resources"


def main():
    """Basic pygame setup and main event loop."""
    port, baud = read_connection_settings()
    pygame.display.set_caption(f"Bowmont Town Layout PC Control ({port})")

    pygame.init()
    pygame.font.init()

    width = 1280
    height = 800

    # Title font
    title_font = pygame.font.Font(resources / "britrdn_.ttf", 39)
    title_surface = title_font.render("Bowmont Town", True, (255, 255, 255))
    sign_outline = pygame.Rect(width / 2 - title_surface.get_width() / 2 - 10, 5, title_surface.get_width() + 20, 40)

    # Serial Monitor Text
    monitor_font = pygame.font.SysFont("Consolas", 12)
    serial_monitor_buffer = [""] * 5

    # Set up the display
    # full screen if linux, windowed if windows
    if sys.platform == "linux":
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((width, height))

    # Connect the serial
    try:
        ser = ZeroWaitSerial(port, baud)
        connected = True
    except SerialException as e:
        connected = False
        connnection_message = title_font.render("NOT CONNECTED", True, (255, 0, 0))
        ser = DummySerial()
        print("Unable to start Serial" + str(e))

    layout = Layout(ser)
    layout_pos = (5, 50)

    image = pygame.image.load(resources / "sign_small.png")
    roundel = pygame.image.load(resources / "roundel.png")
    roundel_rect = roundel.get_rect(topleft=(width - 40 - 5, 5))

    # sync button
    Button(
        screen,
        width - 55,
        height - 35,
        50,
        30,
        fontSize=25,
        text="SYNC",
        inactiveColour=(200, 50, 0),
        hoverColour=(150, 0, 0),
        pressedColour=(0, 200, 20),
        textColor=(100, 100, 100),
        radius=8,
        onClick=lambda: request_sync(ser),
    )

    running = True

    while running:
        mouse_up = False

        events = pygame.event.get()

        # Handle events
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_up = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if roundel_rect.collidepoint(event.pos):
                    running = False

        mouse_pos = pygame.mouse.get_pos()

        screen.fill((0, 0, 0))

        pygame_widgets.update(events)

        # Draw the layout with the mouse position relative to the layout pos.
        layout.draw(((mouse_pos[0] - layout_pos[0])/2, (mouse_pos[1] - layout_pos[1])/2), mouse_up)

        # Blit the layout and text
        scaled_layout = pygame.transform.scale2x(layout)
        screen.blit(scaled_layout, layout_pos)
        screen.blit(title_surface, (width / 2 - title_surface.get_width() / 2, 7))
        screen.blit(image, (5, 5))
        screen.blit(roundel, roundel_rect)
        pygame.draw.rect(screen, (255, 255, 255), sign_outline, 2)

        if not connected:
            screen.blit(connnection_message, (width / 2 - connnection_message.get_width() / 2, height - 50))

        lines = ser.read_available_lines()

        process_lines(lines, layout, serial_monitor_buffer)
        draw_serial_monitor(monitor_font, serial_monitor_buffer, height, screen)

        pygame.display.flip()

        pygame.time.wait(10)

    pygame.quit()


def request_sync(ser: ZeroWaitSerial):
    print("request sync")
    ser.write(str.encode("r\n"))


def draw_serial_monitor(font, buffer, top, screen):
    for index, line in enumerate(buffer):
        # draw to the screen
        try:
            rendered_line = font.render(line, True, (255, 255, 255))
            v_pos = top - 12 * (len(buffer) - index)
            screen.blit(rendered_line, (5, v_pos))
        except ValueError:
            print("Unable to display " + line)


def process_lines(new_lines: list[str], layout: Layout, monitor_buffer: list[str]):
    for line in new_lines:
        monitor_buffer.append(f"{datetime.now().strftime('%H:%M:%S')}: {line}")
        monitor_buffer.pop(0)

        # any empty line, let's skip
        if len(line) == 0:
            continue

        match line[0]:
            case "S":
                if line[1] == "0" or line[1] == "1":
                    try:
                        states = [int(char) for char in line[1:].strip()]
                        states[7] = int(line[7:9], 2)  # convert the sidings into a single number
                        # remove the doubles
                        states.pop(8)
                        states.pop(6)
                        states.pop(3)
                        layout.update_points(states)
                    except Exception as e:
                        print(e)
            case "<":
                pass
            case _:
                pass


if __name__ == "__main__":
    main()
