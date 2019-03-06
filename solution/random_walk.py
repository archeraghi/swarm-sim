import logging
import random

NE = 0
E = 1
SE = 2
SW = 3
W = 4
NW = 5


direction = [NE, E, SE, SW, W, NW]


def solution(sim):

    if sim.get_actual_round() % 2 == 0:
        for particle in sim.get_particle_list():
            particle.move_to(random.choice(direction))