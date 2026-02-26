# Camera.py file
# PBRT Chapter 5
# Handles transforms between
# three spaces: camera space, world space,
# and camera-world space
# One of these is designated the rendering space.

# For simplicity I will only implement the camera space
# as the rendering space, since we have been using a rasterization
# renderer up to this point. 
# *In future iterations I will either improve this rasterization
#  renderer or move to ray-tracing renderers, undecided for now.
# Also, for now I will only implement the perspective camera format
# This iteration with PBRT as reference will enable depth
# differentiation in our image.

# Functions the camera must handle
# 1) for raster-based rendering, a function that maps a point
# in world space to a point in screen space
# - this is done in two stages, first world space to NDC, and then
#   from NDC to raster space
#

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
    # 
