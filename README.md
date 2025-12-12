# RenderEng
Building a rendering engine from scratch using first principles. I plan to make iterations on the project, implementing more and more features as we go.<br>
I never took a graphics class, so this will be a fun learning experience. This is something of a pet project, so progress will probably be slow.

# Tech Stack
For starters, this project will be written in python with graphics done using the library pyopengl. This makes it easy to modify the code and add to it as needed.

# Chapter 1: 3D Geometry
Starting with a barebones model with a fixed camera, we start off using a fairly intuitive nonhomogeneous coordinate system. This however requires us to use a clunky plane-ray intersection function to perform the perspective transform. In the second iteration we make our fixed camera pannable. In the third iteration we get rid of the plane-ray intersection function for the more elegant homogeneous coordinate system and the perspective transform.

## Part 1: the bare-bones (version 0.1)
Create a bare-bones rendering model with only triangular surfaces (tuples of 3 points), rendered by simple ray projection. No support for movement.<br>
<b>Iteration 1<b>: This first iteration will not track any information about the objects being rendered including, crucially, depth. It also maps each pixel of the image frame to a ray, which means we need to be able to adjust the rendered image at the pixel level. This can't be done with opengl, so we will use opencv instead.<br>

Improvements to-do: <br>
- map triangles onto the image frame instead of vice versa
- use drawcalls for lines and polygons instead of pixel changes (one layer of abstraction up), use opengl drawing instead of opencv pixel functions
- add a z-buffer to allow for overlapping objects
- systematize vectors in 2d and 3d space by defining vector objects and matrix transforms, associated addition/subtraction, dot/cross product, projections, coordinate systems
- better methods to keep track of pixel coordinates, built in functions for this purpose
- use projection matrices, because calculating all the vectors individually with dot and cross products is exhausting

## Part 2: Improved Geometry Capabilities (version 0.2)
Expand the geometry library to incorporate object-oriented programming. Vectors are now objects, with associated methods for subtraction, addition, dot/cross products, scalar multiplication. Incorporate reference frames as objects, and have methods for transforms between them. Vectors use global coordinates by default, but can be transformed to other reference frames. Objects are now mapped to the image instead of vice versa. Instead of directly setting pixel values (with opencv), drawing is done with opengl functions. Incorporate movements: camera panning, camera movement, zoom.<br>

Improvements to-do: <br>
- make the camera axes attached to the camera, instead of the image plane (the way it is right now makes rotations a bit weird)
- bug where the intersection detection catches objects directly behind you
- perspective transform is currently implemented with the intersection function of the ProjectivePlane class, which is clunky.
- Having no distinction between points and vectors is also clunky
- While homogeneous coordinate geometry is more unintuitive, it is much more elegant. Which is why we will be using it in the next iteration.
- Still need to implement z-buffer and object overlap
- Still need to implement 3d alternative reference frames (only the 2d projective plane so far)

