from math import sqrt
from math import sin
from math import cos
from math import pi

# 2D Vector class and associated methods
class Vector2d:
    tolerance = 0.01
    def __init__(self, x = 0.0, y = 0.0):
        self.x = float(x)
        self.y = float(y)
        self.updateisunit()

    # returns self plus argument as new Vector2d
    # if modify is True, returns None and argument is added to self
    def sum(self, vec, modify = False):
        assert type(vec) == Vector2d, "argument must be of type Vector2d"
        if (modify):
            self.x += vec.x
            self.y += vec.y
            self.updateisunit()
            return None
        return Vector2d(self.x + vec.x, self.y + vec.y)
    
    # returns self minus argument as new Vector2d
    # if modify is True, returns None and argument is subtracted from self
    def difference(self, vec, modify = False):
        assert type(vec) == Vector2d, "argument must be of type Vector2d"
        if (modify):
            self.x -= vec.x
            self.y -= vec.y
            self.updateisunit()
            return None
        return Vector2d(self.x - vec.x, self.y - vec.y)
    
    # returns self times c as new Vector2d
    # if modify is True, returns None and argument is multiplied by self
    def timesscalar(self, c, modify = False):
        if (modify):
            self.x *= c
            self.y *= c
            self.updateisunit()
            return None
        return Vector2d(self.x * c, self.y * c)
    
    # returns unit vector in the same direction as self as Vector3d
    # if modify is True, sets self to normalized vector and returns None
    def normalize(self, modify = False):
        mag = self.magnitude()
        if (modify):
            self.isunit = True
        return self.timesscalar(1 / mag, modify)
    
    # returns dot product of self and argument
    def dot(self, vec):
        assert type(vec) == Vector2d
        return (self.x * vec.x) + (self.y + vec.y)
    
    # returns 2d cross product of self and argument
    def cross(self, vec):
        assert type(vec) == Vector2d
        return (self.x * vec.y) - (self.y - vec.x)
    
    # returns magnitude of vector
    def magnitude(self):
        return sqrt(self.x **2 + self.y ** 2)
    
    #updates whether is unit
    def updateisunit(self):
        self.isunit = abs(self.magnitude() - 1.0) <= Vector2d.tolerance

    # returns tuple representation of vector
    def astuple(self):
        return (self.x, self.y)
    
    # print function
    def __str__(self):
        return "Vector2d: ("+str(self.x)+", "+str(self.y)+")"
    
