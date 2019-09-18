"""
This solution is an example for creating and deleting, particles, tiles or markers
"""
#Standard Lib that has to be in each solution
from lib.swarm_sim_header import *

def solution(world):
    if world.get_actual_round() == 1:
        for particle in world.get_particle_list():
            print("World started")
            particle.create_tile_in(E)
            particle.create_marker_in(W)
    if world.get_actual_round() == 2:
       if len(world.get_particle_list()) > 0:
          # world.get_particle_list()[0].delete_marker_in(W)
           world.get_particle_list()[0].create_particle_in(W)
           world.get_particle_list()[0].create_particle_in(W)
    if world.get_actual_round() == 3:
        if len(world.get_particle_list()) > 0:
            world.get_particle_list()[0].take_particle_in(W)
            world.get_particle_list()[0].delete_particle_in(W)
            world.get_particle_list()[0].delete_tile_in(E)
    if world.get_actual_round() == 4:
        world.get_particle_list()[0].create_tile_on(1,0)
        world.get_particle_list()[0].create_marker_on(1, 0)
    if world.get_actual_round() == 5:
        world.get_particle_list()[0].delete_tile_on(1,0)
    if world.get_actual_round() == 6:
        world.get_particle_list()[0].create_particle_on(-1, 0)
        world.get_particle_list()[0].delete_marker_on(1, 0)
    if world.get_actual_round() == 7:
        world.get_particle_list()[0].delete_particle_on(-1, 0)
    if world.get_actual_round() == 8:
        world.get_particle_list()[0].create_tile()
        world.get_particle_list()[0].create_marker()

    if world.get_actual_round() == 9:
        world.get_particle_list()[0].delete_tile()
    if world.get_actual_round() == 12:
        world.get_particle_list()[0].create_particle()
    if world.get_actual_round() == 15:
        world.get_particle_list()[0].delete_particle()
        world.get_particle_list()[0].delete_marker()
