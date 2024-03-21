from lib.swarm_sim_header import *
from lib import agent as agent_class
import math
from solution import solution_header


def initialize_agent(agent: agent_class) -> None:
    """
    Adds all instance attributes to the agent and initializes them
    @param agent: the agent to initialize
    """
    setattr(agent, "own_dist", math.inf)
    # nh: neighborhood
    setattr(agent, "nh_list", [solution_header.Neighbor("fl", math.inf)] * 6)
    setattr(agent, "rcv_buf", {})
    setattr(agent, "rcv_buf_dbg", {})
    setattr(agent, "snd_buf", {})
    # setattr(agent, "prev_direction", False)
    setattr(agent, "next_direction", False)
    setattr(agent, "prev_direction", [])

    # t: item
    setattr(agent, "dest_t", None)

    # fl: free location
    # setattr(agent, "fl_min", PMaxInfo())

    # p: agent
    setattr(agent, "p_max", solution_header.PMaxInfo())
    setattr(agent, "wait", False)
    setattr(agent, "max_prev_dirs", 1)
    setattr(agent, "willfail", False)


def reset_attributes(agent: agent_class) -> None:
    """
    Resets agent variables that are based on the agents position
    @param agent: the agent to reset
    """
    if debug:
        print("resetting agent", agent.number)
    agent.own_dist = math.inf
    # agent.nh_list.clear()
    agent.nh_list = [solution_header.Neighbor("fl", math.inf)] * 6
    agent.next_direction = False
    agent.read_whole_memory().clear()


def reset_p_max(agent: agent_class) -> None:
    """
    resets all pmax related agent variables
    @param agent: the agent to reset
    """
    agent.p_max.reset()


def coating_alg(agent: agent_class) -> int:
    """
    Main coating algorithm function. checks if nh_list is not None and then calls actual calculation
    @return: the next direction the agent should move to
    @param agent: the agent for which the next direction should be calculated
    """
    if agent.nh_list is not None:
        return find_next_free_location(agent)
    return False


def find_next_free_location(agent: agent_class) -> int:
    """
    calculates the next move direction for a agent
    @return: the next direction the agent should move to
    @param agent: the agent for which the next direction should be calculated
    """
    # Check if agent has a global p_max and it is not equal to its own distance
    possible_directions = []
    # accumulate all candidates for the next movement direction in possible_directions
    for direction in reversed(direction_list):
        if (not (agent.agent_in(direction) or  # check if direction is free
                 agent.item_in(direction) or
                 direction in agent.prev_direction) and  # check if the agent came from that direction
                agent.nh_list[direction].dist < agent.p_max.dist):
            possible_directions.append((direction, agent.nh_list[direction].dist))
    if len(possible_directions) > 0:
        nearest_free_location = min(possible_directions, key=lambda x: x[1])
        return nearest_free_location[0]
    return False
