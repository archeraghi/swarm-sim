import random

from lib.oppnet import routing
from lib.oppnet.message_types import LeaderMessageType
from lib.oppnet.mobility_model import MobilityModel, MobilityModelMode
from lib.oppnet.particles import FlockMemberType
from lib.swarm_sim_header import red


def solution(world):
    global leader, particles, followers

    current_round = world.get_actual_round()
    dirs = world.grid.get_directions_dictionary()
    t_wait = world.config_data.flock_radius * 2
    t_pick = t_wait * 5

    if current_round == 1:
        particles = world.get_particle_list()
        leader, followers = split_particles(1)
        initialize_leaders(t_wait)
    else:
        routing.next_step(particles)
        move_particles_to_next_direction()
        if current_round % 30 == 0:
            safe_location = leader.get_a_safe_location()
            leader.set_mobility_model(MobilityModel(leader.coordinates, MobilityModelMode.POI, poi=safe_location))
        elif current_round % 50 == 0:
            leader.broadcast_safe_location(leader.coordinates)
        else:
            send_new_instruct(current_round % t_pick == 0)


def split_particles(leader_count):
    """
    Splits the list of particles in two followers and leaders.
    :param leader_count: the number of leaders
    :return: list of leaders, set of followers
    """
    leader_particle = random.sample(particles, leader_count)[0]
    follower_set = set(particles).difference({leader_particle})
    return leader_particle, list(follower_set)


def initialize_leaders(t_wait):
    """
    Initializes all leaders by setting color t_wait and proposal rounds.
    :param t_wait: the t_wait value to use.
    :return: None
    """
    leader.set_t_wait(t_wait)
    leader.set_color(red)
    leader.set_flock_member_type(FlockMemberType.Leader)
    leader.broadcast_safe_location()


def send_new_instruct(choose_new_direction):
    """
    Leader sends a new direction instruct.
    :return: None
    """
    if choose_new_direction:
        leader.choose_direction(True)
        leader.multicast_leader_message(LeaderMessageType.instruct)
    else:
        next_direction = leader.mobility_model.next_direction(leader.coordinates)
        if not leader.proposed_direction or leader.proposed_direction != next_direction:
            leader.proposed_direction = next_direction
            leader.multicast_leader_message(LeaderMessageType.instruct)


def move_particles_to_next_direction():
    """
    Moves particle to their next direction.
    :return: None
    """
    particle_directions = {}
    for particle in followers:
        next_direction = particle.get_next_direction()
        if next_direction:
            if particle.mobility_model.mode == MobilityModelMode.POI:
                particle.move_to(next_direction)
            else:
                particle_directions[particle] = next_direction
    if particle_directions:
        particles[0].world.move_particles(particle_directions)
    try:
        leader.move_to(leader.proposed_direction)
    except TypeError:
        pass
