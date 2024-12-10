# TODO : Change neopixel number to start with 0 and currently the last one is the fist one

SECTION_MAP_ROBE = [
    ## Start Robe
    {
        'id': 1,
        'neighbors': [2, 3, 4, 14, 13],
        'neopixels': [1],
        'description': ""
    },
    {
        'id': 2,
        'neighbors': [1, 4, 13],
        'neopixels': [2],
        'description': ""
    },
    {
        'id': 3,
        'neighbors': [1, 4, 5],
        'neopixels': [3],
        'description': ""
    },
    {
        'id': 4,
        'neighbors': [1, 2, 3, 5, 6],
        'neopixels': [5],
        'description': ""
    },
    {
        'id': 5,
        'neighbors': [3, 4, 6, 7], #
        'neopixels': [5],
        'description': ""
    },
    {
        'id': 6,
        'neighbors': [4, 5, 7, 8],
        'neopixels': [6],
        'description': ""
    },
    {
        'id': 7,
        'neighbors': [5, 6, 8, 9, 11],
        'neopixels': [7],
        'description': ""
    },
    {
        'id': 8,
        'neighbors': [6, 7, 11],
        'neopixels': [8],
        'description': ""
    },
    { 
        'id': 9,
        'neighbors': [7, 11, 10, 15],
        'neopixels': [9],
        'description': ""
    },
    {
        'id': 10,
        'neighbors': [9, 11, 15, 12],
        'neopixels': [10],
        'description': ""
    },
    {
        'id': 11,
        'neighbors': [7, 8, 9, 10],
        'neopixels': [11],
        'description': ""
    },
    {
        'id': 12,
        'neighbors': [10, 15, 13, 14],
        'neopixels': [12],
        'description': ""
    },
    {
        'id': 13,
        'neighbors': [12, 14, 1, 2],
        'neopixels': [13],
        'description': ""
    },
    {
        'id': 14,
        'neighbors': [15, 12, 13, 1],
        'neopixels': [14],
        'description': ""
    },
    {
        'id': 15,
        'neighbors': [],
        'neopixels': [15],
        'description': ""
    },
]

SECTION_MAP_TUNIQUE = [
    ## Start Tunique
    {
        'id': 0,
        'neighbors': [8, 3],
        'neopixels': [0],
        'description': ""
    },
    {
        'id': 1,
        'neighbors': [3, 2],
        'neopixels': [1, 3],
        'description': "Tunique "
    },
    {
        'id': 2,
        'neighbors': [1, 4, 5],
        'neopixels': [2, 4],
        'description': ""
    },
    {
        'id': 3,
        'neighbors': [1, 0, 5],
        'neopixels': [5],
        'description': ""
    },
    {
        'id': 4,
        'neighbors': [2, 5],
        'neopixels': [6],
        'description': ""
    },
    {
        'id': 5,
        'neighbors': [2, 4, 3],
        'neopixels': [7],
        'description': ""
    },
    {
        'id': 6,
        'neighbors': [0, 5, 7],
        'neopixels': [8],
        'description': ""
    },
    {
        'id': 7,
        'neighbors': [6, 13, 12, 8],
        'neopixels': [9],
        'description': ""
    },
    {
        'id': 8,
        'neighbors': [7, 13, 9],
        'neopixels': [10],
        'description': ""
    },
    {
        'id': 9,
        'neighbors': [8, 10],
        'neopixels': [11],
        'description': ""
    },
    {
        'id': 10,
        'neighbors': [9, 11],
        'neopixels': [12],
        'description': ""
    },
    {
        'id': 11,
        'neighbors': [8, 10, 12],
        'neopixels': [13],
        'description': ""
    },
     {
         'id': 12,
         'neighbors': [11, 7, 13],
         'neopixels': [14],
         'description': ""
     },
     {
         'id': 13,
         'neighbors': [12, 7],
         'neopixels': [15],
         'description': ""
     },
]
