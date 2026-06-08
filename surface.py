from geometry import *
from texture import *
# Class to contain a surface
# should handle intersections when given a ray (with option for closest surface only)
# should contain methods to transform itself by a camera
# should be able to compose with other surfaces
# methods for spacial sorting or partitioning?
# does a first pass of its subsurfaces for the closest, returns the closest surface along with t.
# TODO: implement toRenderSpace transform for all surfaces (possibly won't need this unless things travel really far)
# TODO: colorAt functions for Triangle and Sphere
# TODO: alpha transparency and generating secondary 
# REQUIREMENT: ALL COLORS MUST BE 4 TUPLES, formatted (r,g,b,a)
# TODO: backface-culling?
# TODO: implement solid-objects defined with triangles: refraction handling should be done at a higher level.

class Surface:
    color = (0,0,0,128)

    def __init__(self):
        self.subsurfaces = []
        self.color = Surface.color
        self.singleFaced = False
        self.shadingKAmbient = 0.5
        self.shadingKDiffuse = 0.5
        self.shadingKSpecular = 0.00
        self.shadingNSpecular = 2 #blinnphongexponent
        self.shadingKReflective = 0.0
        self.shadingKRefractive = 0.0
        self.snellRatio = 1.0 #ratio of sines of incident angles (relative to air, which is approximated as vacuum)
        self.shadowTransparency = 0.0
        self.name = "Surface"
    # ray intersection
    def intersectRay(self, origin, direction, tmin = 0.0, tmax = float('inf'), shadowRay = False):
        # first pass: closest-surface determination
        t = float("inf")
        if (shadowRay):
            t = 1.0
        surf = None
        for surface in self.subsurfaces:
            new_t, temp_surf = surface.intersectRay(origin, direction, tmin, tmax)
            if (shadowRay):
                if (new_t > tmin and new_t < tmax):
                    t = t * temp_surf.shadowTransparency
                    if (t == 0.0):
                        break
            elif (new_t < t):
                t = new_t
                surf = temp_surf
        # return prevailing Surface for now
        return t, surf
    
    # add subsurface
    def addSurface(self, surf):
        self.subsurfaces.append(surf)
    
    # dummy function
    def computeSurfaceNormal(self, point, viewdirection):
        assert False, "surface normal cannot be called on wrapper object"
        return 
    
    # returns reflection direction given view direction
    def computeReflectionDirection(self, point, viewdirection):
        surfaceNormal = self.computeSurfaceNormal(point, viewdirection)
        return viewdirection - (2 * np.dot(viewdirection, surfaceNormal) * surfaceNormal)
    
    # returns refraction direction given view direction and whether entering/exiting
    # WARNING: returns None if total internal reflection occurs
    def computeRefractionDirection(self, point, viewdirection, snellRatioOther = 1.0, exiting = False):
        """Computes Refraction Direction. WARNING: returns None for Total Internal Reflection"""
        surfaceNormal = self.computeSurfaceNormal(point, viewdirection)
        incidentcos = -1.0 * np.dot(viewdirection, surfaceNormal)
        if (incidentcos **2 >= 1.0):
            return None
        incidentsin = np.sqrt(1 - (incidentcos ** 2))
        # compute Snell Ratio, depending on exiting/entering
        if (exiting):
            snellRat = snellRatioOther / self.snellRatio
        else:
            snellRat = self.snellRatio / snellRatioOther
        # check for total internal reflection
        if (snellRat * incidentsin > 1.0):
            return None
        # otherwise, return refraction direction
        return (snellRat * viewdirection) + ((snellRat - 1) * incidentcos * surfaceNormal)
    
    # determines if looking at surface from backside or frontside (distinguishing sides determined by subclass)
    def isBackside(self, point, viewdirection):
        """True if viewdirection is from the back of surface"""
        assert False, "generic surface has no isBackside function"

    # returns Color at given point
    # WARNING: Does not check if point is on Surface
    def colorAt(self, point):
        assert False, "generic Surface should not have colorAt function called"
    

    
