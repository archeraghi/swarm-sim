import numpy as np

from lib.swarm_sim_header import get_hexagon_coordinates, black
from lib.world import World


def scenario(world: World):
    radius = world.config_data.flock_radius
    centre = (0, 0)
    hexagon = get_hexagon_coordinates(centre, radius)

    if world.config_data.particle_color is None:
        particle_color = black
    else:
        particle_color = world.config_data.particle_color

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


def create_random_predators(world):
    if world.config_data.predator_initial_amount == 0:
        return
    np.random.seed(world.config_data.seed_value)
    flock_radius = world.config_data.flock_radius
    predator_interaction_radius = world.config_data.predator_interaction_radius
    x_range = np.union1d(
        np.arange(-world.get_world_x_size(), - (flock_radius + predator_interaction_radius), 1),
        np.arange((flock_radius + predator_interaction_radius), world.get_world_x_size(), 1)
    )
    y_range = np.union1d(
        np.arange(-world.get_world_y_size(), - (flock_radius + predator_interaction_radius), 1),
        np.arange((flock_radius + predator_interaction_radius), world.get_world_y_size(), 1)
    )

    for _ in range(0, world.config_data.predator_initial_amount):
        valid_coordinates = False
        while not valid_coordinates:
            x = x_range[np.random.random_integers(x_range.size) - 1]
            y, z = y_range[np.random.random_integers(y_range.size) - 1], 0
            valid_coordinates = world.add_predator((x, y, z))
