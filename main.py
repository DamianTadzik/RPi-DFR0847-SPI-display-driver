#!/usr/bin/env python3
"""
Minimal dashboard runner for DFR0847 display.

- Implement or extend `get_data()` to read real values.
- Implement or extend `make_display(data)` to render custom panel.
- Dev mode: `python3 main.py --dev` writes `dev_preview.png`.
- Hardware: `python3 main.py` uses `DFR0847().show(image)`.
"""

import argparse
import time
import subprocess
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont

# Try hardware driver (allowed to fail in dev)
try:
    from dfr0847 import DFR0847
except Exception:
    DFR0847 = None

WIDTH, HEIGHT = 160, 80
# Default VecTerminus family you picked
FONTS = {
    "t12": "fonts/VecTerminus12Medium.otf",
    "t14": "fonts/VecTerminus14Medium.otf",
    "t16": "fonts/VecTerminus16Medium.otf",
}


def safe_truetype(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


# -----------------------
# User-extensible parts
# -----------------------

def get_data(dev=False):
    """
    Return a dict with status values. Example structure:
    {
        "time": "HH:MM:SS",
        "eth": {"present": True, "up": True, "addr": "192.168.1.10"},
        "wlan": {"present": False, "up": False, "addr": None},
        "uptime_s": 12345,
        "cpu_temp_c": 42.1,
        "note": "optional custom text",
        "refresh": 1.0
    }

    In dev mode this returns sensible dummy values. In real mode try to probe system.
    Extend this function to add more probes (internet, services, etc).
    """
    if dev:
        return {
            "time": datetime.now().strftime("%H:%M:%S"),
            "eth": {"present": True, "up": True, "addr": "192.168.0.42"},
            "wlan": {"present": True, "up": False, "addr": None},
            "uptime_s": 3600 * 5 + 23 * 60,
            "cpu_temp_c": 48.3,
            "note": "DEV DUMMY",
            "refresh": 1.0,
        }

    # Real probes (best-effort, failures become None or sensible fallback)
    def _run(cmd):
        try:
            out = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL)
            return out.decode().strip()
        except Exception:
            return ""

    def iface_info(iface):
        info = {"present": False, "up": False, "addr": None}
        link = _run(f"ip link show dev {iface}")
        if not link:
            return info
        info["present"] = True
        info["up"] = ("state UP" in link) or ("UP" in link.split())
        inet = _run(f"ip -4 addr show dev {iface} | grep -oP '(?<=inet\\s)\\d+\\.\\d+\\.\\d+\\.\\d+' || true")
        if inet:
            info["addr"] = inet
        return info

    # uptime
    uptime_s = None
    try:
        with open("/proc/uptime", "r") as f:
            uptime_s = int(float(f.readline().split()[0]))
    except Exception:
        uptime_s = None

    # cpu temp
    cpu_t = None
    try:
        s = open("/sys/class/thermal/thermal_zone0/temp").read().strip()
        cpu_t = int(s) / 1000.0
    except Exception:
        cpu_t = None

    return {
        "time": datetime.now().strftime("%H:%M:%S"),
        "eth": iface_info("eth0"),
        "wlan": iface_info("wlan0"),
        "uptime_s": uptime_s,
        "cpu_temp_c": cpu_t,
        "note": "",
        "refresh": 1.0,
    }


def make_display(data):
    """
    Given `data` (from get_data), return a PIL.Image sized WIDTHxHEIGHT.
    Edit this function to change layout / widgets.
    """
    img = Image.new("RGB", (WIDTH, HEIGHT), "black")
    draw = ImageDraw.Draw(img)

    f_small = safe_truetype(FONTS["t12"], 10)
    f_mid = safe_truetype(FONTS["t14"], 12)
    f_big = safe_truetype(FONTS["t16"], 16)

    # Header (compact)
    draw.rectangle((0, 0, WIDTH - 1, 18), fill=(6, 12, 20))
    draw.text((WIDTH - 60, 1), data.get("time", "--:--:--"), font=f_big, fill="white")

    # Network
    eth = data.get("eth", {})
    wlan = data.get("wlan", {})

    def _status_text(iface):
        if not iface.get("present"):
            return "no hw"
        if iface.get("addr"):
            return iface["addr"]
        return "UP" if iface.get("up") else "down"

    draw.text((4, 22), "ETH:", font=f_mid, fill="white")
    draw.text((42, 22), _status_text(eth), font=f_mid, fill="lime" if eth.get("up") else "red")

    draw.text((4, 36), "WLAN:", font=f_mid, fill="white")
    draw.text((42, 36), _status_text(wlan), font=f_mid, fill="lime" if wlan.get("up") else "red")

    # System
    up = data.get("uptime_s")
    if up is not None:
        h = up // 3600
        m = (up % 3600) // 60
        draw.text((4, 50), f"Uptime: {h}h{m}m", font=f_mid, fill="white")
    else:
        draw.text((4, 50), "Uptime: n/a", font=f_mid, fill="white")

    cpu = data.get("cpu_temp_c")
    if cpu is not None:
        draw.text((4, 62), f"CPU: {cpu:.1f}C", font=f_mid, fill="white")
    else:
        draw.text((4, 62), "CPU: n/a", font=f_mid, fill="white")

    note = data.get("note", "")
    if note:
        draw.text((80, 36), note[:26], font=f_mid, fill="yellow")

    draw.rectangle((0, 0, WIDTH - 1, HEIGHT - 1), outline=(30, 60, 80))
    return img


# -----------------------
# Runner
# -----------------------

def run_loop(dev=False):
    if dev:
        print("Running in dev mode (writes dev_preview.png)")
    else:
        if DFR0847 is None:
            print("DFR0847 driver not available, falling back to dev mode")
            dev = True

    try:
        if dev:
            while True:
                data = get_data(dev=True)
                img = make_display(data)
                img.save("dev_preview.png")
                time.sleep(max(0.1, data.get("refresh", 1.0)))
        else:
            with DFR0847() as display:
                while True:
                    data = get_data(dev=False)
                    img = make_display(data)
                    display.show(img)
                    time.sleep(max(0.1, data.get("refresh", 1.0)))
    except KeyboardInterrupt:
        print("Stopped by user")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dev", action="store_true", help="use dummy values and save dev_preview.png")
    args = parser.parse_args()
    run_loop(dev=args.dev)
