from copy import deepcopy
from lib.swarm_sim_header import *
from solution import solution_header
from lib import agent as agent_class
from typing import List, Tuple

MAX_WAITING_ROUNDS = 15


def read_and_clear(memory: solution_header.RCV_BUF_TYPE) -> solution_header.RCV_BUF_TYPE:
    """
    Reads all received messages from memory and clears it
    @return: a dictionary with all messages in the memory
    @param memory: a agents memory
    """
    if debug and debug_read:
        print("memory: ", ["direction: " + direction_number_to_string(memkey) + " | " + str(mem) for memkey, mem in memory.items()])
    if memory:
        rcv_buf = deepcopy(memory)
        memory.clear()
        return rcv_buf
    return {}


def check_for_new_target_item(agent: agent_class) -> None:
    """
    Checks the messages of the agent for coordinates to a new target item
    @param agent: the agent whose messages to check
    """
    for rcv_direction in agent.rcv_buf:
        if isinstance(agent.rcv_buf[rcv_direction], solution_header.TargetitemInfo):
            agent.dest_t = agent.rcv_buf[rcv_direction].target


def send_target_item(agent: agent_class, target_direction: int) -> None:
    """
    Sends the coordinates of the agents current target item in the target direction
    @param agent: the sender agent
    @param target_direction: the direction in which to send the message
    """
    dist_package = solution_header.TargetitemInfo(agent.dest_t)
    target_agent = agent.get_agent_in(target_direction)
    # invert the direction so the receiver agent knows from where direction it got the package
    agent.write_to_with(target_agent, key=get_the_invert(target_direction), data=deepcopy(dist_package))


def send_own_distance(agent: agent_class, targets: List[int]) -> None:
    """
    Sends a message in all target directions containing only the agents own_dist
    @param agent: the sender agents
    @param targets: all directions the message should be send to
    """
    dist_package = solution_header.OwnDistance(agent.own_dist, agent.number)
    for target_direction in targets:
        target_agent = agent.get_agent_in(target_direction)
        if debug and debug_write:
            print("P", agent.number, "sends own distance package", dist_package.agent_distance,
                  " to", target_agent.number, " in direction", direction_number_to_string(target_direction))
        # invert the direction so the receiver agent knows from where direction it got the package
        agent.write_to_with(target_agent, key=get_the_invert(target_direction), data=deepcopy(dist_package))


def send_p_max(agent: agent_class, targets: List[int]) -> None:
    """
    Sends a message in all target directions containing the agents own_dist and p_max
    @param agent: the sender agents
    @param targets: all directions the message should be send to
    """
    dist_package = solution_header.PMax(agent.own_dist, agent.number, agent.p_max)
    for target_direction in targets:
        target_agent = agent.get_agent_in(target_direction)
        if debug and debug_write:
            print("P", agent.number, "sends Pmax package", dist_package.p_max_dist, " to", target_agent.number,
                  " in direction", direction_number_to_string(target_direction))
        agent.write_to_with(target_agent, key=get_the_invert(target_direction), data=deepcopy(dist_package))


def send_dummy_messages(agent: agent_class, targets: List[int]) -> None:
    """
    Sends a message in all target directions containing only the agents own_dist
    @param agent: the sender agents
    @param targets: all directions the message should be send to
    """
    dist_package = solution_header.OwnDistance(math.inf, agent.number)
    for target_direction in targets:
        target_agent = agent.get_agent_in(target_direction)
        if debug and debug_write:
            print("P", agent.number, "sends own distance package", dist_package.agent_distance,
                  " to", target_agent.number, " in direction", direction_number_to_string(target_direction))
        # invert the direction so the receiver agent knows from where direction it got the package
        agent.write_to_with(target_agent, key=get_the_invert(target_direction), data=deepcopy(dist_package))


def find_neighbor_agents(agent: agent_class) -> List[int]:
    """
    Find all directions containing agents
    @return: all directions containing agents
    @param agent: the agent whose neighborhood ist checked
    """
    directions_with_agents = []
    for direction in direction_list:
        if agent.agent_in(direction):
            directions_with_agents.append(direction)
    return directions_with_agents


def divide_neighbors(nh_list: solution_header.NH_LIST_TYPE, neighbor_directions: List[int], own_distance: float)\
        -> Tuple[List[int], List[int]]:
    """
    Divides all neighbors into those that have a higher distance than the sending agent
    and those that have a lower distance
    @param nh_list: Neighborhood list of the sender agent
    @param neighbor_directions: List of directions that contain agents
    @param own_distance: Own distance of the sender agent
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


def send_p_max_to_neighbors(agent: agent_class) -> None:
    """
    Sends information to all neighbors based on the agents own judgement
    @param agent: the sender agent
    """
    directions_with_agents = find_neighbor_agents(agent)
    own_dist_targets = []
    p_max_targets = []
    for direction in directions_with_agents:
        if direction in agent.p_max.directions:
            own_dist_targets.append(direction)
        else:
            p_max_targets.append(direction)
    send_p_max(agent, p_max_targets)
    send_own_distance(agent, own_dist_targets)


def send_own_dist_to_neighbors(agent: agent_class) -> None:
    """
    Only sends own_dist info and never sends p_max
    @param agent: the sender agent
    """
    directions_with_agents = find_neighbor_agents(agent)
    own_distance_targets, dummy_message_targets = divide_neighbors(agent.nh_list,
                                               directions_with_agents,
                                               agent.own_dist)
    send_own_distance(agent, own_distance_targets)
    if agent.waiting_rounds > MAX_WAITING_ROUNDS:
        send_dummy_messages(agent, dummy_message_targets)
        #agent.waiting_rounds = 0
    else:
        agent.waiting_rounds += 1
