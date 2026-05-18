# Version 0.3
# Switch to PBRT
# Chapter 5: Cameras and Film
# We implement the camera class in PBRT to provide functionality of
# previous versions with the added benefit of modularity and
# instance-specific settings.

# issues to iron out: User Interface for testing/usage
# triangles don't render unless all vertices are in-screen
# currently no methods to move the cameras
# problems with perspective projection type

from geometry import *
from camera import *

#cameratype = "Locked"
cameratype = "Normal"
cam = Camera()
cam.renderSpace = "World"
    # regular camera parameters for turning to x axis
cam.SetCamera(0.0, 0.0, 0.0, 90.0, 0.0, 90.0)
print(cam.origin.aslist())
print(cam.forwardVector.aslist())
print(cam.upVector.aslist())
print(cam.leftVector.aslist())


# cam.setCamType("Perspective")




aspectx = 10
aspecty = 10
# triangles
triangles = [[(2,-2,0),(2,2,0), (-2,2,0)], [(2,-2,0), (-2,-2,0), (-2,2,0)],  #base
             [(2,-2,0),(2,2,0),(0,0,2)],
              [(-2,-2,0),(2,-2,0),(0,0,2)],
              [(-2,2,0),(-2,-2,0),(0,0,2)],
              [(-2,2,0),(2,2,0),(0,0,2)]] #faces
trianglesnew = [[Coordinate3D.from_3tuple(p) for p in triangle] for triangle in triangles]

## initiate window and rendering
from OpenGL.GL import *
from OpenGL.GLUT import *

def draw2():
    global altitudalrotation, rot_counter
    ## rotations
    glClear(GL_COLOR_BUFFER_BIT)
    trianglesdrawn = 0
    for triangle in trianglesnew:
        tripoints = []
        for point in triangle:
            
            proj = cam.trNDCFromCamera(cam.trCameraFromRender(cam.trRenderFromWorld(point)))
            if (proj == None):
                break
            tripoints += [proj.aslist()]
        if (len(tripoints) == 3):
            glBegin(GL_TRIANGLES)
            for p in tripoints:
                glVertex2f(p[0],p[1])
            glEnd()
            trianglesdrawn += 1
    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutCreateWindow(b"PyOpenGL Test")
glutDisplayFunc(draw2)
glutMainLoop()

