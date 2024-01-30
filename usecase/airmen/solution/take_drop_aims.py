"""
This solution just scans for particles that are within 5 hops range and prints them out.
"""
#Standard Lib that has to be in each solution
from lib.std_lib import *

def solution(sim):
    if sim.get_actual_round() == 1 :
        sim.get_particle_list()[0].take_tile_in(E)
    elif sim.get_actual_round() == 2 :
        sim.get_particle_list()[0].drop_tile_in(NW)
    elif sim.get_actual_round() == 3 :
        sim.get_particle_list()[0].take_particle_in(W)
    elif sim.get_actual_round() == 4:
        sim.get_particle_list()[0].drop_particle_in(SE)

