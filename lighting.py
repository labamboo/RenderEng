# Class to handle lighting
# Contains all lighting for a scene
# One scene should only have one Lighting object
# implements Blinn-Phong shading
# TODO: implement toRenderSpace transform
# TODO: colored lights
# TODO: when calculating light direction dot product surface normal, figure out effect of surface normal
# TODO: puzzle out a proper model for keeping track of light traveling medium (1. keep track of current medium snell ratio, 2. distinguish between back
#       and front side of a surface to distinguish between entering and exiting rays
# TODO: erroneous check for surface hit in reflection computation, should incorporate background color if no surface intersected.
# Reinhard tone mapping: 0-80% brightness occurs between values [0,4.0]
from surface import *

class Lighting:
    def __init__(self):
        self.lights = []
        self.ambientIntensity = 0.25
        self.tonemap = Lighting.ReinhardToneMap
        self.recursionDepth = 2
        self.secondaryRayOffset = 0.008
        self.background = np.array([0,0,0,0])

    # adds light
    def addLight(self, lightpos, brightness, color = None):
        self.lights.append((lightpos, brightness))

    # compute light intensity and color via Blinn-Phong shading
    def computeColorBlinnPhong(self, point, surf, viewdirection, surfOcclusion, notonemap = False):
        # compute secondary shadow rays
        # Blinn-Phong equation: k_aI_a + k_dI_l(N dot L) + K_sI_l(H dot N)
        # where H is halfway between view direction and light direction H = (L + V) / (||L + V||)
        # ambient light calculation
        shadowrayoffset = 0.005
        lighttotal = surf.shadingKAmbient * self.ambientIntensity
        # SHADOW RAY GENERATION
        for light in self.lights:
            # calculate light direction
            lightdirection = light[0] - point
            lightdistance = np.sqrt(np.sum(lightdirection ** 2))
            lightdirection = lightdirection / lightdistance
            # check for occlusion
            diminishmentFactor, surfdum = surfOcclusion.intersectRay(point, lightdirection, tmin = shadowrayoffset, tmax = lightdistance, shadowRay = True)
            if (diminishmentFactor > 0.0):
                #if not occluded (or only partially occluded), add diffuse / specular components
                surfaceNormal = surf.computeSurfaceNormal(point, viewdirection)
                lighttotal += surf.shadingKDiffuse * light[1] * max(np.dot(lightdirection, surfaceNormal), 0) * diminishmentFactor
                halfvector = lightdirection + viewdirection
                halfvector = halfvector / np.sqrt(np.sum(halfvector ** 2))
                lighttotal += surf.shadingKSpecular * light[1] * ((max(np.dot(halfvector, surfaceNormal), 0)) ** surf.shadingNSpecular) * diminishmentFactor
        # tone-mapping for brightness oversaturation (lighttotal is a scalar diminishment factor):
        if (notonemap):
            ans =  np.array(list(surf.colorAt(point))) * lighttotal
            return ans
        else:
            return self.tonemap(surf.colorAt(point), lighttotal)
    
    # compute color, including refractive and reflective rays
    def computeColorWhitted(self, point, surf, viewdirection, surfPrimary, depth = 0, decay = 1.0, shading = computeColorBlinnPhong, mediumSnell = 1.0):
        # recursion stop cases (account for recursion, limiting), also allow decay factor
        if depth >= self.recursionDepth or decay < 0.05:
            return self.background
        # compute blinn-phong color (BLINN-PHONG)
        surfaceColor = shading(self, point, surf, viewdirection, surfPrimary, True)
        # if surface is not transparent or reflective, return blinn-phong color
        # REFLECTION
        # if surface is reflective (refractive), cast secondary reflection (refraction) ray and combine weighted-linearly
        if surf.shadingKReflective > 0.0:
            reflectiondirection = surf.computeReflectionDirection(point, viewdirection)
            t, surfnew = surfPrimary.intersectRay(point, reflectiondirection, tmin = self.secondaryRayOffset)
            # if reflected ray hits surface, compute color there and multiply by KReflective of this surface
            if t < float('inf'):
                newColor = self.computeColorWhitted(point + (t * reflectiondirection), surfnew, 
                                                    reflectiondirection, surfPrimary, depth + 1, decay * surf.shadingKReflective, shading)
                ShadingKTotal = surf.shadingKAmbient + surf.shadingKDiffuse + surf.shadingKSpecular + surf.shadingKReflective
                surfaceColor = ((surf.shadingKReflective * np.array(list(newColor))) + np.array(list(surfaceColor)))/ ShadingKTotal
        # REFRACTION
        # if surface is reflective and refractive, cast two secondary rays and combine weighted-linearly
        if surf.shadingKRefractive > 0.0:
            refractiondirection = surf.computeRefractionDirection(point, viewdirection, snellRatioOther = mediumSnell, exiting = surf.isBackside(point, viewdirection))
            # check for total internal reflection (do nothing if totally reflected)
            if (type(refractiondirection) == np.ndarray):
                # propagate ray and find new surface hit
                t, surfnew = surfPrimary.intersectRay(point, refractiondirection, tmin = self.secondaryRayOffset)
                # if surface is hit, compute color there and add to total light detected, weighted by KRefractive of this surface.
                if t < float('inf'):
                    newColor = self.computeColorWhitted(point + (t * refractiondirection), surfnew, 
                                                        refractiondirection, surfPrimary, depth + 1, decay * surf.shadingKRefractive, shading)
                    ShadingKTotal = surf.shadingKAmbient + surf.shadingKDiffuse + surf.shadingKSpecular + surf.shadingKReflective + surf.shadingKRefractive
                    surfaceColor = ((surf.shadingKRefractive * np.array(list(newColor))) + np.array(list(surfaceColor)))/ ShadingKTotal
        # in recursion, also allow for decay factor between bounces (make decay factor dependent on distance traveled?)
        return self.tonemap(surfaceColor)


    @classmethod
    def ReinhardToneMap(cls, rgba):
        rgba = rgba / 20.0
        return (min(255,int(255 * rgba[0] / (1+rgba[0]))),
                min(255,int(255 * rgba[1] / (1+rgba[1]))),
                min(255,int(255 * rgba[2] / (1+rgba[2]))),
                0)
    