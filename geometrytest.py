from geometry import *

# Test 1
print("Test 1.....")

testvec = Coordinate3D.from_coordinates(0,0,0,1)
print(testvec)
print(testvec.vec)

# Test 2
print("Test 2......")
mat1 = np.identity(4,float)
print("Rotate identity matrix 90 degrees (X axis)")
rotX = Transform3D.rotation_matrixX(90)

print(rotX.apply(mat1))
print("Rotate identity matrix 90 degrees (Y axis)")
rotY = Transform3D.rotation_matrixY(90)

print(rotY.apply(mat1))
print("Rotate identity matrix 90 degrees (Z axis)")
rotZ = Transform3D.rotation_matrixZ(90)

print(rotZ.apply(mat1))

# Test 3
print("Test 3")
scale = Transform3D.scaling_matrix(2,3,4)
print(scale.apply(mat1))

# Test 4
print("Test 4")
mat2 = np.array([[1.,0.,0.,0.],
                 [0.,1.,0.,0.],
                 [0.,0.,1.,0.],
                 [1.,1.,1.,1.]])
translate = Transform3D.translation_matrix(1,2,3)
print(translate.apply(mat2))