# ----------------------------------------------------------------------------------------
# 3D Vector class and associated methods
class Vector3d:
    tolerance = 0.01
    def __init__(self, x = 0.0, y = 0.0, z = 0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.updateisunit()

    # returns self plus argument as new Vector3d
    # if modify is True, returns None and argument is added to self
    def sum(self, vec, modify = False):
        assert type(vec) == Vector3d, "argument must be of type Vector2d"
        if (modify):
            self.x += vec.x
            self.y += vec.y
            self.z += vec.z
            self.updateisunit()
            return None
        return Vector3d(self.x + vec.x, self.y + vec.y, self.z + vec.z)
    
    # returns self minus argument as new Vector3d
    # if modify is True, returns None and argument is subtracted from self
    def difference(self, vec, modify = False):
        assert type(vec) == Vector3d, "argument must be of type Vector2d"
        if (modify):
            self.x -= vec.x
            self.y -= vec.y
            self.z -= vec.z
            self.updateisunit()
            return None
        return Vector3d(self.x - vec.x, self.y - vec.y, self.z - vec.z)
    
    # returns self times c as new Vector3d
    # if modify is True, returns None and argument is multiplied by self
    def timesscalar(self, c, modify = False):
        if (modify):
            self.x *= c
            self.y *= c
            self.z *= c
            self.updateisunit()
            return None
        return Vector3d(self.x * c, self.y * c, self.z * c)
    
    # returns unit vector in the same direction as self as Vector3d
    # if modify is True, sets self to normalized vector and returns None
    def normalize(self, modify = False):
        mag = self.magnitude()
        if (modify):
            self.isunit = True
        return self.timesscalar(1 / mag, modify)
    
    # returns dot product of self and argument
    def dot(self, vec):
        assert type(vec) == Vector3d
        return (self.x * vec.x) + (self.y * vec.y) + (self.z * vec.z)
    
    # returns 3d cross product of self and argument as new Vector3d
    def cross(self, vec):
        assert type(vec) == Vector3d
        xn = (self.y * vec.z) - (self.z * vec.y)
        yn = (self.z * vec.x) - (self.x * vec.z)
        zn = (self.x * vec.y) - (self.y - vec.x)
        return Vector3d(xn, yn, zn)
    
    # returns magnitude of vector
    def magnitude(self):
        return sqrt(self.x **2 + self.y ** 2 + self.z **2)
    
    #updates whether is unit
    def updateisunit(self):
        self.isunit = abs(self.magnitude() - 1.0) <= Vector3d.tolerance

    # returns tuple representation of vector
    def astuple(self):
        return (self.x, self.y, self.z)
    
    # print function
    def __str__(self):
        return "Vector3d: ("+str(self.x)+", "+str(self.y)+", "+str(self.z)+")"
    

# ---------------------------------------------------------------------------------------
# a plane, with origin point, axes, and methods for projection of 3d vectors
class ProjectionPlane:
    intersection_tolerance = 10000
    # initialization: make sure all variables are set, DO NOT MIX CUSTOMS AND DEFAULTS
    # x-axis, y-axis, normal relative to origin
    def __init__(self, origin = Vector3d(), xaxis = Vector3d(1,0,0), yaxis = Vector3d(0,1,0), normal = Vector3d(0,0,1)):
        self.origin = origin
        self.xaxis = xaxis.normalize()
        self.yaxis = yaxis.normalize()
        self.normal = normal.normalize()

    # returns Vector2d containing x,y coordinates of the vector's projection onto the plane
    def projection(self, point):
        assert type(point) == Vector3d, "point must be in 3d"
        point_relative = point.difference(self.origin)
        return Vector2d(point_relative.dot(self.xaxis), point_relative.dot(self.yaxis))
    
    # returns Vector2d containing plane intersection coordinates of ray with specified origin and direction
    # returns None if intersection does not exist
    def intersection(self, rorigin, direction):
        assert type(rorigin) == Vector3d, "origin of ray must be 3d point"
        assert type(direction) == Vector3d, "direction of ray must be 3d point"
        direction = direction.normalize()
        if (abs(direction.dot(self.normal)) < 0.1 ):
            return None
        t = self.normal.dot(self.origin.difference(rorigin)) / direction.dot(self.normal)

        if (t < 0.1):
            return None
        intersection = rorigin.sum(direction.timesscalar(t))
        return self.projection(intersection)
        
    # initializes plane from two noncolinear vectors
    # vector 1, vector 2 are directions with respect to origin
    def from_vectors(self, origin, vec1, vec2):
        assert type(origin) == Vector3d
        assert type(vec1) == Vector3d
        assert type(vec2) == Vector3d
        assert vec1.cross(vec2).magnitude() >= 0.001
        xaxis = vec1.normalize()
        yaxis = vec2.difference( xaxis.timesscalar(vec2.dot(xaxis)))
        yaxis.normalize(True)
        norm = xaxis.cross(yaxis)
        return ProjectionPlane(origin, xaxis, yaxis, norm)
    
    # assumes projectionplane is an image plane, rotates it about the focus azimuthally
    def azimuthalrotation(self,focal_distance, theta):
        self.origin.difference(self.normal.timesscalar(focal_distance), True)
        self.normal = rotateazimuthal(self.normal, theta)
        self.xaxis = rotateazimuthal(self.xaxis, theta)
        self.yaxis = rotateazimuthal(self.yaxis, theta)
        self.origin.sum(self.normal.timesscalar(focal_distance), True)

    # assumes projectionplane is an image plane, rotates it about the focus azimuthally
    def altitudalrotation(self,focal_distance, theta):
        self.origin.difference(self.normal.timesscalar(focal_distance), True)
        self.normal = rotatealtitudal(self.normal, theta)
        self.xaxis = rotatealtitudal(self.xaxis, theta)
        self.yaxis = rotatealtitudal(self.yaxis, theta)
        self.origin.sum(self.normal.timesscalar(focal_distance), True)

    
# rotation theta degrees of the azimuthal angle (counterclockwise) (in degrees)
def rotateazimuthal(vec, theta):
    assert type(vec) == Vector3d
    theta = pi * theta / 180
    # matrix maps (1,0,0) -> (cos(theta),sin(theta),0)
    # (0,1,0) -> (-sin(theta),cos(theta),0)
    # (0,0,1) -> (0,0,1)
    # matrix is
    # cos(theta) -sin(theta) 0
    # sin(theta) cos(theta) 0
    # 0 0 1
    v1 = Vector3d(cos(theta), sin(theta), 0)
    v2 = Vector3d(-1 * sin(theta), cos(theta), 0)
    v3 = Vector3d(0,0,1)
    return v1.timesscalar(vec.x).sum(v2.timesscalar(vec.y)).sum(v3.timesscalar(vec.z))

def rotatealtitudal(vec, theta):
    assert type(vec) == Vector3d
    theta = pi * theta / 180
    # matrix maps (1,0,0) -> (cos(theta), 0, -sin(theta))
    # (0,1,0) -> (0,1,0)
    # (0,0,1) -> (sin(theta), 0, cos(theta))
    v1 = Vector3d(cos(theta), 0, -1 * sin(theta))
    v2 = Vector3d(0,1,0)
    v3 = Vector3d(sin(theta), 0, cos(theta))
    return v1.timesscalar(vec.x).sum(v2.timesscalar(vec.y)).sum(v3.timesscalar(vec.z))

    
