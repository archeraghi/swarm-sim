import random
from solution.goal_params import check_all_goal_params
from solution.utils import *

NE = 0
E = 1
SE = 2
SW = 3
W = 4
NW = 5


direction = [NE, E, SE, SW, W, NW]


def solution(sim):
    # Algorithm for 2-Particle phototaxing.
    for particle in sim.get_particle_list():
        delete_light_information(sim)
        init_full_light_propagation(sim)

        # If the simulation is not part of multiple tests, the parameter lambda has to be declared here
        param_lambda = sim.param_lambda
        if not sim.multiple:
            param_lambda = 6

        # Get the neighboring particle's position (If there are <1 or >1 there is something wrong)
        neighbor_list = particle.scan_for_particle_in(1)
        if neighbor_list is not None and len(neighbor_list) == 1:
            calculate_positions_and_move(neighbor_list, param_lambda, particle, sim)


def calculate_positions_and_move(list, param_lambda, particle, sim):
    # Calculating the possible positions to move to
    direction_of_neighbor = determine_direction_from_coords(particle.coords, list[0].coords)
    possible_locations = [-1, -1]
    possible_locations[0] = (direction_of_neighbor - 1) % 6
    possible_locations[1] = (direction_of_neighbor + 1) % 6
    # If the position is unoccupied, add the position to the choices
    choices = []
    if sim.get_tile_map_coords().get(
            determine_coords_from_direction(particle.coords, possible_locations[0])) is None:
        choices.insert(0, possible_locations[0])
    if sim.get_tile_map_coords().get(
            determine_coords_from_direction(particle.coords, possible_locations[1])) is None:
        choices.insert(0, possible_locations[1])
    # If the particle senses light, move to one of the choices
    # If not, move to one of the choices with a 25% probability
    if particle.read_memory_with("light") is not None or random.randint(0, param_lambda - 1) == 0:
        particle.move_to(random.choice(choices))
