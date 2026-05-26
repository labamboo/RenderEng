# Class to handle lighting
# Contains all lighting for a scene
# One scene should only have one Lighting object
# implements Blinn-Phong shading
# TODO: implement toRenderSpace transform
# TODO: colored lights
# TODO: when calculating light direction dot product surface normal, figure out effect of surface normal
# Reinhard tone mapping: 0-80% brightness occurs between values [0,4.0]
from surface import *

class Lighting:
    def __init__(self):
        self.lights = []
        self.ambientIntensity = 0.25
        self.tonemap = Lighting.ReinhardToneMap

    # adds light
    def addLight(self, lightpos, brightness, color = None):
        self.lights.append((lightpos, brightness))

    # compute light intensity and color via Blinn-Phong shading
    def computeColorBlinnPhong(self, point, surf, viewdirection, surfOcclusion):
        # compute secondary rays 
        # Blinn-Phong equation: k_aI_a + k_dI_l(N dot L) + K_sI_l(H dot N)
        # where H is halfway between view direction and light direction H = (L + V) / (||L + V||)
        # ambient light calculation
        lightocclusionoffset = 0.005
        lighttotal = surf.shadingKAmbient * self.ambientIntensity
        for light in self.lights:
            # calculate light direction
            lightdirection = light[0] - point
            lightdistance = np.sqrt(np.sum(lightdirection ** 2))
            lightdirection = lightdirection / lightdistance
            # check for occlusion
            minocclusion, surfdum = surfOcclusion.intersectRay(point + lightdirection * lightocclusionoffset, lightdirection)
            if (minocclusion > lightdistance):
                #if not occluded, add diffuse / specular components
                # TODO: single/double-facedness check? for now, using abs to disregard facedness
                surfaceNormal = surf.computeSurfaceNormal(point)
                lighttotal += surf.shadingKDiffuse * light[1] * np.abs(np.dot(lightdirection, surfaceNormal))
                halfvector = lightdirection + viewdirection
                halfvector = halfvector / np.sqrt(np.sum(halfvector ** 2))
                lighttotal += surf.shadingKSpecular * light[1] * ((max(np.dot(halfvector, surfaceNormal), 0)) ** surf.shadingNSpecular)
        # tone-mapping for brightness oversaturation:
        return self.tonemap(surf.color, lighttotal)


    @classmethod
    def ReinhardToneMap(cls, rgba, multiplier):
        return (min(255,int(255 * rgba[0] * multiplier / (1+rgba[0]))),
                min(255,int(255 * rgba[1] * multiplier / (1+rgba[1]))),
                min(255,int(255 * rgba[2] * multiplier / (1+rgba[2]))),
                rgba[3])