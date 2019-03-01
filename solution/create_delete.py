"""
This solution is an example for creating and deleting, particles, tiles or locations
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

def solution(sim, world):
    if sim.get_actual_round() == 1:
        for particle in world.get_particle_list():
            print("Sim started")
            particle.create_tile_in(E)
            particle.create_location_in(W)
    if sim.get_actual_round() == 2:
       if len(world.get_particle_list()) > 0:
          # world.get_particle_list()[0].delete_location_in(W)
           world.get_particle_list()[0].create_particle_in(W)
           world.get_particle_list()[0].create_particle_in(W)
    if sim.get_actual_round() == 3:
        if len(world.get_particle_list()) > 0:
            world.get_particle_list()[0].take_particle_in(W)
            world.get_particle_list()[0].delete_particle_in(W)
            world.get_particle_list()[0].delete_tile_in(E)
    if sim.get_actual_round() == 4:
        world.get_particle_list()[0].create_tile_on(1,0)
        world.get_particle_list()[0].create_location_on(1, 0)
    if sim.get_actual_round() == 5:
        world.get_particle_list()[0].delete_tile_on(1,0)
    if sim.get_actual_round() == 6:
        world.get_particle_list()[0].create_particle_on(-1, 0)
        world.get_particle_list()[0].delete_location_on(1, 0)
    if sim.get_actual_round() == 7:
        world.get_particle_list()[0].delete_particle_on(-1, 0)
    if sim.get_actual_round() == 8:
        world.get_particle_list()[0].create_tile()
        world.get_particle_list()[0].create_location()

    if sim.get_actual_round() == 9:
        world.get_particle_list()[0].delete_tile()
    if sim.get_actual_round() == 12:
        world.get_particle_list()[0].create_particle()
    if sim.get_actual_round() == 15:
        world.get_particle_list()[0].delete_particle()
        world.get_particle_list()[0].delete_location()
