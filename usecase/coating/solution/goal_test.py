import math
import numpy as np
from lib.swarm_sim_header import *
from lib import world, agent as agent_class


def end_sim(sim: world) -> None:
    """
    Checks if a termination state was reached
    @param sim: The current world state
    """
    if goal_reached(sim):
        if complete_check(sim):
            sim.set_successful_end()
            # own_dists = np.array([p.own_dist for p in sim.agents])
            # unique, counts = np.unique(own_dists, return_counts=True)
            # print(dict(zip(unique, counts)))
            if sim.config_data.visualization:
                print("successful end reached after round:", sim.get_actual_round())


def goal_reached(sim: world) -> bool:
    """
    Checks if a termination state is reached using only information available to the agents
    @param sim: The current world state
    @return: True if a termination state is reached, False otherwise
    """
    min_fl_distance = min(list(map(get_smallest_fl, sim.agents)), default=0)
    max_agent_distance = max((agent.own_dist for agent in sim.agents), default=math.inf)
    if min_fl_distance is math.inf or min_fl_distance < max_agent_distance:
        return False
    else:
        return True


def get_smallest_fl(agent: agent_class) -> int:
    """
    Calculates the lowest distance of all free locations in the agents neighborhood
    @param agent: the agent whose neighborhood to check
    @return: the lowest distance of free locations in the agents neighborhood
    """
    return min((neighbor.dist for neighbor in agent.nh_list if neighbor.type == "fl"), default=math.inf)


def complete_check(sim: world) -> bool:
    """
    Checks if a termination state is reached using global information from the world
    @param sim: The current world state
    @return: True if a termination state is reached, False otherwise
    """
    agent_distance_list = []
    locations_distance_list = []
    for agent in sim.agents:
        for direction in sim.grid.get_directions_list():
            if not agent.matter_in(direction):
                locations_distance_list.append(get_closest_item_distance(
                    get_coordinates_in_direction(agent.coordinates, direction), sim))
        agent_distance_list.append(get_closest_item_distance(agent.coordinates, sim))
    if agent_distance_list and locations_distance_list:
        if max(agent_distance_list) <= min(locations_distance_list):
            return True
    return False


def get_closest_item_distance(source: agent_class, sim: world) -> int:
    """
    Calculates the distance from the agent to the closest item
    @param source: agent from which to measure distance
    @param sim: The world state containing all items
    @return: Distance from the agent to the closest item
    """
    return min((sim.grid.get_distance(source, item.coordinates) for item in sim.get_items_list()))