# Triangle Surface for intersections
# takes vertices as np arrays
# front, back faces distinguished by order of vertices
# looking down the normal vector, vertices are counterclockwise
class Triangle(Surface):
    def __init__(self, vertex1, vertex2, vertex3, color = None, singleFaced = False):
        assert type(vertex1) == np.ndarray and type(vertex2) == np.ndarray and type(vertex3) == np.ndarray, "vertices must be numpy arrays"
        assert len(vertex1) == 4 and len(vertex2) == 4 and len(vertex3) == 4, "vertices must be homogeneous points"
        assert vertex1[3] == 1 and vertex2[3] == 1 and vertex3[3] == 1, "vertices must be points"
        super().__init__()
        self.vertex = vertex1
        self.edge1 = vertex2 - vertex1
        self.edge2 = vertex3 - vertex1
        self.normal = np.cross(self.edge1[0:3], self.edge2[0:3])# DIRECTION MATTERS, WHICH MEANS ORDER OF VERTICES MATTERS IF BACK/FRONT FACES DISTINGUISHED
        self.normal = np.append((self.normal / np.sqrt(np.sum(self.normal ** 2))), 0)
        if (color != None):
            self.color = color
        self.singleFaced = singleFaced
        

    #Moller Trumbore Algorithm
    def intersectRay(self, origin, direction, tmin = 0.0, tmax = float('inf')):
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
        if t >= tmin and t <= tmax:
            return t, self
        return float('inf'), None
    
    # see superclass definition
    def computeSurfaceNormal(self, point, viewdirection):
        if (np.dot(self.normal, viewdirection) >= 0):
            return -1 * self.normal
        return self.normal
    
    # see superclass definition
    def isBackside(self, point, viewdirection):
        return np.dot(self.normal, viewdirection) >= 0
    
    # returns Color at point
    def colorAt(self, point = None):
        return self.color

# Surface Class for a sphere
# takes central point and a radius
# TODO: implement toRenderSpace transform
class Sphere(Surface):
    def __init__(self, center, radius, color = None):
        super().__init__()
        assert type(center) == np.ndarray and len(center) == 4
        assert center[3] == 1, "center must be a point"
        assert type(radius) == int or type(radius) == float
        self.center = center
        self.radius = radius
        if (color != None):
            self.color = color
    
    # Ray intersection algorithm
    def intersectRay(self, point, direction, tmin = 0.0, tmax = float('inf')):
        # sphere equation is given by (x-x0)^2 + (y-x0)^2 + (z-z0)^2 = R^2
        # rearranging: r dot r = R^2
        # plugging in ray equation r = o + td gives us o + td - c dot o + td - c= R^2
        # (o - c) dot (o - c) + 2t ((o - c) dot d) + t^2 ||d||^2 = R^2
        # solve the quadratic
        pointminuscenter = point - self.center
        c = np.dot(pointminuscenter, pointminuscenter) - (self.radius ** 2)
        b = 2 * np.dot(pointminuscenter, direction)
        a = 1
        det = (b**2) - (4*a*c)
        if (det <= 0.0):
            return float('inf'), None
        t = min(((-1 * b) + np.sqrt(det) ) / 2,  ((-1 * b) - np.sqrt(det) ) / 2)
        if (t <= tmin or t >= tmax):
            return float('inf'), None
        return t, self
    
    # compute surface normal
    def computeSurfaceNormal(self, point, viewdirection):
        assert point[3] == 1
        norm = (point - self.center) / self.radius
        if (np.dot(norm, viewdirection) >= 0.0):
            return norm * -1.0
        return norm
    
    # see superclass definition
    def isBackside(self, point, viewdirection):
        assert point[3] == 1
        norm = (point - self.center) / self.radius
        return np.dot(norm, viewdirection) >= 0.0
    
    # returns color at point
    def colorAt(self, point = None):
        return self.color
    

# Surface Class for a Quadrilateral Plane (extends triangle)
# first point is corner 1, the other two define the edges: corner 1 is mirrored across the other two points for the other half of the quadrilateral
class Plane(Triangle):
    # constructor
    def __init__(self, vertex1, vertex2, vertex3, color = None, singleFaced = False):
        super().__init__(vertex1, vertex2, vertex3, color, singleFaced)
        # texture: solid color
        if (color == None):
            self.texture = Texture(Surface.color)
        else:
            self.texture = Texture(color)
        # Gram matrix for uv computations
        self.gram = np.linalg.inv(np.array([[np.dot(self.edge1, self.edge1), np.dot(self.edge1, self.edge2)],
                         [np.dot(self.edge1, self.edge2), np.dot(self.edge2, self.edge2)]]))


    #Moller Trumbore Algorithm Analog for Surfaces
    def intersectRay(self, origin, direction, tmin = 0.0, tmax = float('inf')):
        # checks
        assert origin[3] == 1 and direction[3] == 0
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
        # unlike triangle, no bounds on v+u (only v,u \in [0.0,1.0])
        # compute t
        else:
            t = np.dot(self.edge2, perp2) / np.dot(self.edge1, perp)
        # check if t >= 0
        if t >= tmin and t <= tmax:
            return t, self
        return float('inf'), None
    
    # returns color at point
    def colorAt(self, point):
        # compute u,v coordinates of point
        # no need to assume point is on surface already, but point is projected onto surface
        # using method of gram matrix
        project = np.array([np.dot(point, self.edge1), np.dot(point, self.edge2)])
        decomp = project @ self.gram
        # call colorAtUV on texture contained in Surface
        return self.texture.colorAtUV(decomp[0],decomp[1])
    

