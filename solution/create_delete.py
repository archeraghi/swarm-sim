"""
This solution is an example for creating and deleting, particles, tiles or markers
"""

import logging
from locale import str
import random

NE = 0
E = 1
SE = 2
SW = 3
W = 4
NW = 5


direction = [NE, E, SE, SW, W, NW]

def solution(sim):
    if sim.get_actual_round() == 1:
        for particle in sim.get_particle_list():
            print("Sim started")
            particle.create_tile_in(E)
            particle.create_marker_in(W)
    if sim.get_actual_round() == 2:
       if len(sim.get_particle_list()) > 0:
          # sim.get_particle_list()[0].delete_marker_in(W)
           sim.get_particle_list()[0].create_particle_in(W)
           sim.get_particle_list()[0].create_particle_in(W)
    if sim.get_actual_round() == 3:
        if len(sim.get_particle_list()) > 0:
            sim.get_particle_list()[0].take_particle_in(W)
            sim.get_particle_list()[0].delete_particle_in(W)
            sim.get_particle_list()[0].delete_tile_in(E)
    if sim.get_actual_round() == 4:
        sim.get_particle_list()[0].create_tile_on(1,0)
        sim.get_particle_list()[0].create_marker_on(1, 0)
    if sim.get_actual_round() == 5:
        sim.get_particle_list()[0].delete_tile_on(1,0)
    if sim.get_actual_round() == 6:
        sim.get_particle_list()[0].create_particle_on(-1, 0)
        sim.get_particle_list()[0].delete_marker_on(1, 0)
    if sim.get_actual_round() == 7:
        sim.get_particle_list()[0].delete_particle_on(-1, 0)
    if sim.get_actual_round() == 8:
        sim.get_particle_list()[0].create_tile()
        sim.get_particle_list()[0].create_marker()

    if sim.get_actual_round() == 9:
        sim.get_particle_list()[0].delete_tile()
    if sim.get_actual_round() == 12:
        sim.get_particle_list()[0].create_particle()
    if sim.get_actual_round() == 15:
        sim.get_particle_list()[0].delete_particle()
        sim.get_particle_list()[0].delete_marker()
