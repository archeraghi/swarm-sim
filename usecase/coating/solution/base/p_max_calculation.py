from lib.swarm_sim_header import *
from lib import particle as particle_class
from solution import solution_header


def find_p_max(particle: particle_class) -> None:
    """
    calculates the p_max for a particle based on all information this particle has
    @param particle: the particle for which the p_max should be calculated
    """
    if debug and debug_p_max_calculation:
        print("\n After P", particle.number, "own distance", particle.own_dist)
        print("Direction | Distance")
        for direction in direction_list:
            print(direction_number_to_string(direction), "|", particle.nh_list[direction])
        print("Before P MAX:")
        print("id | dist | direction")
        print(particle.p_max)

    own_p_max(particle.own_dist, particle.p_max, particle.number, particle.nh_list)
    global_p_max(particle)

    if debug and debug_p_max_calculation:
        print("P MAX:")
        print("id | dist | direction")
        print(particle.p_max)

    if debug and debug_p_max_calculation:
        print("P_Max Table \n ID | Distance")
        print(particle.p_max_table)


def own_p_max(own_distance: float, p_max: solution_header.PMaxInfo, particle_number: int,
              nh_list: solution_header.NH_LIST_TYPE) -> bool:
    """
    Checks if this particle or any of its neighbors has maximum distance and sets the values of the p_max object
    @return: True if this particle is at maximum distance, False otherwise
    @param own_distance: the distance of this particle
    @param p_max: the current p_max of this particle. Will be changed if this particle is at maximum distance
    @param particle_number: the particles id
    @param nh_list: the particles neighborhood
    """
    if own_distance is not math.inf:
        p_max.dist = own_distance
        p_max.ids = {particle_number}
        for direction in direction_list:
            neighbor = nh_list[direction]
            if neighbor.type == "p" and p_max.dist < neighbor.dist:
                p_max.dist = neighbor.dist
    return False


def global_p_max(particle: particle_class) -> None:
    """
    Finds the greatest p_max in all messages received
    @param particle: the particle for which the p_max should be calculated
    """
    for rcv_direction in particle.rcv_buf:
        if isinstance(particle.rcv_buf[rcv_direction], solution_header.PMax):
            if particle.rcv_buf[rcv_direction].p_max_dist > particle.p_max.dist:
                particle.p_max.dist = particle.rcv_buf[rcv_direction].p_max_dist
                particle.p_max.ids = {particle.number}