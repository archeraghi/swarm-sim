"""The world module provides the interface of the simulation world. In the simulation world
all the data of the particles, tiles, and locations are stored.
It also have the the coordination system and stated the maximum of the x and y coordinate.

 .. todo:: What happens if the maximum y or x axis is passed? Either the start from the other side or turns back.
"""

import importlib
import logging
import random

from lib import particle, tile, location

x_offset = [1, 0.5, -0.5, -1 , -0.5, 0.5, 0]
y_offset = [0, -1, -1, 0, 1, 1, 0]

NE = 0
E = 1
SE = 2
SW = 3
W = 4
NW = 5
S = 6

direction = [NE, E, SE, SW, W, NW, S]

read = 0
write = 1

black = 1
gray = 2
red = 3
green = 4
blue = 5


class World:
    def __init__(self, size_x=0, size_y=0, world_name=None, sim=None, max_particles=50,
                 mm_limitation=False, particle_mm_size=0, tile_mm_size=0, location_mm_size=0, dir="",
                 csv_round="", random_order=False, ms_size=100):
        """Initializing the World constructor

        :param size_x: the maximal size of the x axes
        :param size_y: the maximal size of the y axes
        :param world_name: the name of the world file that is used to build up the world
        :param solution_name: the name of the solution file that is only used for the csv file
        :param seed: the seed number it is only used here for the csv file
        :param max_particles: the maximal number of particles that are allowed to be or created in this world
        """
        self.mm_limitation = mm_limitation
        self.init_particles = []
        self.particle_num = 0
        self.particles = []
        self.particles_created = []
        self.particle_rm = []
        self.particle_map_coords = {}
        self.particle_map_id = {}
        self.particle_mm_size = particle_mm_size
        self.particle_ms_size = ms_size
        self.__particle_deleted = False
        self.tiles_num = 0
        self.tiles = []
        self.tiles_created = []
        self.tiles_rm = []
        self.tile_map_coords = {}
        self.tile_map_id = {}
        self.__tile_deleted = False
        self.new_tile_flag = False
        self.tile_mm_size = tile_mm_size
        self.locations_num = 0
        self.locations = []
        self.locations_created = []
        self.location_map_coords = {}
        self.location_map_id = {}
        self.locations_rm = []
        self.location_mm_size = location_mm_size
        self.__location_deleted = False
        self.new_tile = None
        self.__size_x = size_x
        self.__size_y = size_y
        self.max_particles = max_particles
        self.directory = dir

        # csv attributes
        self.csv_round_writer = csv_round

        mod = importlib.import_module('scenario.' + world_name.rsplit('.', 1)[0])
        mod.create_world(self)
        if random_order:
            random.shuffle(self.particles)

    def get_particles_num(self):
        """
        Returns the actual number of particles in the world

        :return: The actual number of Particles
        """
        return self.tiles_num

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

    def get_tiles_num(self):
        """
        Returns the actual number of particles in the world

        :return: The actual number of Particles
        """
        return self.tiles_num

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

    def get_location_num(self):
        """
        Returns the actual number of locations in the world

        :return: The actual number of locations
        """
        return self.locations_num

    def get_location_list(self):
        """
        Returns the actual number of locations in the world

        :return: The actual number of locations
        """
        return self.locations

    def get_location_map_coords(self):
        """
        Get a dictionary with all locations mapped with their actual coordinates

        :return: a dictionary with locations and their coordinates
        """
        return self.location_map_coords

    def get_location_map_id(self):
        """
        Get a dictionary with all locations mapped with their own ids

        :return: a dictionary with locations and their own ids
        """
        return self.location_map_id

    def get_coords_in_dir(self, coords, dir):
        """
        Returns the coordination data of the pointed directions

        :param coords: particles actual staying coordination
        :param dir: The direction. Options:  E, SE, SW, W, NW, or NE
        :return: The coordinaiton of the pointed directions
        """
        return coords[0] + x_offset[dir], coords[1] + y_offset[dir]

    def get_world_x_size(self):
        """

        :return: Returns the maximal x size of the world
        """
        return self.__size_x

    def get_world_y_size(self):
        """
        :return: Returns the maximal y size of the world
        """
        return self.__size_y

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

    def check_coords(self, coords_x, coords_y):
        """
        Checks if the given coordinates are matching the
        hexagon coordinates

        :param coords_x: proposed x coordinate
        :param coords_y: proposed y coordinate
        :return: True: Correct x and y coordinates; False: Incorrect coordinates
        """

        if (coords_x / 0.5) % 2 == 0:
            if coords_y % 2 != 0:
                return False
            else:
                return True
        else:
            if coords_y % 2 == 0:
                return False
            else:
                return True

    def add_particle(self, x, y, color=black, alpha=1):
        """
        Add a particle to the world database

        :param x: The x coordinate of the particle
        :param y: The y coordinate of the particle
        :param state: The state of the particle. Default: S for for Stopped or Not Moving. Other options
                      are the moving directions: E, SE, SW, W, NW, NE
        :param color: The color of the particle. Coloroptions: black, gray, red, green, or blue
        :return: True: Successful added; False: Unsuccsessful
        """
        if alpha < 0 or alpha > 1:
            alpha = 1
        if len(self.particles) < self.max_particles:
            if self.check_coords(x, y) == True:
                if (x, y) not in self.get_particle_map_coords():
                    new_particle = particle.Particle(self, x, y, color, alpha, self.mm_limitation,
                                                     self.particle_mm_size, ms_size=self.particle_ms_size)
                    self.particles_created.append(new_particle)
                    self.particle_map_coords[new_particle.coords] = new_particle
                    self.particle_map_id[new_particle.get_id()] = new_particle
                    self.particles.append(new_particle)
                    new_particle.touch()
                    self.csv_round_writer.update_particle_num(len(self.particles))
                    self.init_particles.append(new_particle)
                    new_particle.created = True
                    logging.info("Created particle at %s", new_particle.coords)
                    return True
                else:
                    print("for x %f and y %f not not possible because Particle exist   ", x, y)
                    return False
            else:
                print("for x %f and y %f not possible to draw ", x, y)
                return False
        else:
            logging.info("Max of particles reached and no more particles can be created")
            return False

    def remove_particle(self, id):
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
            self.csv_round_writer.update_particle_num(len(self.particles))
            self.csv_round_writer.update_metrics(particle_deleted=1)
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
            # del self.tile_map_coords[rm_tile.coords]
            try:  # cher: added so the program does not crashed if it does not find any entries in the map
                del self.particle_map_id[self.particle_map_coords[coords].get_id()]
            except KeyError:
                pass
            try:  # cher: added so the program does not crashed if it does not find any entries in the map
                del self.particle_map_coords[coords]
            except KeyError:
                pass
            self.csv_round_writer.update_particle_num(len(self.particles))
            self.csv_round_writer.update_metrics(particle_deleted=1)
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
        :return: True: Successful added; False: Unsuccsessful
        """
        if alpha < 0 or alpha > 1:
            alpha = 1
        if self.check_coords(x, y) == True:
            if (x, y) not in self.tile_map_coords:
                self.new_tile = tile.Tile(self, x, y, color, alpha, self.mm_limitation, self.tile_mm_size)
                print("Before adding ", len(self.tiles))
                self.tiles.append(self.new_tile)
                self.csv_round_writer.update_tiles_num(len(self.tiles))
                self.tile_map_coords[self.new_tile.coords] = self.new_tile
                self.tile_map_id[self.new_tile.get_id()] = self.new_tile

                print("Afer adding ", len(self.tiles), self.new_tile.coords)
                logging.info("Created tile with tile id %s on coords %s", str(self.new_tile.get_id()),
                             str(self.new_tile.coords))
                self.new_tile.touch()
                return True
            else:
                logging.info("on x %f and y %f coordinates is a tile already", x, y)
                return False
        else:
            logging.info("for x %f and y %f not possible to draw ", x, y)
            return False

    def add_tile_vis(self, x, y, color=gray, alpha=1):
        """
        Adds a tile to the world database

        :param color:
        :param x: the x coordinates on which the tile should be added
        :param y: the y coordinates on which the tile should be added
        :return: True: Successful added; False: Unsuccsessful
        """
        if self.check_coords(x, y) == True:
            if (x, y) not in self.tile_map_coords:
                self.new_tile = tile.Tile(self, x, y, color, alpha, self.mm_limitation, self.tile_mm_size)
                self.tiles.append(self.new_tile)

                self.tile_map_coords[self.new_tile.coords] = self.new_tile
                self.tile_map_id[self.new_tile.get_id()] = self.new_tile

                print("world.add_tile", self.new_tile.coords)
                logging.info("Created tile with tile id %s on coords %s", str(self.new_tile.get_id()),
                             str(self.new_tile.coords))
                return True
            else:
                logging.info("on x %f and y %f coordinates is a tile already", x, y)
                return False

    def remove_tile(self, id):
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
            logging.info("Deleted tile with tile id %s on %s", str(rm_tile.get_id()), str(rm_tile.coords))
            # del self.tile_map_coords[rm_tile.coords]
            try:  # cher: added so the program does not crashed if it does not find any entries in the map
                del self.tile_map_id[rm_tile.get_id()]
            except KeyError:
                pass
            try:  # cher: added so the program does not crashed if it does not find any entries in the map
                del self.tile_map_coords[rm_tile.coords]
            except KeyError:
                pass
            self.csv_round_writer.update_tiles_num(len(self.tiles))
            self.csv_round_writer.update_metrics(tile_deleted=1)
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
            # del self.tile_map_coords[rm_tile.coords]
            try:  # cher: added so the program does not crashed if it does not find any entries in the map
                del self.tile_map_id[self.tile_map_coords[coords].get_id()]
            except KeyError:
                pass
            try:  # cher: added so the program does not crashed if it does not find any entries in the map
                del self.tile_map_coords[coords]
            except KeyError:
                pass
            self.csv_round_writer.update_tiles_num(len(self.tiles))
            self.csv_round_writer.update_metrics(tile_deleted=1)
            self.__tile_deleted = True
            return True
        else:
            return False

    def add_location(self, x, y, color=black, alpha=1):
        """
        Add a tile to the world database

        :param color:
        :param x: the x coordinates on which the tile should be added
        :param y: the y coordinates on which the tile should be added
        :return: True: Successful added; False: Unsuccsessful
        """
        if alpha < 0 or alpha > 1:
            alpha = 1
        if self.check_coords(x, y) == True:
            if (x, y) not in self.location_map_coords:
                self.new_location = location.Location(self, x, y, color, alpha, self.mm_limitation,
                                                      self.location_mm_size)
                self.locations.append(self.new_location)
                self.location_map_coords[self.new_location.coords] = self.new_location
                self.location_map_id[self.new_location.get_id()] = self.new_location
                self.csv_round_writer.update_locations_num(len(self.locations))
                logging.info("Created location with id %s on coords %s", str(self.new_location.get_id()),
                             str(self.new_location.coords))

                self.new_location.created = True
                self.new_location.touch()
                return self.new_location
            else:
                logging.info("on x %f and y %f coordinates is a location already", x, y)
                return False
        else:
            logging.info("for x %f and y %f not possible to draw ", x, y)

    def remove_location(self, id):
        """
        Removes a tile with a given tile_id from to the world database

        :param id: The locations id that should be removec
        :return:  True: Successful removed; False: Unsuccessful
        """
        if id in self.location_map_id:
            rm_location = self.location_map_id[id]
            rm_location.touch()
            if rm_location in self.locations:
                self.locations.remove(rm_location)

            self.locations_rm.append(rm_location)
            logging.info("Deleted location with location id %s on %s", str(id), str(rm_location.coords))
            try:
                del self.location_map_coords[rm_location.coords]
            except KeyError:
                pass
            try:
                del self.location_map_id[id]
            except KeyError:
                pass
            self.csv_round_writer.update_locations_num(len(self.locations))
            self.csv_round_writer.update_metrics(location_deleted=1)
            self.__location_deleted = True
            return True
        else:
            return False

    def remove_location_on(self, coords):
        """
        Removes a location on a give coordinat from to the world database

        :param coords: A tupel that includes the x and y coorindates
        :return: True: Successful removed; False: Unsuccessful
        """
        if coords in self.location_map_coords:
            self.locations.remove(self.location_map_coords[coords])
            self.locations_rm.append(self.location_map_coords[coords])
            try:  # cher: added so the program does not crashed if it does not find any entries in the map
                del self.location_map_id[self.location_map_coords[coords].get_id()]
            except KeyError:
                pass
            try:  # cher: added so the program does not crashed if it does not find any entries in the map
                del self.location_map_coords[coords]
            except KeyError:
                pass
            self.csv_round_writer.update_locations_num(len(self.locations))
            self.csv_round_writer.update_metrics(location_deleted=1)
            self.__location_deleted = True
            return True
        else:
            return False
