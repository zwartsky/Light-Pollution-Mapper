
import os
from PIL import Image
from scipy.spatial import distance


# transform rgb color code to hex color code
def rgb_to_hex(color):
    hex = "#"
    n1 = str(int_to_hex(color[0] // 16))
    n2 = str(int_to_hex(((color[0] / 16) - (color[0] // 16)) * 16))
    n3 = str(int_to_hex(color[1] // 16))
    n4 = str(int_to_hex(((color[1] / 16) - (color[1] // 16)) * 16))
    n5 = str(int_to_hex(color[2] // 16))
    n6 = str(int_to_hex(((color[2] / 16) - (color[2] // 16)) * 16))
    return str(hex + n1 + n2 + n3 + n4 + n5 + n6)

# turn decimal to hexadecimal
def int_to_hex(n):
    if n == 10:
        return 'A'
    elif n == 11:
        return 'B'
    elif n == 12:
        return 'C'
    elif n == 13:
        return 'D'
    elif n == 14:
        return 'E'
    elif n == 15:
        return 'F'
    else:
        return int(n)

# get the pollution of a pixel
def pollution(hex_color):
    if hex_color == '#000000': # black - radiance 0 - 0.15
        #print("radiance of 0 - 0.15")
        return 0
    elif hex_color == '#051637': # dark blue - radiance 0.15 - 0.25
        #print("radiance of 0.15 - 0.25")
        return 0.15
    elif hex_color == '#135863': # lighter blue - radiance 0.25 - 0.5
        #print("radiance of 0.25 - 0.5")
        return 0.25
    #else:
        #print("Too polluted")

# find the closest unpolluted point
def closest(node, nodes):
    closest_index = distance.cdist([node], nodes).argmin()
    return nodes[closest_index]

# return pixel of the closest unpolluted point
def find_spot_edge():
    '''
    processing px by px
    starting from the corner
    following the pattern
    123
    456
    789
    '''
    
    im = Image.open('lpm.png')
    pixelmap = im.load()
    sz = im.size
    img_mid = (sz[0] // 2, sz[1] // 2)

    # arrays
    bl = [] # black
    db = [] # dark blue
    lb = [] # light blue
    for i in range(sz[0]):
        for j in range(sz[1]):
            color = pixelmap[i,j]
            hex_color = rgb_to_hex(color)
            pol = pollution(hex_color)
            if pol == 0:
                bl.append((i, j))
            elif pol == 0.15:
                db.append((i, j))
            elif pol == 0.25:
                lb.append((i, j))
            j += 1
        i += 1

    return closest(img_mid, bl), closest(img_mid, db), closest(img_mid, lb)

def find_spot_center():
    '''
    px by px
    starting from the center
    following the pattern
    #2
    513
    #4
    ''' 
    #WIP

# calculate closest spot coordinates
def spot_coords(location, spot, zoom, resolution):
    resolution = resolution.split(",")
    resolution[0] = int(resolution[0])
    resolution[1] = int(resolution[1])
    print(resolution)
    
    inplat = location[1]
    inplng = location[0]
    latpx = spot[0]
    lngpx = spot[1]
    
    if zoom == 10:
        one_pxlat = 0.0006862917
        one_pxlng = 0.0004186759
    elif zoom == 9:
        one_pxlat = 0.0024401389
        one_pxlng = 0.0006847396
    
    spotlat = inplat - (resolution[0] / 2 * one_pxlat) + ((latpx) * one_pxlat)
    spotlng = inplng - (resolution[1] / 2 * one_pxlng) + ((resolution[1] - lngpx) * one_pxlng)
    coords = (spotlng, spotlat)
    
    os.remove('lpm.png')
    return coords