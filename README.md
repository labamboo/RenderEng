# RenderEng
Building a rendering engine from scratch in Python with reference to Fundamentals of Computer Graphics by Marschner and Shirley and additional reference to Scratchapixel. I plan to make iterations on the project, implementing more and more features as we go.<br>
I never took a graphics class, so this will be a fun learning experience. This is something of a pet project, so progress will probably be slow.

# Tech Stack
For starters, this project will be written in python with graphics done using the library pyopengl. This makes it easy to modify the code and add to it as needed.<br>
UPDATE: To accommodate user-input events, I have changed to the pygame library, which handles user input and drawing. This will apply as of version 0.2.

# Version 0.1: 3D Geometry
Starting with a barebones model with a fixed camera, we start off using a fairly intuitive nonhomogeneous coordinate system. This however requires us to use a clunky plane-ray intersection function to perform the perspective transform. In the second iteration we make our fixed camera pannable. In the third iteration we get rid of the plane-ray intersection function for the more elegant homogeneous coordinate system and the perspective transform.

## the bare-bones (version 0.11)
Create a bare-bones rendering model with only triangular surfaces (tuples of 3 points), rendered by simple ray projection. No support for movement.<br>
<b>Iteration 1<b>: This first iteration will not track any information about the objects being rendered including, crucially, depth. It also maps each pixel of the image frame to a ray, which means we need to be able to adjust the rendered image at the pixel level. This can't be done with opengl, so we will use opencv instead.<br>

Improvements to-do: <br>
- map triangles onto the image frame instead of vice versa
- use drawcalls for lines and polygons instead of pixel changes (one layer of abstraction up), use opengl drawing instead of opencv pixel functions
- add a z-buffer to allow for overlapping objects
- systematize vectors in 2d and 3d space by defining vector objects and matrix transforms, associated addition/subtraction, dot/cross product, projections, coordinate systems
- better methods to keep track of pixel coordinates, built in functions for this purpose
- use projection matrices, because calculating all the vectors individually with dot and cross products is exhausting

## Part 2: Improved Geometry Capabilities (version 0.12)
Expand the geometry library to incorporate object-oriented programming. Vectors are now objects, with associated methods for subtraction, addition, dot/cross products, scalar multiplication. Incorporate reference frames as objects, and have methods for transforms between them. Vectors use global coordinates by default, but can be transformed to other reference frames. Objects are now mapped to the image instead of vice versa. Instead of directly setting pixel values (with opencv), drawing is done with opengl functions. Incorporate movements: camera panning, camera movement, zoom.<br>

Improvements to-do: <br>
- make the camera axes attached to the camera, instead of the image plane (the way it is right now makes rotations a bit weird)
- perspective transform is currently implemented with the intersection function of the ProjectivePlane class, which is clunky.
- Having no distinction between points and vectors is also clunky
- While homogeneous coordinate geometry is more unintuitive, it is much more elegant. Which is why we will be using it in the next iteration.
- Still need to implement z-buffer and object overlap
- Still need to implement 3d transforms between reference frames (only the 2d projective plane so far)

## Version 0.2: Abstraction Layers and the Camera Model. 
At this point I have decided to change gears and use Physically Based Rendering by Pharr, Jakob, and Humphreys as a reference. Most of the functionality in the first iterations consists the core of the Camera class as defined in PBRT Chapter 5, specifically the Perspective-Projection Camera class that uses Camera-Space for Rendering and rasterization methods. We will now rewrite this code with modularity and abstraction in mind.<br>
We implement PBRT's Camera class, allowing us to focus on more advanced rendering techniques later on by building on the core functionality of this class.<br>
At this point we have completed a crude rasterization engine. It has no clipping nor Z-buffer but it can render some basic shapes. To be able to use it without occlusion capabilities we draw only wireframe shapes, and we can view them in both orthographic and perspective views, and pan around to different angles. NOTE: The main entrypoint is pygametest, not main.<br>
Note: I have realized that Physically Based Rendering features some pretty advanced graphics ideas, so I will start with a more fundamental text for graphics, Fundamentals of Computer Graphics by Marschner and Shirley, while also referencing the very organized material on Scratchapixel. Hopefully in the future once I am familiar with the more fundamental graphics topics I will be able to return to Physically Based Rendering.<br>
To do the more interesting stuff such as lighting and light-matter interactions, I will have to shift to a ray-tracing system. So, we shift gears to version 0.3, a ray-tracing system, to explore these effects. We will still use python and pygame for now, although I may need to include GPU programming at some point to speed-up the computations. As for our rasterization engine, we will return to it later for real-time rendering.
<img src="demos/version 0.20 demo.png" alt="Version 0.20 demo image">
<img src="demos/version 0.20 demo2.png" alt="Version 0.20 demo image"><br>

## Version 0.3: A Basic Ray Tracing System
Note: Working on the functions for ray-tracing rendering, I find myself writing a wrapper for numpy's dot product and cross product and think to myself: this Coordinate3D class I've created is clunky and outright terrible. Besides format validation, it serves no real purpose, and if I used bare numpy arrays instead, it would be simpler and less memory intensive. So, that is what I will do. Most format validation doesn't need to be done for every vector operation anyway, so I think I will just bake it into a higher level, like when instances are created, or wherever else necessary. Also, I'd like to speed up the pace a bit, so I will be putting a bit more time into this project, at least for a week or two.<br>
Note 2: The entry point for this version is in raytracertest.py <br>
<img src="demos/version 0.30 demo.png" alt="Version 0.30 demo image">

