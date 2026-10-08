import time

from PIL import Image, ImageDraw, ImageFont, ImageOps
import sys, termios, tty, select

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


def custom_fonts_demo(display):
    print("Custom fonts demo")

    font_tests = [
        # Spleen
        ("Spleen 8px",  "fonts/spleen-5x8.ttf", 8),
        ("Spleen 12px", "fonts/spleen-6x12.ttf", 12),
        ("Spleen 16px", "fonts/spleen-8x16.ttf", 16),
        ("Spleen 24px", "fonts/spleen-12x24.ttf", 24),

        # Tamzen
        ("Tamzen 9px",  "fonts/Tamzen5x9r.ttf", 9),
        ("Tamzen 12px", "fonts/Tamzen6x12r.ttf", 12),
        ("Tamzen 16px", "fonts/Tamzen8x16r.ttf", 16),
        ("Tamzen 20px", "fonts/Tamzen10x20r.ttf", 20),

        # Cherry
        ("Cherry 10px", "fonts/cherry-10-r.ttf", 10),
        ("Cherry 12px", "fonts/cherry-12-r.ttf", 12),
        ("Cherry 13px", "fonts/cherry-13-r.ttf", 13),

        # Cozette
        ("Cozette 13px", "fonts/CozetteVector.ttf", 13),

        # ProFont
        ("ProFont 10px", "fonts/ProFont_r400-10.ttf", 10),
        ("ProFont 12px", "fonts/ProFont_r400-12.ttf", 12),
        ("ProFont 15px", "fonts/ProFont_r400-15.ttf", 15),
        ("ProFont 17px", "fonts/ProFont_r400-17.ttf", 17),

        # Gohu
        ("Gohu 11px", "fonts/gohufont-uni-11.ttf", 11),
        ("Gohu 14px", "fonts/gohufont-uni-14.ttf", 14),

        # VecTerminus
        ("Terminus 12px", "fonts/VecTerminus12Medium.otf", 12),
        ("Terminus 14px", "fonts/VecTerminus14Medium.otf", 14),
        ("Terminus 16px", "fonts/VecTerminus16Medium.otf", 16),
        ("Terminus 20px", "fonts/VecTerminus20Medium.otf", 20),

        # Scientifica
        ("Scientifica 10px", "fonts/scientifica.ttf", 10),
        ("Scientifica 12px", "fonts/scientifica.ttf", 12),
        ("Scientifica 14px", "fonts/scientifica.ttf", 14),
        ("Scientifica 16px", "fonts/scientifica.ttf", 16),
    ]
    def _read_key(timeout):
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            r, _, _ = select.select([sys.stdin], [], [], timeout)
            if not r:
                return None
            ch = sys.stdin.read(1)
            if ch == "\x1b":
                seq = sys.stdin.read(2)
                if seq == "[D":
                    return "LEFT"
                if seq == "[C":
                    return "RIGHT"
                return None
            if ch in ("q", "Q"):
                return "QUIT"
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
    duration_per_font = 2.0
    index = 0
    count = len(font_tests)
    while True:
        name, path, size = font_tests[index]
        print(f"[{index+1}/{count}] {name}")
        image = Image.new("RGB", (WIDTH, HEIGHT), "white")
        draw = ImageDraw.Draw(image)
        draw.fontmode = "1"
        try:
            test_font = ImageFont.truetype(path, size)
        except Exception:
            test_font = font(size)
            draw.text((2, 20), "(font load failed)", font=font(10), fill=(255, 0, 0))
        draw.text((2, 2), name, font=font(10), fill=(100, 100, 100))
        draw.text((2, 20), "textTEXT 0123", font=test_font, fill="black")
        draw.text((2, 20 + size + 5), "Il1 O0 5S 8B", font=test_font, fill="black")
        display.show(image)
        remaining = duration_per_font
        last = time.monotonic()
        while remaining > 0:
            key = _read_key(timeout=min(0.1, remaining))
            now = time.monotonic()
            remaining -= now - last
            last = now

            if key == "RIGHT":
                index = (index + 1) % count
                break
            if key == "LEFT":
                index = (index - 1) % count
                break
            if key == "QUIT":
                return
        else:
            index = (index + 1) % count
    # for name, path, size in font_tests:
    #     print(name)
    #     image = Image.new("RGB", (WIDTH, HEIGHT), "white")
    #     draw = ImageDraw.Draw(image)
    #     # Important for pixel fonts:
    #     # disable antialiasing where Pillow supports it.
    #     draw.fontmode = "1"
    #     test_font = ImageFont.truetype(path, size)
    #     # Font name / size using Pillow default font
    #     draw.text(
    #         (2, 2),
    #         name,
    #         font=font(10),
    #         fill=(100, 100, 100),
    #     )
    #     # Main sample
    #     draw.text(
    #         (2, 20),
    #         "textTEXT 0123",
    #         font=test_font,
    #         fill="black",
    #     )
    #     # Characters useful for checking readability
    #     draw.text(
    #         (2, 20 + size + 5),
    #         "Il1 O0 5S 8B",
    #         font=test_font,
    #         fill="black",
    #     )
    #     display.show(image)
    #     time.sleep(2)


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

