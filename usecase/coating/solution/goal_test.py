import math
import numpy as np
from lib.swarm_sim_header import *
from lib import world, particle as particle_class


def end_sim(sim: world) -> None:
    """
    Checks if a termination state was reached
    @param sim: The current world state
    """
    if goal_reached(sim):
        if complete_check(sim):
            sim.set_successful_end()
            # own_dists = np.array([p.own_dist for p in sim.particles])
            # unique, counts = np.unique(own_dists, return_counts=True)
            # print(dict(zip(unique, counts)))
            if sim.config_data.visualization:
                print("successful end reached after round:", sim.get_actual_round())


def goal_reached(sim: world) -> bool:
    """
    Checks if a termination state is reached using only information available to the particles
    @param sim: The current world state
    @return: True if a termination state is reached, False otherwise
    """
    min_fl_distance = min(list(map(get_smallest_fl, sim.particles)), default=0)
    max_particle_distance = max((particle.own_dist for particle in sim.particles), default=math.inf)
    if min_fl_distance is math.inf or min_fl_distance < max_particle_distance:
        return False
    else:
        return True


def get_smallest_fl(particle: particle_class) -> int:
    """
    Calculates the lowest distance of all free locations in the particles neighborhood
    @param particle: the particle whose neighborhood to check
    @return: the lowest distance of free locations in the particles neighborhood
    """
    return min((neighbor.dist for neighbor in particle.nh_list if neighbor.type == "fl"), default=math.inf)


def complete_check(sim: world) -> bool:
    """
    Checks if a termination state is reached using global information from the world
    @param sim: The current world state
    @return: True if a termination state is reached, False otherwise
    """
    particle_distance_list = []
    locations_distance_list = []
    for particle in sim.particles:
        for direction in sim.grid.get_directions_list():
            if not particle.matter_in(direction):
                locations_distance_list.append(get_closest_tile_distance(
                    get_coordinates_in_direction(particle.coordinates, direction), sim))
        particle_distance_list.append(get_closest_tile_distance(particle.coordinates, sim))
    if particle_distance_list and locations_distance_list:
        if max(particle_distance_list) <= min(locations_distance_list):
            return True
    return False


def get_closest_tile_distance(source: particle_class, sim: world) -> int:
    """
    Calculates the distance from the particle to the closest tile
    @param source: Particle from which to measure distance
    @param sim: The world state containing all tiles
    @return: Distance from the particle to the closest tile
    """
    return min((sim.grid.get_distance(source, tile.coordinates) for tile in sim.get_tiles_list()))


