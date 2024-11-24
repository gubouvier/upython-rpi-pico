import time
import bluetooth
import lib.my_TCS34725 as my_TCS34725
import lib.ble_central as ble_central

from machine import Pin, I2C
from neopixel import NeoPixel

status_pixel = NeoPixel(Pin(2), 1, bpp=3)

WAIT_FOR_RESPONSE = False
TCS_READ_TIME_MS = 1000
STATUS_PIXEL = 6
STATUS_INTENSITY = 15
FIBER_PIXEL = 7
BUTTON_TCS = 14

i2c = I2C(0, scl=Pin(5), sda=Pin(4))

tcs = my_TCS34725.Adafruit_TCS34725(i2c)
ble = bluetooth.BLE()
central = ble_central.BLESimpleCentral(ble)
status_pixel = NeoPixel(Pin(STATUS_PIXEL), 1)
fiber_pixel = NeoPixel(Pin(FIBER_PIXEL), 1)
button_tcs = Pin(BUTTON_TCS, Pin.IN, Pin.PULL_UP)


device_not_found = False

fiber_colors = (0, 0, 0)

button_last_pressed_time = 0

def on_scan(addr_type, addr, name):
    if addr_type is not None:
        print("Found peripheral:", addr_type, addr, name)
        central.connect()
    else:
        device_not_found = True
        print("No peripheral found.")


def button_tcs_pressed(pin):
    global button_last_pressed_time
    global fiber_colors
    current_time = time.ticks_ms()
    if (current_time - button_last_pressed_time) > 500:
        print("Button pressed!")
        fiber_colors = increase_brightness(get_rgb())
        fiber_pixel.fill(fiber_colors)
        fiber_pixel.write()

        print("Color:", fiber_colors)
    else:
        print("Bounce Detected!")

    
def connect_to_peripheral():
    device_not_found = False
    central.scan(callback=on_scan)
    while not central.is_connected():
        if device_not_found:
            return False
        else:
            time.sleep_ms(100)

    return True


def start_tcs():
    if not tcs.begin():
        print("No TCS34725 found!")
        return False
    else:
        tcs.setInterrupt(True)
        return True


def get_rgb():
    tcs.setInterrupt(False)
    time.sleep_ms(TCS_READ_TIME_MS)
    red, green, blue = tcs.getRGB()
    tcs.setInterrupt(True)

    return int(red), int(green), int(blue)


def increase_brightness(colors):
    max_value = max(colors)

    return tuple([int((255 / max_value) * color) for color in colors])


def update_status(status):
    if status == "red":
        status_pixel.fill((STATUS_INTENSITY, 0, 0))
    elif status == "green":
        status_pixel.fill((0,STATUS_INTENSITY,0))
    elif status == "blue":
        status_pixel.fill((0,0,STATUS_INTENSITY))
    elif status == "off":
        status_pixel.fill((0,0,0))

    status_pixel.write()


def before_exit():
    print("Cleaning up...")
    print("Disconnecting TCS34725...")
    tcs.setInterrupt(True)
    print("Closing remote leds...")
    message = f"0,0,0"
    print("TX:", message)
    central.write(message, WAIT_FOR_RESPONSE)
    time.sleep(1)
    print("Disconnecting from preripheral...")
    central.disconnect()
    print("Fiber pixel turned off...")
    fiber_pixel.fill((0,0,0))
    fiber_pixel.write()
    print("Status pixel updated...")
    update_status('red')
    print("Exiting...")


def main():
    # Initial setup
    if not start_tcs():
        return

    # Cleat status and fiber pixels
    update_status("off")
    fiber_pixel.fill((0,0,0))
    fiber_pixel.write()

    # Set interrupt pin
    button_tcs.irq(trigger=Pin.IRQ_RISING, handler=button_tcs_pressed)

    while(True):
        # Connect to peripheral
        update_status("blue")
        print("Connecting...")
        if not connect_to_peripheral():
            print("No peripheral found.")
            return
        else:
            print("Connected to peripheral")
            update_status("green")

        while central.is_connected():
            try:
                message = f"{fiber_colors[0]},{fiber_colors[1]},{fiber_colors[2]}"

                print("TX:", message)
                central.write(message, WAIT_FOR_RESPONSE)
            except Exception as e:
                print("TX failed :")
                print(e)

            time.sleep_ms(1000)

        print("Disconnected from peripheral.")
        update_status("red")
        time.sleep_ms(500)


if __name__ == '__main__':
    try:
        main()
    finally:
        before_exit()
