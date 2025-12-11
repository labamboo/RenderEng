## For now, all code will be written in a monolithic file
from math import sqrt


## tolerance for float comparisons
tolerance = 0.01

## computes dot product
def dotproduct(a, b):
    assert len(a) == len(b)
    assert len(a) > 0
    sum = 0.0
    for i in range(len(a)):
        sum += a[i] * b[i]
    return sum
    
## computes cross product
def crossproduct(a,b):
    assert len(a) == 3
    assert len(b) == 3
    x = (a[1] * b[2]) - (a[2] * b[1])
    y = (a[2] * b[0]) - (a[0] * b[2])
    z = (a[0] * b[1]) - (a[1] * b[0])
    return (x,y,z)

# Computes 2d cross product, which is a scalar
def crossproduct2d(a,b):
    assert len(a) == 2
    assert len(b) == 2
    return (a[0] * b[1]) - (a[1] * b[0])

## updated version should probably map triangle geometry to the image plane pixels, not the other way around lol
## checks if given ray collides with given triangle (in 3D)
## this function assumes the triangle is a proper triangle
def collision(ray_o, ray_dir, triangle_points, debug = False):
    assert len(ray_o) == 3
    assert len(ray_dir) == 3
    assert len(triangle_points) == 3
    for point in triangle_points:
        assert len(point) == 3
    # transform problem into 2d problem
    # find the triangle normal vector to find the triangle's plane equation. Find the intersection of the plane and ray. Then map all the points to a 2d
    # surface.
    new_triangle_points = [(0,0)]
    origin3d = triangle_points[0]
    xaxisvec = (triangle_points[1][0] - origin3d[0], triangle_points[1][1] - origin3d[1], triangle_points[1][2] - origin3d[2])
    xaxismag = sqrt(dotproduct(xaxisvec,xaxisvec))
    xaxisvec = (xaxisvec[0] / xaxismag, xaxisvec[1] / xaxismag, xaxisvec[2] / xaxismag)
    thirdvec = (triangle_points[2][0] - origin3d[0], triangle_points[2][1] - origin3d[1], triangle_points[2][2] - origin3d[2])
    new_triangle_points += [(xaxismag, 0)]
    thirdvecx = dotproduct(thirdvec,xaxisvec)
    thirdvecxcomp = (xaxisvec[0] * thirdvecx, xaxisvec[1] * thirdvecx, xaxisvec[2] * thirdvecx)
    yaxisvec = (thirdvec[0] - thirdvecxcomp[0], thirdvec[1] - thirdvecxcomp[1], thirdvec[2] - thirdvecxcomp[2])
    yaxismag = sqrt(dotproduct(yaxisvec, yaxisvec))
    yaxisvec = (yaxisvec[0] / yaxismag, yaxisvec[1] / yaxismag, yaxisvec[2] / yaxismag)
    thirdvecy = yaxismag
    # define y axis to be normal component of third edge wrt x axis edge
    new_triangle_points += [(thirdvecx, thirdvecy)]
    trianglenorm = crossproduct(xaxisvec, yaxisvec)
    if (debug):
        print(dotproduct(trianglenorm, trianglenorm))
    # eq of ray is (x,y,z) = (ox,oy,oz) + (tux,tuy,tuz)
    # eq of plane is (x-x0)nx + (y-y0)ny + (z-z0)nz = 0
    # point satisfying both is the intersection, x' = ox + tux, y' = oy + tuy, z' = oz + tuz
    # nx(ox + tux) + ny(oy + tuy) + nz(oz + tuz) = nx(x0) + ny(y0) + nz(z0)
    # nx(tux) + ny(tuy) + nz(tuz) = nx(x0 - ox) + ny(y0 - oy) + nz(z0 - oz)
    # t = nx(x0 - ox) + ny(y0 - oy) + nz(z0 - oz) / (nxux + nyuy + nzuz)
    # note: answer does not exist if (nxux + nyuy + nzuz) = 0, or if t is negative (because ray goes in one direction only)
    if (dotproduct(trianglenorm, ray_dir) == 0):
        return False
    t = trianglenorm[0] * (origin3d[0] - ray_o[0])
    t += trianglenorm[1] * (origin3d[1] - ray_o[1])
    t += trianglenorm[2] * (origin3d[2] - ray_o[2])
    t = t / dotproduct(trianglenorm, ray_dir)
    if (t <= tolerance):
        return False
    intersection_point3d = (ray_o[0] + (ray_dir[0] * t), ray_o[1] + (ray_dir[1] * t), ray_o[2] + (ray_dir[2] * t))
    if (debug):
        print(intersection_point3d)
        dbgsum = 0.0
        dbgsum += (triangle_points[2][0] - origin3d[0]) * trianglenorm[0]
        dbgsum += (triangle_points[2][1] - origin3d[1]) * trianglenorm[1]
        dbgsum += (triangle_points[2][2] - origin3d[2]) * trianglenorm[2]
        print(dbgsum)
    intersection_point3d = (intersection_point3d[0] - origin3d[0], intersection_point3d[1] - origin3d[1],intersection_point3d[2] - origin3d[2])
    intersection_pointx = dotproduct(intersection_point3d, xaxisvec)
    intersection_pointy = dotproduct(intersection_point3d, yaxisvec)

    intersection_point = (intersection_pointx,intersection_pointy)
    return in_triangle2d(new_triangle_points, intersection_point)


