from lib.swarm_sim_header import *


def scenario(sim, particle_count):
    if particle_count == -1:
        particle_count = 80
    sim.add_item((0.0, 0.0))
    sim.add_item((-0.5, 1.0))
    sim.add_item((-1.0, 2.0))
    sim.add_item((1.0, 6.0))
    sim.add_item((2.0, 6.0))
    sim.add_item((3.0, 6.0))
    sim.add_item((4.0, 6.0))
    sim.add_item((5.0, 6.0))
    sim.add_item((5.5, 5.0))
    sim.add_item((6.0, 4.0))
    sim.add_item((6.5, 3.0))
    sim.add_item((6.0, 2.0))
    sim.add_item((5.5, 1.0))
    sim.add_item((5.0, 0.0))
    sim.add_item((-1.5, 3.0))
    sim.add_item((-1.0, 4.0))
    sim.add_item((-0.5, 5.0))
    sim.add_item((-0.0, 6.0))
    #sim.add_location((0.0, 0.0))
    generating_random_spraded_particles(sim, particle_count)
