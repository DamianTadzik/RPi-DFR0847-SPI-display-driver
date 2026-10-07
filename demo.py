import time

from PIL import Image, ImageDraw, ImageFont

from dfr0847 import DFR0847


WIDTH = 160
HEIGHT = 80


def font(size):
    """Return Pillow's built-in font at the requested size."""
    return ImageFont.load_default(size=size)


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

    draw.rectangle(
        (0, 0, WIDTH - 1, HEIGHT - 1),
        outline="white",
    )

    draw.rectangle((5, 5, 45, 25), fill="red")
    draw.rectangle((60, 5, 100, 25), fill="green")
    draw.rectangle((115, 5, 154, 25), fill="blue")

    draw.line((5, 35, 155, 35), fill="white")
    draw.line((5, 40, 155, 70), fill="yellow")
    draw.line((5, 70, 155, 40), fill="cyan")

    display.show(image)
    time.sleep(2)


def text_demo(display):
    print("Text demo")

    image = Image.new("RGB", (WIDTH, HEIGHT), "black")
    draw = ImageDraw.Draw(image)

    draw.text(
        (5, 3),
        "DFRobot DFR0847",
        font=font(14),
        fill="white",
    )

    draw.text(
        (5, 28),
        "Raspberry Pi Zero W",
        font=font(12),
        fill="cyan",
    )

    draw.text(
        (5, 51),
        "SPI display works!",
        font=font(14),
        fill="lime",
    )

    display.show(image)
    time.sleep(3)


def font_size_demo(display):
    print("Font size demo")

    pages = [
        [8, 10, 12],
        [14, 18, 24],
    ]

    for sizes in pages:
        image = Image.new("RGB", (WIDTH, HEIGHT), "white")
        draw = ImageDraw.Draw(image)

        y = 1

        for size in sizes:
            current_font = font(size)
            text = f"{size}px textTEXT"

            draw.text(
                (2, y),
                text,
                font=current_font,
                fill="black",
            )

            bbox = draw.textbbox(
                (2, y),
                text,
                font=current_font,
            )

            text_height = bbox[3] - bbox[1]
            y += text_height + 4

        display.show(image)
        time.sleep(3)


def brightness_demo(display):
    print("Backlight PWM test")

    image = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(image)

    draw.text(
        (10, 27),
        "PWM BACKLIGHT",
        font=font(18),
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

    draw.rectangle(
        (3, 3, 156, 76),
        outline="cyan",
    )

    draw.text(
        (42, 13),
        "DFR0847",
        font=font(18),
        fill="white",
    )

    draw.text(
        (37, 42),
        "READY :)",
        font=font(20),
        fill="lime",
    )

    display.show(image)


def main():
    print("Starting DFR0847 demo")

    with DFR0847() as display:
        color_test(display)
        graphics_demo(display)
        text_demo(display)
        font_size_demo(display)
        brightness_demo(display)
        final_screen(display)

        print("Demo finished successfully")


if __name__ == "__main__":
    main()
