import bluetooth
import time
import random
from lib.ble_peripheral import BLESimplePeripheral

from machine import Pin
from neopixel import NeoPixel
from sections import Section, SectionMap
from section_map import SECTION_MAP_ROBE, SECTION_MAP_TUNIQUE

STRIP_LEN = 20
strip_robe = NeoPixel(Pin(15), STRIP_LEN)
strip_robe.fill((0,0,255))
strip_robe.write()

strip_tunique = NeoPixel(Pin(14), STRIP_LEN)
strip_tunique.fill((0,0,255))
strip_tunique.write()


section_map_robe = SectionMap()
section_map_robe.load_sections(SECTION_MAP_ROBE, strip_robe)

section_map_tunique = SectionMap()
section_map_tunique.load_sections(SECTION_MAP_TUNIQUE, strip_tunique)

received_color = (0,0,0)
strip_color = (0,0,0)

gammatable = []
for i in range(256):
    x = i / 255
    x = pow(x, 2.5)
    x *= 255
    gammatable.append(int(x))


def cleanup():
    strip_robe.fill((0,0,0))
    strip_robe.write()
    strip_tunique.fill((0,0,0))
    strip_tunique.write()


def on_rx(v):  # v is what has been received
        ss = str(v)     
        l = len(ss)
        ss = ss[2:l-1]    
        p = ss.find(",")  
        r = int(ss[0:p])  
        ss = ss[p+1:]     
        p = ss.find(",")  
        g = int(ss[0:p])  
        b = int(ss[p+1:]) 
        print(r,g,b)
        global strip_color
        global received_color
        received_color = (r,g,b)
        if received_color != strip_color:
            strip_color = received_color
            update_color(received_color)


def update_color(color):
    color = (gammatable[color[0]],gammatable[color[1]],gammatable[color[2]])
    print("Update Color:",color)

    # Shutdown all the sections
    section_map_robe.fill((0,0,0))
    section_map_tunique.fill((0,0,0))
          
    time.sleep(1)

    first_section = section_map_robe.sections[0]
    first_section.set_color(color)   
    time.sleep(1)
 
    for section in section_map_robe.get_random_order():
        section.set_ramdom_color(color) 
        time.sleep(.5)
    
    for section in section_map_tunique.get_random_order():
        section.set_ramdom_color(color) 
        time.sleep(.5)


def main():
    ble = bluetooth.BLE()
    p = BLESimplePeripheral(ble)
        
    p.on_write(on_rx)

    while(True):
        time.sleep(500)


if __name__ == "__main__":
    try:
        main()
    finally:
        cleanup()
