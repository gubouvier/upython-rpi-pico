# Robe-Noel-MBA-2024
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