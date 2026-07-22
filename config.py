import numpy as np

materials = [
"air.png",
"battery_neg.png",
"battery_pos.png",
"copper.png",
"insl.png"]
conductivity = np.array([
    0.04,  # air
    1.0,  # battery_neg
    1.0,  # battery_pos
    1.0,  # copper
    0.001   # insl
])

map_surface = None
map_array = None
map_conductivity_array = None

electron_x = np.array([])
electron_y = np.array([])
electron_x_vel = np.array([])
electron_y_vel = np.array([])