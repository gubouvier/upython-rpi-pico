# Needs  Neopixel strip on GP15
# Modified from Official Rasp Pi example here:
# https://github.com/micropython/micropython/tree/master/examples/bluetooth
# Tony Goodhew 23 June 2023

import bluetooth
import time
import random
import math
from ble_peripheral import BLESimplePeripheral

from machine import Pin
from neopixel import NeoPixel
strip = NeoPixel(Pin(15), 1)

received_color = (0,0,0)

gammatable = []
for i in range(256):
    x = i / 255
    x = pow(x, 2.5)
    x *= 255
    gammatable.append(int(x))

COLORS = {
    (0, 128, 0), 
    (3, 210, 220),
    (5, 210, 145),
    (5, 210, 220),
    (10, 190, 110),
    (13, 205, 45),
    (30, 70, 120),
    (50, 75, 100),
    (80, 85, 90),
    (100, 50, 60),
    (150, 20, 40),
    (195, 220, 225),
    (245, 15, 140),
    (245, 15, 200),
    (250, 10, 230),
    (253, 5, 235),
    (255, 0, 0),
    (255, 0, 150),
    (255, 192, 203),
    (0, 0, 255),
}


def euclidean_distance(color1, color2):
    return math.sqrt((color1[0] - color2[0]) ** 2 + (color1[1] - color2[1]) ** 2 + (color1[2] - color2[2]) ** 2)


# def find_closest_color(target_color, color_list):
#     closest_color = None
#     min_distance = float('inf')
#     for color in color_list:
#         distance = euclidean_distance(target_color, color)
#         if distance < min_distance:
#             min_distance = distance
#             closest_color = color
#     return closest_color


class Section:
    def __init__(self, id, neopixels, neighbors, strip):
        self.id = id
        self.neighnors = neighbors
        self.neopixels = neopixels
        self.color = (0,0,0)
        self.strip = strip

    def get_neighbors_colors(self):
        colors = {}
        for neighbor in self.neighnors:
            color = neighbor.get_color()
            if color in colors:
                colors[color] += 1
            else:
                colors[color] = 1
        return colors

    def get_color(self):
        return self.color
    
    def set_color(self, color):
        for neopixel in self.neopixels:
            strip[neopixel] = color
        strip.write()
    
    def remove_similar(self, colors, color):
        new_colors = set()
        for c in colors:
            if euclidean_distance(c, color) > 50:
                new_colors.add(c)
        return new_colors

    def pick_random_color(self, color):
        available_colors = self.remove_similar(COLORS, color)
        available_colors.add(color)
        neighbors_colors = self.get_neighbors_colors()
        for color in neighbors_colors:
            available_colors.remove(color)
        if len(available_colors) > 0:
            return random.choice(available_colors)
        else:
            # Pick the least used color from the neighbors
            color = min(neighbors_colors, key=neighbors_colors.get) # type: ignore
    
    def set_ramdom_color(self, color):
        color = self.pick_random_color(color)
        self.set_color(color)


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
        update_color(r, g, b)


def update_color(r, g, b):
     strip.fill((gammatable[r],gammatable[g],gammatable[b]))   
     strip.write()   
     print("Color updated")      
        

def main():    # This part modified to control Neopixel strip
    ble = bluetooth.BLE()
    p = BLESimplePeripheral(ble)
        
    p.on_write(on_rx)

    while(True):
        time.sleep(500)


if __name__ == "__main__":
    main()