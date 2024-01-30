import logging
import random

from lib.oppnet import routing
from lib.oppnet.message_types import LeaderMessageType
from lib.oppnet.mobility_model import MobilityModelMode
from lib.oppnet.particles import FlockMemberType, FlockMode
from lib.swarm_sim_header import red


def solution(world):
    current_round = world.get_actual_round()
    particles = world.get_particle_list()
    t_wait = world.config_data.flock_radius * 2
    t_pick = t_wait * 5

    if current_round == 1:
        leader_count = world.config_data.leader_count
        leaders, _ = split_particles(particles, leader_count)
        world.add_leaders(leaders)
        initialise_leaders(t_wait, leaders)
        world.csv_flock_round.add_flock(particles)
    else:
        leaders = get_leaders(world)
        routing.next_step(particles)
        if current_round == 5:
            log_all_routes(particles, current_round)
        if current_round > t_wait * 3 + 1:
            move_to_next_direction(particles)
        send_direction_proposals(current_round, leaders)
        predators_pursuit(world.get_predators_list())


def get_leaders(world):
    """
    Gets the list of leaders
    :param world: simulator world
    :return: list of leaders
    """
    leaders = world.leaders
    if len(leaders) > world.config_data.leader_count:
        logging.warning("round {}: more than leaders ({}) than set in config ({})"
                        .format(world.get_actual_round(), len(leaders), world.config_data.leader_count))
    return leaders


def predators_pursuit(predators):
    """
    Activate pursuit of predators
    :param predators: list of predators
    :return: None
    """
    for predator in predators:
        predator.pursuit()


def log_all_routes(particles, current_round):
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


def initialise_leaders(t_wait, leaders):
    """
    Initializes all leaders by setting color t_wait and proposal rounds.
    :param t_wait: the t_wait value to use.
    :return: None
    """
    left_bound = t_wait * 3 + 1
    for index, leader in enumerate(leaders):
        leader.set_t_wait(t_wait)
        leader.set_color(red)
        leader.set_flock_member_type(FlockMemberType.Leader)
        leader.set_next_direction_proposal_round(left_bound * (index % 2))
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


def send_direction_proposals(current_round, leaders):
    """
    Sends the direction proposals of leaders.
    :param current_round: current simulator round
    :return: None
    """
    for leader in leaders:
        if leader.next_direction_proposal_round == current_round:
            if leader.flock_mode == FlockMode.Flocking:
                leader.send_direction_proposal()
            else:
                # leader.broadcast_safe_location(leader.coordinates)
                leader.multicast_leader_message(LeaderMessageType.discover)
                leader.reset_random_next_direction_proposal_round()


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
            if particle.mobility_model.mode == MobilityModelMode.POI:
                particle.move_to(next_direction)
            else:
                particle_directions[particle] = next_direction
    if particle_directions:
        particles[0].world.move_particles(particle_directions)
