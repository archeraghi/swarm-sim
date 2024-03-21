from lib.swarm_sim_header import *


def scenario(sim, particle_count):
    if particle_count == -1:
        particle_count = 42
    sim.add_tile((0, 0))
    sim.add_tile((-1.0, 0.0))
    sim.add_tile((-1.5, -1.0))
    sim.add_tile((0.5, -1.0))
    sim.add_tile((1.5, 1.0))
    sim.add_tile((0.5, 1.0))
    sim.add_tile((-1.0, 2.0))
    sim.add_tile((-0.5, 1.0))
    sim.add_tile((-1.5, 1.0))
    sim.add_tile((0.5, 1.0))
    sim.add_tile((0.5, 3.0))
    sim.add_tile((-0.0, 2.0))
    sim.add_tile((1.0, 4.0))
    sim.add_tile((1.5, 5.0))
    sim.add_tile((-0.5, 3.0))
    sim.add_tile((-2.0, 4.0))
    sim.add_tile((-1.5, 3.0))
    sim.add_tile((-4.0, 4.0))
    sim.add_tile((-3.0, 4.0))
    sim.add_tile((-2.0, 6.0))
    sim.add_tile((-1.5, 5.0))
    sim.add_tile((-2.5, 1.0))
    sim.add_tile((-3.5, 1.0))
    sim.add_tile((-4.5, 1.0))
    #sim.add_location((0.0, 0.0))
    generating_random_spraded_particles(sim, particle_count)
