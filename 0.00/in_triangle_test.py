import numpy as np
def crossproduct2d(a,b):
    assert len(a) == 2
    assert len(b) == 2
    return (a[0] * b[1]) - (a[1] * b[0])

## check if point in 2D plane lies on a given triangle (including boundaries)
def in_triangle2d(triangle_points, given_point):
    tolerance = 0.01
    assert len(given_point) == 2
    assert len(triangle_points) == 3
    for point in triangle_points:
        assert len(point) == 2
    ## Method: using the method of cross products, checking if the point in question is the same direction with respect to all three edges of the triangle
    vecpoint = (given_point[0] - triangle_points[0][0], given_point[1] - triangle_points[0][1])
    vecedge = (triangle_points[1][0] - triangle_points[0][0], triangle_points[1][1] - triangle_points[0][1])
    a = crossproduct2d(vecedge, vecpoint)
    vecpoint = (given_point[0] - triangle_points[1][0], given_point[1] - triangle_points[1][1])
    vecedge = (triangle_points[2][0] - triangle_points[1][0], triangle_points[2][1] - triangle_points[1][1])
    b = crossproduct2d(vecedge, vecpoint)
    vecpoint = (given_point[0] - triangle_points[2][0], given_point[1] - triangle_points[2][1])
    vecedge = (triangle_points[0][0] - triangle_points[2][0], triangle_points[0][1] - triangle_points[2][1])
    c = crossproduct2d(vecedge, vecpoint)
    if (a <= tolerance and b <= tolerance and c <= tolerance):
        return True
    mtolerance = -1 * tolerance
    if (a >= mtolerance and b >= mtolerance and c >= mtolerance):
        return True
    return False

sample_count = 1000
rangex = 20
rangey = 20
# test case 1
triangle_points = [(0,0), (3,3), (3,0)]
randomizer = np.random.default_rng()
errors = 0
errorlog = []
for i in range(sample_count):
    scalrx = randomizer.uniform(0.0, 1.0)
    scalry = randomizer.uniform(0.0,1.0)
    point = (scalrx * 2 * rangex - rangex, scalry * 2 * rangey - rangey)
    result = in_triangle2d(triangle_points, point)
    ans = False
    if (point[0] >= 0 and point[0] <= 3 and point[1] <= point[0] and point[1] >= 0):
        ans = True
    if (result != ans):
        errors += 1
        errorlog += [(point, result)]
print("Errors: "+str(errors))
print(errorlog)


