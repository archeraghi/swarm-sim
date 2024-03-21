from core.swarm_sim_header import *
from core import agent as agent_class, matter as matter_class
import math
from usecase.coating.solution import solution_header


def calculate_distances(agent: agent_class) -> solution_header.NH_LIST_TYPE:
    """
    Main function for calculating the distance and neighborhood of a agent
    @param agent: the agent whose turn it is
    @return: the list of neighbors with distances of the agent
    """
    if debug and debug_distance_calculation:
        print("\n***************************************************************")
        print(" Before P", agent.number, "own distance", agent.own_dist, "coords", agent.coords)

    nh_list = scan_nh(agent)

    for direction in direction_list:
        nh_list[direction].dist = get_nh_dist(direction, nh_list[direction].type, agent.rcv_buf)

    if debug and debug_distance_calculation:
        print("Direction | Type | Distance")
        for direction in direction_list:
            print(direction_number_to_string(direction), "|", nh_list[direction].type, "|", nh_list[direction].dist)

    new_own_dist = calc_own_dist(nh_list)
    if new_own_dist < agent.own_dist:
        agent.own_dist = new_own_dist
    # recalculate unknown neighbor distances based on own distance
    if agent.own_dist != math.inf:
        for direction in direction_list:
            nh_list[direction].dist = calc_nh_dist(direction, nh_list, agent.own_dist)
            #if agent is beside a item then this item is the new target
            if nh_list[direction].type == "t":
                agent.dest_t = agent.get_item_in(direction).coordinates
    return nh_list


def scan_nh(agent: agent_class) -> solution_header.NH_LIST_TYPE:
    """
    Scans all directions for the type of neighbor they contain
    @return: the new neighborhood list containing only the neighbor types
    @param agent: the agent whose neighborhood to check
    """
    nh_list = []
    for direction in direction_list:
        if agent.agent_in(direction):
            nh_list.append(solution_header.Neighbor("p", math.inf))
            if direction not in agent.rcv_buf and agent.own_dist < math.inf:
                agent.wait = True
        elif agent.item_in(direction):
            nh_list.append(solution_header.Neighbor("t", 0))
        else:
            nh_list.append(solution_header.Neighbor("fl", math.inf))
    return nh_list


def get_nh_dist(direction: int, type: str, rcv_buf: solution_header.RCV_BUF_TYPE) -> float:
    """
    Checks received messages for distance information of neighbors
    @return: The distance of the neighbor if the agent has a message from it
    @param direction: direction of the neighbor
    @param type: The type of the neighbor
    @param rcv_buf: the messages containing distance information
    """
    if type == "t":
        return 0
    elif direction in rcv_buf and isinstance(rcv_buf[direction], solution_header.OwnDistance):
        return rcv_buf[direction].agent_distance
    return math.inf


def calc_own_dist(nh_list: solution_header.NH_LIST_TYPE) -> float:
    """
    calculates a agents own distance
    @return: The own distance of the the agent
    @param nh_list: the neighborhood of the agent
    """
    min_nh_dist = min([neighbor.dist for neighbor in nh_list])
    return min_nh_dist + 1


def calc_own_dist_t(matter: matter_class) -> float:
    """
    If a item is in a agents neighborhood it's distance is always 1
    @return: The own distance of the the agent
    @param matter: any matter in the agents neighborhood
    """
    if matter.type == "item":
        return 1
    return math.inf


def calc_nh_dist(direction: int, nh_list: solution_header.NH_LIST_TYPE, own_dist: float) -> float:
    """
    Calculates the distance of a neighbor based on own distance
    @return: the estimated distance of the neighbor
    @param direction: the direction of the neighbor
    @param nh_list: the agents neighborhood
    @param own_dist: the agents own distance
    """
    estimated_distance = 1 + min(own_dist,
                                 nh_list[direction_in_range(direction + 1)].dist,
                                 nh_list[direction_in_range(direction - 1)].dist)
    return min(estimated_distance, nh_list[direction].dist)
