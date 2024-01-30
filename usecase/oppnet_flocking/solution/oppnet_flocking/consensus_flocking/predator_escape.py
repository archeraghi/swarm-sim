import logging
import math

from lib.oppnet import routing
from lib.oppnet.mobility_model import MobilityModel


def solution(world):
    current_round = world.get_actual_round()
    particles = world.get_particle_list()
    predators = world.get_predators_list()
    t_pick = world.config_data.flock_radius * 10

    reset_neighborhood_counters(particles)

    if current_round == 1:
        world.csv_flock_round.add_flock(particles)
        query_relative_locations(particles)
    # route messages every other round
    else:
        routing.next_step(particles)
        relative_location_propagated = current_round % (world.config_data.flock_radius * 2 + 10)
        if relative_location_propagated == 0:
            try_and_fill_flock_holes(particles)
            move_to_next_direction(particles)
        if relative_location_propagated == 1:
            query_relative_locations(particles)
        predators_pursuit(predators)
    # send direction every round
    if current_round % t_pick == 0 or current_round == 1:
        send_random_next_directions(particles)
    else:
        send_current_directions(particles)

    move_to_next_direction(particles)


def reset_neighborhood_counters(particles):
    """
    Resets the neighborhood direction counters of particles.
    :param particles: list of particles
    :return: None
"""
    for particle in particles:
        particle.reset_neighborhood_direction_counter()


def send_current_directions(particles):
    """
    Sends the current direction of particles.
    :param particles: list of particles
    :return: None
"""
    for particle in particles:
        particle.update_current_neighborhood()
        particle.send_direction_message(particle.mobility_model.current_dir)
        logging.debug("round {}: send current particle {} direction {}"
                      .format(particle.world.get_actual_round(), particle.number, particle.mobility_model.current_dir))


def send_random_next_directions(particles, split=.5):
    """
    Sends a random next direction for particles. Splits the list by :param split such that by default half
    the particles will use the same random direction.
    :param particles: list of particles
    :param split: how to split the list
    :return: None
"""
    per_split = math.ceil(len(particles) * split)
    random_direction = MobilityModel.random_direction()
    for i, particle in enumerate(particles):
        if i % per_split == 0:
            random_direction = MobilityModel.random_direction()
        particle.update_current_neighborhood()
        particle.send_direction_message(random_direction)
        logging.debug("round {}: send next particle {} direction {}"
                      .format(particle.world.get_actual_round(), particle.number, random_direction))


def query_relative_locations(particles):
    """
    Queries relative location for particles.
    :param particles: list of particles
    :return: None
    """
    for particle in particles:
        particle.query_relative_location()


def try_and_fill_flock_holes(particles):
    """
    Tries to set particles to fill flock holes.
    :param particles: list of particles
    :return: None
    """
    for particle in particles:
        particle.try_and_fill_flock_holes()


def predators_pursuit(predators):
    """
    Activates pursuit of predators.
    :param predators: list of predators
    :return: None
    """
    for predator in predators:
        predator.pursuit()


def move_to_next_direction(particles):
    """
    Moves particle to their next direction.
    :param particles: list of particles
    :return: None
    """
    particle_directions = {}
    for particle in particles:
        next_direction = particle.get_next_direction()
        if next_direction:
            particle_directions[particle] = next_direction
        else:
            logging.debug("round {}: predator_test -> particle {} did not return a direction.".format(
                particle.world.get_actual_round(), particle.number))
    if particle_directions:
        particles[0].world.move_particles(particle_directions)
