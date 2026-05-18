# RenderEng
Building a rendering engine from scratch in Python with reference to Physically Based Rendering by Pharr, Jakob, and Humphreys. I plan to make iterations on the project, implementing more and more features as we go.<br>
I never took a graphics class, so this will be a fun learning experience. This is something of a pet project, so progress will probably be slow.

# Tech Stack
For starters, this project will be written in python with graphics done using the library pyopengl. This makes it easy to modify the code and add to it as needed.<br>
UPDATE: To accommodate user-input events, I have changed to the pygame library, which handles user input and drawing. This will hold as of version 0.2.

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
At this point I have started consulting an additional reference, Fundamentals of Computer Graphics by Marschner and Shirley. To do the more interesting stuff such as lighting and light-matter interactions, I will have to shift to a ray-tracing system. So, we shift gears to version 0.3, a ray-tracing system, to explore these effects. We will still use python and pygame for now, although we may need to include GPU programming at some point to speed-up the computations. As for our rasterization engine, we will return to it later for real-time rendering.

## Version 0.3: A Basic Ray Tracing System


