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

def solution(self, world):
    if self.get_actual_round() == 1 :
        world.get_particle_list()[0].take_tile_in(E)
    elif self.get_actual_round() == 2 :
        world.get_particle_list()[0].drop_tile_in(NW)
    elif self.get_actual_round() == 3 :
        world.get_particle_list()[0].take_particle_in(W)
    elif self.get_actual_round() == 4:
        world.get_particle_list()[0].drop_particle_in(SE)

