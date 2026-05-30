# Test setup for user-input and drawing with pygame library
# TODO: View-Direction/Light-Direction/Normal-Direction figuring out
import pygame

from geometry import *
from camera import *
from surface import *
from lighting import *

# Camera Setup
#cameratype = "Locked"
cam = Camera()
cam.setCamType("Perspective")
cam.renderSpace = "World"
cam.fov_max_view_distance = 25
    # regular camera parameters for turning to x axis
cam.SetCamera(0.0, 0.0, 0.0, 90.0, 0.0, 90.0)
cam.MoveAndRotateCamera(Dy = 3.0, Dz = -4.0)
cam.MoveAndRotateCamera(Dphi = 10.0)

aspectx = 256 #1280
aspecty = 144 #720


# triangles
triangletest = Sphere(np.array([2, 0, 2,1]), 1.0, (255,0,0,0))#Triangle(np.array([2,-2,0,1]),np.array([2,2,0,1]), np.array([2,2,2,1]), (255,0,0,0))
triangletest.shadingKSpecular = 3.0
triangletest2 = Surface()
triangletest2.addSurface(triangletest)
#triangletest2.addSurface(Triangle(np.array([4,-2,0,1]),np.array([4,2,2,1]), np.array([4,-2,2,1]), (255,0,0,0)))
triangletest2.addSurface(Triangle(np.array([0,0,0,1]),np.array([4,4,0,1]), np.array([4,-4,0,1]), (125,0,125,0))) # to be normal inverted
triangletest2.addSurface(Triangle(np.array([0,0,0,1]),np.array([-4,-4,0,1]), np.array([4,-4,0,1]), (0,125,0,0)))
triangletest2.addSurface(Triangle(np.array([0,0,0,1]),np.array([-4,-4,0,1]), np.array([-4,4,0,1]), (0,125,125,0))) # to be normal inverted
triangletest2.addSurface(Triangle(np.array([0,0,0,1]),np.array([4,4,0,1]), np.array([-4,4,0,1]), (125,125,0,0)))
triangletest2.addSurface(Sphere(np.array([1.5, -2, 3,1]), 1.0, (0,255,0,0)))
triangletest2.addSurface(Sphere(np.array([2.5, 2, 3,1]), 1.0, (0,0,255,0)))

triangletest = triangletest2

# Lighting Setup
lights = Lighting()
lights.addLight(np.array([0,0,5,1]), 1.75)
lights.ambientIntensity = 0.25

#triangles = [[(2,-2,0),(2,2,0), (-2,2,0)], [(2,-2,0), (-2,-2,0), (-2,2,0)],  #base
 #            [(2,-2,0),(2,2,0),(0,0,2)],
  #            [(-2,-2,0),(2,-2,0),(0,0,2)],
   #           [(-2,2,0),(-2,-2,0),(0,0,2)],
    #          [(-2,2,0),(2,2,0),(0,0,2)]] #faces

#trianglescolors = [pygame.Color(0,0,0,0), pygame.Color(0,0,0,0),
                    #pygame.Color(255,0,0,0), pygame.Color(0,255,0,0), pygame.Color(0,0,255,0), pygame.Color(125,125,125,0),]
#trianglesnew = [([Coordinate3D.from_3tuple(p) for p in triangles[i]],trianglescolors[i]) for i in range(len(triangles))]

# pygame setup
pygame.init()
screen = pygame.display.set_mode((aspectx, aspecty))
clock = pygame.time.Clock()
running = True
reRender = True

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

    if (reRender):
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("white")
        # RENDER YOUR GAME HERE
        # transform surface to render space
        # transform lights to render space
        for i in range(aspectx):
            for j in range(aspecty):
                origin, direction = cam.rayFromScreenCoordsNormalized(i / aspectx, j / aspecty)
                origin = origin.vec.flatten()
                direction = direction.vec.flatten()
                
                t, surf = triangletest.intersectRay(origin, direction)
                if t < float('inf'):
                    color = lights.computeColorBlinnPhong(origin + (t * direction), surf, direction, triangletest)
                    screen.set_at([aspectx - 1 - i,aspecty - 1 - j], pygame.Color(color[0],color[1],color[2],color[3]))

        # flip() the display to put your work on screen
        pygame.display.flip()
        reRender = False

    clock.tick(3)  # limits FPS to 60

pygame.quit()