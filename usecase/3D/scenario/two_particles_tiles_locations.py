"""
A world is created that has two particles, two markers, and two tiles.
"""
from lib.swarm_sim_header import get_multiple_steps_in_direction, get_coordinates_in_direction


def scenario(world):

    center = world.grid.get_center()
    dirs = world.grid.get_directions_list()

    world.add_particle(center)
    world.add_particle(get_coordinates_in_direction(center, dirs[0]))
    world.add_location(get_coordinates_in_direction(center, dirs[1]))
    world.add_location(get_multiple_steps_in_direction(center, dirs[1], 2))
    world.add_tile(get_coordinates_in_direction(center, dirs[2]))
    world.add_tile(get_coordinates_in_direction(center, dirs[3]))