### Version 0.31: Blinn-Phong Shading and Spheres
Now that we have a functional visibility framework for ray-tracing, we can move on to the more interesting shading portion. I will first implement the Blinn-Phong light reflection model for opaque surfaces. This will make the objects look a bit more realistic, instead of being solid bright blobs of color. To showcase the Blinn-Phong light model I will also implement Spheres as surfaces that can be added. In the future I hope to explore the more modern models for light transport, such as BRDF, Cook-Torrance, and physically based rendering (time allowing). <br>
To handle saturation of brightness values, we will use Reinhard tone-mapping.<br>
The images below demonstrate the model: on the left is a 256x144 resolution image, the right 1280x720<br>
<img src="demos/version 0.31 demo.png" alt="Version 0.31 demo image">
<img src="demos/version 0.31 demo2 highres.png" alt="Version 0.31 demo image high resolution (1280x720)">
<br>
There are still some bugs, one of the obvious ones being the diffuse lighting showing up on both sides of the sphere instead of only the illuminated side.<br>
Bug Fix 1: shadow ray propagation often detects intersections with the originating surface. I originally hacked a solution where the ray origin would be displaced slightly off the surface, but Marschner and Shirley detail a better workaround with using a lower-bound for t in the ray-intersection algorithm (Section 4.5.3). (This method is known as "shadow bias" and is also used in rasterization shadow maps.)<br>
Bug Fix 2: diffuse lighting showing up on both sides of the sphere (because I used absolute value of the dot product instead of a minimum cap at 0). Changed it to the capped version, but now the surface normals are behaving badly, causing faces exposed to light instead being dark.<br>
Bug Fix 3: surface normal implementation right now does not depend on viewing direction. This makes it so surfaces can only be illuminated if the light is on the "front" side, and light illuminating the "back" side will not function properly. Fixed by incorporating viewing direction into the surface normal computation, so that the surface normal will be on the face being viewed.<br>

### Version 0.32: Whitted-Style Shading (Reflection/Refraction) and Checkerboards
As planned, this version will incorporate reflection and refraction properties, and try to replicate Turner Whitted's iconic 1980 image featuring these two aspects of light-matter interaction. To make a proper recreation of the image, I will also incorporate the ability to render a checkerboarded surface for the ground. As I'm sure the checkerboard pattern will introduce considerable aliasing, the plan is for the next section to tackle anti-aliasing methods (although if rendering times take far too long I may tackle parallel rendering and GPU programming first).<br>
For transparent and semi-transparent objects, we need to take into account that light is not fully blocked by them and therefore any shadows cast are either fully nonexistent or attenuated. Essentially shadow rays are attenuated by the objects instead of fully blocked.<br>
For reflection, we simply cast a reflection (specular) ray. There should be some dimming of the reflected light, and if the material is not fully reflective then compose the object color with the reflected light color.<br>
Finally, for the checkerboard we need to implement procedural texturing. <br>
Note: I originally planned to incorporate Fresnel splitting into this version, but seeing as its a bit more advanced I will save that for later. I will simply use constant material coefficients for reflection and refraction. <br>
Issue: There was a bug in the tone-mapping of 0.31, where the total light scale factor was applied after tone-mapping instead of before. Fixing it causes coloring of all the surfaces to become oversaturated. So, I may as well take this chance to set up a proper system for determining color values. Color values will be changed to numpy arrays as well, and they will range over all real numbers, represented by floats. Before drawing the pixel values to a screen color values will be tone-mapped using a function (currently Reinhard tone-mapping). Furthermore when calculating reflections, I will normalize the total brightness by the sum of coefficients k (shadingKAmbient, shadingKDiffuse, shadingKSpecular, shadingKReflection, shadingKRefraction)<br>
Bug Fix 1: shadow rays are completely obstructed by transparent objects. For now, I won't calculate shadow-ray refraction but rather just decrease the light by a multiplier for each transparent surface crossed, this also means shadow-ray light will pass in a straight-line fashion through transparent objects.<br>
Note 2: To implement the checkerboard pattern, I will add a function to all surfaces that returns the color at any given point. I will also create a new class, Texture, that returns a color for a given texture coordinate. The function in Surface will compute texture coordinates and call its Texture to return a color.<br>
Issue: Should I return u,v coordinates when the surface intersection is originally computed? For triangles and quadrilateral surfaces at least, this would save a redundant computation of u and v. I will kick this question down the road for now. If this becomes a problem later, I can optimize for it.<br>
Bug: checkerboard pattern only seems to work properly for even numbers<br>
The completed version is demo-ed below, in low-resolution (256x144) and high-resolution (1280x720) (I say "completed but there are still some bugs). With everything we have here, we can produce a recreation of a Whitted-Style graphics rendering, minus the anti-aliasing, which I will tackle later. The high-res image took about 4.5 minutes to render on my computer, so I will probably need to tackle parallelization very soon.<br>
<img src="demos/version 0.32 demo.png" alt="Version 0.32 demo image">
<img src="demos/version 0.32 demo highres.png" alt="Version 0.32 demo image high resolution (1280x720)">
<br>


Future topics to be explored: Monte Carlo integration and distributed ray-tracing, global illumination models, HDR (high dynamic range) rendering and tone mappers, anti-aliasing, parallel optimization and GPU programming, Post-Processing Effects, Gouraud (smooth) shading, BRDF and Lighting (including light intensity spherical falloff), shadow maps (shadows in rasterization), automatic computation of shadow-bias, Fresnel shading


