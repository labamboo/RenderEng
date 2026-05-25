from surface import *
triangletest = Triangle(np.array([2,-2,0,1]),np.array([2,2,0,1]), np.array([2,2,2,1]))
print(triangletest.intersectRay(np.array([0,0,0.5,1]), np.array([1,0,0,0])))