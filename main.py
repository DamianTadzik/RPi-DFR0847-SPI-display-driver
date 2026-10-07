import time

import spidev
from gpiozero import OutputDevice


# BCM GPIO numbering
RST_PIN = 23
DC_PIN = 24
BL_PIN = 18


rst = OutputDevice(RST_PIN)
dc = OutputDevice(DC_PIN)
bl = OutputDevice(BL_PIN)

spi = spidev.SpiDev()
spi.open(0, 0)                  # SPI0, CE0 = GPIO8 / physical pin 24
spi.max_speed_hz = 4_000_000    # zaczynamy spokojnie od 4 MHz
spi.mode = 0


def command(cmd, data=None):
    dc.off()
    spi.xfer2([cmd])

    if data:
        dc.on()
        spi.xfer2(list(data))


def reset():
    rst.on()
    time.sleep(0.05)

    rst.off()
    time.sleep(0.05)

    rst.on()
    time.sleep(0.15)


def init_display():
    reset()

    # Software reset
    command(0x01)
    time.sleep(0.15)

    # Sleep out
    command(0x11)
    time.sleep(0.15)

    # 16-bit RGB565
    command(0x3A, [0x05])

    # Memory access control
    command(0x36, [0xC8])

    # Display inversion ON
    command(0x21)

    # Normal display mode
    command(0x13)
    time.sleep(0.01)

    # Display ON
    command(0x29)
    time.sleep(0.1)


def fill_screen(color):
    width = 160
    height = 80

    # ST7735 160x80 panel RAM offset.
    x_offset = 1
    y_offset = 26

    x0 = x_offset
    x1 = x_offset + width - 1
    y0 = y_offset
    y1 = y_offset + height - 1

    # Column address
    command(0x2A, [
        0x00, x0,
        0x00, x1,
    ])

    # Row address
    command(0x2B, [
        0x00, y0,
        0x00, y1,
    ])

    # Memory write
    dc.off()
    spi.xfer2([0x2C])
    dc.on()

    high = (color >> 8) & 0xFF
    low = color & 0xFF

    # Send in chunks so spidev doesn't complain about transfer size.
    pixels_per_chunk = 1024
    chunk = [high, low] * pixels_per_chunk

    pixels_left = width * height

    while pixels_left:
        n = min(pixels_left, pixels_per_chunk)
        spi.xfer2(chunk[:n * 2])
        pixels_left -= n


def main():
    print("Initializing DFR0847...")

    bl.on()
    init_display()

    print("RED")
    fill_screen(0xF800)
    time.sleep(1)

    print("GREEN")
    fill_screen(0x07E0)
    time.sleep(1)

    print("BLUE")
    fill_screen(0x001F)
    time.sleep(1)

    print("WHITE")
    fill_screen(0xFFFF)

    print("Display test finished.")


if __name__ == "__main__":
    try:
        main()
    finally:
        spi.close()
