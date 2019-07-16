"""
This solution just scans for particles that are within 5 hops range and prints them out.
"""

#Standard Lib that has to be in each solution
from lib.std_lib import *

def solution(sim):

    all_matters_list=[]
    if sim.get_actual_round() == 1:
        all_matters_list=sim.get_particle_map_coords()[(0,0)].scan_for_matter_within(hop=5)
        for list in all_matters_list:
            if list.type=='particle':
                print ("particle at", list.coords)
            elif list.type=='tile':
                print("tile", list.coords)
            elif list.type=='marker':
                print("marker", list.coords)

