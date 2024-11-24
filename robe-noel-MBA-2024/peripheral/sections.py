import math
import random
from neopixel import NeoPixel

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

class Section:
    def __init__(self, id: int, neopixels: list[int], strip: NeoPixel,  neighbors: list = []):
        self.id = id
        self.neighnors: list[Section] = neighbors
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
            self.strip[neopixel] = color
        self.strip.write()
    
    def remove_similar(self, colors, color):
        new_colors = set()
        for c in colors:
            if euclidean_distance(c, color) > 50:
                new_colors.add(c)
            else:
                print(f"Removed {c}")
        return new_colors

    def pick_random_color(self, color):
        available_colors = self.remove_similar(COLORS, color)
        available_colors.add(color)
        neighbors_colors = self.get_neighbors_colors()
        for neighbor_color in neighbors_colors:
            if neighbor_color != (0,0,0):
                available_colors.remove(neighbor_color)
        if len(available_colors) > 0:
            return random.choice(list(available_colors))
        else:
            # Pick the least used color from the neighbors
            color = min(neighbors_colors, key=neighbors_colors.get) # type: ignore
    
    def set_ramdom_color(self, color):
        color = self.pick_random_color(color)
        self.set_color(color)


class SectionMap:
    def __init__(self):
        self.sections: list[Section] = []

    def load_sections(self, section_map_data: list, strip: NeoPixel):
        for section_data in section_map_data:
            section = Section(
                id=section_data['id'],
                neopixels=section_data['neopixels'],
                strip=strip
            )
            self.sections.append(section)
        
        for section_data in section_map_data:
            section = self.get_section(section_data['id'])
            for neighbor_id in section_data['neighbors']:
                section.neighnors.append(self.get_section(neighbor_id))
                

    def get_random_color(self):
        return random.choice(COLORS)
    
    def fill(self, color):
        for section in self.sections:
            section.set_color(color)

    def get_section(self, id):
        return [section for section in self.sections if section.id == id][0]
    
    def get_random_order(self) -> list[Section]:
        old_order = self.sections.copy()[1:] # The first section should never change
        new_order = []
        for _ in range(len(old_order)):
            section = random.choice(old_order)
            new_order.append(section)
            old_order.remove(section)
        return new_order
    

