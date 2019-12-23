"""
.. module:: particle
   :platform: Unix, Windows
   :synopsis: This module provides the interfaces of the robotics particle

.. moduleauthor:: Ahmad Reza Cheraghi

TODO: Erase Memory

"""

import logging
from lib import csv_generator, matter
from lib.swarm_sim_header import *


class Particle(matter.Matter):

    def __init__(self, world, coordinates, color, particle_counter=0):
        """Initializing the particle constructor"""
        super().__init__(world, coordinates, color,
                         type="particle", mm_size=world.config_data.particle_mm_size)
        self.number = particle_counter
        self.__isCarried = False
        self.carried_tile = None
        self.carried_particle = None
        self.steps = 0
        self.csv_particle_writer = csv_generator.CsvParticleData(self.get_id(), self.number)

    def has_tile(self):
        if self.carried_tile is None:
            return False
        else:
            return True

    def has_particle(self):
        if self.carried_particle is None:
            return False
        else:
            return True

    def get_carried_status(self):
        """
        Get the status if it is taken or not

        :return: Tiles status
        """
        return self.__isCarried

    def check_on_tile(self):
        """
        Checks if the particle is on a tile

        :return: True: On a tile; False: Not on a Tile
        """
        if self.coordinates in self.world.tile_map_coordinates:
            return True
        else:
            return False

    def check_on_particle(self):
        """
        Checks if the particle is on a particle

        :return: True: On a particle; False: Not on a particle
        """
        if self.coordinates in self.world.particle_map_coordinates:
            return True
        else:
            return False

    def check_on_location(self):
        """
        Checks if the particle is on a location

        :return: True: On a location; False: Not on a location
        """
        if self.coordinates in self.world.location_map_coordinates:
            return True
        else:
            return False

    def move_to(self, direction):
        """
        Moves the particle to the given direction

        :param direction: The direction is defined by loaded grid class
        :return: True: Success Moving;  False: Non moving
        """
        direction_coord = get_coordinates_in_direction(self.coordinates, direction)
        direction, direction_coord = self.check_within_border(direction, direction_coord)
        if self.world.grid.are_valid_coordinates(direction_coord) \
        and direction_coord not in self.world.particle_map_coordinates:
            if self.coordinates in self.world.particle_map_coordinates:
                del self.world.particle_map_coordinates[self.coordinates]
            self.coordinates = direction_coord
            self.world.particle_map_coordinates[self.coordinates] = self
            if self.world.vis is not None:
                self.world.vis.particle_changed(self)
            logging.info("particle %s successfully moved to %s", str(self.get_id()), direction)
            self.world.csv_round.update_metrics(steps=1)
            self.csv_particle_writer.write_particle(steps=1)
            self.check_for_carried_tile_or_particle()
            return True

        return False

    def check_for_carried_tile_or_particle(self):
        if self.carried_tile is not None:
            self.carried_tile.coordinates = self.coordinates
            if self.world.vis is not None:
                self.world.vis.tile_changed(self.carried_tile)
        elif self.carried_particle is not None:
            self.carried_particle.coordinates = self.coordinates
            if self.world.vis is not None:
                self.world.vis.particle_changed(self.carried_particle)

    def check_within_border(self, direction, direction_coord):
        if self.world.config_data.border == 1 and \
                (abs(direction_coord[0]) > self.world.get_sim_x_size() or abs(
                    direction_coord[1]) > self.world.get_sim_y_size()):
            direction = direction - 3 if direction > 2 else direction + 3
            direction_coord = get_coordinates_in_direction(self.coordinates, direction)
        return direction, direction_coord

    def read_from_with(self, target, key=None):
        """
        Read the memories from the matters (particle, tile, or location object) memories with a given keyword

        :param target: The matter can be either a particle, tile, or location
        :param key: A string keyword to searcg for the data in the memory
        :return: The matters memory; None
        """
        if key is not None:
            tmp_memory = target.read_memory_with(key)
        else:
            tmp_memory = target.read_whole_memory()

        if tmp_memory is not None \
        and not (hasattr(tmp_memory, '__len__')) or len(tmp_memory) > 0:
            if target.type == "particle":
                self.world.csv_round.update_metrics(particle_read=1)
                self.csv_particle_writer.write_particle(particle_read=1)
            elif target.type == "tile":
                self.world.csv_round.update_metrics(tile_read=1)
                self.csv_particle_writer.write_particle(tile_read=1)
            elif target.type == "location":
                self.world.csv_round.update_metrics(location_read=1)
                self.csv_particle_writer.write_particle(location_read=1)
            return tmp_memory
        return None

    def matter_in(self, direction):
        """
        :param direction: the directionection to check if a matter is there
        :return: True: if a matter is there, False: if not
        """
        if get_coordinates_in_direction(self.coordinates, direction) in self.world.get_tile_map_coordinates() \
                or get_coordinates_in_direction(self.coordinates, direction) \
                in self.world.get_particle_map_coordinates() \
                or get_coordinates_in_direction(self.coordinates, direction) \
                in self.world.get_location_map_coordinates():
            return True
        else:
            return False

    def tile_in(self, direction):
        """
        :param direction: the direction to check if a tile is there
        :return: True: if a tile is there, False: if not
        """
        if get_coordinates_in_direction(self.coordinates, direction) in self.world.get_tile_map_coordinates():
            return True
        else:
            return False

    def particle_in(self, direction):
        """
        :param direction: the direction to check if a particle is there
        :return: True: if a particle is there, False: if not
        """
        if get_coordinates_in_direction(self.coordinates, direction) in self.world.get_particle_map_coordinates():
            return True
        else:
            return False

    def location_in(self, direction):
        """
        :param direction: the direction to check if a location is there
        :return: True: if a location is there, False: if not
        """
        if get_coordinates_in_direction(self.coordinates, direction) in self.world.get_location_map_coordinates():
            return True
        else:
            return False

    def get_matter_in(self, direction):
        if get_coordinates_in_direction(self.coordinates, direction) in self.world.get_tile_map_coordinates():
            return self.world.get_tile_map_coordinates()[get_coordinates_in_direction(self.coordinates, direction)]
        elif get_coordinates_in_direction(self.coordinates, direction) in self.world.get_particle_map_coordinates():
            return self.world.get_particle_map_coordinates()[get_coordinates_in_direction(self.coordinates, direction)]
        elif get_coordinates_in_direction(self.coordinates, direction) in self.world.get_location_map_coordinates():
            return self.world.get_location_map_coordinates()[get_coordinates_in_direction(self.coordinates, direction)]
        else:
            return False

    def get_tile_in(self, direction):
        if get_coordinates_in_direction(self.coordinates, direction) in self.world.get_tile_map_coordinates():
            return self.world.get_tile_map_coordinates()[get_coordinates_in_direction(self.coordinates, direction)]
        else:
            return False

    def get_particle_in(self, direction):
        if get_coordinates_in_direction(self.coordinates, direction) in self.world.get_particle_map_coordinates():
            return self.world.get_particle_map_coordinates()[get_coordinates_in_direction(self.coordinates, direction)]
        else:
            return False

    def get_location_in(self, direction):
        if get_coordinates_in_direction(self.coordinates, direction) in self.world.get_location_map_coordinates():
            return self.world.get_location_map_coordinates()[get_coordinates_in_direction(self.coordinates, direction)]
        else:
            return False

    def get_location(self):
        if self.coordinates in self.world.location_map_coordinates:
            return self.world.get_location_map_coordinates()[self.coordinates]
        else:
            return False

    def get_tile(self):
        if self.coordinates in self.world.get_tile_map_coordinates():
            return self.world.get_tile_map_coordinates()[self.coordinates]
        else:
            return False

    def write_to_with(self, target, key=None, data=None):
        """
        Writes data with given a keyword direction on the matters (particle, tile, or location object) memory

        :param target: The matter can be either a particle, tile, or location
        :param key: A string keyword so to order the data that is written into the memory
        :param data: The data that should be stored into the memory
        :return: True: Successful written into the memory; False: Unsuccessful
        """
        if data is not None:
            if key is None:
                wrote = target.write_memory(data)
            else:
                wrote = target.write_memory_with(key, data)
            if wrote:
                if target.type == "particle":
                    self.world.csv_round.update_metrics(particle_write=1)
                    self.csv_particle_writer.write_particle(particle_write=1)
                elif target.type == "tile":
                    self.world.csv_round.update_metrics(tile_write=1)
                    self.csv_particle_writer.write_particle(tile_write=1)
                elif target.type == "location":
                    self.world.csv_round.update_metrics(location_write=1)
                    self.csv_particle_writer.write_particle(location_write=1)
                return True
            else:
                return False
        else:
            return False

    def scan_for_matters_within(self, matter_type='all', hop=1):
        """
        Scans for particles, tiles, or locations on a given hop distance and all the matters within the hop distance

        :todo: If nothing then everything should be scanned

        :param matter_type: For what matter this method should scan for.
                            Can be either particles, tiles, locations, or (default) all
        :param hop: The hop distance from the actual position of the scanning particle
        :return: A list of the founded matters
        """

        within_hop_list = []
        for i in range(hop + 1):
            in_list = self.scan_for_matters_in(matter_type, i)
            if in_list is not None:
                within_hop_list.extend(in_list)
        if len(within_hop_list) != 0:
            return within_hop_list
        else:
            return None

    def scan_for_matters_in(self, matter_type='all', hop=1):
        """
         Scanning for particles, tiles, or locations on a given hop distance

         :param matter_type: For what matter this method should scan for.
                             Can be either particles, tiles, locations, or (default) all
         :param hop: The hop distance from thee actual position of the scanning particle
         :return: A list of the founded matters
         """

        logging.info("particle on %s is scanning for %s in %i hops", str(self.coordinates), matter_type, hop)

        if matter_type == "particles":
            scanned_list = scan_in(self.world.particle_map_coordinates, self.coordinates, hop, self.world.grid)
        elif matter_type == "tiles":
            scanned_list = scan_in(self.world.tile_map_coordinates, self.coordinates, hop, self.world.grid)
        elif matter_type == "locations":
            scanned_list = scan_in(self.world.location_map_coordinates, self.coordinates, hop, self.world.grid)
        else:
            scanned_list = []
            scanned_list.extend(scan_in(self.world.particle_map_coordinates, self.coordinates, hop, self.world.grid))
            scanned_list.extend(scan_in(self.world.tile_map_coordinates, self.coordinates, hop, self.world.grid))
            scanned_list.extend(scan_in(self.world.location_map_coordinates, self.coordinates, hop, self.world.grid))
        return scanned_list

    def scan_for_particles_within(self, hop=1):
        """
        Scans for particles on a given hop distance and all the matters within the hop distance

        :todo: If nothing then everything should be scanned

        :param hop: The hop distance from the actual position of the scanning particle
        :return: A list of the founded matters
        """
        return scan_within(self.world.particle_map_coordinates, self.coordinates, hop, self.world.grid)

    def scan_for_particles_in(self, hop=1):
        """
        Scanning for particles on a given hop distance

        :param hop: The hop distance from thee actual position of the scanning particle
        :return: A list of the founded matters
        """

        return scan_in(self.world.particle_map_coordinates, self.coordinates, hop, self.world.grid)

    def scan_for_tiles_within(self, hop=1):
        """
        Scans for tiles on a given hop distance and all the matters within the hop distance

        :todo: If nothing then everything should be scanned

        :param hop: The hop distance from the actual position of the scanning particle
        :return: A list of the founded matters
        """

        return scan_within(self.world.tile_map_coordinates, self.coordinates, hop, self.world.grid)

    def scan_for_tiles_in(self, hop=1):
        """
        Scanning for tiles on a given hop distance

        :param hop: The hop distance from thee actual position of the scanning particle
        :return: A list of the founded matters
        """
        return scan_in(self.world.tile_map_coordinates, self.coordinates, hop, self.world.grid)

    def scan_for_locations_within(self, hop=1):
        """
        Scans for particles, tiles, or location on a given hop distance and all the matters within the hop distance

        :todo: If nothing then everything should be scanned

        :param hop: The hop distance from the actual position of the scanning particle
        :return: A list of the founded matters
        """

        return scan_within(self.world.location_map_coordinates, self.coordinates, hop, self.world.grid)

    def scan_for_locations_in(self, hop=1):
        """
        Scanning for particles, tiles, or location on a given hop distance

        :param hop: The hop distance from thee actual position of the scanning particle
        :return: A list of the founded matters
        """
        return scan_in(self.world.location_map_coordinates, self.coordinates, hop, self.world.grid)

    def take_me(self, coordinates):
        """
        The particle is getting taken from the the other particle on the given coordinate

        :param coordinates, the coordinates of the particle which takes this particle
        :return: True: Successful taken; False: Cannot be taken or wrong Coordinates
        """

        if not self.__isCarried:
            if self.coordinates in self.world.particle_map_coordinates:
                del self.world.particle_map_coordinates[self.coordinates]
            self.__isCarried = True
            self.coordinates = coordinates
            if self.world.vis is not None:
                self.world.vis.particle_changed(self)
            return True
        else:
            return False

    def drop_me(self, coordinates):
        """
        The actual particle is getting dropped

        :param coordinates: the given position
        :return: None
        """
        self.coordinates = coordinates
        self.world.particle_map_coordinates[coordinates] = self
        self.__isCarried = False
        if self.world.vis is not None:
            self.world.vis.particle_changed(self)

    def create_tile(self):
        """
        Creates a tile on the particles actual position

        :return: New Tile or False
        """
        logging.info("Going to create a tile on position %s", str(self.coordinates))
        new_tile = self.world.add_tile(self.coordinates)
        if new_tile:
            self.world.tile_map_coordinates[self.coordinates].created = True
            self.csv_particle_writer.write_particle(tile_created=1)
            self.world.csv_round.update_tiles_num(len(self.world.get_tiles_list()))
            self.world.csv_round.update_metrics(tile_created=1)
            return new_tile
        else:
            return False

    def create_tile_in(self, direction=None):
        """
        Creates a tile either in a given direction

        :param direction: The direction on which the tile should be created.
        :return: New tile or False
        """
        logging.info("particle with id %s is" % self.get_id())
        logging.info("Going to create a tile in %s " % str(direction))
        if direction is not None:
            coordinates = get_coordinates_in_direction(self.coordinates, direction)
            new_tile = self.world.add_tile(coordinates)
            if new_tile:
                self.world.tile_map_coordinates[coordinates].created = True
                logging.info("Tile is created")
                self.world.new_tile_flag = True
                self.csv_particle_writer.write_particle(tile_created=1)
                self.world.csv_round.update_tiles_num(len(self.world.get_tiles_list()))
                self.world.csv_round.update_metrics(tile_created=1)
                return new_tile
            else:
                return False
        else:
            logging.info("Not created tile ")
            return False

    def create_tile_on(self, coordinates=None):
        """
        Creates a tile either on a given x,y coordinates

        :param coordinates: the coordinates
        :return: New Tile or False
        """

        logging.info("particle with id %s is", self.get_id())
        if coordinates is not None:
            if self.world.grid.are_valid_coordinates(coordinates):
                logging.info("Going to create a tile on position %s" % str(coordinates))
                if self.world.add_tile(coordinates):
                    self.world.tile_map_coordinates[coordinates].created = True
                    self.world.new_tile_flag = True
                    self.csv_particle_writer.write_particle(tile_created=1)
                    self.world.csv_round.update_tiles_num(len(self.world.get_tiles_list()))
                    self.world.csv_round.update_metrics(tile_created=1)
                    return True
                else:
                    logging.info("Not created tile on coordinates %s" % str(coordinates))
                    return False
            else:
                logging.info("Not created tile on coordinates %s" % str(coordinates))
                return False

    def delete_tile(self):
        """
        Deletes a tile on current position

        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        logging.info("Particle %s is" % self.get_id())
        logging.info("is going to delete a tile on current position")
        if self.coordinates in self.world.get_tile_map_coordinates():
            if self.world.remove_tile_on(self.coordinates):
                self.csv_particle_writer.write_particle(tile_deleted=1)
                return True
        else:
            logging.info("Could not delet tile")
            return False

    def delete_tile_with(self, tile_id):
        """
        Deletes a tile with a given tile-id

        :param tile_id: The id of the tile that should be deleted
        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        logging.info("Particle %s is" % self.get_id())
        logging.info("is going to delete a tile with tile id %s" % str(tile_id))
        if self.world.remove_tile(tile_id):
            self.csv_particle_writer.write_particle(tile_deleted=1)
            return True
        else:
            logging.info("Could not delet tile with tile id %s" % str(tile_id))
            return False

    def delete_tile_in(self, direction=None):
        """
        Deletes a tile either in a given directionection

        :param direction: The directionection on which the tile should be deleted. Options: E, SE, SW, W, NW, NE,

        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        coordinates = ()
        if direction is not None:
            coordinates = get_coordinates_in_direction(self.coordinates, direction)
            logging.info("Deleting tile in %s directionection" % str(direction))
            if coordinates is not None:
                if self.world.remove_tile_on(coordinates):
                    logging.info("Deleted tile with tile on coordinates %s" % str(coordinates))
                    self.csv_particle_writer.write_particle(tile_deleted=1)
                    return True
                else:
                    logging.info("Could not delet tile on coordinates %s" % str(coordinates))
                    return False
        else:
            logging.info("Could not delet tile on coordinates %s" % str(coordinates))
            return False

    def delete_tile_on(self, x=None, y=None):
        """
        Deletes a tile either on a given x,y coordinates
