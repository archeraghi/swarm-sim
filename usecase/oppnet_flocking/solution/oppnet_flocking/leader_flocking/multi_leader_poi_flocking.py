import logging
import random

from lib.oppnet import routing
from lib.oppnet.message_types import LeaderMessageType
from lib.oppnet.particles import FlockMemberType
from lib.swarm_sim_header import red


def solution(world):
    global leaders, followers

    current_round = world.get_actual_round()
    particles = world.get_particle_list()
    t_wait = world.config_data.flock_radius * 2
    t_pick = t_wait * 5

    if current_round == 1:
        leader_count = world.config_data.leader_count
        leaders, followers = split_particles(particles, leader_count)
        set_t_wait_values(particles, t_wait)
        initialise_leaders()
    else:
        check_neighborhoods(particles)
        routing.next_step(particles)
        update_particle_states(particles)
        if current_round > t_wait * 3 + 1:
            move_to_next_direction(particles)
        if current_round == 5:
            print_all_routes(particles, current_round)
        if current_round % 30 == 0:
            leader = random.choice(leaders)
            leader.send_safe_location_proposal()
        if current_round % 100 == 0:
            for leader in leaders:
                leader.broadcast_safe_location()


def print_all_routes(particles, current_round):
    """
    Logs routes of particles.
    :param current_round: simulator round
    :param particles: list of particles
    :return: None
    """
    for particle in particles:
        for target_particle, contacts in particle.leader_contacts.items():
            for contact in contacts.values():
                contact_particle = contact.get_contact_particle()
                logging.debug("round: {} route: #{} reaches #{} via #{} with {} hops"
                              .format(current_round, particle.number, target_particle.number, contact_particle.number,
                                      contact.get_hops()))


def set_t_wait_values(particles, t_wait):
    """
    Sets the t_wait of particles to :param t_wait.
    :param particles: list of particles
    :param t_wait: t_wait value to set
    :return: None
    """
    for particle in particles:
        particle.set_t_wait(t_wait)


def split_particles(particles, leader_count):
    """
    Splits the list of particles in two followers and leaders.
    :param particles: the list of particles.
    :param leader_count: the number of leaders
    :return: list of leaders, set of followers
    """
    leader_set = set(random.sample(particles, leader_count))
    follower_set = set(particles).difference(leader_set)
    return list(leader_set), follower_set


def initialise_leaders():
    """
    Initializes all leaders by setting color and proposal rounds.
    :return: None
    """
    for index, leader in enumerate(leaders):
        leader.set_color(red)
        leader.set_flock_member_type(FlockMemberType.Leader)
        leader.multicast_leader_message(LeaderMessageType.discover)
        logging.debug("round 1: leader {} next_direction_proposal: {}".format(leader.number,
                                                                              leader.next_direction_proposal_round))


def check_neighborhoods(particles):
    """
    Updates the neighbourhood of particles.
    :param particles: list of particles
    :return: None
    """
    for particle in particles:
        particle.update_current_neighborhood()


def update_particle_states(particles):
    """
    Updates the free locations of the particles.
    :param particles: list of particles
    :return:
    """
    for leader in leaders:
        leader.update_leader_states()
    for particle in particles:
        particle.update_free_locations()


def move_to_next_direction(particles):
    """
    Moves particle to their next direction.
    :param particles: list of particles
    :return: None
    """
    for particle in particles:
        next_direction = particle.get_next_direction()
        if next_direction:
            particle.move_to(next_direction)
