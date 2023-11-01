import numpy as np
import os


matrix = np.load("./matrix_22_2.npy")

size = len(matrix)

x, y, z = [], [], []

limit = 500 + 22

for i in range(size):
    for j in range(size):
        if matrix[i, j] > limit:
            x.append(i)
            y.append(j)
            z.append(matrix[i, j])

np.savez("points", x=x, y=y, z=z)
np.savez_compressed("points_zip", x=x, y=y, z=z)

print(f"points      = {os.path.getsize('points.npz')}")
print(f"points_zip  = {os.path.getsize('points_zip.npz')}")
