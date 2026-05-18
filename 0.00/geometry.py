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
    

    
