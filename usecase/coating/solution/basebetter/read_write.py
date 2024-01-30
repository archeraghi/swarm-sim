from copy import deepcopy
from lib.swarm_sim_header import *
from solution import solution_header
from lib import particle as particle_class
from typing import List, Tuple

MAX_WAITING_ROUNDS = 15


def read_and_clear(memory: solution_header.RCV_BUF_TYPE) -> solution_header.RCV_BUF_TYPE:
    """
    Reads all received messages from memory and clears it
    @return: a dictionary with all messages in the memory
    @param memory: a particles memory
    """
    if debug and debug_read:
        print("memory: ", ["direction: " + direction_number_to_string(memkey) + " | " + str(mem) for memkey, mem in memory.items()])
    if memory:
        rcv_buf = deepcopy(memory)
        memory.clear()
        return rcv_buf
    return {}


def check_for_new_target_tile(particle: particle_class) -> None:
    """
    Checks the messages of the particle for coordinates to a new target tile
    @param particle: the particle whose messages to check
    """
    for rcv_direction in particle.rcv_buf:
        if isinstance(particle.rcv_buf[rcv_direction], solution_header.TargetTileInfo):
            particle.dest_t = particle.rcv_buf[rcv_direction].target


def send_target_tile(particle: particle_class, target_direction: int) -> None:
    """
    Sends the coordinates of the particles current target tile in the target direction
    @param particle: the sender particle
    @param target_direction: the direction in which to send the message
    """
    dist_package = solution_header.TargetTileInfo(particle.dest_t)
    target_particle = particle.get_particle_in(target_direction)
    # invert the direction so the receiver particle knows from where direction it got the package
    particle.write_to_with(target_particle, key=get_the_invert(target_direction), data=deepcopy(dist_package))


def send_own_distance(particle: particle_class, targets: List[int]) -> None:
    """
    Sends a message in all target directions containing only the particles own_dist
    @param particle: the sender particles
    @param targets: all directions the message should be send to
    """
    dist_package = solution_header.OwnDistance(particle.own_dist, particle.number)
    for target_direction in targets:
        target_particle = particle.get_particle_in(target_direction)
        if debug and debug_write:
            print("P", particle.number, "sends own distance package", dist_package.particle_distance,
                  " to", target_particle.number, " in direction", direction_number_to_string(target_direction))
        # invert the direction so the receiver particle knows from where direction it got the package
        particle.write_to_with(target_particle, key=get_the_invert(target_direction), data=deepcopy(dist_package))


def send_p_max(particle: particle_class, targets: List[int]) -> None:
    """
    Sends a message in all target directions containing the particles own_dist and p_max
    @param particle: the sender particles
    @param targets: all directions the message should be send to
    """
    dist_package = solution_header.PMax(particle.own_dist, particle.number, particle.p_max)
    for target_direction in targets:
        target_particle = particle.get_particle_in(target_direction)
        if debug and debug_write:
            print("P", particle.number, "sends Pmax package", dist_package.p_max_dist, " to", target_particle.number,
                  " in direction", direction_number_to_string(target_direction))
        particle.write_to_with(target_particle, key=get_the_invert(target_direction), data=deepcopy(dist_package))


def send_dummy_messages(particle: particle_class, targets: List[int]) -> None:
    """
    Sends a message in all target directions containing only the particles own_dist
    @param particle: the sender particles
    @param targets: all directions the message should be send to
    """
    dist_package = solution_header.OwnDistance(math.inf, particle.number)
    for target_direction in targets:
        target_particle = particle.get_particle_in(target_direction)
        if debug and debug_write:
            print("P", particle.number, "sends own distance package", dist_package.particle_distance,
                  " to", target_particle.number, " in direction", direction_number_to_string(target_direction))
        # invert the direction so the receiver particle knows from where direction it got the package
        particle.write_to_with(target_particle, key=get_the_invert(target_direction), data=deepcopy(dist_package))


def find_neighbor_particles(particle: particle_class) -> List[int]:
    """
    Find all directions containing particles
    @return: all directions containing particles
    @param particle: the particle whose neighborhood ist checked
    """
    directions_with_particles = []
    for direction in direction_list:
        if particle.particle_in(direction):
            directions_with_particles.append(direction)
    return directions_with_particles


def divide_neighbors(nh_list: solution_header.NH_LIST_TYPE, neighbor_directions: List[int], own_distance: float)\
        -> Tuple[List[int], List[int]]:
    """
    Divides all neighbors into those that have a higher distance than the sending particle
    and those that have a lower distance
    @param nh_list: Neighborhood list of the sender particle
    @param neighbor_directions: List of directions that contain particles
    @param own_distance: Own distance of the sender particle
    @return: Two Lists containing the different neighbors
    """
    p_max_targets = []
    own_distance_targets = []
    for direction in neighbor_directions:
        if nh_list[direction].dist > own_distance:
            own_distance_targets.append(direction)
        else:
            p_max_targets.append(direction)
    return own_distance_targets, p_max_targets


def send_p_max_to_neighbors(particle: particle_class) -> None:
    """
    Sends information to all neighbors based on the particles own judgement
    @param particle: the sender particle
    """
    directions_with_particles = find_neighbor_particles(particle)
    own_dist_targets = []
    p_max_targets = []
    for direction in directions_with_particles:
        if direction in particle.p_max.directions:
            own_dist_targets.append(direction)
        else:
            p_max_targets.append(direction)
    send_p_max(particle, p_max_targets)
    send_own_distance(particle, own_dist_targets)


def send_own_dist_to_neighbors(particle: particle_class) -> None:
    """
    Only sends own_dist info and never sends p_max
    @param particle: the sender particle
    """
    directions_with_particles = find_neighbor_particles(particle)
    own_distance_targets, dummy_message_targets = divide_neighbors(particle.nh_list,
                                               directions_with_particles,
                                               particle.own_dist)
    send_own_distance(particle, own_distance_targets)
    if particle.waiting_rounds > MAX_WAITING_ROUNDS:
        send_dummy_messages(particle, dummy_message_targets)
        #particle.waiting_rounds = 0
    else:
        particle.waiting_rounds += 1
