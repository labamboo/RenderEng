# Test setup for user-input and drawing with pygame library
# TODO: handle triangles as solids vs triangles as flat surfaces for refraction
# TODO: light occlusion with refractive objects (shadow rays)
# TODO: amalgamated shadowRay test into intersectRay, probably bad form, need to fix later
import pygame

from geometry import *
from camera import *
from surface import *
from lighting import *
from texture import *

# Camera Setup
#cameratype = "Locked"
cam = Camera()
cam.setCamType("Perspective")
cam.renderSpace = "World"
cam.fov_max_view_distance = 25
    # regular camera parameters for turning to x axis
cam.SetCamera(0.0, 0.0, 0.0, 90.0, 0.0, 90.0)
cam.MoveAndRotateCamera(Dy = 4.0, Dz = -4.0)
cam.MoveAndRotateCamera(Dphi = 20.0)

aspectx = 256 #1280
aspecty = 144 #720


# surfaces
triangletest = Surface()
newsurface = Sphere(np.array([3, 7, 4,1]), 1.0, (255,0,0,0)) #[0] red sphere
newsurface.shadingKSpecular = 3.0
triangletest.addSurface(newsurface)

newsurface = Triangle(np.array([2,0,0,1]),np.array([6,-4,0,1]), np.array([6,0,4,1]), (125,0,125,0)) #[1] pyramid 1
newsurface.shadingKReflective = 0.5
triangletest.addSurface(newsurface)

newsurface = Triangle(np.array([2,0,0,1]),np.array([6,4,0,1]), np.array([6,0,4,1]), (0,125,125,0)) #[2] pyramid 2
newsurface.shadingKReflective = 0.5
triangletest.addSurface(newsurface)

newsurface = Triangle(np.array([6,4,0,1]),np.array([10,0,0,1]), np.array([6,0,4,1]), (0,125,0,0)) #[3] pyramid 3
newsurface.shadingKReflective = 0.5
triangletest.addSurface(newsurface)

newsurface = Triangle(np.array([10,0,0,1]),np.array([6,-4,0,1]), np.array([6,0,4,1]), (125,125,0,0)) #[4] pyramid 4
newsurface.shadingKReflective = 0.5
triangletest.addSurface(newsurface)

newsurface = Plane(np.array([-35,35,-0.25,1]), np.array([-35,-35,-0.25,1]), np.array([35,35,-0.25,1]), (125,125,125,0))# [4] planar floor
newsurface.texture = Checkerboard((125,125,125,0),(55, 55, 55, 0), 40, 40)
triangletest.addSurface(newsurface) 

triangletest.addSurface(Sphere(np.array([4.5, 3, 5,1]), 1.0, (0,255,0,0))) #[5] green sphere


triangletest.addSurface(Sphere(np.array([0.5, 3, 2,1]), 1.0, (0,0,255,0))) #[6] blue sphere

newsurface = Sphere(np.array([9, -8, 5,1]), 2, (50,50,50,0)) #mirror sphere [7]
newsurface.shadingKReflective = 0.8
newsurface.shadingKAmbient = 0.1
newsurface.shadingKDiffuse = 0.2
triangletest.addSurface(newsurface)

newsurface = Sphere(np.array([2, -2, 2.5,1]), 1.5, (20,20,20,0))#glass sphere [8]
# glass sphere parameters
newsurface.shadingKDiffuse = 0.0
newsurface.shadingKAmbient = 0.0
newsurface.shadingKSpecular = 1.0
newsurface.shadingKReflective = 0.3
newsurface.shadingKRefractive = 0.6
newsurface.snellRatio = 1.25
newsurface.shadowTransparency = 0.8
triangletest.addSurface(newsurface) 


# Lighting Setup
lights = Lighting()
lights.addLight(np.array([6,0,6,1]), 1.75)
lights.addLight(np.array([0,0,5,1]), 0.5)
lights.ambientIntensity = 0.05
lights.recursionDepth = 3


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
        screen.fill(color=(lights.background[0], lights.background[1], lights.background[2],0))
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
                    color = lights.computeColorWhitted(origin + (t * direction), surf, direction, triangletest)
                    screen.set_at([aspectx - 1 - i,aspecty - 1 - j], pygame.Color(color[0],color[1],color[2],0))

        # flip() the display to put your work on screen
        pygame.display.flip()
        reRender = False

    clock.tick(3)  # limits FPS to 60

pygame.quit()