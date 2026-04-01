# Geometry library version 0.3
# implements homogeneous coordinates
# coordinates are of the form [x y z w]
# the 3d homogeneous coordinate w will be limited to 0 or 1,
# to distinguish between points and vectors, and allow for
# affine transformations in matrix form

import numpy as np
from math import cos,sin,pi

class Coordinate3D:
    # initialization
    def __init__(self, vector):
        assert type(vector) == np.ndarray, "vector must be a formatted np array"
        assert vector.shape == (4,1), "vector must have shape (4,1)"
        assert vector[3,0] == 1 or vector[3,0] == 0, "w coordinate must be 0 or 1"
        self.vec = vector
        self.aslist = self.tolist

    # from 3d tuple
    @classmethod
    def from_3tuple(cls,tuple, vector = False):
        assert len(tuple) == 3, "tuple must be length 3"
        if (vector):
            return Coordinate3D.from_coordinates(tuple[0],tuple[1],tuple[2],0)
        else:
            return Coordinate3D.from_coordinates(tuple[0],tuple[1],tuple[2],1)
        
    def tolist(self):
        return self.vec.flatten().tolist()
    
        
    # from np vector
    @classmethod
    def from_coordinates(cls, x, y, z, w):
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
    def __init__(self, matrix, mat_type = "custom"):
        assert type(matrix) == np.ndarray
        assert matrix.shape == (4,4)
        self.mat = matrix
        self.type = type

    def apply(self, vector):
        if (type(vector) == Coordinate3D):
            return Coordinate3D(self.mat @ vector.vec)
        elif (type(vector) == np.ndarray):
            assert (vector.shape[1] == 4)
            return self.mat @ vector
        else:
            assert False , "vector of bad type"
    
    def compose(self,mat2):
        return Transform3D(self.mat @ mat2.mat)
    
    # returns inverse transform
    def inverse(self):
        return Transform3D(np.linalg.inv(self.mat))
    
    # All angles defined as counterclockwise positive 
    # Rotation x degrees about x axis y->z
    @classmethod
    def rotation_matrixX(cls,anglex):
        anglex = float(anglex)
        c = cos(anglex  * pi / 180.0)
        s = sin(anglex * pi / 180.0)
        return Transform3D(np.array([[1.0,0.0,0.0,0.0],
                                     [0.0,c,-1.0 * s,0.0],
                                     [0.0,s,c,0.0],
                                     [0.0,0.0,0.0,1.0]]))

    # All angles defined as counterclockwise positive z->x
    # Rotation x degrees about y axis
    @classmethod
    def rotation_matrixY(cls,angley):
        angley = float(angley)
        c = cos(angley  * pi / 180.0)
        s = sin(angley * pi / 180.0)
        return Transform3D(np.array([[c,0.0,s,0.0],
                                     [0.0,1.0,0.0,0.0],
                                     [-1.0 * s,0.0,c,0.0],
                                     [0.0,0.0,0.0,1.0]]))
    

    # All angles defined as counterclockwise positive
    # Rotation x degrees about z axis: x -> y
    @classmethod
    def rotation_matrixZ(cls,anglez):
        anglez = float(anglez)
        c = cos(anglez * pi / 180.0)
        s = sin(anglez * pi / 180.0)
        return Transform3D(np.array([[c,-1.0*s,0.0,0.0],
                                     [s,c,0.0,0.0],
                                     [0.0,0.0,1.0,0.0],
                                     [0.0,0.0,0.0,1.0]]))

        

    # Scale x,y,z by specified amounts
    @classmethod
    def scaling_matrix(cls,mul_x,mul_y,mul_z):
        return Transform3D(np.array([[mul_x,0.0,0.0,0.0],
                                     [0.0,mul_y,0.0,0.0],
                                     [0.0,0.0,mul_z,0.0],
                                     [0.0,0.0,0.0,1.0]]))
    
    # Translate x,y,z by specified amounts
    @classmethod
    def translation_matrix(cls,x,y,z):
        return Transform3D(np.array([[1.0,0.0,0.0,x],
                                     [0.0,1.0,0.0,y],
                                     [0.0,0.0,1.0,z],
                                     [0.0,0.0,0.0,1.0]]))
    
    # Transform that is the identity matrix
    @classmethod
    def identity(cls):
        return Transform3D(np.identity(4,float))


