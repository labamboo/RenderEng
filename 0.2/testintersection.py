from math import sqrt

## computes dot product
def dotproduct(a, b):
    assert len(a) == len(b)
    assert len(a) > 0
    sum = 0.0
    for i in range(len(a)):
        sum += a[i] * b[i]
    return sum
    
## computes cross product
def crossproduct(a,b):
    assert len(a) == 3
    assert len(b) == 3
    x = (a[1] * b[2]) - (a[2] * b[1])
    y = (a[2] * b[0]) - (a[0] * b[2])
    z = (a[0] * b[1]) - (a[1] * b[0])
    return (x,y,z)

# Computes 2d cross product, which is a scalar
def crossproduct2d(a,b):
    assert len(a) == 2
    assert len(b) == 2
    return (a[0] * b[1]) - (a[1] * b[0])

# computes magnitude of a vector
def magnitude(a):
    return sqrt(dotproduct(a,a))

# Computes vector difference
# for 2d and 3d vectors only
def vectordifference(a, b):
    assert len(a) == len(b), "vectors have different lengths!"
    assert len(a) == 2 or len(a) == 3, "this function only accepts 2d or 3d vectors"
    if (len(a) == 2):
        return (a[0] - b[0], a[1] - b[1])
    else:
        return (a[0] - b[0], a[1] - b[1], a[2] - b[2])
    

# Computes vector sum
# for 2d and 3d vectors only
def vectorsum(a, b):
    assert len(a) == len(b), "vectors have different lengths!"
    assert len(a) == 2 or len(a) == 3, "this function only accepts 2d or 3d vectors"
    if (len(a) == 2):
        return (a[0] + b[0], a[1] + b[1])
    else:
        return (a[0] + b[0], a[1] + b[1], a[2] + b[2])
  
# Normalizes vector to magnitude 1
# for 2d and 3d vectors only
def vectornormalized(a):
    assert len(a) == 2 or len(a) == 3, "this function only accepts 2d or 3d vectors"
    mag = magnitude(a)
    if (len(a) == 2):
        return (a[0] / mag, a[1] / mag)
    else:
        return (a[0] / mag, a[1] / mag, a[2] / mag)
    
# Computes scalar product of a vector
# for 2d and 3d vectors only
def vectorscalarproduct(c, vec):
    assert len(vec) == 2 or len(vec) == 3, "this function only accepts 2d or 3d vectors"
    if (len(vec) == 2):
        return (c * vec[0], c * vec[1])
    else:
        return (c * vec[0], c * vec[1], c * vec[2])


from geometry import *


focus = (0,0,0)

def intersectionpoint(ray_o, ray_dir, triangle_points, debug = False):
    new_triangle_points = [(0,0)]
    origin3d = triangle_points[0]
    xaxisvec = vectordifference(triangle_points[1], origin3d)
    xaxismag = magnitude(xaxisvec)
    xaxisvec = vectornormalized(xaxisvec)
    thirdvec = vectordifference(triangle_points[2], origin3d)
    new_triangle_points += [(xaxismag, 0)]
    thirdvecx = dotproduct(thirdvec,xaxisvec)
    thirdvecxcomp = vectorscalarproduct(thirdvecx, xaxisvec)
    yaxisvec = vectordifference(thirdvec, thirdvecxcomp)
    yaxismag = magnitude(yaxisvec)
    yaxisvec = vectornormalized(yaxisvec)
    thirdvecy = yaxismag
    # define y axis to be normal component of third edge wrt x axis edge
    new_triangle_points += [(thirdvecx, thirdvecy)]
    trianglenorm = crossproduct(xaxisvec, yaxisvec)
    if (debug):
        print(dotproduct(trianglenorm, trianglenorm))
    # eq of ray is (x,y,z) = (ox,oy,oz) + (tux,tuy,tuz)
    # eq of plane is (x-x0)nx + (y-y0)ny + (z-z0)nz = 0
    # point satisfying both is the intersection, x' = ox + tux, y' = oy + tuy, z' = oz + tuz
    # nx(ox + tux) + ny(oy + tuy) + nz(oz + tuz) = nx(x0) + ny(y0) + nz(z0)
    # nx(tux) + ny(tuy) + nz(tuz) = nx(x0 - ox) + ny(y0 - oy) + nz(z0 - oz)
    # t = nx(x0 - ox) + ny(y0 - oy) + nz(z0 - oz) / (nxux + nyuy + nzuz)
    # note: answer does not exist if (nxux + nyuy + nzuz) = 0, or if t is negative (because ray goes in one direction only)
    if (dotproduct(trianglenorm, ray_dir) == 0):
        return False
    t = trianglenorm[0] * (origin3d[0] - ray_o[0])
    t += trianglenorm[1] * (origin3d[1] - ray_o[1])
    t += trianglenorm[2] * (origin3d[2] - ray_o[2])
    t = t / dotproduct(trianglenorm, ray_dir)
    if (t <= 0.01):
        return False
    intersection_point3d = vectordifference(vectorsum(ray_o, vectorscalarproduct(t, ray_dir)), origin3d)
    intersection_pointx = dotproduct(intersection_point3d, xaxisvec)
    intersection_pointy = dotproduct(intersection_point3d, yaxisvec)

    intersection_point = (intersection_pointx,intersection_pointy)
    return intersection_point


point1 = Vector3d(0,0,0)
point2 = Vector3d(0,2,2)
point3 = Vector3d(-2,5,7)
plane = ProjectionPlane.from_vectors(point1, point2.difference(point1), point3.difference(point1))
