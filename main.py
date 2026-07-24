import pygame
import os
import updater as upd
import numpy as np
import config
pygame.init()

screen = pygame.display.set_mode((640, 640), flags=16)
electron_surface = pygame.Surface(config.surface_size, pygame.SRCALPHA)
electron_surface.set_alpha(255)
clock = pygame.time.Clock()

# grid_size = 5, 5
electron_spawn_perc = 0.05

main_path = os.path.abspath(__file__)
project_path = os.path.dirname(main_path)
with open(f"{project_path}/build.txt") as file:
    data = np.array(file.read().replace("\n", "").split(), dtype=np.uint8)
    grid_size = tuple(data[0: 2])
    material_array = data[2:].reshape(grid_size)

tile_textures = []
for p in sorted(os.listdir(f"{project_path}/assets")):
    img = pygame.image.load(f"{project_path}/assets/{p}")
    img = pygame.transform.scale(img, (config.pixel_scalar, config.pixel_scalar))
    
    tile_textures .append(pygame.surfarray.array3d(img))
tile_textures = np.array(tile_textures)

def texture_grid_to_surface(texture_grid): # converts a 5D array into a pygame surface
    grid_array = np.array(texture_grid)

    combined = grid_array.transpose(1, 3, 0, 2, 4)
    combined = combined.reshape(
        combined.shape[0] * combined.shape[1],
        combined.shape[2] * combined.shape[3],
        3)

    return pygame.surfarray.make_surface(combined.swapaxes(0, 1))

def spawn(x, y): # spawns an electron with a random direction
    config.electron_x = np.append(config.electron_x, x)
    config.electron_y = np.append(config.electron_y, y)
    config.electron_x_vel = np.append(config.electron_x_vel, 0)
    config.electron_y_vel = np.append(config.electron_y_vel, 0)

    direction = np.random.random(len(config.electron_x)) * 2*np.pi
    speed = 5
    config.electron_x_vel = np.cos(direction) * speed
    config.electron_y_vel = np.sin(direction) * speed




def fade_surface(surface, amount=1): # subtracts the alpha channe60l
    alpha = pygame.surfarray.pixels_alpha(surface)
    np.subtract(alpha, amount, out=alpha, where=alpha >= amount)
    alpha[alpha < amount] = 0 
    del alpha

def post_init(): # init for during the first game tick
    config.map_conductivity_array = config.conductivity[config.map_array]
    
    #creates battery forces
    config.battery_map = np.zeros((grid_size[1], grid_size[0], 2))
    for y_idx in range(grid_size[1]):
        for x_idx in range(grid_size[0]):
            if config.map_array[y_idx, x_idx] == 1:
                for f_pos in [[2, 0], [-2, 0], [0, 2], [0, -2]]:
                    fx = f_pos[0]
                    fy = f_pos[1]
                     
                    alter_x = (x_idx + fx) % grid_size[0].astype(int)
                    alter_y = (y_idx + fy) % grid_size[1].astype(int)
                    
                    if config.map_array[alter_y, alter_x] == 2: 
                        config.battery_map[y_idx, x_idx] = np.array([fy, fx])
                        # config.battery_map[alter_y, alter_x] = np.array([fy, fx])

    adjust_scalar = np.array(config.surface_size) / np.array(grid_size * np.array(config.pixel_scalar))
    for y, row in enumerate(material_array):
        for x, material in enumerate(row):
            amount = max(int(config.conductivity[material] / electron_spawn_perc), 10)

            for i in range(amount):
                spawn((y * config.pixel_scalar + np.random.random() * config.pixel_scalar) * adjust_scalar[0],
                      (x * config.pixel_scalar + np.random.random() * config.pixel_scalar) * adjust_scalar[1])
                    
tick = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    # electron_surface.fill((0, 0, 0, 0))
    tick += 1

    fade_surface(electron_surface, 255)

    config.mouse_x, config.mouse_y = pygame.mouse.get_pos()

    texture_grid = tile_textures[material_array]
    #surface = texture_grid_to_surface(texture_grid)
    surface = pygame.transform.scale(texture_grid_to_surface(texture_grid), config.surface_size)
    config.map_surface = surface
    config.map_array = material_array
    if tick == 1: post_init()

    upd.update(1) # updates electrons
    for x, y in zip(config.electron_x, config.electron_y):
        pygame.draw.circle(electron_surface, (50, 50, 255, 255), (x, y), 5)
        
    screen.blit(surface, (0, 0))
    screen.blit(electron_surface, (0, 0))

    #if config.battery_map[config.mouse_x//config.pixel_scalar][config.mouse_y//config.pixel_scalar]: 0
    pygame.display.flip()
    # clock.tick(60)
pygame.quit()