from geometry import *
from camera import *
# Test: camera rotation
# function should carry out three parts of camera rotation,
# yaw, pitch, roll in that order
def testCameraRotation():
    vec1 = Coordinate3D.from_3tuple((1,0,0))
    vec2 = Coordinate3D.from_3tuple((0,1,0))
    vec3 = Coordinate3D.from_3tuple((0,0,1))
    x = 0.0
    y = 0.0
    z = 0.0
    yaw = 0.0
    pitch = 0.0
    roll = 0.0
    cam = Camera()
    # print camera parameters
    print("Camera  Rotation Parameters: theta = "+str(cam.camera_rotation_theta)+" phi = "+str(cam.camera_rotation_phi_mod)+" omega = "+str(cam.camera_rotation_omega))
    print("Camera  translation Parameters: x = "+str(cam.camera_translationx)+" y = "+str(cam.camera_translationy)+" z = "+str(cam.camera_translationx))
    # test world to camera-world transform
    print("World to Camera World:")
    cam.SetCamera(x,y,z,yaw, pitch, roll)
    print(cam.trRenderFromWorld(vec1).aslist())
    print(cam.trRenderFromWorld(vec2).aslist())
    print(cam.trRenderFromWorld(vec3).aslist())
    # test camera_world to camera transform
    print("World to Camera:")
    print(cam.trCameraFromRender(cam.trRenderFromWorld(vec1)).aslist())
    print(cam.trCameraFromRender(cam.trRenderFromWorld(vec2)).aslist())
    print(cam.trCameraFromRender(cam.trRenderFromWorld(vec3)).aslist())

def testCameraFullTransform(x,y,z,theta, phi, omega,vec):
    cam = Camera()
    # test world to camera-world transform
    print("World to Camera World:")
    cam.SetCamera(x,y,z,theta, phi, omega)
    print(cam.trRenderFromWorld(vec).aslist())
    # test camera_world to camera transform
    print("World to Camera:")
    print(cam.trCameraFromRender(cam.trRenderFromWorld(vec)).aslist())
    


def unittest1():
    testCameraRotation()
    
def unittest2():
    testCameraFullTransform(0.0,0.0,0.0,-90.0, 0.0, 0.0, Coordinate3D.from_3tuple((2,-2,0)))

# main
#unittest1()
unittest2()