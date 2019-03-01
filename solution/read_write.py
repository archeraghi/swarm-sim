"""
The particles are moving infront each other but in the different direction but whenever they meet each other
the start either to write to each other and then they give out the what it they received from each other.
"""

import logging

NE = 0
E = 1
SE = 2
SW = 3
W = 4
NW = 5


direction = [NE, E, SE, SW, W, NW]


def solution(sim, world):
    """
    All the magic starts from here

    :param sim: The object instance of the sim.py
    :param world: The object instance of the created world
    """
  #  two_particle_inverse_walk(world)
    read_write(world)


def read_write( world):
    world.get_particle_list()[0].write_to_with(world.locations[0], "location", "test1")
    world.get_particle_list()[0].write_to_with(world.tiles[0], "tile", "test2")
    world.get_particle_list()[0].write_to_with(world.get_particle_list()[1], "particle1", "test3")
    world.get_particle_list()[0].write_to_with(world.get_particle_list()[1], "particle2", "test4")
    world.get_particle_list()[0].write_to_with(world.get_particle_list()[1], "particle3", "test5")
    world.get_particle_list()[0].write_to_with(world.get_particle_list()[1], "particle4", "test6")
    loc_data = world.get_particle_list()[0].read_from_with(world.locations[0], "location")
    tile_data = world.get_particle_list()[0].read_from_with(world.tiles[0], "tile")
    #part_data = world.get_particle_list()[0].read_from_with(world.get_particle_list()[1], "particle")
    if loc_data != 0:
        print(loc_data)
    if tile_data != 0:
        print(tile_data)
    for part_key in world.get_particle_list()[1].read_whole_memory():
        print(world.get_particle_list()[1].read_whole_memory()[part_key])


