"""
.. module:: particle
   :platform: Unix, Windows
   :synopsis: This module provides the interfaces of the robotics particle

.. moduleauthor:: Ahmad Reza Cheraghi

TODO: Erase Memory

"""

import logging, math
from lib import csv_generator, matter
from lib.swarm_sim_header import *


class Particle(matter.Matter):
    """In the classe marker all the methods for the characterstic of a marker is included"""
    def __init__(self, world, coordinates, color=black, transparency=1, particle_counter=0):
        """Initializing the marker constructor"""
        super().__init__( world, coordinates, color, transparency,
                          type="particle", mm_size=world.config_data.particle_mm_size)
        self.number = particle_counter
        self.__isCarried = False
        self.carried_tile = None
        self.carried_particle = None
        self.steps = 0
        self.csv_particle_writer = csv_generator.CsvParticleData( self.get_id(), self.number)

    def has_tile(self):
        if self.carried_tile == None:
            return False
        else:
            return True

    def has_particle(self):
        if self.carried_particle == None:
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

    def check_on_marker(self):
        """
        Checks if the particle is on a marker

        :return: True: On a marker; False: Not on a marker
        """
        if self.coordinates in self.world.marker_map_coordinates:
            return True
        else:
            return False

    def move_to(self, direction):
        """
        Moves the particle to the given directionection

        :param direction: The direction is defined by loaded grid class
        :return: True: Success Moving;  False: Non moving
        """
        direction_coord = get_coordinates_in_direction(self.coordinates, direction)
        direction, direction_coord = self.check_within_border(direction, direction_coord)
        if grid.is_valid_location(direction_coord):

            if self.coordinates in self.world.particle_map_coordinates:
                del self.world.particle_map_coordinates[self.coordinates]

            if not direction_coord in self.world.particle_map_coordinates:
                self.coordinates = direction_coord
                self.world.particle_map_coordinates[self.coordinates] = self
                logging.info("particle %s successfully moved to %s", str(self.get_id()), direction)
                self.world.csv_round.update_metrics( steps=1)
                self.csv_particle_writer.write_particle(steps=1)
                self.touch()
                self.check_for_carried_tile_or_particle()
                return True
        return False

    def check_for_carried_tile_or_particle(self):
        if self.carried_tile is not None:
            self.carried_tile.coordinates = self.coordinates
            self.carried_tile.touch()
        elif self.carried_particle is not None:
            self.carried_particle.coordinates = self.coordinates
            self.carried_particle.touch()

    def check_within_border(self, direction, direction_coord):
        if self.world.config_data.border == 1 and \
                (abs(direction_coord[0]) > self.world.get_sim_x_size() or abs(direction_coord[1]) > self.world.get_sim_y_size()):
            direction = direction - 3 if direction > 2 else direction + 3
            direction_coord = get_coordinates_in_direction(self.coordinates, direction)
        return direction, direction_coord

    def move_to_in_bounds(self, direction):
        """
            Moves the particle to the given directionection if it would remain in bounds.

            :param direction: The directionection must be either: E, SE, SW, W, NW, or NE
            :return: True: Success Moving;  False: Non moving
        """
        direction_coord = get_coordinates_in_direction(self.coordinates, direction)
        sim_coord = coordinates_to_sim(direction_coord)
        if self.world.get_sim_x_size() >=  abs(sim_coord[0]) and \
                        self.world.get_sim_y_size() >=  abs(sim_coord[1]):
            return self.move_to(direction)
        else:
            # 'bounce' off the wall
            n_direction = direction - 3 if direction > 2 else direction + 3
            self.move_to(n_direction)

    def read_from_with(self, matter, key=None):
        """
        Read the memories from the matters (paricle, tile, or marker object) memories with a given keyword

        :param matter: The matter can be either a particle, tile, or marker
        :param key: A string keyword to searcg for the data in the memory
        :return: The matters memory; None
        """
        if key != None:
            tmp_memory = matter.read_memory_with(key)
        else:
            tmp_memory =  matter.read_whole_memory()

        if tmp_memory != None:
            if not(hasattr(tmp_memory, '__len__')) or len(tmp_memory) > 0:
                if matter.type == "particle":
                    self.world.csv_round.update_metrics( particle_read=1)
                    self.csv_particle_writer.write_particle(particle_read=1)
                elif matter.type == "tile":
                    self.world.csv_round.update_metrics( tile_read=1)
                    self.csv_particle_writer.write_particle(tile_read=1)
                elif matter.type == "marker":
                    self.world.csv_round.update_metrics( marker_read=1)
                    self.csv_particle_writer.write_particle(marker_read=1)
                return tmp_memory
        return None

    def matter_in(self, direction=E):
        """
        :param direction: the directionection to check if a matter is there
        :return: True: if a matter is there, False: if not
        """
        if  get_coordinates_in_direction(self.coordinates, direction) in self.world.get_tile_map_coordinates() \
            or get_coordinates_in_direction(self.coordinates, direction) in self.world.get_particle_map_coordinates() \
            or get_coordinates_in_direction(self.coordinates, direction) in self.world.get_marker_map_coordinates():
            return True
        else:
            return False

    def tile_in(self, direction=E):
        """
        :param direction: the directionection to check if a tile is there
        :return: True: if a tile is there, False: if not
        """
        if get_coordinates_in_direction(self.coordinates, direction) in self.world.get_tile_map_coordinates():
            return True
        else:
            return False

    def particle_in(self, direction=E):
        """
        :param direction: the directionection to check if a particle is there
        :return: True: if a particle is there, False: if not
        """
        if get_coordinates_in_direction(self.coordinates, direction) in self.world.get_particle_map_coordinates():
            return True
        else:
            return False

    def marker_in(self, direction=E):
        """
        :param direction: the directionection to check if a marker is there
        :return: True: if a marker is there, False: if not
        """
        if get_coordinates_in_direction(self.coordinates, direction) in self.world.get_marker_map_coordinates():
            return True
        else:
            return False

    def get_matter_in(self, direction=E):
        if get_coordinates_in_direction(self.coordinates, direction) in self.world.get_tile_map_coordinates():
            return self.world.get_tile_map_coordinates()[get_coordinates_in_direction(self.coordinates, direction)]
        elif get_coordinates_in_direction(self.coordinates, direction) in self.world.get_particle_map_coordinates():
            return self.world.get_particle_map_coordinates()[get_coordinates_in_direction(self.coordinates, direction)]
        elif get_coordinates_in_direction(self.coordinates, direction) in self.world.get_marker_map_coordinates():
            return self.world.get_marker_map_coordinates()[get_coordinates_in_direction(self.coordinates, direction)]
        else:
            return False

    def get_tile_in(self, direction=E):
        if get_coordinates_in_direction(self.coordinates, direction) in self.world.get_tile_map_coordinates():
            return self.world.get_tile_map_coordinates()[get_coordinates_in_direction(self.coordinates, direction)]
        else:
            return False

    def get_particle_in(self, direction=E):
        if get_coordinates_in_direction(self.coordinates, direction) in self.world.get_particle_map_coordinates():
            return self.world.get_particle_map_coordinates()[get_coordinates_in_direction(self.coordinates, direction)]
        else:
            return False

    def get_marker_in(self, direction=E):
        if get_coordinates_in_direction(self.coordinates, direction) in self.world.get_marker_map_coordinates():
            return self.world.get_marker_map_coordinates()[get_coordinates_in_direction(self.coordinates, direction)]
        else:
            return False

    def get_marker(self):
        if self.coordinates in self.world.marker_map_coordinates:
            return self.world.get_marker_map_coordinates()[self.coordinates]
        else:
            return False

    def get_tile(self):
        if self.self.coordinates in self.world.get_tile_map_coordinates():
            return self.world.get_tile_map_coordinates()[self.coordinates]
        else:
            return False

    def write_to_with(self, matter, key=None, data=None):
        """
        Writes data with given a keyword directionectly on the matters (paricle, tile, or marker object) memory

        :param matter: The matter can be either a particle, tile, or marker
        :param key: A string keyword so to order the data that is written into the memory
        :param data: The data that should be stored into the memory
        :return: True: Successful written into the memory; False: Unsuccessful
        """
        wrote=False
        if data != None:
            wrote=False
            if key==None:
                wrote=matter.write_memory(data)
            else:
                wrote= matter.write_memory_with(key, data)
            if  wrote==True:
                if matter.type == "particle":
                    self.world.csv_round.update_metrics( particle_write=1)
                    self.csv_particle_writer.write_particle(particle_write=1)
                elif matter.type == "tile":
                    self.world.csv_round.update_metrics( tile_write=1)
                    self.csv_particle_writer.write_particle(tile_write=1)
                elif matter.type == "marker":
                    self.world.csv_round.update_metrics( marker_write=1)
                    self.csv_particle_writer.write_particle(marker_write=1)
                return True
            else:
                return False
        else:
            return False

    def scan_for_matters_within(self, matter='all', hop=1):
        """
        Scans for particles, tiles, or marker on a given hop distance and all the matters within the hop distance

        :todo: If nothing then everything should be scanned

        :param matter: For what matter this method should scan for. Can be either particles, tiles, markers, or (default)all
        :param hop: The hop distance from the actual position of the scanning particle
        :return: A list of the founded matters
        """

        within_hop_list = []
        for i in range(1, hop + 1):
            in_list = self.scan_for_matters_in(matter, i)
            if in_list is not None:
                within_hop_list.extend(in_list)
        if len(within_hop_list) != 0:
            return within_hop_list
        else:
            return None

    def scan_for_matters_in(self, matter='all', hop=1):
        """
         Scanning for particles, tiles, or marker on a given hop distance

         :param matter: For what matter this method should scan for. Can be either particles, tiles, markers, or (default)all
         :param hop: The hop distance from thee actual position of the scanning particle
         :return: A list of the founded matters
         """
        starting_x = self.coordinates[0]
        starting_y = self.coordinates[1]
        scanned_list = []
        logging.info("particle on %s is scanning for %s in %i hops", str(self.coordinates), matter, hop)

        if matter == "particles":
            scanned_list = global_scanning(self.world.particle_map_coordinates, hop, self.coordinates)
        elif matter == "tiles":
            scanned_list = global_scanning(self.world.tile_map_coordinates, hop, self.coordinates)
        elif matter == "markers":
            scanned_list = global_scanning(self.world.marker_map_coordinates, hop, self.coordinates)
        else:
            scanned_list = global_scanning(self.world.particle_map_coordinates, hop, self.coordinates)
            if scanned_list is not None:
                scanned_list.extend(global_scanning(self.world.tile_map_coordinates, hop, self.coordinates))
                scanned_list.extend(global_scanning(self.world.marker_map_coordinates, hop, self.coordinates))
            else:
                scanned_list = global_scanning(self.world.tile_map_coordinates, hop, self.coordinates)
                if scanned_list is not None:
                    scanned_list.extend(global_scanning(self.world.marker_map_coordinates, hop, self.coordinates))
                else:
                    scanned_list = global_scanning(self.world.marker_map_coordinates, hop, self.coordinates)
        if scanned_list is not None:
            return scanned_list
        else:
            return None

    def scan_for_particles_within(self, hop=1):
        """
        Scans for particles, tiles, or marker on a given hop distance and all the matters within the hop distance

        :todo: If nothing then everything should be scanned

        :param matter: For what matter this method should scan for. Can be either particles, tiles, markers, or (default)all
        :param hop: The hop distance from the actual position of the scanning particle
        :return: A list of the founded matters
        """

        within_hop_list = []
        for i in range(1, hop + 1):
            in_list = self.scan_for_particles_in(hop=i)
            if in_list is not None:
                within_hop_list.extend(in_list)
        if len(within_hop_list) != 0:
            return within_hop_list
        else:
            return None

    def scan_for_particles_in(self, hop=1):
        """
        Scanning for particles, tiles, or marker on a given hop distance

        :param matter: For what matter this method should scan for. Can be either particles, tiles, markers, or (default)all
        :param hop: The hop distance from thee actual position of the scanning particle
        :return: A list of the founded matters
        """

        scanned_list = self.scan_for_matters_in(matter='particles', hop=hop)
        return scanned_list

    def scan_for_tiles_within(self,  hop=1):
        """
        Scans for particles, tiles, or marker on a given hop distance and all the matters within the hop distance

        :todo: If nothing then everything should be scanned

        :param matter: For what matter this method should scan for. Can be either particles, tiles, markers, or (default)all
        :param hop: The hop distance from the actual position of the scanning particle
        :return: A list of the founded matters
        """

        within_hop_list = []
        for i in range(1, hop + 1):
            in_list = self.scan_for_tiles_in( hop=i)
            if in_list is not None:
                within_hop_list.extend(in_list)
        if len(within_hop_list) != 0:
            return within_hop_list
        else:
            return None

    def scan_for_tiles_in(self, hop=1):
        """
        Scanning for particles, tiles, or marker on a given hop distance

        :param matter: For what matter this method should scan for. Can be either particles, tiles, markers, or (default)all
        :param hop: The hop distance from thee actual position of the scanning particle
        :return: A list of the founded matters
        """
        scanned_list = self.scan_for_matters_in(matter='tiles', hop=hop)
        return scanned_list

    def scan_for_markers_within(self, hop=1):
        """
        Scans for particles, tiles, or marker on a given hop distance and all the matters within the hop distance

        :todo: If nothing then everything should be scanned

        :param matter: For what matter this method should scan for. Can be either particles, tiles, markers, or (default)all
        :param hop: The hop distance from the actual position of the scanning particle
        :return: A list of the founded matters
        """

        within_hop_list = []
        for i in range(1, hop + 1):
            in_list = self.scan_for_markers_in(hop=i)
            if in_list is not None:
                within_hop_list.extend(in_list)
        if len(within_hop_list) != 0:
            return within_hop_list
        else:
            return None

    def scan_for_markers_in(self, hop=1):
        """
        Scanning for particles, tiles, or marker on a given hop distance

        :param matter: For what matter this method should scan for. Can be either particles, tiles, markers, or (default)all
        :param hop: The hop distance from thee actual position of the scanning particle
        :return: A list of the founded matters
        """
        scanned_list = self.scan_for_matters_in(matter='markers', hop=hop)
        return scanned_list

    def take_me(self, coordinates=0):
        """
        The particle is getting taken from the the other particle on the given coordinate

        :param coordinates: Coordination of particle that should be taken
        :return: True: Successful taken; False: Cannot be taken or wrong Coordinates
        """

        if not self.__isCarried:
            if self.coordinates in self.world.particle_map_coordinates:
                del self.world.particle_map_coordinates[self.coordinates]
            self.__isCarried = True
            self.coordinates = coordinates
            self.set_transparency(0.5)
            self.touch()
            return True
        else:
            return False

    def drop_me(self, coordinates):
        """
        The actual particle is getting dropped

        :param coordinates: the given position
        :return: None
        """
        self.world.particle_map_coordinates[coordinates] = self
        self.coordinates = coordinates
        self.__isCarried = False
        self.set_transparency(1)
        self.touch()

    def create_tile(self, color=gray, transparency=1):
        """
        Creates a tile on the particles actual position

        :return: New Tile or False
        """
        logging.info("Going to create a tile on position %s", str(self.coordinates))
        new_tile = self.world.add_tile(self.coordinates, color, transparency)
        if new_tile:
            self.world.tile_map_coordinates[self.coordinates].created = True
            self.csv_particle_writer.write_particle(tile_created=1)
            self.world.csv_round.update_tiles_num(len(self.world.get_tiles_list()))
            self.world.csv_round.update_metrics( tile_created=1)
            return new_tile
        else:
            return False

    def create_tile_in(self, direction=None, color=gray, transparency=1):
        """
        Creates a tile either in a given directionection

        :param direction: The directionection on which the tile should be created. Options: E, SE, SW, W, NW, NE,
        :return: New tile or False
        """
        logging.info("particle with id %s is", self.get_id())
        logging.info("Going to create a tile in %s ", str(direction) )
        if direction is not None:
            coordinates = get_coordinates_in_direction(self.coordinates, direction)
            new_tile = self.world.add_tile(coordinates, color, transparency)
            if new_tile:
                self.world.tile_map_coordinates[coordinates].created = True
                logging.info("Tile is created")
                self.world.new_tile_flag = True
                self.csv_particle_writer.write_particle(tile_created=1)
                self.world.csv_round.update_tiles_num(len(self.world.get_tiles_list()))
                self.world.csv_round.update_metrics( tile_created=1)
                return new_tile
            else:
                return False
        else:
            logging.info("Not created tile ")
            return False

    def create_tile_on(self, coordinates=None, color=gray, transparency=1):
        """
        Creates a tile either on a given x,y coordinates

        :param coordinates: the coordinates
        :return: New Tile or False
        """

        logging.info("particle with id %s is", self.get_id())
        if coordinates is not None:
            if grid.is_valid_location(coordinates):
                logging.info("Going to create a tile on position \(%i , %i\)", x,y )
                if self.world.add_tile(coordinates, color, transparency):
                    self.world.tile_map_coordinates[coordinates, coordinates[1]].created = True
                    self.world.new_tile_flag = True
                    self.csv_particle_writer.write_particle(tile_created=1)
                    self.world.csv_round.update_tiles_num(len(self.world.get_tiles_list()) )
                    self.world.csv_round.update_metrics( tile_created=1)
                    return True
                else:
                    logging.info("Not created tile on coordinates  \(%i , %i\)", y,x )
                    return False
            else:
                logging.info("Not created tile on coordinates   \(%i , %i\)", y,x )
                return False

    def delete_tile(self):
        """
        Deletes a tile on current position

        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        logging.info("Particle %s is", self.get_id())
        logging.info("is going to delete a tile on current position")
        if self.coordinates in self.world.get_tile_map_coordinates():
            if self.world.remove_tile_on(self.coordinates):
                self.csv_particle_writer.write_particle(tile_deleted=1)
                return True
        else:
            logging.info("Could not delet tile")
            return False

    def delete_tile_with(self, id):
        """
        Deletes a tile with a given tile-id

        :param tile_id: The id of the tile that should be deleted
        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        logging.info("Particle %s is", self.get_id())
        logging.info("is going to delete a tile with tile id %s", str(id))
        if self.world.remove_tile(id):
            self.csv_particle_writer.write_particle(tile_deleted=1)
            return True
        else:
            logging.info("Could not delet tile with tile id %s", str(id))
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
            logging.info("Deleting tile in %s directionection", str(direction))
            if coordinates is not None:
                if self.world.remove_tile_on(coordinates):
                    logging.info("Deleted tile with tile on coordinates %s", str(coordinates))
                    self.csv_particle_writer.write_particle(tile_deleted=1)
                    return True
                else:
                    logging.info("Could not delet tile on coordinates %s", str(coordinates))
                    return False
        else:
            logging.info("Could not delet tile on coordinates %s", str(coordinates))
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
                logging.info("Deleted tile with tile on coordinates %s", str(coordinates))
                self.csv_particle_writer.write_particle(tile_deleted=1)
                return True
            else:
                logging.info("Could not delet tile on coordinates %s", str(coordinates))
                return False
        else:
            logging.info("Could not delet tile on coordinates %s", str(coordinates))
            return False

    def take_tile(self):
        """
        Takes a tile on the actual position

        :param id:  The id of the tile that should be taken
        :return: True: successful taken; False: unsuccessful taken
        """
        if self.carried_particle is None and self.carried_tile is None:
            if self.coordinates in self.world.tile_map_coordinates:
                self.carried_tile = self.world.tile_map_coordinates[self.coordinates]
                if self.carried_tile.take(coordinates=self.coordinates):
                    logging.info("Tile has been taken")
                    self.world.csv_round.update_metrics( tiles_taken=1)
                    self.csv_particle_writer.write_particle(tiles_taken=1)
                    return True
                else:
                    logging.info("Tile could not be taken")
                    return False
            else:
                logging.info("No tile on the actual position not in the world")
                return False
        else:
            logging.info("Tile cannot taken because particle is carrieng either a tile or a particle")
            return False

    def take_tile_with(self, id):
        """
        Takes a tile with a given tile id

        :param id:  The id of the tile that should be taken
        :return: True: successful taken; False: unsuccessful taken
        """
        if self.carried_particle is None and self.carried_tile is None:
            if id in self.world.tile_map_id:
                logging.info("Tile with tile id %s is in the world", str(id))
                self.carried_tile = self.world.tile_map_id[id]
                if self.carried_tile.take(coordinates=self.coordinates):
                    logging.info("Tile with tile id %s  has been taken", str(id))
                    self.world.csv_round.update_metrics( tiles_taken=1)
                    self.csv_particle_writer.write_particle(tiles_taken=1)
                    return True
                else:
                    logging.info("Tile with tile id %s could not be taken", str(id))
                    return False
            else:
                logging.info("Tile with tile id %s is not in the world", str(id))
                return False
        else:
            logging.info("Tile cannot taken because particle is carrieng either a tile or a particle", str(id))
            return False

    def take_tile_in(self, direction):
        """
        Takes a tile that is in a given directionection

        :param direction: The direction on which the tile should be taken.
        :return: True: successful taken; False: unsuccessful taken
        """
        if self.carried_particle is None and self.carried_tile is None:
            coordinates = get_coordinates_in_direction(self.coordinates, direction)
            if coordinates in self.world.tile_map_coordinates:
                self.carried_tile = self.world.tile_map_coordinates[coordinates]
                logging.info("Tile with tile id %s is in the world", str(self.carried_tile.get_id()))
                if self.carried_tile.take(coordinates=self.coordinates):
                    logging.info("Tile with tile id %s  has been taken", str(self.carried_tile.get_id()))
                    self.world.csv_round.update_metrics( tiles_taken=1)
                    self.csv_particle_writer.write_particle(tiles_taken=1)
                    return True
                else:
                    logging.info("Tile with tile id %s could not be taken", str(self.carried_tile.get_id()))
                    return False
            else:
                logging.info("Tile is not in the world")
                return False
        else:
            logging.info("Tile cannot taken because particle is carrieng either a tile or a particle")
            return False

    def take_tile_on(self, coordinates):
        """
        Takes a tile that is in a given directionection

        :param coordinates
        :return: True: successful taken; False: unsuccessful taken
        """
        if self.carried_particle is None and self.carried_tile is None:
            if grid.is_valid_location(coordinates):

                if coordinates in self.world.tile_map_coordinates:
                    self.carried_tile = self.world.tile_map_coordinates[coordinates]
                    logging.info("Tile with tile id %s is in the world", str(self.carried_tile.get_id()))
                    if self.carried_tile.take(coordinates=self.coordinates):
                        self.world.csv_round.update_metrics( tiles_taken=1)
                        self.csv_particle_writer.write_particle(tiles_taken=1)
                        logging.info("Tile with tile id %s  has been taken", str(self.carried_tile.get_id()))
                        return True
                    else:
                        logging.info("Tile with tile id %s could not be taken", str(self.carried_tile.get_id()))
                        return False
                else:
                    logging.info("Tile is not in the world")
                    return False
            else:
                logging.info("Coordinates are wrong")
                return False
        else:
            logging.info("Tile cannot taken because particle is carrieng either a tile or a particle")
            return False

    def drop_tile(self):
        """
        Drops the taken tile on the particles actual position

        :return: None
        """
        if self.carried_tile is not None:
            if self.coordinates not in self.world.tile_map_coordinates:
                try:  # cher: insert so to overcome the AttributeError
                    self.carried_tile.drop_me(self.coordinates)
                except AttributeError:
                    pass
                self.carried_tile = None
                logging.info("Tile has been dropped on the actual position")
                self.world.csv_round.update_metrics( tiles_dropped=1)
                self.csv_particle_writer.write_particle(tiles_dropped=1)
                return True
            else:
                logging.info("Is not possible to drop the tile on that position because it is occupied")
                return False
        else:
            return False

    def drop_tile_in(self, direction):
        """
        Drops the taken tile on a given directionection

         :param direction: The directionection on which the tile should be dropped. Options: E, SE, SW, W, NW, NE,
        """
        if self.carried_tile is not None:
            coordinates = get_coordinates_in_direction(self.coordinates, direction)
            if coordinates not in self.world.tile_map_coordinates:
                try:  # cher: insert so to overcome the AttributeError
                    self.carried_tile.drop_me(coordinates)
                except AttributeError:
                    pass
                self.carried_tile = None
                self.world.csv_round.update_metrics( tiles_dropped=1)
                self.csv_particle_writer.write_particle(tiles_dropped=1)
                logging.info("Dropped tile on %s coordinate", str(coordinates))
                return True
            else:
                logging.info("Is not possible to drop the tile on that position")
                return False

        else:
            logging.info("No tile taken for dropping")
            return False

    def drop_tile_on(self, coordinates):
        """
        Drops the taken tile on a given directionection

        :param coordinates
        """
        if self.carried_tile is not None:
            if grid.is_valid_location(coordinates):
                if coordinates not in self.world.get_tile_map_coordinates():
                    try:  # cher: insert so to overcome the AttributeError
                        self.carried_tile.drop_me(coordinates)
                    except AttributeError:
                        pass
                    self.carried_tile = None
                    self.world.csv_round.update_metrics( tiles_dropped=1)
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

    def create_particle(self, color=black, transparency=1):
        """
        Creates a particle on the particles actual position

        :return: New Particle or False
        """
        logging.info("Going to create on position %s", str(self.coordinates))
        new_particle = self.world.add_particle(self.coordinates[0], self.coordinates[1], color, transparency)
        if new_particle:
            self.world.particle_map_coordinates[self.coordinates[0], self.coordinates[1]].created=True
            self.csv_particle_writer.write_particle(particle_created=1)
            self.world.csv_round.update_particle_num(len(self.world.get_particle_list()))
            self.world.csv_round.update_metrics( particle_created=1)
            return new_particle
        else:
            return False

    def create_particle_in(self, direction=None, color=black, transparency=1):
        """
        Creates a particle either in a given directionection

        :toDo: seperate the directionection and coordinates and delete state

        :param direction: The directionection on which the particle should be created. Options: E, SE, SW, W, NW, NE,
        :return: New Particle or False
        """
        coordinates = (0, 0)
        if direction is not None:
            coordinates = get_coordinates_in_direction(self.coordinates, direction)
            logging.info("Going to create a particle in %s on position %s", str(direction), str(coordinates))
            new_particle= self.world.add_particle(coordinates[0], coordinates[1], color, transparency)
            if new_particle:
                self.world.particle_map_coordinates[coordinates[0], coordinates[1]].created = True
                logging.info("Created particle on coordinates %s", coordinates)
                self.world.csv_round.update_particle_num(len(self.world.get_particle_list()))
                self.world.csv_round.update_metrics( particle_created=1)
                self.csv_particle_writer.write_particle(particle_created=1)
                return new_particle
            else:
                return False
        else:
            logging.info("Not created particle on coordinates %s", str(coordinates))
            return False

    def create_particle_on(self, x=None, y=None, color=black, transparency=1):
        """
        Creates a particle either on a given x,y coordinates

        :toDo: seperate the directionection and coordinates and delete state

        :param x: x coordinate
        :param y: y coordinate
        :return: New Particle or False
        """
        coordinates = (0, 0)
        if x is not None and y is not None:
            if grid.is_valid_location(coordinates):
                logging.info("Going to create a particle on position %s", str(coordinates))
                new_particle = self.world.add_particle(coordinates[0], coordinates[1], color, transparency)
                if new_particle:
                    self.world.particle_map_coordinates[coordinates[0], coordinates[1]].created = True
                    logging.info("Created particle on coordinates %s", str(coordinates))
                    self.world.csv_round.update_particle_num(len(self.world.get_particle_list()))
                    self.world.csv_round.update_metrics( particle_created=1)
                    self.csv_particle_writer.write_particle(particle_created=1)
                    return new_particle
                else:
                    return False
            else:
                return False
        else:
            logging.info("Not created particle on coordinates %s", str(coordinates))
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

    def delete_particle_with(self, id):
        """
        Deletes a particle with a given id

        :param id: The id of the particle that should be deleted
        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        logging.info("Particle %s is", self.get_id())
        logging.info("is going to delete a particle with id %s", str(id))
        if self.world.remove_particle(id):
            self.csv_particle_writer.write_particle(particle_deleted=1)
            return True
        else:
            logging.info("Could not delet particle with particle id %s", str(id))
            return False

    def delete_particle_in(self, direction=None):
        """
        Deletes a particle either in a given directionection

        :param direction: The directionection on which the particle should be deleted. Options: E, SE, SW, W, NW, NE,
        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        if direction is not None:
            coordinates = get_coordinates_in_direction(self.coordinates, direction)
            logging.info("Deleting tile in %s directionection", str(direction))
            if self.world.remove_particle_on(coordinates):
                logging.info("Deleted particle with particle on coordinates %s", str(coordinates))
                self.csv_particle_writer.write_particle(particle_deleted=1)
                return True
            else:
                logging.info("Could not delet particle on coordinates %s", str(coordinates))
                return False

    def delete_particle_on(self, coordinates=None):
        """
        Deletes a particle either on a given x,y coordinates

        :param coordinates
        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        if coordinates is not None:
            if grid.is_valid_location(coordinates):
                if self.world.remove_particle_on(coordinates):
                    logging.info("Deleted particle with particle on coordinates %s", str(coordinates))
                    self.csv_particle_writer.write_particle(particle_deleted=1)
                    return True
                else:
                    logging.info("Could not delet particle on coordinates %s", str(coordinates))
                    return False
            else:
                return False
        else:
            return False

    def take_particle(self):
        """
        Takes a particle on the actual position

        :return: True: successful taken; False: unsuccessful taken
        """
        if self.carried_particle is None and self.carried_tile is None:
            if self.coordinates in self.world.particle_map_coordinates:
                self.carried_particle = self.world.particle_map_coordinates[self.coordinates]
                if self.carried_particle.take_me(coordinates=self.coordinates):
                    logging.info("particle has been taken")
                    self.world.csv_round.update_metrics( particles_taken=1)
                    self.csv_particle_writer.write_particle(particles_taken=1)
                    return True
                else:
                    logging.info("particle could not be taken")
                    return False
            else:
                logging.info("No particle on the actual position not in the world")
                return False
        else:
            logging.info("particle cannot taken because particle is carrieng either a particle or a particle")
            return False

    def take_particle_with(self, id):
        """
        Takes a particle with a given tile id

        :param id:  The id of the particle that should be taken
        :return: True: successful taken; False: unsuccessful taken
        """
        if self.carried_tile is None and self.carried_particle is None:
            if id in self.world.get_particle_map_id():
                logging.info("particle with particle id %s is in the world", str(id))
                self.carried_particle = self.world.particle_map_id[id]
                if self.carried_particle.take_me(self.coordinates):
                    logging.info("particle with particle id %s  has been taken", str(id))

                    self.world.csv_round.update_metrics(
                                                               particles_taken=1)
                    self.csv_particle_writer.write_particle(particles_taken=1)
                    return True
                else:
                    logging.info("particle with particle id %s could not be taken", str(id))
                    return False
            else:
                logging.info("particle with particle id %s is not in the world", str(id))
        else:
            logging.info("particle cannot taken because particle is carrieng either a particle or a particle", str(id))

    def take_particle_in(self, direction):
        """
        Takes a particle that is in a given directionection

        :param direction: The directionection on which the particle should be taken. Options: E, SE, SW, W, NW, NE,
        :return: True: successful taken; False: unsuccessful taken
        """
        if self.carried_tile is None and self.carried_particle is None:
            coordinates = get_coordinates_in_direction(self.coordinates, direction)
            if coordinates in self.world.particle_map_coordinates:
                logging.info("Take particle")
                self.carried_particle = self.world.particle_map_coordinates[coordinates]
                if self.carried_particle.take_me(coordinates=self.coordinates):
                    logging.info("particle with particle id %s  has been taken", str(self.carried_particle.get_id()))
                    self.world.csv_round.update_metrics(
                                                               particles_taken=1)
                    self.csv_particle_writer.write_particle(particles_taken=1)
                    return True
                else:
                    logging.info("particle could not be taken")
                    return False
            else:
                logging.info("particl is not in the world")
                return False
        else:
            logging.info("particle cannot be  taken")
            return False

    def take_particle_on(self, coordinates):
        """
        Takes the particle on the given coordinate if it is not taken

        :param y:
        :param x:
        :return: True: Successful taken; False: Cannot be taken or wrong Coordinates
        """
        if self.carried_particle is None and self.carried_tile is None:
            if grid.is_valid_location(coordinates):
                if coordinates in self.world.particle_map_coordinates:
                    self.carried_particle = self.world.particle_map_coordinates[coordinates]
                    logging.info("Particle with id %s is in the world", str(self.carried_particle.get_id()))
                    if self.carried_particle.take_me(coordinates=self.coordinates):
                        self.world.csv_round.update_metrics( particles_taken=1)
                        self.csv_particle_writer.write_particle(particles_taken=1)
                        logging.info("particle with tile id %s has been taken", str(self.carried_particle.get_id()))
                        return True
                    else:
                        logging.info("Particle with id %s could not be taken", str(self.carried_particle.get_id()))
                        return False
                else:
                    logging.info("Particle is not in the world")
                    return False
            else:
                logging.info("Coordinates are wrong")
                return False
        else:
            logging.info("Particle cannot taken because particle is carrieng either a tile or a particle")
            return False

    def drop_particle(self):
        """
        Drops the taken particle on the particles actual position

        :return: None
        """
        if self.carried_particle is not None:
            if self.coordinates not in self.world.particle_map_coordinates:
                try:  # cher: insert so to overcome the AttributeError
                    self.carried_particle.drop_me(self.coordinates)
                except AttributeError:
                    logging.info("Dropped particle: Error while dropping")
                    return False
            self.carried_particle = None
            self.world.csv_round.update_metrics( particles_dropped=1)
            self.csv_particle_writer.write_particle(particles_dropped=1)
            logging.info("Particle succesfull dropped")
            return True
        else:
            logging.info("No particle taken to drop")
            return False

    def drop_particle_in(self, direction):
        """
        Drops the particle tile in a given directionection

         :param direction: The directionection on which the particle should be dropped. Options: E, SE, SW, W, NW, NE,
        """
        if self.carried_particle is not None:
            coordinates = get_coordinates_in_direction(self.coordinates, direction)
            if coordinates not in self.world.particle_map_coordinates:
                try:  # cher: insert so to overcome the AttributeError
                    self.carried_particle.drop_me(coordinates)
                except AttributeError:
                    logging.info("Dropped particle in: Error while dropping")
                    return False
                self.carried_particle = None
                logging.info("Dropped particle on %s coordinate", str(coordinates))
                self.world.csv_round.update_metrics( particles_dropped=1)
                self.csv_particle_writer.write_particle(particles_dropped=1)
                return True
            else:
                logging.info("Is not possible to drop the particle on that position because it is occupied")
                return False
        else:
            logging.info("No particle taken to drop")
            return False

    def drop_particle_on(self, coordinates=None):
        """
        Drops the particle tile on a given x and y coordination

        :param x: x coordinate
        :param y: y coordinate
        """
        if self.carried_particle is not None and coordinates is not None and grid.is_valid_location(coordinates):
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
                logging.info("Is not possible to drop the particle on that position  because it is occupied")
                return False
        else:
            logging.info("drop_particle_on: Wrong Inputs")
            return False

    def update_particle_coordinates(self, particle, new_coordinates):
        """
        Upadting the particle with new coordinates
        Only necessary for taking and moving particles

        :param particle: The particle object
        :param new_coordinates: new coorindation points
        :return: None
        """
        if grid.is_valid_location(new_coordinates):
            particle.coordinates = new_coordinates
            self.particle_map_coordinates[new_coordinates] = particle
            return True
        else:
            return False

    def create_marker(self, color=black, transparency=1):
        """
         Creates a marker on the particles actual position

        :return: New marker or False
        """

        logging.info("Going to create on position %s", str(self.coordinates))
        new_marker=self.world.add_marker(self.coordinates[0], self.coordinates[1], color, transparency)
        if new_marker != False:
            self.csv_particle_writer.write_particle(marker_created=1)
            self.world.csv_round.update_markers_num(len(self.world.get_marker_list()))
            self.world.csv_round.update_metrics( marker_created=1)
            return new_marker
        else:
            return False

    def create_marker_in(self, direction=None, color=black, transparency=1):
        """
        Creates a marker either in a given directionection
        :param direction: The directionection on which the marker should be created. Options: E, SE, SW, W, NW, NE,
        :return: New marker or False

        """
        coordinates = (0, 0)
        if direction is not None:
            coordinates = get_coordinates_in_direction(self.coordinates, direction)
            logging.info("Going to create a marker in %s on position %s", str(direction), str(coordinates))
            new_marker = self.world.add_marker(coordinates[0], coordinates[1], color, transparency)
            if new_marker:
                logging.info("Created marker on coordinates %s", str(coordinates))
                self.world.csv_round.update_markers_num(len(self.world.get_marker_list()))
                self.world.csv_round.update_metrics( marker_created=1)
                return new_marker
            else:
                return False
        else:
            logging.info("Not created marker on coordinates %s", str(coordinates))
            return False

    def create_marker_on(self, coordinates=None, color=black, transparency=1):
        """
        Creates a marker either on a given x,y coordinates

        :param x: x coordinate
        :param y: y coordinate
        :return: New marker or False

        """
        if coordinates is not None:
            if grid.is_valid_location(coordinates):
                logging.info("Going to create a marker on position %s", str(coordinates))
                new_marker =  self.world.add_marker(coordinates[0], coordinates[1], color, transparency)
                if new_marker:
                    logging.info("Created marker on coordinates %s", str(coordinates))
                    self.world.csv_round.update_markers_num(len(self.world.get_marker_list()))
                    self.world.csv_round.update_metrics(marker_created=1)
                    return new_marker
            else:
                return False
        else:
            logging.info("Not created marker on coordinates %s", str(coordinates))
            return False

    def delete_marker(self):
        """
        Deletes a marker on current position

        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        logging.info("Particle %s is", self.get_id())
        logging.info("is going to delete a marker on current position")
        if self.coordinates in self.world.get_marker_map_coordinates():
            if self.world.remove_marker_on(self.coordinates):
                self.csv_particle_writer.write_particle(marker_deleted=1)
                return True
        else:
            logging.info("Could not delet marker")
            return False

    def delete_marker_with(self, marker_id):
        """
        Deletes a marker with a given marker-id

        :param marker_id: The id of the marker that should be deleted
        :return: True: Deleting successful; False: Deleting unsuccessful
        """

        logging.info("marker %s is", self.get_id())
        logging.info("is going to delete a marker with id %s", str(marker_id))
        if self.world.remove_marker(marker_id):
            self.csv_particle_writer.write_particle(marker_deleted=1)
            return True
        else:
            logging.info("Could not delet marker with marker id %s", str(marker_id))
            return False

    def delete_marker_in(self, direction=None):
        """
        Deletes a marker either in a given directionection or on a given x,y coordinates

        :param direction: The directionection on which the marker should be deleted. Options: E, SE, SW, W, NW, NE,
        :param x: x coordinate
        :param y: y coordinate
        :return: True: Deleting successful; False: Deleting unsuccessful
        """

        if direction is not None:
            coordinates = get_coordinates_in_direction(self.coordinates, direction)
            logging.info("Deleting tile in %s directionection", str(direction))
            if self.world.remove_marker_on(coordinates):
                logging.info("Deleted marker with marker on coordinates %s", str(coordinates))
                self.csv_particle_writer.write_particle(marker_deleted=1)
                return True
            else:
                logging.info("Could not delet marker on coordinates %s", str(coordinates))
                return False

    def delete_marker_on(self, coordinates=None):
        """
        Deletes a particle either on a given x,y coordinates

        :param coordinates: the coordinates
        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        if coordinates is not None:
            if grid.is_valid_location(coordinates):
                if self.world.remove_marker_on(coordinates):
                    logging.info("Deleted marker  oords %s", str(coordinates))
                    self.csv_particle_writer.write_particle(marker_deleted=1)
                    return True
                else:
                    logging.info("Could not delet marker on coordinates %s", str(coordinates))
                    return False
            else:
                return False
        else:
            return False