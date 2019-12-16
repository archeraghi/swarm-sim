"""The world module provides the interface of the simulation world. In the simulation world
all the data of the particles, tiles, and markers are stored.
It also have the the coordination system and stated the maximum of the x and y coordinate.

 .. todo:: What happens if the maximum y or x axis is passed? Either the start from the other side or turns back.
"""
import importlib
import logging
import random
import threading

from lib import csv_generator, particle, tile, marker, vis3d


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

        self.markers = []
        self.marker_map_coordinates = {}
        self.marker_map_id = {}
        self.markers_created = []
        self.markers_rm = []
        self.__marker_deleted = False
        self.new_marker = None

        self.config_data = config_data
        self.grid = config_data.grid

        self.csv_round = csv_generator.CsvRoundData(scenario=config_data.scenario,
                                                    solution=config_data.solution,
                                                    seed=config_data.seed_value,
                                                    directory=config_data.direction_name)

        if config_data.visualization:
            self.vis = vis3d.Visualization(self)

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
        resets everything (particles, tiles, markers) except for the logging in system.log and in the csv file...
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

        self.markers = []
        self.markers_created = []
        self.marker_map_coordinates = {}
        self.marker_map_id = {}
        self.markers_rm = []
        self.__marker_deleted = False
        self.new_marker = None

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

    def get_amount_of_markers(self):
        """
        Returns the actual number of markers in the world

        :return: The actual number of markers
        """
        return len(self.markers)

    def get_marker_list(self):
        """
        Returns the actual number of markers in the world

        :return: The actual number of markers
        """
        return self.markers

    def get_marker_map_coordinates(self):
        """
        Get a dictionary with all markers mapped with their actual coordinates

        :return: a dictionary with markers and their coordinates
        """
        return self.marker_map_coordinates

    def get_marker_map_id(self):
        """
        Get a dictionary with all markers mapped with their own ids

        :return: a dictionary with markers and their own ids
        """
        return self.marker_map_id

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

    def get_world_size(self):
        """
        :return: Returns the maximal (x,y) size of the world as a tupel
        """
        return self.config_data.size_x, self.config_data.size_y

    def get_tile_deleted(self):
        return self.__tile_deleted

    def get_particle_deleted(self):
        return self.__particle_deleted

    def get_marker_deleted(self):
        return self.__marker_deleted

    def set_tile_deleted(self):
        self.__tile_deleted = False

    def set_particle_deleted(self):
        self.__particle_deleted = False

    def set_marker_deleted(self):
        self.__marker_deleted = False

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
            if self.grid.is_valid_location(coordinates):
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
            return self.remove_particle(self.particle_map_coordinates[coordinates])
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

        if self.grid.is_valid_location(coordinates):
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

    def add_marker(self, coordinates, color=None):
        """
        Add a tile to the world database

        :param color:
        :param coordinates: the coordinates on which the tile should be added
        :return: True: Successful added; False: Unsuccessful
        """

        if len(coordinates) == 2:
            coordinates = (coordinates[0], coordinates[1], 0.0)

        if self.grid.is_valid_location(coordinates):
            if coordinates not in self.marker_map_coordinates:
                if color is None:
                    color = self.config_data.marker_color
                self.new_marker = marker.Marker(self, coordinates, color)
                self.markers.append(self.new_marker)
                if self.vis is not None:
                    self.vis.marker_changed(self.new_marker)
                self.marker_map_coordinates[self.new_marker.coordinates] = self.new_marker
                self.marker_map_id[self.new_marker.get_id()] = self.new_marker
                self.csv_round.update_markers_num(len(self.markers))
                logging.info("Created marker with id %s on coordinates %s",
                             str(self.new_marker.get_id()), str(self.new_marker.coordinates))
                self.new_marker.created = True
                return self.new_marker
            else:
                logging.info("there is already a marker on %s" % str(coordinates))
                return False
        else:
            logging.info("%s is not a valid location!" % str(coordinates))
            return False

    def remove_marker(self, marker_id):
        """
        Removes a tile with a given tile_id from to the world database

        :param marker_id: The markers id that should be removed
        :return:  True: Successful removed; False: Unsuccessful
        """
        if marker_id in self.marker_map_id:
            rm_marker = self.marker_map_id[marker_id]
            if rm_marker in self.markers:
                self.markers.remove(rm_marker)
            if self.vis is not None:
                self.vis.remove_marker(rm_marker)
            self.markers_rm.append(rm_marker)
            logging.info("Deleted marker with marker id %s on %s", str(marker_id), str(rm_marker.coordinates))
            try:
                del self.marker_map_coordinates[rm_marker.coordinates]
            except KeyError:
                pass
            try:
                del self.marker_map_id[marker_id]
            except KeyError:
                pass
            self.csv_round.update_markers_num(len(self.markers))
            self.csv_round.update_metrics(marker_deleted=1)
            self.__marker_deleted = True
            return True
        else:
            return False

    def remove_marker_on(self, coordinates):
        """
        Removes a marker on a give coordinates from to the world database

        :param coordinates: A tuple that includes the x and y coordinates
        :return: True: Successful removed; False: Unsuccessful
        """
        if coordinates in self.marker_map_coordinates:
            return self.remove_marker(self.marker_map_coordinates[coordinates].get_id())
        else:
            return False
