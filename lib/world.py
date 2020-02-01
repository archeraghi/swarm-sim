"""The world module provides the interface of the simulation world. In the simulation world
all the data of the particles, tiles, and locations are stored.
It also have the the coordination system and stated the maximum of the x and y coordinate.

 .. todo:: What happens if the maximum y or x axis is passed? Either the start from the other side or turns back.
"""
import importlib
import logging
import random
import threading
import os
import datetime
import time

from lib import csv_generator, particle, tile, location, vis3d
from lib.swarm_sim_header import eprint


class World:
    def __init__(self, config_data):
        """
        Initializing the world constructor
        :param config_data: configuration data from config.ini file
        """
        self.__round_counter = 1
        self.__end = False

        self.init_particles = []
        self.particle_id_counter = 0
        self.particles = []
        self.particle_map_coordinates = {}
        self.particle_map_id = {}
        self.particles_created = []
        self.particle_rm = []
        self.__particle_deleted = False
        self.new_particle = None

        self.tiles = []
        self.tile_map_coordinates = {}
        self.tile_map_id = {}
        self.tiles_created = []
        self.tiles_rm = []

        self.__tile_deleted = False
        self.new_tile = None
        self.__tile_deleted = False

        self.locations = []
        self.location_map_coordinates = {}
        self.location_map_id = {}
        self.locations_created = []
        self.locations_rm = []
        self.__location_deleted = False
        self.new_location = None

        self.config_data = config_data
        self.grid = config_data.grid

        self.csv_round = csv_generator.CsvRoundData(scenario=config_data.scenario,
                                                    solution=config_data.solution,
                                                    seed=config_data.seed_value,
                                                    directory=config_data.direction_name)

        if config_data.visualization:
            self.vis = vis3d.Visualization(self)
        else:
            self.vis = None

        mod = importlib.import_module('scenario.' + self.config_data.scenario)

        if config_data.visualization:
            import threading
            x = threading.Thread(target=mod.scenario, args=(self,))
            self.vis.wait_for_thread(x, "loading scenario... please wait.", "Loading Scenario")
        else:
            mod.scenario(self)

        if self.config_data.particle_random_order:
            random.shuffle(self.particles)

    def reset(self):
        """
        resets everything (particles, tiles, locations) except for the logging in system.log and in the csv file...
        reloads the scenario.
        :return:
        """
        self.__round_counter = 1
        self.__end = False

        self.init_particles = []
        self.particle_id_counter = 0
        self.particles = []
        self.particles_created = []
        self.particle_rm = []
        self.particle_map_coordinates = {}
        self.particle_map_id = {}
        self.__particle_deleted = False
        self.new_particle = None

        self.tiles = []
        self.tiles_created = []
        self.tiles_rm = []
        self.tile_map_coordinates = {}
        self.tile_map_id = {}
        self.__tile_deleted = False
        self.new_tile = None

        self.locations = []
        self.locations_created = []
        self.location_map_coordinates = {}
        self.location_map_id = {}
        self.locations_rm = []
        self.__location_deleted = False
        self.new_location = None

        if self.config_data.visualization:
            self.vis.reset()

        mod = importlib.import_module('scenario.' + self.config_data.scenario)

        if self.config_data.visualization:
            # if visualization is on, run the scenario in a separate thread and show that the program runs..
            x = threading.Thread(target=mod.scenario, args=(self,))
            self.vis.wait_for_thread(x, "loading scenario... please wait.", "Loading Scenario")
            self.vis.update_visualization_data()

        else:
            # if no vis, just run the scenario on the main thread
            mod.scenario(self)

        if self.config_data.particle_random_order:
            random.shuffle(self.particles)

    def save_scenario(self):

        # create scenario folder, if it doesn't already exist.
        if not os.path.exists("scenario") or not os.path.isdir("scenario"):
            os.mkdir("scenario")

        # if the scenario folder exists, try to create and save the new scenario file, if it fails print the error.
        if os.path.exists("scenario") and os.path.isdir("scenario"):
            now = datetime.datetime.now()
            filename = str("scenario/%d-%d-%d_%d-%d-%d_scenario.py"
                           % (now.year, now.month, now.day, now.hour, now.minute, now.second))
            try:
                f = open(filename, "w+")
                f.write("def scenario(world):\n")
                for p in self.particle_map_coordinates.values():
                    f.write("\tworld.add_particle(%s, color=%s)\n" % (str(p.coordinates), str(p.get_color())))
                for t in self.tile_map_coordinates.values():
                    f.write("\tworld.add_tile(%s, color=%s)\n" % (str(t.coordinates), str(t.get_color())))
                for l in self.location_map_coordinates.values():
                    f.write("\tworld.add_location(%s, color=%s)\n" % (str(l.coordinates), str(l.get_color())))
                f.flush()
                f.close()
            except IOError as e:
                eprint(e)

            # checks if the file exists. If not, some unknown error occured while saving.
            if not os.path.exists(filename) or not os.path.isfile(filename):
                eprint("Error: scenario couldn't be saved due to unknown reasons.")
        else:
            eprint("\"scenario\" folder couldn't be created.")

    def csv_aggregator(self):
        self.csv_round.aggregate_metrics()
        particle_csv = csv_generator.CsvParticleFile(self.config_data.direction_name)
        for p in self.particles:
            particle_csv.write_particle(p)
        particle_csv.csv_file.close()

    def set_successful_end(self):
        self.csv_round.success()
        # self.set_end()

    def get_max_round(self):
        """
        The max round number
    
        :return: maximum round number
        """
        return self.config_data.max_round

    def get_actual_round(self):
        """
        The actual round number

        :return: actual round number
        """
        return self.__round_counter

    def set_unsuccessful_end(self):
        """
        Allows to terminate before the max round is reached
        """
        self.__end = True

    def get_end(self):
        """
            Returns the end parameter values either True or False
        """
        return self.__end

    def inc_round_counter_by(self, number=1):
        """
        Increases the the round counter by

        :return:
        """
        self.__round_counter += number

    def get_solution(self):
        """
        actual solution name

        :return: actual solution name
        """
        return self.config_data.solution

    def get_amount_of_particles(self):
        """
        Returns the actual number of particles in the world

        :return: The actual number of Particles
        """
        return len(self.particles)

    def get_particle_list(self):
        """
        Returns the actual number of particles in the world

        :return: The actual number of Particles
        """
        return self.particles

    def get_particle_map_coordinates(self):
        """
        Get a dictionary with all particles mapped with their actual coordinates

        :return: a dictionary with particles and their coordinates
        """
        return self.particle_map_coordinates

    def get_particle_map_id(self):
        """
        Get a dictionary with all particles mapped with their own ids

        :return: a dictionary with particles and their own ids
        """
        return self.particle_map_id

    def get_amount_of_tiles(self):
        """
        Returns the actual number of particles in the world

        :return: The actual number of Particles
        """
        return len(self.tiles)

    def get_tiles_list(self):
        """
        Returns the actual number of tiles in the world

        :return: a list of all the tiles in the world
        """
        return self.tiles

    def get_tile_map_coordinates(self):
        """
        Get a dictionary with all tiles mapped with their actual coordinates

        :return: a dictionary with particles and their coordinates
        """
        return self.tile_map_coordinates

    def get_tile_map_id(self):
        """
        Get a dictionary with all particles mapped with their own ids

        :return: a dictionary with particles and their own ids
        """
        return self.tile_map_id

    def get_amount_of_locations(self):
        """
        Returns the actual number of locations in the world

        :return: The actual number of locations
        """
        return len(self.locations)

    def get_location_list(self):
        """
        Returns the actual number of locations in the world

        :return: The actual number of locations
        """
        return self.locations

    def get_location_map_coordinates(self):
        """
        Get a dictionary with all locations mapped with their actual coordinates

        :return: a dictionary with locations and their coordinates
        """
        return self.location_map_coordinates

    def get_location_map_id(self):
        """
        Get a dictionary with all locations mapped with their own ids

        :return: a dictionary with locations and their own ids
        """
        return self.location_map_id

    def get_world_x_size(self):
        """

        :return: Returns the maximal x size of the world
        """
        return self.config_data.size_x

    def get_world_y_size(self):
        """
        :return: Returns the maximal y size of the world
        """
        return self.config_data.size_y

    def get_world_z_size(self):
        """

        :return: Returns the maximal z size of the world
        """
        return self.config_data.size_z

    def get_world_size(self):
        """
        :return: Returns the maximal (x,y) size of the world as a tupel
        """
        return self.config_data.size_x, self.config_data.size_y

    def get_tile_deleted(self):
        return self.__tile_deleted

    def get_particle_deleted(self):
        return self.__particle_deleted

    def get_location_deleted(self):
        return self.__location_deleted

    def set_tile_deleted(self):
        self.__tile_deleted = False

    def set_particle_deleted(self):
        self.__particle_deleted = False

    def set_location_deleted(self):
        self.__location_deleted = False

    def add_particle(self, coordinates, color=None):
        """
        Add a particle to the world database

        :param coordinates: The x coordinate of the particle
        :param color: The color of the particle
        :return: Added Matter; False: Unsuccessful
        """

        if len(coordinates) == 2:
            coordinates = (coordinates[0], coordinates[1], 0.0)

        if len(self.particles) < self.config_data.max_particles:
            if self.grid.are_valid_coordinates(coordinates):
                if coordinates not in self.get_particle_map_coordinates():
                    if color is None:
                        color = self.config_data.particle_color
                    self.particle_id_counter += 1
                    self.new_particle = particle.Particle(self, coordinates, color, self.particle_id_counter)
                    if self.vis is not None:
                        self.vis.particle_changed(self.new_particle)
                    self.particles_created.append(self.new_particle)
                    self.particle_map_coordinates[self.new_particle.coordinates] = self.new_particle
                    self.particle_map_id[self.new_particle.get_id()] = self.new_particle
                    self.particles.append(self.new_particle)
                    self.csv_round.update_particle_num(len(self.particles))
                    self.init_particles.append(self.new_particle)
                    self.new_particle.created = True
                    logging.info("Created particle at %s", self.new_particle.coordinates)
                    return self.new_particle

                else:
                    logging.info("there is already a particle on %s" % str(coordinates))
                    return False
            else:
                logging.info("%s is not a valid location!" % str(coordinates))
                return False
        else:
            logging.info("Max of particles reached and no more particles can be created")
            return False

    def remove_particle(self, particle_id):
        """ Removes a particle with a given particle id from the world database


        :param particle_id: particle id
        :return: True: Successful removed; False: Unsuccessful
        """
        rm_particle = self.particle_map_id[particle_id]
        if rm_particle:
            self.particles.remove(rm_particle)
            del self.particle_map_coordinates[rm_particle.coordinates]
            del self.particle_map_id[particle_id]
            self.particle_rm.append(rm_particle)
            if self.vis is not None:
                self.vis.remove_particle(rm_particle)
            self.csv_round.update_particle_num(len(self.particles))
            self.csv_round.update_metrics(particle_deleted=1)
            self.__particle_deleted = True
            return True
        else:
            return False

    def remove_particle_on(self, coordinates):
        """
        Removes a particle on a give coordinate from to the world database

        :param coordinates: A tuple that includes the x and y coordinates
        :return: True: Successful removed; False: Unsuccessful
        """
        if coordinates in self.particle_map_coordinates:
            return self.remove_particle(self.particle_map_coordinates[coordinates].get_id())
        else:
            return False

    def add_tile(self, coordinates, color=None):
        """
        Adds a tile to the world database
        :param color: color of the tile (None for config default)
        :param coordinates: the coordinates on which the tile should be added
        :return: Successful added matter; False: Unsuccessful
        """

        if len(coordinates) == 2:
            coordinates = (coordinates[0], coordinates[1], 0.0)

        if self.grid.are_valid_coordinates(coordinates):
            if coordinates not in self.tile_map_coordinates:
                if color is None:
                    color = self.config_data.tile_color
                self.new_tile = tile.Tile(self, coordinates, color)
                self.tiles.append(self.new_tile)
                if self.vis is not None:
                    self.vis.tile_changed(self.new_tile)
                self.csv_round.update_tiles_num(len(self.tiles))
                self.tile_map_coordinates[self.new_tile.coordinates] = self.new_tile
                self.tile_map_id[self.new_tile.get_id()] = self.new_tile
                logging.info("Created tile with tile id %s on coordinates %s",
                             str(self.new_tile.get_id()), str(coordinates))
                return self.new_tile

            else:
                logging.info("there is already a tile on %s " % str(coordinates))
                return False
        else:
            logging.info("%s is not a valid location!" % str(coordinates))
            return False

    def remove_tile(self, tile_id):
        """
        Removes a tile with a given tile_id from to the world database

        :param tile_id: The tiles id that should be removed
        :return:  True: Successful removed; False: Unsuccessful
        """
        if tile_id in self.tile_map_id:
            rm_tile = self.tile_map_id[tile_id]
            self.tiles.remove(rm_tile)
            self.tiles_rm.append(rm_tile)
            if self.vis is not None:
                self.vis.remove_tile(rm_tile)
            logging.info("Deleted tile with tile id %s on %s", str(rm_tile.get_id()), str(rm_tile.coordinates))
            try:  # cher: added so the program does not crashed if it does not find any entries in the map
                del self.tile_map_id[rm_tile.get_id()]
            except KeyError:
                pass
            try:  # cher: added so the program does not crashed if it does not find any entries in the map
                del self.tile_map_coordinates[rm_tile.coordinates]
            except KeyError:
                pass
            self.csv_round.update_tiles_num(len(self.tiles))
            self.csv_round.update_metrics(tile_deleted=1)
            self.__tile_deleted = True
            return True
        else:
            return False

    def remove_tile_on(self, coordinates):
        """
        Removes a tile on a give coordinates from to the world database

        :param coordinates: A tuple that includes the x and y coordinates
        :return: True: Successful removed; False: Unsuccessful
        """
        if coordinates in self.tile_map_coordinates:
            return self.remove_tile(self.tile_map_coordinates[coordinates].get_id())

        else:
            return False

    def add_location(self, coordinates, color=None):
        """
        Add a tile to the world database

        :param color:
        :param coordinates: the coordinates on which the tile should be added
        :return: True: Successful added; False: Unsuccessful
        """

        if len(coordinates) == 2:
            coordinates = (coordinates[0], coordinates[1], 0.0)

        if self.grid.are_valid_coordinates(coordinates):
            if coordinates not in self.location_map_coordinates:
                if color is None:
                    color = self.config_data.location_color
                self.new_location = location.Location(self, coordinates, color)
                self.locations.append(self.new_location)
                if self.vis is not None:
                    self.vis.location_changed(self.new_location)
                self.location_map_coordinates[self.new_location.coordinates] = self.new_location
                self.location_map_id[self.new_location.get_id()] = self.new_location
                self.csv_round.update_locations_num(len(self.locations))
                logging.info("Created location with id %s on coordinates %s",
                             str(self.new_location.get_id()), str(self.new_location.coordinates))
                self.new_location.created = True
                return self.new_location
            else:
                logging.info("there is already a location on %s" % str(coordinates))
                return False
        else:
            logging.info("%s is not a valid location!" % str(coordinates))
            return False

    def remove_location(self, location_id):
        """
        Removes a tile with a given tile_id from to the world database

        :param location_id: The locations id that should be removed
        :return:  True: Successful removed; False: Unsuccessful
        """
        if location_id in self.location_map_id:
            rm_location = self.location_map_id[location_id]
            if rm_location in self.locations:
                self.locations.remove(rm_location)
            if self.vis is not None:
                self.vis.remove_location(rm_location)
            self.locations_rm.append(rm_location)
            logging.info("Deleted location with location id %s on %s", str(location_id), str(rm_location.coordinates))
            try:
                del self.location_map_coordinates[rm_location.coordinates]
            except KeyError:
                pass
            try:
                del self.location_map_id[location_id]
            except KeyError:
                pass
            self.csv_round.update_locations_num(len(self.locations))
            self.csv_round.update_metrics(location_deleted=1)
            self.__location_deleted = True
            return True
        else:
            return False

    def remove_location_on(self, coordinates):
        """
        Removes a location on a give coordinates from to the world database

        :param coordinates: A tuple that includes the x and y coordinates
        :return: True: Successful removed; False: Unsuccessful
        """
        if coordinates in self.location_map_coordinates:
            return self.remove_location(self.location_map_coordinates[coordinates].get_id())
        else:
            return False
