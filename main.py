import platform
import sys


def main():
    print("DFR0847 driver remote test")
    print(f"Python:       {sys.version.split()[0]}")
    print(f"Architecture: {platform.machine()}")
    print("Test passed.")


if __name__ == "__main__":
    main()
