import random


def generating_random_spraded_particles (world, max_size_particle):
    for _ in range(0, max_size_particle):
        x = random.randrange(-world.get_sim_x_size(), world.get_sim_x_size())
        y = random.randrange(-world.get_sim_y_size(), world.get_sim_y_size())
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
