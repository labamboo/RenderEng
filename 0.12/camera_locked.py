# The locked camera is a simplified version of the camera
# commonly used in video games, where camera movement is
# not based on the axes of the camera itself, but around
# a humanoid model. The camera can pivot up and down along
# an axis in the world x-y plane set to a certain height,
# and it can turn within the x-y plane to look around.

# World to World-Camera transform is a translation

# World-Camera to Camera transform is a rotation

# World to Camera process:
# subtract camera translation x,y,z
# apply camera rotations in reverse

# Camera to World process
# apply camera rotations
# add camera translation x,y,z

# phi should be locked to [0,180.0]
# theta should be modulo 360.0

from geometry import *
from camera import *

class CameraLocked(Camera):
    def __init__(self):
        super().__init__()
        self.translational_velocity = 0.5
        self.rotational_velocity_vertical = 15.0
        self.rotational_velocity_horizontal = 15.0

    # important methods/variables
    # self.RenderFromWorld
    # self.WorldFromRender
    # self.RenderFromCamera
    # self.CameraFromRender
    # self.camera_translationx = 0.0
    # self.camera_translationy = 0.0
    # self.camera_translationz = 0.0
    # self.camera_rotation_theta = 0.0
    # self.camera_rotation_phi = 0.0

    # methods to modify/overwrite
    # self.SetMatrices
    # self.MoveCamera
    # self.SetCamera
    # order of rotations is panning (yaw), then pitch
    def SetMatrices(self):
        rotational_matrix_CameraFromWorld =Transform3D.rotation_matrixX(-1.0 * self.camera_rotation_phi).compose(
                            Transform3D.rotation_matrixZ(-1.0 * self.camera_rotation_theta)
                            )
        translational_matrix_CameraFromWorld = Transform3D.translation_matrix(-1.0 * self.camera_translationx,
                                                              -1.0 * self.camera_translationy,
                                                              -1.0 * self.camera_translationz)
        identity_matrix = Transform3D.identity()
        
        if (self.renderSpace == "Camera"):
            self.RenderFromCamera = identity_matrix
            self.CameraFromRender = identity_matrix
            self.RenderFromWorld = rotational_matrix_CameraFromWorld.compose(translational_matrix_CameraFromWorld)
            self.WorldFromRender = self.RenderFromWorld.inverse()
        elif(self.renderSpace == "World"):
            self.WorldFromRender = identity_matrix
            self.RenderFromWorld = identity_matrix
            self.CameraFromRender = rotational_matrix_CameraFromWorld.compose(translational_matrix_CameraFromWorld)
            self.RenderFromCamera = self.CameraFromRender.inverse()
        elif(self.renderSpace == "Camera-World"):
            # Camera-World Space
            self.WorldFromRender = translational_matrix_CameraFromWorld.inverse()
            self.RenderFromWorld = Transform3D.translation_matrix(-1.0 * self.camera_translationx,
                                                              -1.0 * self.camera_translationy,
                                                              -1.0 * self.camera_translationz)
            self.RenderFromCamera = rotational_matrix_CameraFromWorld.inverse()
            self.CameraFromRender = self.RenderFromCamera.inverse()
        else:
            assert False, "Camera Render-Space not supported"