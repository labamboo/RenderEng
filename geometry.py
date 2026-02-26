# Geometry library version 0.3
# implements homogeneous coordinates
# coordinates are of the form [x y z w]
# the 3d homogeneous coordinate w will be limited to 0 or 1,
# to distinguish between points and vectors, and allow for
# affine transformations in matrix form

import numpy as np

class Coordinate3D:
    # initialization
    def __init__(self, vector):
        assert type(vector) == np.ndarray, "vector must be a formatted np array"
        assert vector.shape == (4,1), "vector must have shape (4,1)"
        assert vector[3,0] == 1 or vector[3,0] == 0, "w coordinate must be 0 or 1"
        self.vec = vector

    # from 3d tuple
    def from_3tuple(self,tuple, vector = False):
        assert len(tuple) == 3, "tuple must be length 3"
        if (vector):
            return Coordinate3D.from_coordinates(tuple[0],tuple[1],tuple[2],0)
        else:
            return Coordinate3D.from_coordinates(tuple[0],tuple[1],tuple[2],1)
        
    # from np vector
    def from_coordinates(x, y, z, w):
        return Coordinate3D(np.array([x,y,z,w]).reshape(4,1))
        
    # addition
    def add(self, other):
        assert type(other) == Coordinate3D
        assert self.vec[3,0] + other.vec[3,0] < 2, "cannot add two points"
        return Coordinate3D(self.vec + other.vec)
    
    # subtraction
    def subtract(self, other):
        assert type(other) == Coordinate3D
        assert self.vec[3,0] - other.vec[3,0] > -1, "cannot subtract point from a vector"
        return Coordinate3D(self.vec - other.vec)
    
    # whether object is a point
    def ispoint(self):
        return self.vec[3,0] == 1
    
    # whether point is within z bounds specified
    def withinzbounds(self, zlow, zhigh):
        assert self.ispoint(), "coordinate cannot be a vector"
        assert zlow < zhigh, "zlow must be below zhigh"
        vec = self.vec.tolist()
        if (vec[2] < zlow or vec[2] > zhigh):
            return False
        return True
    
    # return normalized 2d projection point as nparray
    def projnorm(self):
        assert self.ispoint(), "vectors cannot be projected"
        vec = self.vec.tolist()
        return np.array([vec[0] / vec[2], vec[1] / vec[2]])
    
class Transform3D:
    def __init__(self, matrix, type = "custom"):
        assert type(matrix) == np.ndarray
        assert matrix.shape == (4,4)
        self.mat = matrix
        self.type = type

    



testvec = Coordinate3D.from_coordinates(0,0,0,1)
print(testvec)
print(testvec.vec)

