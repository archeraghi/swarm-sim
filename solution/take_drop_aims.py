"""
This solution just scans for particles that are within 5 hops range and prints them out.
"""

#Standard Lib that has to be in each solution
from solution.std_lib import *

def solution(world):
    if world.get_actual_round() == 1 :
        world.get_particle_list()[0].take_tile_in(E)
    elif world.get_actual_round() == 2 :
        world.get_particle_list()[0].drop_tile_in(NW)
    elif world.get_actual_round() == 3 :
        world.get_particle_list()[0].take_particle_in(W)
    elif world.get_actual_round() == 4:
        world.get_particle_list()[0].drop_particle_in(SE)

