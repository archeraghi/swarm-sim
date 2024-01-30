import random

from lib.oppnet.mobility_model import MobilityModel, MobilityModelMode


def solution(sim):
    particles = sim.get_particle_list()

    if sim.get_actual_round() == 1:
        # sim size
        sim_x = sim.get_sim_x_size()
        sim_y = sim.get_sim_y_size()

        # initialize the particle mobility models
        for i, particle in enumerate(particles):
            m_model = MobilityModel(particle.coords[0], particle.coords[1], MobilityModelMode.POI,
                                    poi=(random.randint(-sim_x, sim_x), random.randint(-sim_y, sim_y)))
            particle
    else:
        for particle in particles:
            m_model = MobilityModel.get(particle)
            next_direction = m_model.next_direction(current_x_y=particle.coords)
            if next_direction is not False:
                particle.move_to_in_bounds(next_direction)
