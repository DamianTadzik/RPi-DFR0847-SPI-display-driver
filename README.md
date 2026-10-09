# RPi DFR0847 SPI display driver

## Pinout and connections
TODO

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
