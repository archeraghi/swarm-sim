import random
import lib.header as header

def generating_random_spraded_particles (world, max_size_particle):
    for _ in range(0, max_size_particle):
        x = random.randrange(-world.get_world_x_size(), world.get_world_x_size())
        y = random.randrange(-world.get_world_y_size(), world.get_world_y_size())
        if y % 2 == 1:
            x = x + 0.5
        if (x, y) not in world.tile_map_coords:
            world.add_particle(x, y)
        else:
            print(" x and y ", (x, y))
    print("Max Size of created Particle", len(world.particles))


def create_particle_in_line(world, max_size_particle, start_coords):
    if start_coords[0] % 1 != 0:
        start_i = int(start_coords[0] - 0.5)
        for i in range(start_i, start_i+max_size_particle):
            world.add_particle(i + 1.5, start_coords[1])

    else:
        for i in range(int(start_coords[0] + 1), int(start_coords[0] + 1) + max_size_particle):
            world.add_particle(i, start_coords[1])


def create_particle_in_square(world, max_size_particle, start_coords):

    for y in range(start_coords[1], round(max_size_particle/2)):
        for x in range(start_coords[0], round(max_size_particle/2)):
            world.add_particle(x + 0.5, 2 * y + 1.0)
            world.add_particle(-(x + 0.5), 2 * y + 1.0)
            world.add_particle(x + 0.5, -(2 * y + 1.0))
            world.add_particle(-(x + 0.5), -(2 * y + 1.0))
            world.add_particle(x, 2 * y)
            world.add_particle(-x, 2 * y)
            world.add_particle(x, -2 * y)
            world.add_particle(-x, -  2 * y)


def add_particles_as_hexagon(world, radius, color=header.black):
    world.add_particle(0, 0, color)
    displacement = - radius + 0.5
    iteration = 0
    for i in range(1, radius + 1):
        world.add_particle(i, 0, color)
        world.add_particle(-i, 0, color)
    for i in range(1, radius + 1):
        for j in range(0, (2 * radius) - iteration):
            world.add_particle(displacement + j, i, color)
            world.add_particle(displacement + j, -i, color)
        iteration = iteration + 1
        displacement = displacement + 0.5


def add_tiles_as_hexagon(world, radius, color=header.black):
    world.add_tile(0, 0, color)
    displacement = - radius + 0.5
    iteration = 0
    for i in range(1, radius + 1):
        world.add_tile(i, 0, color)
        world.add_tile(-i, 0, color)
    for i in range(1, radius + 1):
        for j in range(0, (2 * radius) - iteration):
            world.add_tile(displacement + j, i, color)
            world.add_tile(displacement + j, -i, color)
        iteration = iteration + 1
        displacement = displacement + 0.5


def add_markers_as_hexagon(world, radius, color=header.black):
    world.add_marker(0, 0, color)
    displacement = - radius + 0.5
    iteration = 0
    for i in range(1, radius + 1):
        world.add_marker(i, 0, color)
        world.add_marker(-i, 0, color)
    for i in range(1, radius + 1):
        for j in range(0, (2 * radius) - iteration):
            world.add_marker(displacement + j, i, color)
            world.add_marker(displacement + j, -i, color)
        iteration = iteration + 1
        displacement = displacement + 0.5


def create_tiles_formed_as_hexagons_border(world, radius, starting_x = 0, starting_y = 0):
    offset_x = 0
    if starting_y % 2 != 0:
        offset_x = 0.5
    world.add_tile(radius/2 + starting_x + offset_x, radius + starting_y)
    world.add_tile(radius + starting_x + offset_x, starting_y)
    world.add_tile(radius/2 + starting_x + offset_x, -radius  + starting_y)
    world.add_tile(-radius/2 + starting_x + offset_x, -radius + starting_y)
    world.add_tile(-radius + starting_x + offset_x, starting_y)
    world.add_tile(-radius/2 + starting_x + offset_x, radius + starting_y)

    for i in range(1, radius):
        world.add_tile(-radius/2 + i + starting_x + offset_x, radius + starting_y)
        world.add_tile(radius/2 + (0.5 * i ) + starting_x + offset_x, radius - i + starting_y)
        world.add_tile(radius/2 + (0.5 * i) + starting_x + offset_x, -radius + i + starting_y)
        world.add_tile(-radius/2 + i + starting_x + offset_x, -radius + starting_y)
        world.add_tile(-radius/2 - (0.5 * i) + starting_x + offset_x, -radius + i + starting_y)
        world.add_tile(-radius/2 - (0.5 * i) + starting_x + offset_x, radius - i + starting_y)
