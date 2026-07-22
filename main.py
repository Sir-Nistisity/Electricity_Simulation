import pygame
import os
import updater as upd
import numpy as np
import config
pygame.init()

screen = pygame.display.set_mode((640, 640), flags=16)
electron_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
clock = pygame.time.Clock()

# grid_size = 5, 5
pixel_scalar = 64
electron_spawn_perc = 0.025

main_path = os.path.abspath(__file__)
project_path = os.path.dirname(main_path)
with open(f"{project_path}/build.txt") as file:
    data = np.array(file.read().replace("\n", "").split(), dtype=np.uint8)
    grid_size = tuple(data[0: 2])
    material_array = data[2:].reshape(grid_size)

tile_textures = []
for p in sorted(os.listdir(f"{project_path}/assets")):
    img = pygame.image.load(f"{project_path}/assets/{p}")
    img = pygame.transform.scale(img, (pixel_scalar, pixel_scalar))
    
    tile_textures .append(pygame.surfarray.array3d(img))
tile_textures = np.array(tile_textures)

def texture_grid_to_surface(texture_grid):
    grid_array = np.array(texture_grid)

    combined = grid_array.transpose(1, 3, 0, 2, 4)
    combined = combined.reshape(
        combined.shape[0] * combined.shape[1],
        combined.shape[2] * combined.shape[3],
        3)

    return pygame.surfarray.make_surface(combined.swapaxes(0, 1))

def spawn(x, y):
    config.electron_x = np.append(config.electron_x, x)
    config.electron_y = np.append(config.electron_y, y)
    config.electron_x_vel = np.append(config.electron_x_vel, 0)
    config.electron_y_vel = np.append(config.electron_y_vel, 0)

    direction = np.random.random(len(config.electron_x)) * 2*np.pi
    speed = 5
    config.electron_x_vel = np.cos(direction) * speed
    config.electron_y_vel = np.sin(direction) * speed

for y, row in enumerate(material_array):
    for x, material in enumerate(row):
        amount = int(config.conductivity[material] / electron_spawn_perc)

        for i in range(amount):
            spawn(y * pixel_scalar + np.random.random()*pixel_scalar, x * pixel_scalar + np.random.random()*pixel_scalar)


def rgb_alpha_to_surface(rgb_obj, alpha_obj):
    rgba = np.dstack((rgb_obj, alpha_obj))

    return pygame.image.frombuffer(
        rgba.tobytes(),
        rgba.shape[1::-1],
        "RGBA"
    )

# blank_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

tick = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    # electron_surface.fill((0, 0, 0, 0))
    tick += 1

    last_rgb = np.copy(rgb)
    rgb = pygame.surfarray.array3d(electron_surface)

    config.mouse_x, config.mouse_y = pygame.mouse.get_pos()

    texture_grid = tile_textures[material_array]
    surface = texture_grid_to_surface(texture_grid)
    config.map_surface = surface
    config.map_array = material_array
    if tick == 1:
        config.map_conductivity_array = config.conductivity[config.map_array]

    upd.update() # updates electrons
    for x, y in zip(config.electron_x, config.electron_y):
        pygame.draw.circle(electron_surface, (50, 50, 255, 200), (x, y), 5)

    screen.blit(surface, (0, 0))
    screen.blit(electron_surface, (0, 0))

    # print(config.map_array[config.mouse_x//pixel_scalar][config.mouse_y//pixel_scalar])
    pygame.display.flip()
    clock.tick(60)
pygame.quit()