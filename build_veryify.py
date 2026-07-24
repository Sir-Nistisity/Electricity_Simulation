import os
import numpy as np
import runpy

main_path = os.path.abspath(__file__)
project_path = os.path.dirname(main_path)
with open(f"{project_path}/build.txt") as file:
    data = np.array(file.read().replace("\n", "").split(), dtype=int)
    grid_size = tuple(data[0: 2])
    grid_size = int(grid_size[0]), int(grid_size[1])
    
    material_array = data[2:]

print(f"Found at \"{project_path}/build.txt\"")
print(f"Detected grid size of {grid_size}")
print(f"Expected length: {grid_size[0] * grid_size[1]}")
print(f"Data length: {len(material_array)}")
print("Status: ", end = "")
if (grid_size[0] * grid_size[1]) == len(material_array):
    print("Ready!")
else:
    print("Not Ready!")
    print("+" if (grid_size[0] * grid_size[1]) < len(material_array) else "", end=f"{len(material_array) - (grid_size[0] * grid_size[1])}\n")