import numpy as np
import config as c
bounce_angle = np.radians(90)
half_pi = np.pi/2

def update(substeps):
    step = 1/substeps
    for i in range(max(substeps, 1)):
        spawned = len(c.electron_x)
        # getting data
        direction = np.arctan2(c.electron_y_vel,
                               c.electron_x_vel)
        velocity = np.hypot(c.electron_y_vel, c.electron_x_vel)

        tile_x = (c.electron_x // 64).astype(int)
        tile_y = (c.electron_y // 64).astype(int)

        current_tile_conductivity = c.map_conductivity_array[tile_x, tile_y]

        # bouncing
        bounce = np.random.random(spawned) > (current_tile_conductivity)
        loss = np.where(bounce, 0, 1)

        direction = np.where(bounce, direction + np.pi + bounce_angle*(np.random.random(spawned)*0.5-0.25), direction)
        c.electron_x_vel = np.cos(direction) * velocity * loss
        c.electron_y_vel = np.sin(direction) * velocity * loss

        # battery handeling
        forces = c.battery_map[tile_x, tile_y]

        c.electron_x += forces[:, 0] * c.pixel_scalar
        c.electron_y += forces[:, 1] * c.pixel_scalar

        # electron repulsion
        dx = c.electron_x[:, None] - c.electron_x
        dy = c.electron_y[:, None] - c.electron_y

        dist2 = dx ** 2 + dy ** 2
        dist2[dist2 == 0] = 1

        force = np.where(dist2 < 250, 1 / dist2, 0)

        fx = np.sum(dx * force, axis=1)
        fy = np.sum(dy * force, axis=1)

        c.electron_x_vel += fx * 1 * step
        c.electron_y_vel += fy * 1 * step

        c.electron_x += c.electron_x_vel * step
        c.electron_y += c.electron_y_vel * step

        c.electron_x = c.electron_x % c.map_surface.get_width()
        c.electron_y = c.electron_y % c.map_surface.get_height()