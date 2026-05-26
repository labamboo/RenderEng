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

## Version 0.3: A Basic Ray Tracing System
Note: Working on the functions for ray-tracing rendering, I find myself writing a wrapper for numpy's dot product and cross product and think to myself: this Coordinate3D class I've created is clunky and outright terrible. Besides format validation, it serves no real purpose, and if I used bare numpy arrays instead, it would be simpler and less memory intensive. So, that is what I will do. Most format validation doesn't need to be done for every vector operation anyway, so I think I will just bake it into a higher level, like when instances are created, or wherever else necessary. Also, I'd like to speed up the pace a bit, so I will be putting a bit more time into this project, at least for a week or two.<br>
Note 2: The entry point for this version is in raytracertest.py <br>
<img src="demos/version 0.30 demo.png" alt="Version 0.30 demo image">

### Version 0.31
Now that we have a functional visibility framework for ray-tracing, we can move on to the more interesting shading portion. I will first implement the Blinn-Phong light reflection model for opaque surfaces. This will make the objects look a bit more realistic, instead of being solid bright blobs of color. To showcase the Blinn-Phong light model I will also implement Spheres as surfaces that can be added. In the future I hope to explore the more modern models for light transport, such as BRDF, Cook-Torrance, and physically based rendering (time allowing). <br>
To handle saturation of brightness values, we will use Reinhard tone-mapping.<br>
Looking ahead, the plan for now is for 0.32 to explore reflection and refraction and maybe try to replicate Turner Whitted's iconic 1980 image featuring these two aspects of light-matter interaction.<br>
<img src="demos/version 0.31 demo.png" alt="Version 0.31 demo image">
<img src="demos/version 0.31 demo2.png" alt="Version 0.31 demo image">

Future topics to be explored: Monte Carlo integration and distributed ray-tracing, global illumination models, HDR (high dynamic range) rendering and tone mappers.



[def]: demos/'version 0.30 demo'