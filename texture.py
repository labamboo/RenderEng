# classes for handling Textures, both procedurally generated ones and custom texture maps
import numpy as np
from math import pi
from math import sin

# base Texture class, returns a solid color for all uv coordinates
class Texture:

    # constructor
    def __init__(self, color):
        self.color = color

    # basic color function: returns constant color
    def colorAtUV(self, u, v):
        return self.color
    
# checkerboard texture:
# implements checkerboard with sine function
class Checkerboard(Texture):

    #constructor
    def __init__(self, color1, color2, usquares, vsquares):
        self.color1 = color1
        self.color2 = color2
        self.ufreq = pi * (usquares)
        self.vfreq = pi * (vsquares)

    # color function: returns color1 or color2 depending
    # on location
    def colorAtUV(self, u, v):
        # compute sines
        sinu = sin(u * self.ufreq)
        sinv = sin(v * self.vfreq)
        if (sinu > 0.0):
            if (sinv > 0.0):
                return self.color1
            return self.color2
        if (sinv > 0.0):
            return self.color2
        return self.color1



