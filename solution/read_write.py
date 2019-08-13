"""
The particles are moving infront each other but in the different direction but whenever they meet each other
the start either to write to each other and then they give out the what it they received from each other.
"""
#Standard Lib that has to be in each solution

def solution(world):
    """
    All the magic starts from here

    :param world: The object instance of the world.py
    :param world: The object instance of the created world
    """
  #  two_particle_inverse_walk(world)
    read_write(world)


def read_write( world):
    world.get_particle_list()[0].write_to_with(world.markers[0], "marker", "test1")
    world.get_particle_list()[0].write_to_with(world.tiles[0], "tile", "test2")
    world.get_particle_list()[0].write_to_with(world.get_particle_list()[1], "particle1", "test3")
    world.get_particle_list()[0].write_to_with(world.get_particle_list()[1], "particle2", "test4")
    world.get_particle_list()[0].write_to_with(world.get_particle_list()[1], "particle3", "test5")
    world.get_particle_list()[0].write_to_with(world.get_particle_list()[1], "particle4", "test6")
    loc_data = world.get_particle_list()[0].read_from_with(world.markers[0], "marker")
    tile_data = world.get_particle_list()[0].read_from_with(world.tiles[0], "tile")
    if loc_data != 0:
        print(loc_data)
    if tile_data != 0:
        print(tile_data)
    for part_key in world.get_particle_list()[1].read_whole_memory():
        print(world.get_particle_list()[1].read_whole_memory()[part_key])


