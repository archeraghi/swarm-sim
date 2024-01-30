import logging
import random
from solution.utils import *
from solution.goal_params import check_all_goal_params

NE = 0
E = 1
SE = 2
SW = 3
W = 4
NW = 5


direction = [NE, E, SE, SW, W, NW]


def solution(sim):

    for particle in sim.get_particle_list():
        # For every particle in every round, the light beams need to be retraced first
        delete_light_information(sim)
        init_full_light_propagation(sim)

        # Taking the parameters from the multiple simulation
        # If it is a single run, the params can be adjusted here.
        param_lambda = sim.param_lambda
        param_delta = sim.param_delta
        if not sim.multiple:
            param_lambda = 6
            param_delta = 1
        if param_lambda < 0 or param_delta < 0:
            continue
        # Scanning for the particles in the vicinity
        neighbor_list = particle.scan_for_particle_in(1)
        choices = []
        move_decr_edges = detect_valid_move_positions(choices, neighbor_list, particle)
        # The divisor is multiplied with this if the move decreases edges
        prob_divisor = 1
        # This calculates the move probability according to the ASU algorithm
        if move_decr_edges:
            prob_divisor = param_delta
        if particle.read_memory_with("light") is None:
            prob_divisor = prob_divisor * param_lambda
        choice = random.choice((0, 1))
        can_move = True
        # If a tile occupies the space, the particle may not move
        nb_tiles = particle.scan_for_tile_in(1)
        can_move = check_if_tile_occupies_pos(can_move, choice, choices, nb_tiles, particle)
        if len(choices)-1 >= choice and can_move and random.randint(0, prob_divisor - 1) == 0:
            particle.move_to(choices[choice])


# This checks if a tile occupies the position
def check_if_tile_occupies_pos(can_move, choice, choices, nb_tiles, particle):
    if nb_tiles is not None:
        for tile in nb_tiles:
            if len(choices) - 1 >= choice and determine_direction_from_coords(particle.coords, tile.coords) == choices[choice]:
                can_move = False
    return can_move


# This algorithm detects the positions that the particle can move to,
# depending on where it is in the 3-particle system.
# It returns a boolean that shows whether the edges within the system would decrease after a move
def detect_valid_move_positions(choices, neighbor_list, particle):
    move_decr_edges = False
    # This begins the location detection algorithm
    # If there is only one neighbor, the particle may proceed similarly to the 2-particle algorithm
    if len(neighbor_list) == 1:
        move_one_nb_particle(choices, neighbor_list, particle)
    # If there are two neighbors, the particle can be in three different states
    elif len(neighbor_list) == 2:
        move_decr_edges = move_two_nb_particles(choices, move_decr_edges, neighbor_list, particle)
    return move_decr_edges


# This calculates the move  if the particle has two neighbors
def move_two_nb_particles(choices, move_decr_edges, neighbor_list, particle):
    # Calculating the directions of the neighbors
    nbdir = []
    nbdir.append(determine_direction_from_coords(particle.coords, neighbor_list[0].coords))
    nbdir.append(determine_direction_from_coords(particle.coords, neighbor_list[1].coords))
    # In this case, particle is in the middle of a line and can't move
    if (nbdir[0] % 3) != (nbdir[1] % 3):
        # Particle is part of a triangle and has two options to move to
        if (nbdir[0] + nbdir[1]) % 2 == 1:
            move_decr_edges = move_triangle(choices, move_decr_edges, nbdir)
        # The particle is part of a bent curve, which means there is only one location to move to
        elif (nbdir[0] + nbdir[1]) % 2 == 0:
            move_bent_curve(choices, nbdir)
    return move_decr_edges

# This calculates the move if the particle has only one neighbor
# It works like the 2-particle algorithm
def move_one_nb_particle(choices, neighbor_list, particle):
    nbdir = determine_direction_from_coords(particle.coords, neighbor_list[0].coords)
    choices.append((nbdir + 1) % 6)
    choices.append((nbdir - 1) % 6)

# This calculates the move positions if the particle is part of a triangle
def move_triangle(choices, move_decr_edges, nbdir):
    # This is the only move which decreases edges in the system
    move_decr_edges = True
    # This is an edge case in which the regular algorithm fails
    if (nbdir[0] == 5 and nbdir[1] == 0) or (nbdir[0] == 0 and nbdir[1] == 5):
        choices.append(4)
        choices.append(1)
    elif nbdir[0] < nbdir[1]:
        choices.append((nbdir[0] - 1) % 6)
        choices.append((nbdir[1] + 1) % 6)
    elif nbdir[1] < nbdir[0]:
        choices.append((nbdir[0] + 1) % 6)
        choices.append((nbdir[1] - 1) % 6)
    return move_decr_edges

# Here, the particle is in the middle of a slightly bent curve and has exactly one position it can move to
def move_bent_curve(choices, nbdir):
    # The following two are edge cases
    nbsum = nbdir[0] + nbdir[1]
    if (nbdir[0] == 4 or nbdir[1] == 4) and nbsum == 4:
        choices.append(5)
    elif (nbdir[0] == 5 or nbdir[1] == 5) and nbsum == 6:
        choices.append(0)
    else:
        newdir = nbsum / 2
        choices.append(int(newdir))