## check if point in 2D plane lies on a given triangle (including boundaries)
def in_triangle2d(triangle_points, given_point):
    tolerance = 0.01
    assert len(given_point) == 2
    assert len(triangle_points) == 3
    for point in triangle_points:
        assert len(point) == 2
    ## Method: using the method of cross products, checking if the point in question is the same direction with respect to all three edges of the triangle
    vecpoint = (given_point[0] - triangle_points[0][0], given_point[1] - triangle_points[0][1])
    vecedge = (triangle_points[1][0] - triangle_points[0][0], triangle_points[1][1] - triangle_points[0][1])
    a = crossproduct2d(vecedge, vecpoint)
    vecpoint = (given_point[0] - triangle_points[1][0], given_point[1] - triangle_points[1][1])
    vecedge = (triangle_points[2][0] - triangle_points[1][0], triangle_points[2][1] - triangle_points[1][1])
    b = crossproduct2d(vecedge, vecpoint)
    vecpoint = (given_point[0] - triangle_points[2][0], given_point[1] - triangle_points[2][1])
    vecedge = (triangle_points[0][0] - triangle_points[2][0], triangle_points[0][1] - triangle_points[2][1])
    c = crossproduct2d(vecedge, vecpoint)
    if (a <= tolerance and b <= tolerance and c <= tolerance):
        return True
    mtolerance = -1 * tolerance
    if (a >= mtolerance and b >= mtolerance and c >= mtolerance):
        return True
    return False

#import drawing libraries
import numpy as np
import cv2

# create image as array and render using opencv
imwidth = 15.0
imheight = 15.0
focus = (-6,-2,2)
view_direction = (1,0,0)
focal_length = 3
center = (focus[0] + (focal_length * view_direction[0]), focus[1] + (focal_length * view_direction[1]), focus[2] + (focal_length * view_direction[2]))
width_direction = (0.0,1.0,0.0)
height_direction = (0.0,0.0,1.0)
top_left = (center[0] + ((imwidth/2) * width_direction[0]), center[1] + ((imwidth/2)*width_direction[1]), center[2] + ((imwidth/2)*width_direction[2]))
top_left = (top_left[0] + ((imheight/2) * height_direction[0]), top_left[1] + ((imheight/2)*height_direction[1]), top_left[2] + ((imheight/2)*height_direction[2]))

resolution_x = 150
resolution_y = 150

# triangles to render
# a pyramid
# faces: 
# [(2,-2,0),(2,2,0),(0,0,2)]
# [(-2,-2,0),(2,-2,0),(0,0,2)]
# [(-2,2,0),(-2,-2,0),(0,0,2)]
# [(-2,2,0),(2,2,0),(0,0,2)]
triangles = [[(2,-2,0),(2,2,0), (-2,2,0)], [(2,-2,0), (-2,-2,0), (-2,2,0)],  #base
             [(2,-2,0),(2,2,0),(0,0,2)],
              [(-2,-2,0),(2,-2,0),(0,0,2)],
              [(-2,2,0),(-2,-2,0),(0,0,2)],
              [(-2,2,0),(2,2,0),(0,0,2)]] #faces

img = np.ones((resolution_x, resolution_y))
for i in range(resolution_x):
    for j in range(resolution_y):
        currpoint = ((top_left[0] - height_direction[0] * ( j* imheight/resolution_x)), (top_left[1] - height_direction[1] * (j * imheight/resolution_x)), (top_left[2] - height_direction[2] * (j * imheight/resolution_x)))
        currpoint = (currpoint[0] - (width_direction[0] * (i*imwidth/resolution_y)), currpoint[1] - (width_direction[1] * (i*imwidth/resolution_y)), currpoint[2] - (width_direction[2] * (i*imwidth/resolution_y)))
        direction = (currpoint[0] - focus[0], currpoint[1] - focus[1], currpoint[2] - focus[2])
        for triangle in triangles:
            if (collision(focus, direction, triangle)):
                # notation (y, x) for opencv
                if (j == 0 and i == 38):
                    print("i: "+str(i)+"j: "+str(j))
                    print(currpoint)
                    print(direction)
                    print(focus)
                    collision(focus, direction, triangle, True)
                img[j, i] = 0.0
                break
print("img rendering complete")
#img = np.ones((7,7))
#img[0,0] = 0.0
#img[0,1] = 0.0
img = cv2.resize(img, (300,300), interpolation = 0)

cv2.imshow("test",img)
cv2.waitKey(0)


## initiate window and rendering
#from OpenGL.GL import *
#from OpenGL.GLUT import *

#triangle = [(3,0,-1),(3,0,-2), (3,1,-1)]
#triangle2 = [(3,0,1),(3,0,0), (3,1,1)]

#def draw():
#    glClear(GL_COLOR_BUFFER_BIT)
#    glBegin(GL_POINTS)
#    startpoint = (1.5, -3.5, 3.5)
#    for i in range(7):
#        for j in range(7):
#            currpoint = (1.5, startpoint[1] + i, startpoint[2] - j)
#            if (collision(currpoint, currpoint, triangle)):
#                glVertex2f(i - 3.5, 3.5 - j)
#            if (collision(currpoint, currpoint, triangle2)):
#                glVertex2f(i - 3.5, 3.5 - j)
    #glVertex2f(0.0, 0.5)
    #glVertex2f(-0.5, -0.5)
    #glVertex2f(0.5, -0.5)
#    glEnd()
#    glutSwapBuffers()

#glutInit()
#glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
#glutCreateWindow(b"PyOpenGL Test")
#glutDisplayFunc(draw)
#glutMainLoop()