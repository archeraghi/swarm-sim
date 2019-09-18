"""The world module provides the interface of the simulation world. In the simulation world
all the data of the particles, tiles, and markers are stored.
It also have the the coordination system and stated the maximum of the x and y coordinate.

 .. todo:: What happens if the maximum y or x axis is passed? Either the start from the other side or turns back.
"""
import importlib
import random
import math
import logging
from lib import csv_generator, particle, tile, marker, vis
from lib.swarm_sim_header import *


class World:
    def __init__(self, config_data):
        """
        Initializing the world constructor
        :param seed: seed number for new random numbers
        :param max_round: the max round number for terminating the worldulator
        :param solution: The name of the solution that is going to be used
        :param size_x: the maximal size of the x axes
        :param size_y: the maximal size of the y axes
        :param world_name: the name of the world file that is used to build up the world
        :param solution_name: the name of the solution file that is only used for the csv file
        :param seed: the seed number it is only used here for the csv file
        :param max_particles: the maximal number of particles that are allowed to be or created in this world
        """
        self.__round_counter = 1
        self.__end = False

        self.init_particles=[]
        self.particle_id_counter = 0
        self.particles = []
        self.particles_created = []
        self.particle_rm = []
        self.particle_map_coords = {}
        self.particle_map_id = {}
        self.__particle_deleted=False

        self.tiles = []
        self.tiles_created = []
        self.tiles_rm = []
        self.tile_map_coords = {}
        self.tile_map_id = {}
        self.__tile_deleted=False
        self.new_tile = None

        self.markers = []
        self.markers_created = []
        self.marker_map_coords = {}
        self.marker_map_id = {}
        self.markers_rm = []
        self.__marker_deleted = False

        self.config_data = config_data

        self.csv_round = csv_generator.CsvRoundData(scenario=config_data.scenario,
                                                    solution=config_data.solution,
                                                    seed=config_data.seed_value,
                                                    directory=config_data.direction_name)

        mod = importlib.import_module('scenario.' + self.config_data.scenario)
        mod.scenario(self)

        if self.config_data.particle_random_order:
            random.shuffle(self.particles)

        if config_data.visualization:
            self.window = vis.VisWindow(config_data.window_size_x, config_data.window_size_y, self)

    def csv_aggregator(self):
        self.csv_round.aggregate_metrics()
        particle_csv = csv_generator.CsvParticleFile(self.config_data.direction_name)
        for particle in self.particles:
            particle_csv.write_particle(particle)
        particle_csv.csv_file.close()

    def success_termination(self):
        self.csv_round.success()
        self.set_end()
        
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

    def get_max_round(self):
        """
        The max round number

        :return: maximum round number
        """
        return self.config_data.max_round

    def set_end(self):
        """
        Allows to terminate before the max round is reached
        """
        self.__end=True

    def get_end(self):
        """
            Returns the end parameter values either True or False
        """
        return self.__end

    def inc_round_counter(self):
        """
        Increases the the round counter by

        :return:
        """
        self.__round_counter +=  1

    def get_solution(self):
        """
        actual solution name

        :return: actual solution name
        """
        return self.__solution

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

    def get_particle_map_coords(self):
        """
        Get a dictionary with all particles mapped with their actual coordinates

        :return: a dictionary with particles and their coordinates
        """
        return self.particle_map_coords

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

    def get_tile_map_coords(self):
        """
        Get a dictionary with all tiles mapped with their actual coordinates

        :return: a dictionary with particles and their coordinates
        """
        return self.tile_map_coords

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

    def get_marker_map_coords(self):
        """
        Get a dictionary with all markers mapped with their actual coordinates

        :return: a dictionary with markers and their coordinates
        """
        return self.marker_map_coords

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

    def get_tile_deleted(self):
        return self.__tile_deleted

    def get_particle_deleted(self):
        return self.__particle_deleted

    def get_marker_deleted(self):
        return self.__marker_deleted

    def set_tile_deleted(self):
        self.__tile_deleted = False

    def set_particle_deleted(self):
        self.__particle_deleted=False

    def set_marker_deleted(self):
        self.__marker_deleted = False

    def add_particle(self, x, y, color=black, alpha=1):
        """
        Add a particle to the world database

        :param x: The x coordinate of the particle
        :param y: The y coordinate of the particle
        :param state: The state of the particle. Default: S for for Stopped or Not Moving. Other options
                      are the moving directions: E, SE, SW, W, NW, NE
        :param color: The color of the particle. Coloroptions: black, gray, red, green, or blue
        :return: Added Matter; False: Unsuccsessful
        """
        if alpha < 0 or alpha >1:
            alpha = 1
        if len(self.particles) < self.config_data.max_particles:
            if check_coords(x,y) == True:
                if (x,y) not in self.get_particle_map_coords():
                    self.particle_id_counter += 1
                    new_particle = particle.Particle(self, x, y, color, alpha, self.particle_id_counter)
                    print(new_particle.number)
                    self.particles_created.append(new_particle)
                    self.particle_map_coords[new_particle.coords] = new_particle
                    self.particle_map_id[new_particle.get_id()] = new_particle
                    self.particles.append(new_particle)
                    new_particle.touch()
                    self.csv_round.update_particle_num(len(self.particles))
                    self.init_particles.append(new_particle)
                    new_particle.created=True
                    logging.info("Created particle at %s", new_particle.coords)
                    return new_particle
                else:
                    print("for x %f and y %f not not possible because Particle exist   ", x, y)
                    return False
            else:
                 print ("for x %f and y %f not possible to draw ", x, y)
                 return False
        else:
            logging.info("Max of particles reached and no more particles can be created")
            return False

    def remove_particle(self,id):
        """ Removes a particle with a given particle id from the world database


        :param particle_id: particle id
        :return: True: Successful removed; False: Unsuccessful
        """
        rm_particle = self.particle_map_id[id]
        if rm_particle:
            self.particles.remove(rm_particle)
            try:
                del self.particle_map_coords[rm_particle.coords]
                del self.particle_map_id[id]
            except:
                pass
            self.particle_rm.append(rm_particle)
            self.csv_round.update_particle_num(len(self.particles))
            self.csv_round.update_metrics(particle_deleted=1)
            self.__particle_deleted = True
            return True
        else:
            return False

    def remove_particle_on(self, coords):
        """
        Removes a particle on a give coordinat from to the world database

        :param coords: A tupel that includes the x and y coorindates
        :return: True: Successful removed; False: Unsuccessful
        """
        if coords in self.particle_map_coords:
            self.particles.remove(self.particle_map_coords[coords])
            self.particle_rm.append(self.particle_map_coords[coords])
            try:  # cher: added so the program does not crashed if it does not find any entries in the map
                del self.particle_map_id[self.particle_map_coords[coords].get_id()]
            except KeyError:
                pass
            try:  # cher: added so the program does not crashed if it does not find any entries in the map
                del self.particle_map_coords[coords]
            except KeyError:
                pass
            self.csv_round.update_particle_num(len(self.particles))
            self.csv_round.update_metrics( particle_deleted=1)
            self.__particle_deleted = True
            return True
        else:
            return False

    def add_tile(self, x, y, color=gray, alpha=1):
        """
        Adds a tile to the world database

        :param color:
        :param x: the x coordinates on which the tile should be added
        :param y: the y coordinates on which the tile should be added
        :return: Successful added matter; False: Unsuccsessful
        """
        if alpha < 0 or alpha >1:
            alpha = 1
        if check_coords(x,y) == True:
            if (x,y) not in self.tile_map_coords:
                self.new_tile=tile.Tile(self, x, y, color, alpha)
                print("Before adding ", len(self.tiles) )
                self.tiles.append(self.new_tile)
                self.csv_round.update_tiles_num(len(self.tiles))
                self.tile_map_coords[self.new_tile.coords] = self.new_tile
                self.tile_map_id[self.new_tile.get_id()] = self.new_tile

                print("Afer adding ", len(self.tiles), self.new_tile.coords )
                logging.info("Created tile with tile id %s on coords %s",str(self.new_tile.get_id()), str(self.new_tile.coords))
                self.new_tile.touch()
                return self.new_tile
            else:
                logging.info ("on x %f and y %f coordinates is a tile already", x, y)
                return False
        else:
             logging.info ("for x %f and y %f not possible to draw ", x, y)
             return False

    def add_tile_vis(self, x, y, color=gray, alpha=1):
        """
        Adds a tile to the world database

        :param color:
        :param x: the x coordinates on which the tile should be added
        :param y: the y coordinates on which the tile should be added
        :return: True: Successful added; False: Unsuccsessful
        """
        if check_coords(x, y) == True:
            if (x, y) not in self.tile_map_coords:
                self.new_tile = tile.Tile(self, x, y, color, alpha)
                self.tiles.append(self.new_tile)

                self.tile_map_coords[self.new_tile.coords] = self.new_tile
                self.tile_map_id[self.new_tile.get_id()] = self.new_tile

                print("world.add_tile",self.new_tile.coords)
                logging.info("Created tile with tile id %s on coords %s", str(self.new_tile.get_id()),
                             str(self.new_tile.coords))
                return True
            else:
                logging.info("on x %f and y %f coordinates is a tile already", x, y)
                return False

    def remove_tile(self,id):
        """
        Removes a tile with a given tile_id from to the world database

        :param tile_id: The tiles id that should be removec
        :return:  True: Successful removed; False: Unsuccessful
        """
        if id in self.tile_map_id:
            rm_tile = self.tile_map_id[id]
            rm_tile.touch()
            self.tiles.remove(rm_tile)
            self.tiles_rm.append(rm_tile)
            logging.info("Deleted tile with tile id %s on %s", str(rm_tile.get_id()), str(rm_tile.coords) )
            try:  # cher: added so the program does not crashed if it does not find any entries in the map
                del self.tile_map_id[rm_tile.get_id()]
            except KeyError:
                pass
            try:  # cher: added so the program does not crashed if it does not find any entries in the map
                del self.tile_map_coords[rm_tile.coords]
            except KeyError:
                pass
            self.csv_round.update_tiles_num(len(self.tiles))
            self.csv_round.update_metrics(tile_deleted=1)
            self.__tile_deleted = True
            return True
        else:
            return False

    def remove_tile_on(self, coords):
        """
        Removes a tile on a give coordinat from to the world database

        :param coords: A tupel that includes the x and y coorindates
        :return: True: Successful removed; False: Unsuccessful
        """
        if coords in self.tile_map_coords:
            self.tiles.remove(self.tile_map_coords[coords])
            self.tiles_rm.append(self.tile_map_coords[coords])
            try:  # cher: added so the program does not crashed if it does not find any entries in the map
                del self.tile_map_id[self.tile_map_coords[coords].get_id()]
            except KeyError:
                pass
            try:  # cher: added so the program does not crashed if it does not find any entries in the map
                del self.tile_map_coords[coords]
            except KeyError:
                pass
            self.csv_round.update_tiles_num(len(self.tiles))
            self.csv_round.update_metrics( tile_deleted=1)
            self.__tile_deleted = True
            return True
        else:
            return False

    def add_marker(self, x, y, color=black, alpha=1):
        """
        Add a tile to the world database

        :param color:
        :param x: the x coordinates on which the tile should be added
        :param y: the y coordinates on which the tile should be added
        :return: True: Successful added; False: Unsuccsessful
        """
        if alpha < 0 or alpha >1:
            alpha = 1
        if check_coords(x, y) == True:
            if (x, y) not in self.marker_map_coords:
                self.new_marker = marker.Marker(self, x, y, color, alpha)
                self.markers.append(self.new_marker)
                self.marker_map_coords[self.new_marker.coords] = self.new_marker
                self.marker_map_id[self.new_marker.get_id()] = self.new_marker
                self.csv_round.update_markers_num(len(self.markers))
                logging.info("Created marker with id %s on coords %s", str(self.new_marker.get_id()), str(self.new_marker.coords))

                self.new_marker.created = True
                self.new_marker.touch()
                return self.new_marker
            else:
                logging.info("on x %f and y %f coordinates is a marker already", x, y)
                return False
        else:
            logging.info("for x %f and y %f not possible to draw ", x, y)
            return False

    def remove_marker(self, id):
        """
        Removes a tile with a given tile_id from to the world database

        :param id: The markers id that should be removec
        :return:  True: Successful removed; False: Unsuccessful
        """
        if id in self.marker_map_id:
            rm_marker = self.marker_map_id[id]
            rm_marker.touch()
            if rm_marker in self.markers:
                self.markers.remove(rm_marker)

            self.markers_rm.append(rm_marker)
            logging.info("Deleted marker with marker id %s on %s", str(id), str(rm_marker.coords))
            try:
                del self.marker_map_coords[rm_marker.coords]
            except KeyError:
                pass
            try:
                del self.marker_map_id[id]
            except KeyError:
                pass
            self.csv_round.update_markers_num(len(self.markers))
            self.csv_round.update_metrics( marker_deleted=1)
            self.__marker_deleted = True
            return True
        else:
            return False

    def remove_marker_on(self, coords):
        """
        Removes a marker on a give coordinat from to the world database

        :param coords: A tupel that includes the x and y coorindates
        :return: True: Successful removed; False: Unsuccessful
        """
        if coords in self.marker_map_coords:
            self.markers.remove(self.marker_map_coords[coords])
            self.markers_rm.append(self.marker_map_coords[coords])
            try:  # cher: added so the program does not crashed if it does not find any entries in the map
                del self.marker_map_id[self.marker_map_coords[coords].get_id()]
            except KeyError:
                pass
            try:  # cher: added so the program does not crashed if it does not find any entries in the map
                del self.marker_map_coords[coords]
            except KeyError:
                pass
            self.csv_round.update_markers_num(len(self.markers))
            self.csv_round.update_metrics( marker_deleted=1)
            self.__marker_deleted = True
            return True
        else:
            return False