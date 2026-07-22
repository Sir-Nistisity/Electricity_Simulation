import random

import numpy as np
import config as c
bounce_angle = np.radians(2)

def update():
    spawned = len(c.electron_x)

    direction = np.arctan2(c.electron_y_vel,
                           c.electron_x_vel)
    velocity = np.hypot(c.electron_y_vel, c.electron_x_vel)

    tile_x = (c.electron_x // 64).astype(int)
    tile_y = (c.electron_y // 64).astype(int)

    current_tile_conductivity = c.map_conductivity_array[tile_x, tile_y]
    bounce = np.random.random(len(c.electron_x)) > current_tile_conductivity

    direction = np.where(bounce, direction + np.pi + bounce_angle*(np.random.random()*0.5-0.25), direction)
    c.electron_x_vel = np.cos(direction) * velocity
    c.electron_y_vel = np.sin(direction) * velocity

    # electron repulsion
    dx = c.electron_x[:, None] - c.electron_x
    dy = c.electron_y[:, None] - c.electron_y

    dist2 = dx ** 2 + dy ** 2
    dist2[dist2 == 0] = 1

    force = 1 / dist2

    fx = np.sum(dx * force, axis=1)
    fy = np.sum(dy * force, axis=1)

    c.electron_x_vel += fx * 0.01
    c.electron_y_vel += fy * 0.01

    c.electron_x += c.electron_x_vel
    c.electron_y += c.electron_y_vel

    c.electron_x = c.electron_x % c.map_surface.get_width()
    c.electron_y = c.electron_y % c.map_surface.get_height()