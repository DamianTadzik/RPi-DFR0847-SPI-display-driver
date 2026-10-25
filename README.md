# RPi DFR0847 SPI display driver

## Pinout and connections
Raspberry Pi wiring used by this project:
```
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
```
In order to enable SPI run `sudo raspi-config` then `3 Interface Options` then `I4 SPI` then `sudo reboot`

## Workflow on RPi zero W
Since RPi zero W does not support VScode over SSH, following commands were used for launching python scripts remotely on the device over WiFi SSH and GitHub. WiFi was shared from Win 11, the RPi got 192.168.137.43

Casual one:
```ssh brzeropi@brzeropi.local "cd ~/rpi_dfr0847_spi_display_driver && git pull --ff-only origin main && python3 main.py"; if ($LASTEXITCODE -eq 0) { Write-Host "REMOTE TEST: SUCCESS" } else { Write-Host "REMOTE TEST: FAILED (exit $LASTEXITCODE)" }```

Interactive one: 
```ssh -t brzeropi@brzeropi.local 'cd ~/rpi_dfr0847_spi_display_driver && git pull --ff-only origin main && python3 demo.py'; if ($LASTEXITCODE -eq 0) { Write-Host "REMOTE TEST: SUCCESS" } else { Write-Host "REMOTE TEST: FAILED (exit $LASTEXITCODE)" }```

## Preffered fonts
Few fonts were checked with interactive demo and the most readable ones were:
 - all VecTerminus
 - some Cherry fonts

## To Be Done
 - Brightness pin test, need to wire the pin and verify how the brightness is working
 - Automatic startup via services
 - Few info displays rotation
