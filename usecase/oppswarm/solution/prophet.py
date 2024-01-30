import lib.oppnet.routing
from lib.oppnet import routing
from lib.oppnet.communication import generate_random_messages
from lib.oppnet.mobility_model import MobilityModel

new_message_interval = 10
messages_per_interval = 2


def solution(sim):
    particles = sim.get_particle_list()
    config_data = sim.config_data

    current_round = sim.get_actual_round()
    if sim.get_actual_round() == 1:
        # initialize the particle mobility models
        for particle in particles:
            m_model = MobilityModel(particle.coords[0], particle.coords[1], sim.mobility_model_mode)
            m_model.set(particle)
            r_params = lib.oppnet.routing.RoutingParameters(algorithm=config_data.routing_algorithm,
                                                            scan_radius=config_data.scan_radius,
                                                            delivery_delay=config_data.delivery_delay,
                                                            l_encounter=config_data.l_encounter,
                                                            gamma=config_data.gamma,
                                                            beta=config_data.beta, p_init=config_data.p_init)
            r_params.set(particle)
        # initially generate messages per particle
        generate_random_messages(particles, amount=messages_per_interval, sim=sim)
        initialize_delivery_probabilities(particles, config_data.p_init)
    else:
        # generated new messages per particle
        if current_round % new_message_interval == 0:
            generate_random_messages(particles, amount=messages_per_interval, sim=sim)
        # move in every round starting from the second one
        for particle in particles:
            m_model = MobilityModel.get(particle)
            next_direction = m_model.next_direction(current_x_y=particle.coords)
            if next_direction is not False:
                particle.move_to_in_bounds(next_direction)

        lib.oppnet.routing.next_step(particles)


def initialize_delivery_probabilities(particles, p_init):
    for particle in particles:
        # create a dictionary of probability dictionaries for each particle
        # and each possible encountering particle
        probabilities = {}
        for encounter in particles:
            # the list [prob, age] contains the probability and the age of the last encounter
            probabilities[encounter.get_id()] = (p_init, 0)
        particle.write_to_with(matter=particle, key=routing.PROB_KEY, data=probabilities)
