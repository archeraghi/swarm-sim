import random

from lib.oppnet import routing
from lib.oppnet.message_types import LeaderMessageType
from lib.oppnet.mobility_model import MobilityModelMode
from lib.oppnet.particles import FlockMemberType
from lib.swarm_sim_header import red


def solution(world):
    global leader, followers

    current_round = world.get_actual_round()
    particles = world.get_particle_list()
    t_wait = world.config_data.flock_radius * 2
    t_pick = t_wait * 5

    if current_round == 1:
        leader, followers = split_particles(particles, 1)
        initialize_leader(t_wait)
        world.csv_flock_round.add_flock(particles)
    else:
        routing.next_step(particles)
        move_to_next_direction(particles)
        if current_round % t_pick == 0:
            send_new_instruct()


def split_particles(particles, leader_count):
    """
    Splits the list of particles in two followers and leaders.
    :param particles: the list of particles.
    :param leader_count: the number of leaders
    :return: list of leaders, set of followers
    """
    leader_particle = random.sample(particles, leader_count)[0]
    follower_set = set(particles).difference({leader_particle})
    return leader_particle, follower_set


def initialize_leader(t_wait):
    """
    Initializes all leaders by setting color t_wait and proposal rounds.
    :param t_wait: the t_wait value to use.
    :return: None
    """
    leader.set_t_wait(t_wait)
    leader.set_color(red)
    leader.set_flock_member_type(FlockMemberType.Leader)
    send_new_instruct()


def send_new_instruct():
    """
    Leader sends a new direction instruct.
    :return: None
    """
    leader.choose_direction()
    leader.multicast_leader_message(LeaderMessageType.instruct)


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
