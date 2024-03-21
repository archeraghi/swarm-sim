from lib.swarm_sim_header import *


def scenario(sim, particle_count):
    if particle_count == -1:
        particle_count = 30
    sim.add_tile((0.0, 0.0))
    generating_random_spraded_particles(sim, particle_count)
