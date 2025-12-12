from geometry import *

focus = Vector3d(-5,-2,2)

focal_length = 1.0
xaxis = Vector3d(0,1,0)
yaxis = Vector3d(0,0,1)
norm = Vector3d(1,0,0)
cameraplane = ProjectionPlane(focus.sum(norm.timesscalar(focal_length)), xaxis, yaxis, norm)

# triangles
triangles = [[(2,-2,0),(2,2,0), (-2,2,0)], [(2,-2,0), (-2,-2,0), (-2,2,0)],  #base
             [(2,-2,0),(2,2,0),(0,0,2)],
              [(-2,-2,0),(2,-2,0),(0,0,2)],
              [(-2,2,0),(-2,-2,0),(0,0,2)],
              [(-2,2,0),(2,2,0),(0,0,2)]] #faces
trianglesnew = []
for triangle in triangles:
    currtriangle = []
    for point in triangle:
        currtriangle += [Vector3d(point[0], point[1], point[2])]
    trianglesnew += [currtriangle]

print(cameraplane.intersection(trianglesnew[0][0], focus.difference(trianglesnew[0][0])))

## initiate window and rendering
from OpenGL.GL import *
from OpenGL.GLUT import *

def draw2():
    glClear(GL_COLOR_BUFFER_BIT)
    trianglesdrawn = 0
    for triangle in trianglesnew:
        tripoints = []
        for point in triangle:
            proj = cameraplane.intersection(point, focus.difference(point))
            if (proj == None):
                break
            tripoints += [proj.astuple()]
        if (len(tripoints) == 3):
            print(tripoints)
            print("Drawing triangle: " + str(tripoints))
            glBegin(GL_TRIANGLES)
            for p in tripoints:
                glVertex2f(p[0],p[1])
            glEnd()
            trianglesdrawn += 1
    print(trianglesdrawn)
    glutSwapBuffers()

def draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_TRIANGLES)
    glVertex2f(0.0, 0.5)
    glVertex2f(-0.5, -0.5)
    glVertex2f(0.5, -0.5)
    glEnd()
    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutCreateWindow(b"PyOpenGL Test")
glutDisplayFunc(draw2)
glutMainLoop()

