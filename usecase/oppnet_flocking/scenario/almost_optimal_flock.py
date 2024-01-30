import random

from lib.swarm_sim_header import get_hexagon_coordinates, black
from lib.world import World


def scenario(world: World):
    radius = world.config_data.flock_radius
    if world.config_data.particle_color is None:
        particle_color = black
    else:
        particle_color = world.config_data.particle_color

    center = (0, 0)
    hexagon = get_hexagon_coordinates(center, radius)
    # remove a percentage of particles from the optimal flock
    removal_percentage = 0.00
    number_of_holes = round(len(hexagon) * removal_percentage)
    # remove number_of_holes many locations from the optimal hexagon formation
    hexagon = remove_random_locations(hexagon, number_of_holes)
    for location in hexagon:
        world.add_particle(coordinates=location, color=particle_color)

    if world.config_data.border:
        # add borders
        x_min, x_max = int(-world.get_world_x_size()), int(world.get_world_x_size())
        y_min, y_max = int(-world.get_world_y_size()), int(world.get_world_y_size())
        for x in range(round(x_min - 2), round(x_max + 2)):
            for y in [y_min - 2, y_max + 2]:
                world.add_tile((x, y, 0))
                if x != y:
                    world.add_tile((y, x, 0))
    create_random_predators(world)


def remove_random_locations(hexagon: list, number_of_locations_to_remove):
    """
    Removes :param number_of_locations_to_remove many particles randomly from the list :param hexagon and returns the
    result.
    :param hexagon: list of particles
    :param number_of_locations_to_remove: the number of particles to remove
    :return: the resulting list
    """
    total_locations = len(hexagon) - number_of_locations_to_remove
    return random.sample(hexagon, total_locations)


def create_random_predators(world):
    flock_radius = world.config_data.flock_radius
    x_min, x_max = int(-world.get_world_x_size() - flock_radius), int(world.get_world_x_size() + flock_radius)
    y_min, y_max = int(-world.get_world_y_size() - flock_radius), int(world.get_world_y_size() + flock_radius)
    for _ in range(0, world.config_data.predator_initial_amount):
        valid_coordinates = False
        while not valid_coordinates:
            x, y, z = random.randint(x_min, x_max), random.randint(y_min, y_max), 0
            valid_coordinates = world.add_predator((x, y, z))
            if valid_coordinates:
                print("world.add_predator(({}, {}, {}))"
                      .format(x, y, 0))
