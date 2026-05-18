# Test setup for user-input and drawing with pygame library
# TODO: OCCLUSION
import pygame

from geometry import *
from camera import *

# Camera Setup
#cameratype = "Locked"
cameratype = "Perspective"
cam = Camera()
cam.renderSpace = "World"
cam.fov_max_view_distance = 25
    # regular camera parameters for turning to x axis
cam.SetCamera(0.0, 0.0, 0.0, 90.0, 0.0, 90.0)

aspectx = 1280
aspecty = 720
# triangles
triangles = [[(2,-2,0),(2,2,0), (-2,2,0)], [(2,-2,0), (-2,-2,0), (-2,2,0)],  #base
             [(2,-2,0),(2,2,0),(0,0,2)],
              [(-2,-2,0),(2,-2,0),(0,0,2)],
              [(-2,2,0),(-2,-2,0),(0,0,2)],
              [(-2,2,0),(2,2,0),(0,0,2)]] #faces

trianglescolors = [pygame.Color(0,0,0,0), pygame.Color(0,0,0,0),
                    pygame.Color(255,0,0,0), pygame.Color(0,255,0,0), pygame.Color(0,0,255,0), pygame.Color(125,125,125,0),]
trianglesnew = [([Coordinate3D.from_3tuple(p) for p in triangles[i]],trianglescolors[i]) for i in range(len(triangles))]

# pygame setup
pygame.init()
screen = pygame.display.set_mode((aspectx, aspecty))
clock = pygame.time.Clock()
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        if (event.type == pygame.KEYDOWN):
            keycode = event.key
            if (keycode == pygame.K_w):
                print("W pressed")
                cam.MoveAndRotateCamera(Dz = 1.0)
            elif(keycode == pygame.K_a):
                print("A Pressed")
                cam.MoveAndRotateCamera(Dx = -1.0)
            elif(keycode == pygame.K_s):
                print("S Pressed")
                cam.MoveAndRotateCamera(Dz = -1.0)
            elif(keycode == pygame.K_d):
                print("D Pressed")
                cam.MoveAndRotateCamera(Dx = 1.0)
            elif(keycode == pygame.K_i):         ## ROTATION KEYS
                print("I Pressed")
                cam.MoveAndRotateCamera(Dphi = -10.0)
            elif(keycode == pygame.K_k):
                print("D Pressed")
                cam.MoveAndRotateCamera(Dphi = 10.0)
            elif(keycode == pygame.K_j):
                print("D Pressed")
                cam.MoveAndRotateCamera(Dtheta = -10.0)
            elif(keycode == pygame.K_l):
                print("D Pressed")
                cam.MoveAndRotateCamera(Dtheta = 10.0)
            elif(keycode == pygame.K_c):
                print("C Pressed")
                cam.MoveAndRotateCamera(Dy = 1)
            elif(keycode == pygame.K_v):
                print("V Pressed")
                cam.MoveAndRotateCamera(Dy = -1)


    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    # RENDER YOUR GAME HERE
    trianglesdrawn = 0
    for triangle in trianglesnew:
        tripoints = []
        point1 = cam.trNDCFromCamera(cam.trCameraFromRender(cam.trRenderFromWorld(triangle[0][0])))
        point2 = cam.trNDCFromCamera(cam.trCameraFromRender(cam.trRenderFromWorld(triangle[0][1])))
        point3 = cam.trNDCFromCamera(cam.trCameraFromRender(cam.trRenderFromWorld(triangle[0][2])))

        if (point1 != None):
            point1 = point1.aslist()
            tripoints.append(point1)
        if (point2 != None):
            point2 = point2.aslist()
            tripoints.append(point2)
        if (point3 != None):
            point3 = point3.aslist()
            tripoints.append(point3)
        drawpoints = [(p[0]*aspectx,(1 - p[1])* aspecty) for p in tripoints]
        if (len(drawpoints) >=2 ):
            pygame.draw.line(screen, triangle[1], drawpoints[0], drawpoints[1])
        if (len(drawpoints) == 3):
            pygame.draw.line(screen, triangle[1], drawpoints[1], drawpoints[2])
            pygame.draw.line(screen, triangle[1], drawpoints[2], drawpoints[0])

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()