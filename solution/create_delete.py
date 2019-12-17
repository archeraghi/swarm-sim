"""
This solution is an example for creating and deleting, particles, tiles or locations
"""
from lib.swarm_sim_header import *


def solution(world):

    dirs = world.grid.get_directions_list()
    center = world.grid.get_center()

    if world.get_actual_round() == 1:
        for particle in world.get_particle_list():
            print("World started")
            particle.create_tile_in(dirs[0])
            particle.create_location_in(dirs[1])

    if world.get_actual_round() == 2:
        if len(world.get_particle_list()) > 0:
            world.get_particle_list()[0].create_particle_in(dirs[1])
            world.get_particle_list()[0].create_particle_in(dirs[1])

    if world.get_actual_round() == 3:
        if len(world.get_particle_list()) > 0:
            world.get_particle_list()[0].take_particle_in(dirs[1])
            world.get_particle_list()[0].delete_particle_in(dirs[1])
            world.get_particle_list()[0].delete_tile_in(dirs[0])

    if world.get_actual_round() == 4:
        pos = get_coordinates_in_direction(center, dirs[2])
        world.get_particle_list()[0].create_tile_on(pos)
        world.get_particle_list()[0].create_location_on(pos)

    if world.get_actual_round() == 5:
        pos = get_coordinates_in_direction(center, dirs[2])
        world.get_particle_list()[0].delete_tile_on(pos)

    if world.get_actual_round() == 6:
        pos1 = get_coordinates_in_direction(center, dirs[2])
        pos2 = get_coordinates_in_direction(center, dirs[3])
        world.get_particle_list()[0].create_particle_on(pos2)
        world.get_particle_list()[0].delete_location_on(pos1)

    if world.get_actual_round() == 7:
        pos2 = get_coordinates_in_direction(center, dirs[3])
        world.get_particle_list()[0].delete_particle_on(pos2)

    if world.get_actual_round() == 8:
        world.get_particle_list()[0].create_tile()
        world.get_particle_list()[0].create_location()

    if world.get_actual_round() == 9:
        world.get_particle_list()[0].delete_tile()

    if world.get_actual_round() == 12:
        world.get_particle_list()[0].create_particle()

    if world.get_actual_round() == 15:
        world.get_particle_list()[0].delete_particle()
        world.get_particle_list()[0].delete_location()
