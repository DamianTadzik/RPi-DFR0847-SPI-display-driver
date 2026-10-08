ssh brzeropi@brzeropi.local "cd ~/rpi_dfr0847_spi_display_driver && git pull --ff-only origin main && python3 main.py"; if ($LASTEXITCODE -eq 0) { Write-Host "REMOTE TEST: SUCCESS" } else { Write-Host "REMOTE TEST: FAILED (exit $LASTEXITCODE)" }

192.168.137.43

ssh -t brzeropi@brzeropi.local 'cd ~/rpi_dfr0847_spi_display_driver && git pull --ff-only origin main && python3 demo.py'; if ($LASTEXITCODE -eq 0) { Write-Host "REMOTE TEST: SUCCESS" } else { Write-Host "REMOTE TEST: FAILED (exit $LASTEXITCODE)" }