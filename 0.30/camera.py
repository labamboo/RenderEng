# Camera.py file
# PBRT Chapter 5
# Handles transforms between
# three spaces: camera space, world space,
# and camera-world space
# One of these is designated the rendering space.
from geometry import *
from math import atan
from math import tan
# For now, we will use this camera to replicate the primitive ray-tracer
# and rasterization-based renderers from 0.1 and 0.2 of this project.
# *In future iterations I will probably improve both, undecided for now.
# This camera will have both orthographic and perspective projection camera options
# This iteration with PBRT as reference will enable depth
# differentiation in our image, which the previous ones did not.

# Functions the camera must handle
# 1) for raster-based rendering, a function that maps a point
#    in world space to a point in screen space (camera space, which is then
#    mapped to a point on the screen)
# 2) for ray-tracing renderers, a function that maps a point in screen
#    space to a ray in world space.

# Default camera will be orthographic

# Camera space has screen-left as positive x, screen-up as positive y, forward as positive z
# Rotation Angle Conventions:
# +theta: z -> x (yaw rotation counterclockwise)
# +phi: y -> z (pitch rotation downwards)
# +omega: x -> y (roll (in-screen) rotation clockwise)




class Camera:

    # Constructor
    def __init__(self):
        # camera type
        self.camtype = "Orthographic"
        # conversions between camera_space,camera_world space, and world space
        # are mediated by these matrices
        self.type = "Orthographic"
        self.renderSpace = "Camera-World"

        
        # Transform Matrices
        self.RenderFromWorld = Transform3D.identity()
        self.WorldFromRender = Transform3D.identity()
        self.CameraFromRender = Transform3D.identity()
        self.RenderFromCamera = Transform3D.identity()
        self.trNDCFromCamera = self.trNDCFromCameraOrtho
        self.trCameraFromNDC = self.trCameraFromNDCOrtho

        # axes (directional, in World Coordinates)
        self.origin = Coordinate3D.from_coordinates(0.0,0.0,0.0,1.0)
        self.upVector = Coordinate3D.from_coordinates(0.0, 1.0, 0.0, 0.0)
        self.forwardVector = Coordinate3D.from_coordinates(0.0, 0.0, 1.0, 0.0)
        self.leftVector = Coordinate3D.from_coordinates(1.0, 0.0, 0.0, 0.0)


        # film information
        self.film_pixels_x = 0
        self.film_pixels_y = 0

        # field of view bounds
        self.zlow = 0.0
        self.zhigh = 10.0
        self.xlow = -10.0
        self.xhigh = 10.0
        self.ylow = -10.0
        self.yhigh = 10.0
        # perspective projection parameters
        self.focal_length = 1.0
        # field of view, in degrees vertical and horizontal
        self.fov_bound_horizontal = 45.0
        self.fov_bound_vertical = 45.0
        # field of view max viewing distance
        self.fov_max_view_distance = 10.0
        return
    # pbrt Chapter 5 camera transform: when it says the worldfromrender
    # transform cannot be animated, it means that the matrix itself cannot
    # be animated, not that the objects within the rendering space cannot be
    # moving around. The performance hit that might result comes from the
    # intensive computations involved in transform interpolation (chapter 3),
    # not from the computations of transforming objects into rendering space.
    # the worldfromrender matrix itself, of course, changes with camera position/rotation

    # transforms world to/from rendering space
    def trWorldFromRender(self, vec):
        return self.WorldFromRender.apply(vec)
    def trRenderFromWorld(self, vec):
        return self.RenderFromWorld.apply(vec)
    
    # toggles projective transform type
    def setCamType(self, camtype):
        assert camtype in ["Perspective", "Orthographic"], "invalid camera type"
        self.camtype = camtype
        if camtype == "Perspective":
            self.trNDCFromCamera = self.trNDCFromCameraPersp
            self.trCameraFromNDC = self.trCameraFromNDCPersp
            self.xhigh = self.focal_length * tan(self.fov_bound_horizontal)
            self.xlow = -1.0 * self.xhigh
            self.yhigh = self.focal_length * tan(self.fov_bound_vertical)
            self.ylow = -1.0 * self.yhigh
            self.zhigh = 100.0
            self.zlow = 0.0
        else:
            self.trNDCFromCamera = self.trNDCFromCameraOrtho
            self.trCameraFromNDC = self.trCameraFromNDCOrtho
            self.zlow = 0.0
            self.zhigh = 10.0
            self.xlow = -10.0
            self.xhigh = 10.0
            self.ylow = -10.0
            self.yhigh = 10.0

    

    
    # transforms NDC to/from camera space
    # returns None if not within NDC
    def trNDCFromCameraOrtho(self, vec):
        items = vec.tolist()
        assert len(items) > 0, "items cannot be empty"
        assert type(items[0]) == float or type(items[0]) == int, str(items[0])+" is not of int/float type" 
        if (items[0] < self.xlow or items[0] > self.xhigh or
            items[1] < self.ylow or items[1] > self.yhigh or
            items[2] < self.zlow or items[2] > self.zhigh):
            return None
        return Coordinate3D.from_coordinates((items[0] - self.xlow) / (self.xhigh - self.xlow),
                                             (items[1] - self.ylow) / (self.yhigh - self.ylow),
                                             (items[2] - self.zlow) / (self.zhigh - self.zlow),
                                             1.0)
    def trCameraFromNDCOrtho(self, vec):
        items = vec.tolist()
        for coord in items:
            assert (coord >= 0.0 and coord <= 1.0), "vector must have all entries in range [0.0,1.0]"
        return Coordinate3D.from_coordinates(self.xlow + (items[0] * (self.xhigh - self.xlow)),
                                             self.ylow + (items[1] * (self.yhigh - self.ylow)),
                                             self.zlow + (items[2] * (self.zhigh - self.zlow)),
                                             1.0)
    
    # Perspective Projective Transform
    # TODO
    # WARNING: if fov angles are too large then problem may occur at edge of fov
    # WARNING: if fov max view distance too small, can lead to nonrectangular viewing port
    def trNDCFromCameraPersp(self, vec):
        assert self.fov_bound_horizontal < 90.0 and self.fov_bound_vertical < 90.0, "fov bounds must be less than 90 degrees"
        items = vec.tolist()
        assert len(items) > 0, "vec.tolist() cannot be empty"
        assert type(items[0]) == float or type(items[0]) == int, str(items[0])+" is not of int/float type" 
        # check if within near and far distance bounds
        if (items[2] < self.focal_length or (items[0]**2 + items[1]**2 + items[2]**2) > self.fov_max_view_distance ** 2):
            return None
        # compute view angle
        viewanglex = atan(abs(items[2]) / abs(items[0])) * 180.0 / pi
        viewangley = atan(abs(items[2]) / abs(items[1])) * 180.0 / pi
        if (viewanglex > self.fov_bound_horizontal or viewangley > self.fov_bound_vertical):
            return None
        
        
        return Coordinate3D.from_coordinates(((items[0] / items[2]) - self.xlow) / (self.xhigh - self.xlow),
                                             ((items[1] / items[2]) - self.ylow) / (self.yhigh - self.ylow),
                                             items[2] / self.fov_max_view_distance,
                                             1.0)
    def trCameraFromNDCPersp(self, vec):
        #TODO
        return None
    
    # transforms camera space to/from render space
    def trRenderFromCamera(self, vec):
        return self.RenderFromCamera.apply(vec)
    def trCameraFromRender(self, vec):
        return self.CameraFromRender.apply(vec)
        
    # Sets transform matrices using translation,rotation
    # parameters
    # Matrices updated:
    # RenderFromWorld
    # WorldFromRender
    # RenderFromCamera
    # CameraFromRender
    # Camera from World: Rotation yaw, pitch, roll, Translation
    # NOTE: default position for camera is looking straight up.
    def UpdateMatrices(self):
        rotational_matrix_WorldFromCamera = Transform3D.RotationFromCoordinate3D(self.leftVector, self.upVector, self.forwardVector)
        translational_matrix_WorldFromCamera = Transform3D.TranslationFromCoordinate3D(self.origin)
        identity_matrix = Transform3D.identity()
        
        if (self.renderSpace == "Camera"):
            self.RenderFromCamera = identity_matrix
            self.CameraFromRender = identity_matrix
            self.WorldFromRender = translational_matrix_WorldFromCamera.compose(rotational_matrix_WorldFromCamera)
            self.RenderFromWorld = self.WorldFromRender.inverse()
        elif(self.renderSpace == "World"):
            self.WorldFromRender = identity_matrix
            self.RenderFromWorld = identity_matrix
            self.RenderFromCamera = translational_matrix_WorldFromCamera.compose(rotational_matrix_WorldFromCamera)
            self.CameraFromRender = self.RenderFromCamera.inverse()
        elif(self.renderSpace == "Camera-World"):
            # Camera-World Space
            self.WorldFromRender = translational_matrix_WorldFromCamera
            self.RenderFromWorld = translational_matrix_WorldFromCamera.inverse()
            self.RenderFromCamera = rotational_matrix_WorldFromCamera
            self.CameraFromRender = self.RenderFromCamera.inverse()
        else:
            assert False, "Camera Render-Space not supported"
    
    # Moves Camera Position
    # Helper Function
    @classmethod
    def MoveCamera(cls, origin, forward, up, left, Dx = 0.0 , Dy = 0.0, Dz = 0.0):
        return Coordinate3D.weighted_sum([origin, forward, up, left], [1.0, Dz, Dy, Dx])
        
    # Rotates Camera about theta (zx plane)
    # Helper Function
    @classmethod
    def RotateCameraZX(cls,forward, left, Dtheta):
        return Coordinate3D.rotate(forward, left, Dtheta)

    # Rotates Camera about phi (yz plane)
    # Helper Function
    @classmethod
    def RotateCameraYZ(cls,up, forward, Dphi):
        return Coordinate3D.rotate(up, forward, Dphi)

    # Rotates Camera about omega (xy plane)
    # Helper Function
    @classmethod
    def RotateCameraXY(cls,left, up, Domega):
        return Coordinate3D.rotate(left, up, Domega)
    
    # Move and Rotate Camera
    # Order: theta, phi, omega, translation 
    # TODO: figure out if the ordering greatly affects the feel of the movement
    def MoveAndRotateCamera(self, Dx = 0.0, Dy = 0.0, Dz = 0.0, Dtheta = 0.0, Dphi = 0.0, Domega = 0.0):
        origin = self.origin
        forward = self.forwardVector
        up = self.upVector
        left = self.leftVector
        # theta
        if (Dtheta != 0.0):
            forward, left = Camera.RotateCameraZX(forward, left, Dtheta)
        # phi
        if (Dphi != 0.0):
            up, forward = Camera.RotateCameraYZ(up, forward, Dphi)
        # omega
        if (Domega != 0):
            left, up = Camera.RotateCameraXY(left, up, Domega)
        # translation
        if (Dx != 0.0 or Dy != 0.0 or Dz != 0.0):
            origin = Camera.MoveCamera(origin, forward, up, left, Dx, Dy, Dz)
        self.origin = origin
        self.forwardVector = forward
        self.upVector = up
        self.leftVector = left
        self.UpdateMatrices()
        return

    
    # Sets camera location/orientation (order: theta, phi, omega, translation)
    def SetCamera(self, x, y, z, theta, phi, omega):
        # reset Camera Coordinates
        self.origin = Coordinate3D.from_coordinates(0.0,0.0,0.0,1.0)
        self.upVector = Coordinate3D.from_coordinates(0.0, 1.0, 0.0, 0.0)
        self.forwardVector = Coordinate3D.from_coordinates(0.0, 0.0, 1.0, 0.0)
        self.leftVector = Coordinate3D.from_coordinates(1.0, 0.0, 0.0, 0.0)
        # apply transforms in order
        self.MoveAndRotateCamera(x, y, z, theta, phi, omega)
        return
    

    ### BEGIN RAYTRACING FUNCTIONS

    # Takes a position on the screen and returns a ray (origin, direction) in render space
    # x,y must be normalized
    def rayFromScreenCoordsNormalized(self, x, y):
        assert x >= 0.0 and x <= 1.0, "x must be normalized"
        assert y >= 0.0 and y <= 1.0, "y must be normalized"
        # 1) compute origin:
        #    orthogonal: from camera position in render space, move x in x direction, y in y direction
        #    perspective: from camera position, move focal_len in z direction, focal_len * x in x direction, focal_len * y in y direction
        # 2) compute direction:
        #    orthogonal: simply the z-direction
        #    perspective: normalized vector from camera origin to pixel point in space.
        xscalar = ((self.xhigh - self.xlow) * x)+self.xlow
        yscalar = ((self.yhigh - self.ylow) * y)+self.ylow
        if (self.camtype == "Orthographic"):
            ## ray parameters in world-coordinates
            rayorigin = self.origin.add(self.leftVector.scale(xscalar)).add(self.upVector.scale(yscalar))
            raydirection = self.forwardVector
        else:
            rayorigin = self.origin.add(self.leftVector.scale(xscalar)).add(self.upVector.scale(yscalar)).add(self.forwardVector.scale(self.focal_length))
            raydirection = rayorigin.subtract(self.origin).normalized()
        return self.trRenderFromWorld(rayorigin), self.trRenderFromWorld(raydirection)

