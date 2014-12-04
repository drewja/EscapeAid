RESET = '\033[0m'
FSTRING = '\x1b[{}m'
CODE_MAP = dict(
    bold = 1,
    underscore = 4,
    blink = 5,
    reverse = 7,
    concealed = 8,
    scored = 9,
    black = 16,
    red = 9,
    green = 10,
    orange = 202,
    yellow = 11,
    blue = 12,
    magenta = 13,
    purple = 129,
    pink = 206,
    cyan = 14,
    gold = 178,
    brown = 94,
    grey = 7,
    white = 15,
    c256 = 38)
PALLET_256 ={
    'purple': [5, 53, 54, 55, 56, 90, 91, 92, 93, 96, 97, 98, 99, 126, 127, 128,
               129, 132, 133, 134, 135, 139, 140, 141, 146, 147, 165, 170, 171,
               175, 176, 177, 182, 183, 189, 206],
               
    'gold': [178, 179, 220, 221, 222],
    
    'orange': [3, 130, 166, 172, 173, 202, 208, 209, 214, 215],
    
    'blue': [4, 12, 14, 17, 18, 19, 20, 21, 24, 25, 26, 27, 31, 32, 33, 38, 39,
             45, 51, 57, 57, 60, 60, 61, 61, 62, 63, 63, 66, 67, 68, 68, 69, 69,
             74, 75, 81, 87, 103, 104, 105, 109, 110, 111, 111, 117, 123, 153,
             159, 195],
             
    'yellow': [11, 142, 143, 144, 184, 185, 186, 187, 226, 227, 228, 229, 230],
    
    'red': [1, 9, 52, 88, 89, 124, 160, 167, 174, 181, 196, 197, 203],
    
    'grey': [7, 8, 15, 145, 152, 188, 233, 234, 235, 236, 237, 238, 239, 240,
             241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253,
             254, 255],
             
    'pink': [13, 13, 89, 125, 126, 161, 162, 163, 164, 168, 169, 198, 199, 200,
             201, 204, 205, 206, 207, 210, 211, 212, 213, 217, 218, 219, 224,
             225],
             
    'brown': [58, 59, 94, 95, 100, 101, 102, 131, 136, 137, 138, 180, 216, 223],
    
    'green': [2, 6, 6, 10, 22, 23, 28, 29, 30, 34, 35, 36, 37, 40, 41, 42, 43,
              44, 46, 47, 48, 49, 50, 64, 65, 70, 71, 72, 73, 76, 77, 78, 79,
              80, 82, 83, 84, 85, 86, 106, 107, 108, 112, 113, 114, 115, 116,
              118, 119, 120, 121, 122, 148, 149, 150, 151, 154, 155, 156, 157,
              158, 190, 191, 192, 193, 194]
    }
STANDARD_COLORS = [
    'red',
    'orange',
    'yellow',
    'green',
    'blue',
    'purple',
    'magenta',
    'pink',
    'cyan',
    'grey',
    'white',
    'gold',
    'brown']
COLORS_256 = list(range(256))
COLOR_GROUP_256 = ['grey', 'pink','red','purple','blue','green',
                   'yellow','orange','gold','brown']