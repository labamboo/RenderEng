# Camera.py file
# PBRT Chapter 5
# Handles transforms between
# three spaces: camera space, world space,
# and camera-world space
# One of these is designated the rendering space.

# For now, we will use this camera to replicate the primitive ray-tracer
# and rasterization-based renderers from 0.1 and 0.2 of this project.
# *In future iterations I will probably improve both, undecided for now.
# Also, for now I will only implement the perspective camera format
# This iteration with PBRT as reference will enable depth
# differentiation in our image, which the previous ones did not.

# Functions the camera must handle
# 1) for raster-based rendering, a function that maps a point
#    in world space to a point in screen space (camera space, which is then
#    mapped to a point on the screen)
# - this is done in two stages, first world space to rendering space,
#   then rendering space to camera space
# 2) for ray-tracing renderers, a function that maps a point in screen
#    space to a ray in world space.
# = this can be done in any number of stages


class Camera:
    # camera type
    type = "Perspective"

    # Constructor
    def __init__(this):
        return
    # function 1: world to NDC
    # required variables:
    # - world to camera-world space transform matrix
    # (aka camera translation matrix)
    # - camera rotation matrix
    # if using camera/camera-world space as rendering space,
    # transformation mapping world to rendering space.
    # essentially, if the rendering space is not world-space,
    # the rendering space functions as a pseudo world space,
    # and ideally these objects are static. However if the camera is moving around
    # the rendering space itself is moving around, and by necessity locations of objects
    # are animated.
    # pbrt Chapter 5 camera transform: when it says the worldfromrender
    # transform cannot be animated, it means that the matrix itself cannot
    # be animated, not that the objects within the rendering space cannot be
    # moving around. The performance hit that might result comes from the
    # intensive computations involved in transform interpolation (chapter 3),
    # not from the computations of transforming objects into rendering space.
    # the worldfromrender matrix itself, of course, changes with camera position/rotation