,
        :param x: x coordinate
        :param y: y coordinate
        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        coordinates = ()
        if x is not None and y is not None:
            coordinates = (x, y)
            if self.world.remove_tile_on(coordinates):
                logging.info("Deleted tile with tile on coordinates %s" % str(coordinates))
                self.csv_particle_writer.write_particle(tile_deleted=1)
                return True
            else:
                logging.info("Could not delet tile on coordinates %s" % str(coordinates))
                return False
        else:
            logging.info("Could not delet tile on coordinates %s" % str(coordinates))
            return False

    def take_tile_with(self, tile_id):
        """
        Takes a tile with a given tile id

        :param tile_id:  The id of the tile that should be taken
        :return: True: successful taken; False: unsuccessful taken
        """
        if self.carried_particle is None and self.carried_tile is None:
            if tile_id in self.world.tile_map_id:
                self.carried_tile = self.world.tile_map_id[tile_id]
                if self.carried_tile.take():
                    logging.info("Tile with tile id %s  has been taken", str(tile_id))
                    self.carried_tile.coordinates = self.coordinates
                    if self.world.vis is not None:
                        self.world.vis.tile_changed(self.carried_tile)
                    self.world.csv_round.update_metrics(tiles_taken=1)
                    self.csv_particle_writer.write_particle(tiles_taken=1)
                    return True
                else:
                    self.carried_tile = None
                    logging.info("Tile with tile id %s could not be taken" % str(tile_id))
                    return False
            else:
                logging.info("Tile with tile id %s is not in the world" % str(tile_id))
                return False
        else:

            logging.info("Tile cannot taken because particle is carrying either a tile or a particle (%s, %s)"
                         % (str(self.carried_tile), str(self.carried_particle)))
            return False

    def take_tile_in(self, direction):
        """
        Takes a tile that is in a given direction

        :param direction: The direction on which the tile should be taken.
        :return: True: successful taken; False: unsuccessful taken
        """
        coordinates = get_coordinates_in_direction(self.coordinates, direction)
        return self.take_tile_on(coordinates)

    def take_tile_on(self, coordinates):
        """
        Takes a tile on given coordinates

        :param coordinates of the tile
        :return: True: successful taken; False: unsuccessful taken
        """
        if self.world.grid.are_valid_coordinates(coordinates):
            if coordinates in self.world.tile_map_coordinates:
                return self.take_tile_with(self.world.tile_map_coordinates[coordinates].get_id())
            else:
                logging.info("There is no Tile at %s" % str(coordinates))
                return False
        else:
            logging.info("invalid coordinates %s" % str(coordinates))
            return False

    def take_tile(self):
        """
        Takes a tile on the actual position

        :return: True: successful taken; False: unsuccessful taken
        """
        return self.take_tile_on(self.coordinates)

    def drop_tile(self):
        """
        Drops the taken tile on the particles actual position

        :return: None
        """
        return self.drop_tile_on(self.coordinates)

    def drop_tile_in(self, direction):
        """
        Drops the taken tile on a given direction

         :param direction: The directionection on which the tile should be dropped. Options: E, SE, SW, W, NW, NE,
        """
        return self.drop_tile_on(get_coordinates_in_direction(self.coordinates, direction))

    def drop_tile_on(self, coordinates):
        """
        Drops the taken tile on a given direction

        :param coordinates
        """
        if self.carried_tile is not None:
            if self.world.grid.are_valid_coordinates(coordinates):
                if coordinates not in self.world.get_tile_map_coordinates():
                    try:  # cher: insert so to overcome the AttributeError
                        self.carried_tile.drop_me(coordinates)
                    except AttributeError:
                        pass
                    self.carried_tile = None
                    self.world.csv_round.update_metrics(tiles_dropped=1)
                    self.csv_particle_writer.write_particle(tiles_dropped=1)
                    logging.info("Dropped tile on %s coordinate", str(coordinates))
                    return True
                else:
                    logging.info("Is not possible to drop the tile on that position because it is occupied")
                    return False
            else:
                logging.info("Wrong coordinates for dropping the tile")
                return False
        else:
            logging.info("No tile is taken for dropping")
            return False

    def create_particle(self):
        """
        Creates a particle on the particles actual position

        :return: New Particle or False
        """
        logging.info("Going to create on position %s", str(self.coordinates))
        new_particle = self.world.add_particle(self.coordinates)
        if new_particle:
            self.world.particle_map_coordinates[self.coordinates[0], self.coordinates[1]].created = True
            self.csv_particle_writer.write_particle(particle_created=1)
            self.world.csv_round.update_particle_num(len(self.world.get_particle_list()))
            self.world.csv_round.update_metrics(particle_created=1)
            return new_particle
        else:
            return False

    def create_particle_in(self, direction=None):
        """
        Creates a particle either in a given direction

        :toDo: separate the direction and coordinates and delete state

        :param direction: The direction on which the particle should be created. Options: E, SE, SW, W, NW, NE,
        :return: New Particle or False
        """
        if direction is not None:
            coordinates = get_coordinates_in_direction(self.coordinates, direction)
            logging.info("Going to create a particle in %s on position %s", str(direction), str(coordinates))
            new_particle = self.world.add_particle(coordinates)
            if new_particle:
                self.world.particle_map_coordinates[coordinates].created = True
                logging.info("Created particle on coordinates %s", coordinates)
                self.world.csv_round.update_particle_num(len(self.world.get_particle_list()))
                self.world.csv_round.update_metrics(particle_created=1)
                self.csv_particle_writer.write_particle(particle_created=1)
                return new_particle
            else:
                return False
        else:
            logging.info("Particle not created. invalid direction (None)")
            return False

    def create_particle_on(self, coordinates):
        """
        Creates a particle either on the given coordinates

        :toDo: separate the direction and coordinates and delete state

        :param coordinates: the coordinates
        :return: New Particle or False
        """
        if coordinates is not None:
            if self.world.grid.are_valid_coordinates(coordinates):
                logging.info("Going to create a particle on position %s" % str(coordinates))
                new_particle = self.world.add_particle(coordinates)
                if new_particle:
                    self.world.particle_map_coordinates[coordinates].created = True
                    logging.info("Created particle on coordinates %s" % str(coordinates))
                    self.world.csv_round.update_particle_num(len(self.world.get_particle_list()))
                    self.world.csv_round.update_metrics(particle_created=1)
                    self.csv_particle_writer.write_particle(particle_created=1)
                    return new_particle
                else:
                    return False
            else:
                return False
        else:
            logging.info("Not created particle on coordinates %s" % str(coordinates))
            return False

    def delete_particle(self):
        """
        Deletes a tile on current position

        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        logging.info("Particle %s is", self.get_id())
        logging.info("is going to delete a particle on current position")
        if self.coordinates in self.world.get_particle_map_coordinates():
            if self.world.remove_particle_on(self.coordinates):
                self.csv_particle_writer.write_particle(particle_deleted=1)
                return True
        else:
            logging.info("Could not delet particle")
            return False

    def delete_particle_with(self, particle_id):
        """
        Deletes a particle with a given id

        :param particle_id: The id of the particle that should be deleted
        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        logging.info("Particle %s is", self.get_id())
        logging.info("is going to delete a particle with id %s" % str(particle_id))
        if self.world.remove_particle(particle_id):
            self.csv_particle_writer.write_particle(particle_deleted=1)
            return True
        else:
            logging.info("Could not delet particle with particle id %s" % str(particle_id))
            return False

    def delete_particle_in(self, direction=None):
        """
        Deletes a particle either in a given directionection

        :param direction: The directionection on which the particle should be deleted. Options: E, SE, SW, W, NW, NE,
        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        if direction is not None:
            coordinates = get_coordinates_in_direction(self.coordinates, direction)
            logging.info("Deleting tile in %s directionection" % str(direction))
            if self.world.remove_particle_on(coordinates):
                logging.info("Deleted particle with particle on coordinates %s" % str(coordinates))
                self.csv_particle_writer.write_particle(particle_deleted=1)
                return True
            else:
                logging.info("Could not delet particle on coordinates %s" % str(coordinates))
                return False

    def delete_particle_on(self, coordinates=None):
        """
        Deletes a particle either on a given x,y coordinates

        :param coordinates
        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        if coordinates is None:
            logging.info("coordinates are 'None'...")
            return False

        if not self.world.grid.are_valid_coordinates(coordinates):
            logging.info("invalid coordinates")
            return False

        if self.world.remove_particle_on(coordinates):
            logging.info("Deleted particle with particle on coordinates %s" % str(coordinates))
            self.csv_particle_writer.write_particle(particle_deleted=1)
            return True
        else:
            logging.info("Could not delete particle on coordinates %s" % str(coordinates))
            return False


    def take_particle_with(self, particle_id):
        """
        Takes a particle with a given tile id

        :param particle_id:  The id of the particle that should be taken
        :return: True: successful taken; False: unsuccessful taken
        """
        if self.carried_tile is not None or self.carried_particle is not None:
            logging.info("particle %s is already carrying a particle or a tile" % str(self.get_id()))
            return False

        if particle_id not in self.world.get_particle_map_id():
            logging.info("particle with particle id %s is not in the world" % str(particle_id))
            return False

        self.carried_particle = self.world.particle_map_id[particle_id]
        if self.carried_particle.take_me(self.coordinates):
            logging.info("particle with particle id %s  has been taken" % str(particle_id))
            self.carried_particle.coordinates = self.coordinates
            if self.world.vis is not None:
                self.world.vis.particle_changed(self.carried_particle)
            self.world.csv_round.update_metrics(particles_taken=1)
            self.csv_particle_writer.write_particle(particles_taken=1)
            return True
        else:
            self.carried_particle = None
            logging.info("particle with particle id %s could not be taken" % str(particle_id))
            return False


    def take_particle_on(self, coordinates):
        """
        Takes the particle on the given coordinates if it is not taken

        :param coordinates: the particle coordinates
        :return: True: Successful taken; False: Cannot be taken or wrong Coordinates
        """

        if not self.world.grid.are_valid_coordinates(coordinates):
            logging.info("Coordinates are invalid")
            return False

        if coordinates in self.world.particle_map_coordinates:
            return self.take_particle_with(self.world.particle_map_coordinates[coordinates].get_id())
        else:
            logging.info("There is no particle on %s" % str(coordinates))
            return False

    def take_particle_in(self, direction):
        """
        Takes a particle that is in a given direction

        :param direction: The direction on which the particle should be taken. Options: E, SE, SW, W, NW, NE,
        :return: True: successful taken; False: unsuccessful taken
        """
        return self.take_particle_on(get_coordinates_in_direction(self.coordinates, direction))

    def take_particle(self):
        """
        Takes a particle on the actual position

        :return: True: successful taken; False: unsuccessful taken
        """
        return self.take_particle_on(self.coordinates)

    def drop_particle(self):
        """
        Drops the taken particle on the particles actual position

        :return: None
        """
        return self.drop_particle_on(self.coordinates)

    def drop_particle_in(self, direction):
        """
        Drops the particle tile in a given direction

         :param direction: The direction on which the particle should be dropped.
        """
        return self.drop_particle_on(get_coordinates_in_direction(self.coordinates, direction))

    def drop_particle_on(self, coordinates=None):
        """
        Drops the particle tile on the given coordinates

        :param coordinates:
        """
        if self.carried_particle is not None and coordinates is not None:
            if self.world.grid.are_valid_coordinates(coordinates):
                if coordinates not in self.world.particle_map_coordinates:
                    try:  # cher: insert so to overcome the AttributeError
                        self.carried_particle.drop_me(coordinates)
                    except AttributeError:
                        logging.info("Dropped particle on: Error while dropping")
                        return False
                    self.carried_particle = None
                    logging.info("Dropped particle on %s coordinate", str(coordinates))
                    self.world.csv_round.update_metrics(particles_dropped=1)
                    self.csv_particle_writer.write_particle(particles_dropped=1)
                    return True
                else:
                    logging.info("Is not possible to drop the particle on that position because it is occupied")
                    return False
            else:
                logging.info("invalid coordinates")
        else:
            logging.info("drop_particle_on: coordinates are 'None' or not carrying a particle")
            return False

    def update_particle_coordinates(self, particle, new_coordinates):
        """
        Upadting the particle with new coordinates
        Only necessary for taking and moving particles

        :param particle: The particle object
        :param new_coordinates: new coorindation points
        :return: None
        """
        if self.world.grid.are_valid_coordinates(new_coordinates):
            particle.coordinates = new_coordinates
            self.world.particle_map_coordinates[new_coordinates] = particle
            if self.world.vis is not None:
                self.world.vis.particle_changed(particle)
            return True
        else:
            return False

    def create_location(self):
        """
         Creates a location on the particles actual position

        :return: New location or False
        """

        logging.info("Going to create on position %s" % str(self.coordinates))
        new_location = self.world.add_location(self.coordinates)
        if new_location:
            self.csv_particle_writer.write_particle(location_created=1)
            self.world.csv_round.update_locations_num(len(self.world.get_location_list()))
            self.world.csv_round.update_metrics(location_created=1)
            return new_location
        else:
            return False

    def create_location_in(self, direction=None):
        """
        Creates a location either in a given direction
        :param direction: The direction on which the location should be created.
        :return: New location or False

        """
        if direction is not None:
            coordinates = get_coordinates_in_direction(self.coordinates, direction)
            logging.info("Going to create a location in %s on position %s" % (str(direction), str(coordinates)))
            new_location = self.world.add_location(coordinates)
            if new_location:
                logging.info("Created location on coordinates %s" % str(coordinates))
                self.world.csv_round.update_locations_num(len(self.world.get_location_list()))
                self.world.csv_round.update_metrics(location_created=1)
                return new_location
            else:
                return False
        else:
            logging.info("Location not created. Invalid direction (None)")
            return False

    def create_location_on(self, coordinates=None):
        """
        Creates a location either on a given x,y coordinates

        :return: New location or False

        """
        if coordinates is not None:
            if self.world.grid.are_valid_coordinates(coordinates):
                logging.info("Going to create a location on position %s", str(coordinates))
                new_location = self.world.add_location(coordinates)
                if new_location:
                    logging.info("Created location on coordinates %s", str(coordinates))
                    self.world.csv_round.update_locations_num(len(self.world.get_location_list()))
                    self.world.csv_round.update_metrics(location_created=1)
                    return new_location
            else:
                return False
        else:
            logging.info("Location not created. invalid coordinates (None)")
            return False

    def delete_location_with(self, location_id):
        """
        Deletes a location with a given location-id
        :param location_id: The id of the location that should be deleted
        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        logging.info("Particle %s is going to delete location with location id %s" % (self.get_id(), location_id))
        if self.world.remove_location(location_id):
            self.csv_particle_writer.write_particle(location_deleted=1)
            return True
        else:
            logging.info("Could not delete location with location id %s", str(location_id))
            return False

    def delete_location(self):
        """
        Deletes a location on current position

        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        logging.info("Particle %s is going to delete a location on current position" % self.get_id())
        if self.coordinates in self.world.get_location_map_coordinates():
            if self.world.remove_location_on(self.coordinates):
                self.csv_particle_writer.write_particle(location_deleted=1)
                return True
        else:
            logging.info("Could not delete location")
            return False

    def delete_location_in(self, direction=None):
        """
        Deletes a location in a given direction

        :param direction: The direction on which the location should be deleted.
        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        if direction is not None:
            coordinates = get_coordinates_in_direction(self.coordinates, direction)
            logging.info("Deleting tile in %s direction", str(direction))
            if self.world.remove_location_on(coordinates):
                logging.info("Deleted location with location on coordinates %s", str(coordinates))
                self.csv_particle_writer.write_particle(location_deleted=1)
                return True
            else:
                logging.info("Could not delete location on coordinates %s", str(coordinates))
                return False
        else:
            logging.info("invalid direction %d", str(direction))

    def delete_location_on(self, coordinates=None):
        """
        Deletes a particle either on a given x,y coordinates

        :param coordinates: the coordinates
        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        if coordinates is not None:
            if self.world.grid.are_valid_coordinates(coordinates):
                if self.world.remove_location_on(coordinates):
                    logging.info("Deleted location on coordinates %s", str(coordinates))
                    self.csv_particle_writer.write_particle(location_deleted=1)
                    return True
                else:
                    logging.info("Could not delete location on coordinates %s", str(coordinates))
                    return False
            else:
                return False
        else:
            return False

    def set_color(self, color):
        super().set_color(color)
        if self.world.vis is not None:
            self.world.vis.particle_changed(self)