def image_demo(display):
    print("Image demo")

    path = "media/Bliss_(Windows_XP).png"

    original = Image.open(path).convert("RGB")

    variants = [
        ("resize/stretch", original.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)),
        ("contain", ImageOps.contain(original, (WIDTH, HEIGHT), Image.Resampling.LANCZOS)),
        ("fit", ImageOps.fit(original, (WIDTH, HEIGHT), method=Image.Resampling.LANCZOS)),
    ]

    for name, image in variants:
        print(name)

        # contain() moze zwrocic mniejszy obrazek, wiec wklejamy go na czarne tlo 160x80
        if image.size != (WIDTH, HEIGHT):
            canvas = Image.new("RGB", (WIDTH, HEIGHT), "black")
            x = (WIDTH - image.width) // 2
            y = (HEIGHT - image.height) // 2
            canvas.paste(image, (x, y))
            image = canvas

        display.show(image)
        time.sleep(3)

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


def gif_demo(display, duration=10):
    print("GIF demo")

    gif_paths = [
        "media/popejp2-ezgif.com.gif",
        "media/popeleone-ezgif.com.gif",
    ]

    def load_gif(path):
        frames = []
        durations = []

        with Image.open(path) as gif:
            frame_index = 0

            while True:
                try:
                    gif.seek(frame_index)
                except EOFError:
                    break

                frame = gif.convert("RGB").copy()

                if frame.size != (80, 80):
                    raise ValueError(
                        f"{path}: expected 80x80, got {frame.size}"
                    )

                frames.append(frame)

                frame_duration = gif.info.get("duration", 100) / 1000.0
                frame_duration = max(frame_duration, 0.02)

                durations.append(frame_duration)

                frame_index += 1

        return frames, durations

    frames1, durations1 = load_gif(gif_paths[0])
    frames2, durations2 = load_gif(gif_paths[1])

    print(f"GIF 1: {len(frames1)} frames")
    print(f"GIF 2: {len(frames2)} frames")

    index1 = 0
    index2 = 0

    # Create canvas ONCE
    canvas = Image.new("RGB", (WIDTH, HEIGHT), "black")

    canvas.paste(frames1[index1], (0, 0))
    canvas.paste(frames2[index2], (80, 0))

    display.show(canvas)

    start = time.monotonic()

    next1 = start + durations1[index1]
    next2 = start + durations2[index2]

    while time.monotonic() - start < duration:
        now = time.monotonic()

        changed1 = False
        changed2 = False

        while now >= next1:
            index1 = (index1 + 1) % len(frames1)
            next1 += durations1[index1]
            changed1 = True

        while now >= next2:
            index2 = (index2 + 1) % len(frames2)
            next2 += durations2[index2]
            changed2 = True

        # Update only the side that actually changed
        if changed1:
            canvas.paste(frames1[index1], (0, 0))

        if changed2:
            canvas.paste(frames2[index2], (80, 0))

        if changed1 or changed2:
            display.show(canvas)

        time.sleep(0.001)


def main():
    print("Starting DFR0847 demo")

    with DFR0847() as display:
        color_test(display)
        graphics_demo(display)
        image_demo(display)
        text_demo(display)
        font_size_demo(display)
        custom_fonts_demo(display)
        brightness_demo(display)
        gif_demo(display)
        final_screen(display)

        print("Demo finished successfully")


if __name__ == "__main__":
    main()
