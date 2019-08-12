"""
This solution tests all the interfaces that are provided from swarm-sim MAX Round must be at least 41
"""

import logging
import random

#Standard Lib that has to be in each solution
from solution.std_lib import *

def solution(sim):

    if sim.get_actual_round() == 1:
        print ("Scanning for markers, tiles and particles")
        logging.info("Scanning for markers, tiles and particles")
        all_matters_list = sim.get_particle_map_coords()[(0, 0)].scan_for_matter_within()
        for list in all_matters_list:
            if list.type == 'particle':
                print("particle at", list.coords)
            elif list.type == 'tile':
                print("tile", list.coords)
            elif list.type == 'marker':
                print("marker", list.coords)
        print ("Testing Interface: Take Drop Tiles and Particles")
        logging.info("Testing Interface: Take Drop Tiles and Particles")

    elif sim.get_actual_round() == 2 :
        sim.get_particle_list()[0].take_tile_in(E)
    elif sim.get_actual_round() == 3 :
        sim.get_particle_list()[0].take_particle_in(E)
    elif sim.get_actual_round() == 4 :
        sim.get_particle_list()[0].drop_tile_in(E)
        print("Tiles coords ", sim.get_tiles_list()[0].coords[0], sim.get_tiles_list()[0].coords[1])
    elif sim.get_actual_round() == 5:
        print("Tiles coords ", sim.get_tiles_list()[0].coords[0], sim.get_tiles_list()[0].coords[1])
        sim.get_particle_list()[0].take_particle_in(W)
    elif sim.get_actual_round() == 6:
        sim.get_particle_list()[0].drop_particle_in(W)
        sim.get_particle_list()[0].take_tile_in(E)
    elif sim.get_actual_round() == 7:
        sim.get_particle_list()[0].drop_tile()
        sim.get_particle_list()[0].take_tile()
    elif sim.get_actual_round() == 8:
        sim.get_particle_list()[0].drop_particle_in(W)
        sim.get_particle_list()[0].take_particle_in(W)
    elif sim.get_actual_round() == 9:
        sim.get_particle_list()[0].drop_particle()
    elif sim.get_actual_round() == 10:
        if len(sim.get_particle_list()) > 1:
            sim.get_particle_list()[0].take_particle_with(sim.get_particle_list()[1].get_id())
    elif sim.get_actual_round() == 11:
        sim.get_particle_list()[0].drop_particle()
        if len(sim.get_tiles_list()) > 0:
            sim.get_particle_list()[0].take_tile_with(sim.get_tiles_list()[0].get_id())
    elif sim.get_actual_round() == 12:
        sim.get_particle_list()[0].drop_tile()
        sim.get_particle_list()[0].take_tile_on(0,0)
    elif sim.get_actual_round() == 13:
        sim.get_particle_list()[0].drop_tile_on(7,0)
    elif sim.get_actual_round() == 14:
        sim.get_particle_list()[0].take_particle()
    elif sim.get_actual_round() == 15:
        sim.get_particle_list()[0].drop_particle_on(-7, 0)

    elif sim.get_actual_round() == 16:
        logging.info("Testing Read and Write")
        print("Testing Read and Write")
        logging.info("Start Writing ")
        print("Start Writing")

        sim.get_particle_list()[0].write_to_with(sim.markers[0], "K1", "marker Data")
        sim.get_particle_list()[0].write_to_with(sim.tiles[0], "K1", "Tile Data")
        sim.get_particle_list()[0].write_to_with(sim.get_particle_list()[1], "K1", "Particle Data")
    elif sim.get_actual_round() == 17:
        logging.info("Start Reading")
        print("Start Reading")
        loc_data = sim.get_particle_list()[0].read_from_with(sim.markers[0], "K1")
        tile_data = sim.get_particle_list()[0].read_from_with(sim.tiles[0], "K1")
        part_data = sim.get_particle_list()[0].read_from_with(sim.get_particle_list()[1], "K1")

        if loc_data != 0:
            print(loc_data)
        if tile_data != 0:
            print(tile_data)
        if part_data != 0:
            print(part_data)

    elif sim.get_actual_round() > 20:
        for particle in sim.get_particle_list():
            particle.move_to(random.choice(direction))
            if particle.coords in sim.get_tile_map_coords():
                print("Found Tile")
                particle.take_tile()
                particle.carried_tile.set_color(3)
                sim.csv_round_writer.success()
    if sim.get_actual_round() == 24:
        sim.get_particle_list()[1].create_tile()
        sim.get_particle_list()[2].create_marker()
        sim.get_particle_list()[3].create_particle()

    if sim.get_actual_round() == 40:
        sim.get_particle_list()[4].create_tile()
        sim.get_particle_list()[5].create_marker()
        sim.get_particle_list()[6].create_particle()

