from geometry import *
# Class to contain a surface
# should handle intersections when given a ray (with option for closest surface only)
# should contain methods to transform itself by a camera
# should be able to compose with other surfaces
# methods for spacial sorting or partitioning?
# does a first pass of its subsurfaces for the closest, returns the closest surface along with t.
# TODO: alpha transparency and generating secondary 
# REQUIREMENT: ALL COLORS MUST BE 4 TUPLES, formatted (r,g,b,a)

class Surface:
    color = (0,0,0,128)

    def __init__(self):
        self.subsurfaces = []
        self.color = Surface.color
    # ray intersection
    def intersectRay(self, origin, direction):
        # first pass: closest-surface determination
        t = float("inf")
        surf = None
        for surface in self.subsurfaces:
            new_t, temp_surf = surface.intersectRay(origin, direction)
            if (new_t < t):
                t = new_t
                surf = temp_surf
        # return prevailing Surface for now
        return t, surf
    
    # add subsurface
    def addSurface(self, surf):
        self.subsurfaces.append(surf)
    
# Triangle Surface for intersections
# takes vertices as np arrays
class Triangle(Surface):
    def __init__(self, vertex1, vertex2, vertex3, color = None):
        assert type(vertex1) == np.ndarray and type(vertex2) == np.ndarray and type(vertex3) == np.ndarray, "vertices must be numpy arrays"
        assert len(vertex1) == 4 and len(vertex2) == 4 and len(vertex3) == 4, "vertices must be homogeneous points"
        self.vertex = vertex1
        self.edge1 = vertex2 - vertex1
        self.edge2 = vertex3 - vertex1
        if (color != None):
            self.color = color
        

    #Moller Trumbore Algorithm
    def intersectRay(self, origin, direction):
        # checks
        assert isPoint(origin) and not isPoint(direction)
        # cross product direction and edge2
        perp = np.append(np.cross(direction[0:3], self.edge2[0:3]), 0)
        # project edge1 onto cross product
        edge1dot = np.dot(perp, self.edge1)
        # if 0, edge2 has no component beyond direction and edge1, ie direction is in edge1, edge2 plane
        if abs(edge1dot) <= 0.001:
            return float('inf'), None
        # otherwise, project distance from ray origin to triangle vertex onto perpendicular, divide by edge1dot to find u (how many edge1s to reach plane)
        else:
            s = origin - self.vertex
            u = np.dot(s, perp) / edge1dot
        # check if u within bounds (if not, no intersection)
        if u >= 1.0 or u <= 0.0:
            return float('inf'), None
        # otherwise, compute v
        else:
            perp2 = np.append(np.cross(s[0:3], self.edge1[0:3]), 0)
            v = np.dot(direction, perp2) / edge1dot
        # check if v within bounds (if not, no intersection)
        if v >= 1.0 or v <= 0.0:
            return float('inf'), None
        # check if v+u within bounds (if not, no intersection)
        if v + u >= 1.0:
            return float('inf'), self
        # otherwise, compute t
        else:
            t = np.dot(self.edge2, perp2) / np.dot(self.edge1, perp)
        # check if t >= 0
        if t >= 0:
            return t, self
        return float('inf'), None

        
