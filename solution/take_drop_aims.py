"""
This solution just scans for particles that are within 5 hops range and prints them out.
"""

import logging
from locale import str

NE = 0
E = 1
SE = 2
SW = 3
W = 4
NW = 5


direction = [NE, E, SE, SW, W, NW]

def solution(sim):
    if sim.get_actual_round() == 1 :
        sim.get_particle_list()[0].take_tile_in(E)
    elif sim.get_actual_round() == 2 :
        sim.get_particle_list()[0].drop_tile_in(NW)
    elif sim.get_actual_round() == 3 :
        sim.get_particle_list()[0].take_particle_in(W)
    elif sim.get_actual_round() == 4:
        sim.get_particle_list()[0].drop_particle_in(SE)

