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

    all_matters_list=[]
    if self.get_actual_round() == 1:
        all_matters_list=world.get_particle_map_coords()[(0,0)].scan_for_matter_within(hop=5)
        for list in all_matters_list:
            if list.type=='particle':
                print ("particle at", list.coords)
            elif list.type=='tile':
                print("tile", list.coords)
            elif list.type=='location':
                print("location", list.coords)

