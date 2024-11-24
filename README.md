# upython-rpi-pico
Several micropython projects for RPI Pico W

# Libraries
## my_BLE
Coded from several existing BLE examples (ble_advertising.py)

Added a wrapper to simplify Central / Peripheral

## my_TCS34725
Micropython rewrite of the Adafruit Arduino C library for the TCS34725 color sensor.
Existing micropython libs did not support the Flora version (unable to trigger interrupt)

## Neopixel
Vanilla version of the Adafruit Neopixel library

# Projects
## Robe-noel-MBA-2024
BLE Central / Peripheral project.

### Central
The central uses
- RPI Pico W 
- Flora TCS34725
- 2X Neopixel (Status and Fiber)

The central connects to the peripheral and sends the RGB color detected from the TCS34725

### Peripheral
The peripheral uses
- RPI Pico W
- Multiple Neopixels

The peripheral receives the RGB color from the central and sends it to the Neopixels (from a pattern)