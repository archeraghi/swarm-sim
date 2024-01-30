import lib.oppnet.routing
from lib.oppnet import routing
from lib.oppnet.communication import generate_random_messages


def solution(world):
    particles = world.get_particle_list()
    current_round = world.get_actual_round()

    if current_round == 1:
        # initially generate 5 messages per particle
        generate_random_messages(particles, amount=2, world=world)
        initialize_delivery_probabilities(particles)
    else:
        # generate 2 messages per particle, every 20 rounds
        if current_round % 20 == 0:
            generate_random_messages(particles, amount=2, world=world)
        # move in every round starting from the second one
        for particle in particles:
            next_direction = particle.mobility_model.next_direction(current_x_y_z=particle.coordinates)
            if next_direction:
                particle.move_to(next_direction)

        lib.oppnet.routing.next_step(particles)


def initialize_delivery_probabilities(particles):
    for particle in particles:
        p_init = particle.routing_parameters.p_init
        # create a dictionary of probability dictionaries for each particle
        # and each possible encountering particle
        probabilities = {}
        for encounter in particles:
            # the list [prob, age] contains the probability and the age of the last encounter
            probabilities[encounter.get_id()] = (p_init, 0)
        particle.write_to_with(target=particle, key=routing.PROB_KEY, data=probabilities)
