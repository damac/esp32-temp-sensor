# esp32-temp-sensor
A simple esp32 project with a bmp280 to update Home Assistant over wifi with a rooms temp. For use as a proxy thermostat.


## Hardware suggestions

This was written for an esp32-s2 mini bust it should work with virtually any esp32 variant.
The sensor board used is a bmp280 by Bosch and accessed over i2c protocol. 

## Preparing your esp32

Hold 0 Down, plug it in, press reset button.

The device should now be visible at /dev/ttyACM0

python3 esptool.py --chip esp32-s2 -p /dev/ttyACM0 -b 460800 --before no_reset erase_flash 

Go to the lolin_s2_mini page, download combined.bin

python3 esptool.py --chip esp32-s2 -p /dev/ttyACM0 -b 460800 --before no_reset write_flash 0x0 /home/USER/Downloads/combined.bin 

I followed this guide https://circuitpython.org/board/lolin_s2_mini/ and that was successful. 

