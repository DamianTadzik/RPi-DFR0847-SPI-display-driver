import time

from PIL import Image, ImageDraw, ImageFont

from dfr0847 import DFR0847


WIDTH = 160
HEIGHT = 80


def color_test(display):
    print("Color test")

    colors = [
        ("RED", (255, 0, 0)),
        ("GREEN", (0, 255, 0)),
        ("BLUE", (0, 0, 255)),
        ("WHITE", (255, 255, 255)),
        ("BLACK", (0, 0, 0)),
    ]

    for name, color in colors:
        print(name)
        display.fill(color)
        time.sleep(0.5)


def graphics_demo(display):
    print("Graphics demo")

    image = Image.new("RGB", (WIDTH, HEIGHT), "black")
    draw = ImageDraw.Draw(image)

    # Background border
    draw.rectangle(
        (0, 0, WIDTH - 1, HEIGHT - 1),
        outline="white",
    )

    # RGB rectangles
    draw.rectangle((5, 5, 45, 25), fill="red")
    draw.rectangle((60, 5, 100, 25), fill="green")
    draw.rectangle((115, 5, 154, 25), fill="blue")

    # Lines
    draw.line((5, 35, 155, 35), fill="white")
    draw.line((5, 40, 155, 70), fill="yellow")
    draw.line((5, 70, 155, 40), fill="cyan")

    display.show(image)
    time.sleep(2)


def text_demo(display):
    print("Text demo")

    image = Image.new("RGB", (WIDTH, HEIGHT), "black")
    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default()

    draw.text(
        (8, 8),
        "DFRobot DFR0847",
        font=font,
        fill="white",
    )

    draw.text(
        (8, 28),
        "Raspberry Pi Zero W",
        font=font,
        fill="cyan",
    )

    draw.text(
        (8, 48),
        "SPI display works!",
        font=font,
        fill="lime",
    )

    display.show(image)
    time.sleep(3)


def brightness_demo(display):
    print("Backlight PWM test")

    image = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default()

    draw.text(
        (35, 35),
        "PWM BACKLIGHT",
        font=font,
        fill="black",
    )

    display.show(image)

    # Fade down
    for i in range(100, -1, -2):
        display.set_brightness(i / 100)
        time.sleep(0.02)

    # Fade up
    for i in range(0, 101, 2):
        display.set_brightness(i / 100)
        time.sleep(0.02)

    display.set_brightness(1.0)

    time.sleep(1)


def final_screen(display):
    image = Image.new("RGB", (WIDTH, HEIGHT), (10, 10, 20))
    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default()

    draw.rectangle(
        (3, 3, 156, 76),
        outline="cyan",
    )

    draw.text(
        (47, 20),
        "DFR0847",
        font=font,
        fill="white",
    )

    draw.text(
        (42, 40),
        "READY :)",
        font=font,
        fill="lime",
    )

    display.show(image)


def main():
    print("Starting DFR0847 demo")

    with DFR0847() as display:
        color_test(display)
        graphics_demo(display)
        text_demo(display)
        brightness_demo(display)
        final_screen(display)

        print("Demo finished successfully")


if __name__ == "__main__":
    main()
