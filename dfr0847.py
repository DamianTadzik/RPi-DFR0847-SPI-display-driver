import time

import spidev
from gpiozero import OutputDevice, PWMOutputDevice
from PIL import Image


class DFR0847:
    """Minimal driver for the DFRobot DFR0847 160x80 SPI TFT.

    Raspberry Pi wiring used by this project:

        DFR0847    Raspberry Pi
        ------------------------------
        +          3.3 V   pin 17
        -          GND     pin 25
        CK         GPIO11  pin 23  SPI0 SCLK
        SI         GPIO10  pin 19  SPI0 MOSI
        CS         GPIO8   pin 24  SPI0 CE0
        RT         GPIO23  pin 16
        DC         GPIO24  pin 18
        BL         GPIO18  pin 12  PWM0
    """

    WIDTH = 160
    HEIGHT = 80

    def __init__(
        self,
        spi_bus=0,
        spi_device=0,
        rst_pin=23,
        dc_pin=24,
        bl_pin=18,
        spi_speed_hz=16_000_000,
    ):
        self.rst = OutputDevice(rst_pin)
        self.dc = OutputDevice(dc_pin)

        self.bl = PWMOutputDevice(
            bl_pin,
            frequency=1000,
            initial_value=0.0,
        )

        self.spi = spidev.SpiDev()
        self.spi.open(spi_bus, spi_device)
        self.spi.max_speed_hz = spi_speed_hz
        self.spi.mode = 0

        self._init_display()

    # ------------------------------------------------------------------
    # Low-level communication
    # ------------------------------------------------------------------

    def _command(self, command, data=None):
        self.dc.off()
        self.spi.xfer2([command])

        if data is not None:
            self.dc.on()
            self.spi.xfer2(list(data))

    def _reset(self):
        self.rst.on()
        time.sleep(0.05)

        self.rst.off()
        time.sleep(0.05)

        self.rst.on()
        time.sleep(0.15)

    # ------------------------------------------------------------------
    # Display initialization
    # ------------------------------------------------------------------

    def _init_display(self):
        self._reset()

        # Software reset
        self._command(0x01)
        time.sleep(0.15)

        # Sleep out
        self._command(0x11)
        time.sleep(0.15)

        # 16-bit RGB565
        self._command(0x3A, [0x05])

        # Memory access control:
        # landscape orientation + BGR
        self._command(0x36, [0xA8])

        # Display inversion OFF
        self._command(0x20)

        # Normal display mode
        self._command(0x13)
        time.sleep(0.01)

        # Display ON
        self._command(0x29)
        time.sleep(0.1)

        self.set_brightness(1.0)

    # ------------------------------------------------------------------
    # Addressing
    # ------------------------------------------------------------------

    def _set_window(self, x0, y0, x1, y1):
        # In landscape mode the original 24-pixel column offset
        # becomes the Y offset.
        x_offset = 0
        y_offset = 24

        x0 += x_offset
        x1 += x_offset
        y0 += y_offset
        y1 += y_offset

        # CASET - Column Address Set
        self._command(
            0x2A,
            [
                (x0 >> 8) & 0xFF,
                x0 & 0xFF,
                (x1 >> 8) & 0xFF,
                x1 & 0xFF,
            ],
        )

        # RASET - Row Address Set
        self._command(
            0x2B,
            [
                (y0 >> 8) & 0xFF,
                y0 & 0xFF,
                (y1 >> 8) & 0xFF,
                y1 & 0xFF,
            ],
        )

        # RAMWR - Memory Write
        self.dc.off()
        self.spi.xfer2([0x2C])
        self.dc.on()

    def _write_data(self, data):
        # Linux SPI transfers have a size limit.
        # Keep individual transactions comfortably below it.
        chunk_size = 4096

        for offset in range(0, len(data), chunk_size):
            self.spi.xfer2(list(data[offset:offset + chunk_size]))

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def set_brightness(self, brightness):
        """Set backlight brightness from 0.0 to 1.0."""
        brightness = max(0.0, min(1.0, float(brightness)))
        self.bl.value = brightness

    def fill(self, color):
        """Fill the entire display.

        color is an RGB tuple, for example:
            (255, 0, 0)
        """
        r, g, b = color

        rgb565 = (
            ((r & 0xF8) << 8)
            | ((g & 0xFC) << 3)
            | (b >> 3)
        )

        high = (rgb565 >> 8) & 0xFF
        low = rgb565 & 0xFF

        self._set_window(
            0,
            0,
            self.WIDTH - 1,
            self.HEIGHT - 1,
        )

        pixels = self.WIDTH * self.HEIGHT
        data = bytes([high, low]) * pixels

        self._write_data(data)

    def show(self, image):
        """Display a Pillow image.

        The image is converted to RGB and resized to 160x80 if necessary.
        """
        if image.size != (self.WIDTH, self.HEIGHT):
            image = image.resize((self.WIDTH, self.HEIGHT))

        image = image.convert("RGB")

        raw = image.tobytes()

        # RGB888 -> RGB565
        framebuffer = bytearray(self.WIDTH * self.HEIGHT * 2)

        j = 0

        for i in range(0, len(raw), 3):
            r = raw[i]
            g = raw[i + 1]
            b = raw[i + 2]

            rgb565 = (
                ((r & 0xF8) << 8)
                | ((g & 0xFC) << 3)
                | (b >> 3)
            )

            framebuffer[j] = (rgb565 >> 8) & 0xFF
            framebuffer[j + 1] = rgb565 & 0xFF

            j += 2

        self._set_window(
            0,
            0,
            self.WIDTH - 1,
            self.HEIGHT - 1,
        )

        self._write_data(framebuffer)

    def clear(self):
        self.fill((0, 0, 0))

    def close(self):
        self.spi.close()
        self.bl.close()
        self.dc.close()
        self.rst.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
