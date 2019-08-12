"""
The particles are moving infront each other but in the different direction but whenever they meet each other
the start either to write to each other and then they give out the what it they received from each other.
"""
#Standard Lib that has to be in each solution

def solution(sim):
    """
    All the magic starts from here

    :param sim: The object instance of the sim.py
    :param sim: The object instance of the created sim
    """
  #  two_particle_inverse_walk(sim)
    read_write(sim)


def read_write( sim):
    sim.get_particle_list()[0].write_to_with(sim.markers[0], "marker", "test1")
    sim.get_particle_list()[0].write_to_with(sim.tiles[0], "tile", "test2")
    sim.get_particle_list()[0].write_to_with(sim.get_particle_list()[1], "particle1", "test3")
    sim.get_particle_list()[0].write_to_with(sim.get_particle_list()[1], "particle2", "test4")
    sim.get_particle_list()[0].write_to_with(sim.get_particle_list()[1], "particle3", "test5")
    sim.get_particle_list()[0].write_to_with(sim.get_particle_list()[1], "particle4", "test6")
    loc_data = sim.get_particle_list()[0].read_from_with(sim.markers[0], "marker")
    tile_data = sim.get_particle_list()[0].read_from_with(sim.tiles[0], "tile")
    if loc_data != 0:
        print(loc_data)
    if tile_data != 0:
        print(tile_data)
    for part_key in sim.get_particle_list()[1].read_whole_memory():
        print(sim.get_particle_list()[1].read_whole_memory()[part_key])


