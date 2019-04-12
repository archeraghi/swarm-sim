"""
.. module:: particle
   :platform: Unix, Windows
   :synopsis: This module provides the interfaces of the robotics particle

.. moduleauthor:: Ahmad Reza Cheraghi

TODO: Erase Memory

"""

import logging, math
from lib import csv_generator, matter

black = 1
gray = 2
red = 3
green = 4
blue = 5


NE=0
E = 1
SE = 2
SW = 3
W = 4
NW = 5


read = 0
write = 1
particle_counter=0

class Particle(matter.Matter):
    """In the classe location all the methods for the characterstic of a location is included"""

    def __init__(self, sim, x, y, color=black, alpha=1, mm_limit=0, mm_size=0):
        """Initializing the location constructor"""
        super().__init__( sim, x, y, color, alpha, type="particle", mm_limit=mm_limit, mm_size=mm_size)
        global particle_counter
        particle_counter+=1
        self.number=particle_counter
        self.__isCarried = False
        self.created = False
        self.carried_tile = None
        self.carried_particle = None
        self.__isCarried = False
        self.steps = 0
        self.created = False
        self.csv_particle_writer = csv_generator.CsvParticleData( self.get_id(), self.number)

    def coords_to_sim(self, coords):
        return coords[0], coords[1] * math.sqrt(3 / 4)

    def sim_to_coords(self, x, y):
        return x, round(y / math.sqrt(3 / 4), 0)

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
        if self.coords in self.sim.tile_map_coords:
            return True
        else:
            return False


    def check_on_particle(self):
        """
        Checks if the particle is on a particle

        :return: True: On a particle; False: Not on a particle
        """
        if self.coords in self.sim.particle_map_coords:
            return True
        else:
            return False

    def check_on_location(self):
        """
        Checks if the particle is on a location

        :return: True: On a location; False: Not on a location
        """
        if self.coords in self.sim.location_map_coords:
            return True
        else:
            return False

    def move_to(self, dir):
        """
        Moves the particle to the given direction

        :param dir: The direction must be either: E, SE, SW, W, NW, or NE
        :return: True: Success Moving;  False: Non moving
        """
        dir_coord = self.sim.get_coords_in_dir(self.coords, dir)

        if self.sim.border==1 and (abs(dir_coord[0]) > self.sim.get_sim_x_size() \
                                    or  abs(dir_coord[1]) > self.sim.get_sim_y_size()) :
                dir = dir - 3 if dir > 2 else dir + 3
                dir_coord = self.sim.get_coords_in_dir(self.coords, dir)
        if self.sim.check_coords(dir_coord[0], dir_coord[1]):

            try:  # cher: added so the program does not crashed if it does not find any entries in the map
                del self.sim.particle_map_coords[self.coords]
            except KeyError:
                pass
            self.coords = dir_coord
            if not self.coords in self.sim.particle_map_coords:
                self.sim.particle_map_coords[self.coords] = self
                logging.info("particle %s successfully moved to %s", str(self.get_id()), dir)
                self.sim.csv_round_writer.update_metrics( steps=1)
                self.csv_particle_writer.write_particle(steps=1)
                self.touch()
                if self.carried_tile is not None:
                    self.carried_tile.coords = self.coords
                    self.carried_tile.touch()
                elif self.carried_particle is not None:
                    self.carried_particle.coords = self.coords
                    self.carried_particle.touch()
                return True
        return False

    def move_to_in_bounds(self, dir):
        """
            Moves the particle to the given direction if it would remain in bounds.

            :param dir: The direction must be either: E, SE, SW, W, NW, or NE
            :return: True: Success Moving;  False: Non moving
        """
        dir_coord = self.sim.get_coords_in_dir(self.coords, dir)
        sim_coord = self.coords_to_sim(dir_coord)
        if self.sim.get_sim_x_size() >=  abs(sim_coord[0]) and \
                        self.sim.get_sim_y_size() >=  abs(sim_coord[1]):
            return self.move_to(dir)
        else:
            # 'bounce' off the wall
            n_dir = dir - 3 if dir > 2 else dir + 3
            self.move_to(n_dir)

    def read_from_with(self, matter, key=None):
        """
        Read the memories from the matters (paricle, tile, or location object) memories with a given keyword

        :param matter: The matter can be either a particle, tile, or location
        :param key: A string keyword to searcg for the data in the memory
        :return: The matters memory; None
        """
        if key != None:
            tmp_memory = matter.read_memory_with(key)
        else:
            tmp_memory =  matter.read_whole_memory()

        if tmp_memory != None and len(tmp_memory) > 0 :
            if matter.type == "particle":
                self.sim.csv_round_writer.update_metrics( particle_read=1)
                self.csv_particle_writer.write_particle(particle_read=1)
            elif matter.type == "tile":
                self.sim.csv_round_writer.update_metrics( tile_read=1)
                self.csv_particle_writer.write_particle(tile_read=1)
            elif matter.type == "location":
                self.sim.csv_round_writer.update_metrics( location_read=1)
                self.csv_particle_writer.write_particle(location_read=1)
            return tmp_memory
        else:
            return None

    def write_to_with(self, matter, key=None, data=None):
        """
        Writes data with given a keyword directly on the matters (paricle, tile, or location object) memory

        :param matter: The matter can be either a particle, tile, or location
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
                    self.sim.csv_round_writer.update_metrics( particle_write=1)
                    self.csv_particle_writer.write_particle(particle_write=1)
                elif matter.type == "tile":
                    self.sim.csv_round_writer.update_metrics( tile_write=1)
                    self.csv_particle_writer.write_particle(tile_write=1)
                elif matter.type == "location":
                    self.sim.csv_round_writer.update_metrics( location_write=1)
                    self.csv_particle_writer.write_particle(location_write=1)
                return True
            else:
                return False
        else:
            return False



    def matter_in(self, matter="tile", dir=E):
        if matter=="tile":
            return self.sim.get_coords_in_dir(self.coords, dir) in self.sim.get_tile_map_coords()
        if matter=="particle":
            return self.sim.get_coords_in_dir(self.coords, dir) in self.sim.get_particle_map_coords()
        if matter=="location":
            return self.sim.get_coords_in_dir(self.coords, dir) in self.sim.get_location_map_coords()


    def tile_in(self, dir=E):
            return self.sim.get_coords_in_dir(self.coords, dir) in self.sim.get_tile_map_coords()

    def particle_in(self, dir=E):
        return self.sim.get_coords_in_dir(self.coords, dir) in self.sim.get_particle_map_coords()

    def location_in(self, dir=E):
         return self.sim.get_coords_in_dir(self.coords, dir) in self.sim.get_location_map_coords()


    def get_matter_in_dir(self, matter="tile", dir=E):
        if matter=="tile" and self.sim.get_coords_in_dir(self.coords, dir) in self.sim.get_tile_map_coords():
            return self.sim.get_tile_map_coords()[self.sim.get_coords_in_dir(self.coords, dir)]
        if matter=="particle" and self.sim.get_coords_in_dir(self.coords, dir) in self.sim.get_particle_map_coords():
            return self.sim.get_particle_map_coords()[self.sim.get_coords_in_dir(self.coords, dir)]
        if matter=="location" and self.sim.get_coords_in_dir(self.coords, dir) in self.sim.get_location_map_coords():
            return self.sim.get_location_map_coords()[self.sim.get_coords_in_dir(self.coords, dir)]


    def get_tile_in(self, dir=E):
        if self.sim.get_coords_in_dir(self.coords, dir) in self.sim.get_tile_map_coords():
            return self.sim.get_tile_map_coords()[self.sim.get_coords_in_dir(self.coords, dir)]

    def get_particle_in(self, dir=E):
        if self.sim.get_coords_in_dir(self.coords, dir) in self.sim.get_particle_map_coords():
            return self.sim.get_particle_map_coords()[self.sim.get_coords_in_dir(self.coords, dir)]

    def get_location_in(self, dir=E):
        if self.sim.get_coords_in_dir(self.coords, dir) in self.sim.get_location_map_coords():
            return self.sim.get_location_map_coords()[self.sim.get_coords_in_dir(self.coords, dir)]




    def write_to_with(self, matter, key=None, data=None):
        """
        Writes data with given a keyword directly on the matters (paricle, tile, or location object) memory

        :param matter: The matter can be either a particle, tile, or location
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
                    self.sim.csv_round_writer.update_metrics( particle_write=1)
                    self.csv_particle_writer.write_particle(particle_write=1)
                elif matter.type == "tile":
                    self.sim.csv_round_writer.update_metrics( tile_write=1)
                    self.csv_particle_writer.write_particle(tile_write=1)
                elif matter.type == "location":
                    self.sim.csv_round_writer.update_metrics( location_write=1)
                    self.csv_particle_writer.write_particle(location_write=1)
                return True
            else:
                return False
        else:
            return False

    def if_matter_in_dir(self, matter="tile", dir=E):
        if matter=="tile":
            return self.sim.get_coords_in_dir(self.coords, dir) in self.sim.get_tile_map_coords()
        if matter=="particle":
            return self.sim.get_coords_in_dir(self.coords, dir) in self.sim.get_particle_map_coords()
        if matter=="location":
            return self.sim.get_coords_in_dir(self.coords, dir) in self.sim.get_location_map_coords()


    def get_matter_in_dir(self, matter="tile", dir=E):
        if matter=="tile" and  self.sim.get_coords_in_dir(self.coords, dir) in self.sim.get_tile_map_coords():
            return self.sim.get_tile_map_coords()[self.sim.get_coords_in_dir(self.coords, dir)]
        if matter=="particle" and self.sim.get_coords_in_dir(self.coords, dir) in self.sim.get_particle_map_coords():
            return self.sim.get_particle_map_coords()[self.sim.get_coords_in_dir(self.coords, dir)]
        if matter=="location" and self.sim.get_coords_in_dir(self.coords, dir) in self.sim.get_location_map_coords():
            return self.sim.get_location_map_coords()[self.sim.get_coords_in_dir(self.coords, dir)]

    def scan_for_matter_within(self, matter='all', hop=1):
        """
        Scans for particles, tiles, or location on a given hop distance and all the matters within the hop distance

        :todo: If nothing then everything should be scanned

        :param matter: For what matter this method should scan for. Can be either particles, tiles, locations, or (default)all
        :param hop: The hop distance from the actual position of the scanning particle
        :return: A list of the founded matters
        """

        hop_list = []
        for i in range(1, hop + 1):
            list = self.scan_for_matter_in(matter, i)
            if list != None:
                hop_list.extend(list)
        if len(hop_list) != 0:
            return hop_list
        else:
            return None

    def scan_for_matter_in(self, matter='all', hop=1):
        """
        Scanning for particles, tiles, or location on a given hop distance

        :param matter: For what matter this method should scan for. Can be either particles, tiles, locations, or (default)all
        :param hop: The hop distance from thee actual position of the scanning particle
        :return: A list of the founded matters
        """
        hop_list = []
        logging.info("particle on %s is scanning for %s in %i hops", str(self.coords), matter, hop)
        cnt = 0
        x_offset = 0
        y_up_scan = self.coords[1] + hop
        y_down_scan = self.coords[1] - hop
        while cnt < hop:
            x_scan_pos = self.coords[0] + hop - x_offset
            x_scan_neg = self.coords[0] - hop + x_offset
            y_scan_coord_neg = self.coords[1] - cnt
            y_scan_coord_pos = self.coords[1] + cnt
            if cnt == 0:
                if matter == "particles":
                    if (x_scan_pos, y_scan_coord_neg) in self.sim.particle_map_coords:
                        hop_list.append(self.sim.particle_map_coords[(x_scan_pos, y_scan_coord_neg)])
                    if (x_scan_neg, y_scan_coord_neg) in self.sim.particle_map_coords:
                        hop_list.append(self.sim.particle_map_coords[(x_scan_neg, y_scan_coord_neg)])
                elif matter == "locations":
                    if (x_scan_pos, y_scan_coord_neg) in self.sim.location_map_coords:
                        hop_list.append(self.sim.location_map_coords[(x_scan_pos, y_scan_coord_neg)])
                    if (x_scan_neg, y_scan_coord_neg) in self.sim.location_map_coords:
                        hop_list.append(self.sim.location_map_coords[(x_scan_neg, y_scan_coord_neg)])
                elif matter == "tiles":
                    if (x_scan_pos, y_scan_coord_neg) in self.sim.tile_map_coords:
                        hop_list.append(self.sim.tile_map_coords[(x_scan_pos, y_scan_coord_neg)])
                    if (x_scan_neg, y_scan_coord_neg) in self.sim.tile_map_coords:
                        hop_list.append(self.sim.tile_map_coords[(x_scan_neg, y_scan_coord_neg)])
                elif matter == "all":

                    if (x_scan_pos, y_scan_coord_neg) in self.sim.tile_map_coords:
                        hop_list.append(self.sim.tile_map_coords[(x_scan_pos, y_scan_coord_neg)])
                    if (x_scan_neg, y_scan_coord_neg) in self.sim.tile_map_coords:
                        hop_list.append(self.sim.tile_map_coords[(x_scan_neg, y_scan_coord_neg)])
                    if (x_scan_pos, y_scan_coord_neg) in self.sim.location_map_coords:
                        hop_list.append(self.sim.location_map_coords[(x_scan_pos, y_scan_coord_neg)])
                    if (x_scan_neg, y_scan_coord_neg) in self.sim.location_map_coords:
                        hop_list.append(self.sim.location_map_coords[(x_scan_neg, y_scan_coord_neg)])
                    if (x_scan_pos, y_scan_coord_neg) in self.sim.particle_map_coords:
                        hop_list.append(self.sim.particle_map_coords[(x_scan_pos, y_scan_coord_neg)])
                    if (x_scan_neg, y_scan_coord_neg) in self.sim.particle_map_coords:
                        hop_list.append(self.sim.particle_map_coords[(x_scan_neg, y_scan_coord_neg)])
                else:
                    logging.info("No matter specified")
            else:
                if matter == "particles":
                    if (x_scan_pos, y_scan_coord_pos) in self.sim.particle_map_coords:
                        hop_list.append(self.sim.particle_map_coords[(x_scan_pos, y_scan_coord_pos)])
                    if (x_scan_pos, y_scan_coord_neg) in self.sim.particle_map_coords:
                        hop_list.append(self.sim.particle_map_coords[(x_scan_pos, y_scan_coord_neg)])
                    if (x_scan_neg, y_scan_coord_pos) in self.sim.particle_map_coords:
                        hop_list.append(self.sim.particle_map_coords[(x_scan_neg, y_scan_coord_pos)])
                    if (x_scan_neg, y_scan_coord_neg) in self.sim.particle_map_coords:
                        hop_list.append(self.sim.particle_map_coords[(x_scan_neg, y_scan_coord_neg)])
                elif matter == "locations":
                    if (x_scan_pos, y_scan_coord_pos) in self.sim.location_map_coords:
                        hop_list.append(self.sim.location_map_coords[(x_scan_pos, y_scan_coord_pos)])
                    if (x_scan_pos, y_scan_coord_neg) in self.sim.location_map_coords:
                        hop_list.append(self.sim.location_map_coords[(x_scan_pos, y_scan_coord_neg)])
                    if (x_scan_neg, y_scan_coord_pos) in self.sim.location_map_coords:
                        hop_list.append(self.sim.location_map_coords[(x_scan_neg, y_scan_coord_pos)])
                    if (x_scan_neg, y_scan_coord_neg) in self.sim.location_map_coords:
                        hop_list.append(self.sim.location_map_coords[(x_scan_neg, y_scan_coord_neg)])
                elif matter == "tiles":
                    if (x_scan_pos, y_scan_coord_pos) in self.sim.tile_map_coords:
                        hop_list.append(self.sim.tile_map_coords[(x_scan_pos, y_scan_coord_pos)])
                    if (x_scan_pos, y_scan_coord_neg) in self.sim.tile_map_coords:
                        hop_list.append(self.sim.tile_map_coords[(x_scan_pos, y_scan_coord_neg)])
                    if (x_scan_pos, y_scan_coord_neg) in self.sim.tile_map_coords:
                        hop_list.append(self.sim.tile_map_coords[(x_scan_pos, y_scan_coord_neg)])
                    if (x_scan_neg, y_scan_coord_neg) in self.sim.tile_map_coords:
                        hop_list.append(self.sim.tile_map_coords[(x_scan_neg, y_scan_coord_neg)])
                elif matter == "all":
                    if (x_scan_pos, y_scan_coord_pos) in self.sim.particle_map_coords:
                        hop_list.append(self.sim.particle_map_coords[(x_scan_pos, y_scan_coord_pos)])
                    if (x_scan_pos, y_scan_coord_neg) in self.sim.particle_map_coords:
                        hop_list.append(self.sim.particle_map_coords[(x_scan_pos, y_scan_coord_neg)])
                    if (x_scan_neg, y_scan_coord_pos) in self.sim.particle_map_coords:
                        hop_list.append(self.sim.particle_map_coords[(x_scan_neg, y_scan_coord_pos)])
                    if (x_scan_neg, y_scan_coord_neg) in self.sim.particle_map_coords:
                        hop_list.append(self.sim.particle_map_coords[(x_scan_neg, y_scan_coord_neg)])

                    if (x_scan_pos, y_scan_coord_pos) in self.sim.location_map_coords:
                        hop_list.append(self.sim.location_map_coords[(x_scan_pos, y_scan_coord_pos)])
                    if (x_scan_pos, y_scan_coord_neg) in self.sim.location_map_coords:
                        hop_list.append(self.sim.location_map_coords[(x_scan_pos, y_scan_coord_neg)])
                    if (x_scan_neg, y_scan_coord_pos) in self.sim.location_map_coords:
                        hop_list.append(self.sim.location_map_coords[(x_scan_neg, y_scan_coord_pos)])
                    if (x_scan_neg, y_scan_coord_neg) in self.sim.location_map_coords:
                        hop_list.append(self.sim.location_map_coords[(x_scan_neg, y_scan_coord_neg)])

                    if (x_scan_pos, y_scan_coord_pos) in self.sim.tile_map_coords:
                        hop_list.append(self.sim.tile_map_coords[(x_scan_pos, y_scan_coord_pos)])
                    if (x_scan_pos, y_scan_coord_neg) in self.sim.tile_map_coords:
                        hop_list.append(self.sim.tile_map_coords[(x_scan_pos, y_scan_coord_neg)])
                    if (x_scan_pos, y_scan_coord_neg) in self.sim.tile_map_coords:
                        hop_list.append(self.sim.tile_map_coords[(x_scan_pos, y_scan_coord_neg)])
                    if (x_scan_neg, y_scan_coord_neg) in self.sim.tile_map_coords:
                        hop_list.append(self.sim.tile_map_coords[(x_scan_neg, y_scan_coord_neg)])

                else:
                    logging.info("No matter specified")
            cnt += 1
            x_offset += 0.5

        cnt = 0
        x_upper_scan = self.coords[0] + hop / 2
        offset_x = 0
        while cnt < hop + 1:
            x_upper_scan = x_upper_scan - offset_x
            if matter == "particles":
                if (x_upper_scan, y_up_scan) in self.sim.particle_map_coords:
                    hop_list.append(self.sim.particle_map_coords[(x_upper_scan, y_up_scan)])
                if (x_upper_scan, y_down_scan) in self.sim.particle_map_coords:
                    hop_list.append(self.sim.particle_map_coords[(x_upper_scan, y_down_scan)])
            elif matter == "locations":
                if (x_upper_scan, y_up_scan) in self.sim.location_map_coords:
                    hop_list.append(self.sim.location_map_coords[(x_upper_scan, y_up_scan)])
                if (x_upper_scan, y_down_scan) in self.sim.location_map_coords:
                    hop_list.append(self.sim.location_map_coords[(x_upper_scan, y_down_scan)])
            elif matter == "tiles":
                if (x_upper_scan, y_up_scan) in self.sim.tile_map_coords:
                    hop_list.append(self.sim.tile_map_coords[(x_upper_scan, y_up_scan)])
                if (x_upper_scan, y_down_scan) in self.sim.tile_map_coords:
                    hop_list.append(self.sim.tile_map_coords[(x_upper_scan, y_down_scan)])
            if matter == "all":
                if hop == 0:
                    if (0, 0) in self.sim.particle_map_coords:
                        hop_list.append(self.sim.particle_map_coords[(0, 0)])
                    if (0, 0) in self.sim.location_map_coords:
                        hop_list.append(self.sim.location_map_coords[(0, 0)])
                    if (0, 0) in self.sim.tile_map_coords:
                        hop_list.append(self.sim.tile_map_coords[(0, 0)])

                else:
                    if (x_upper_scan, y_up_scan) in self.sim.particle_map_coords:
                        hop_list.append(self.sim.particle_map_coords[(x_upper_scan, y_up_scan)])
                    if (x_upper_scan, y_down_scan) in self.sim.particle_map_coords:
                        hop_list.append(self.sim.particle_map_coords[(x_upper_scan, y_down_scan)])

                    if (x_upper_scan, y_up_scan) in self.sim.location_map_coords:
                        hop_list.append(self.sim.location_map_coords[(x_upper_scan, y_up_scan)])
                    if (x_upper_scan, y_down_scan) in self.sim.location_map_coords:
                        hop_list.append(self.sim.location_map_coords[(x_upper_scan, y_down_scan)])

                    if (x_upper_scan, y_up_scan) in self.sim.tile_map_coords:
                        hop_list.append(self.sim.tile_map_coords[(x_upper_scan, y_up_scan)])
                    if (x_upper_scan, y_down_scan) in self.sim.tile_map_coords:
                        hop_list.append(self.sim.tile_map_coords[(x_upper_scan, y_down_scan)])

            else:
                logging.info("No matter specified")
            cnt += 1
            offset_x = 1
        if len(hop_list) > 0:
            logging.info("Got %s in %s hops", str(len(hop_list)), str(hop))
            return hop_list
        else:
            logging.info("Nothing in %s hops", str(hop))
            return None



    def scan_for_particle_within(self, hop=1):
        """
        Scans for particles, tiles, or location on a given hop distance and all the matters within the hop distance

        :todo: If nothing then everything should be scanned

        :param matter: For what matter this method should scan for. Can be either particles, tiles, locations, or (default)all
        :param hop: The hop distance from the actual position of the scanning particle
        :return: A list of the founded matters
        """

        hop_list = []
        for i in range(1, hop + 1):
            list = self.scan_for_particle_in( i)
            if list != None:
                hop_list.extend(list)
        if len(hop_list) != 0:
            return hop_list
        else:
            return None

    def scan_for_particle_in(self, hop=1):
        """
        Scanning for particles, tiles, or location on a given hop distance

        :param matter: For what matter this method should scan for. Can be either particles, tiles, locations, or (default)all
        :param hop: The hop distance from thee actual position of the scanning particle
        :return: A list of the founded matters
        """
        hop_list = []
        logging.info("particle on %s is scanning for particle in %i hops", str(self.coords), hop)
        cnt = 0
        x_offset = 0
        y_up_scan = self.coords[1] + hop
        y_down_scan = self.coords[1] - hop
        while cnt < hop:
            x_scan_pos = self.coords[0] + hop - x_offset
            x_scan_neg = self.coords[0] - hop + x_offset
            y_scan_coord_neg = self.coords[1] - cnt
            y_scan_coord_pos = self.coords[1] + cnt
            if cnt == 0:
                # if self.coords in self.sim.particle_map_coords:
                #     hop_list.append(self.sim.particle_map_coords[self.coords])
                if (x_scan_pos, y_scan_coord_neg) in self.sim.particle_map_coords:
                    hop_list.append(self.sim.particle_map_coords[(x_scan_pos, y_scan_coord_neg)])
                if (x_scan_neg, y_scan_coord_neg) in self.sim.particle_map_coords:
                    hop_list.append(self.sim.particle_map_coords[(x_scan_neg, y_scan_coord_neg)])
            else:
                if (x_scan_pos, y_scan_coord_pos) in self.sim.particle_map_coords:
                    hop_list.append(self.sim.particle_map_coords[(x_scan_pos, y_scan_coord_pos)])
                if (x_scan_pos, y_scan_coord_neg) in self.sim.particle_map_coords:
                    hop_list.append(self.sim.particle_map_coords[(x_scan_pos, y_scan_coord_neg)])
                if (x_scan_neg, y_scan_coord_pos) in self.sim.particle_map_coords:
                    hop_list.append(self.sim.particle_map_coords[(x_scan_neg, y_scan_coord_pos)])
                if (x_scan_neg, y_scan_coord_neg) in self.sim.particle_map_coords:
                    hop_list.append(self.sim.particle_map_coords[(x_scan_neg, y_scan_coord_neg)])
            cnt += 1
            x_offset += 0.5

        cnt = 0
        x_upper_scan = self.coords[0] + hop / 2
        offset_x = 0
        while cnt < hop + 1:
            x_upper_scan = x_upper_scan - offset_x
            if (x_upper_scan, y_up_scan) in self.sim.particle_map_coords:
                hop_list.append(self.sim.particle_map_coords[(x_upper_scan, y_up_scan)])
            if (x_upper_scan, y_down_scan) in self.sim.particle_map_coords:
                hop_list.append(self.sim.particle_map_coords[(x_upper_scan, y_down_scan)])
            cnt += 1
            offset_x = 1
        if len(hop_list) > 0:
            logging.info("Got %s in %s hops", str(len(hop_list)), str(hop))
            return hop_list
        else:
            logging.info("Nothing in %s hops", str(hop))
            return None



    def scan_for_tile_within(self,  hop=1):
        """
        Scans for particles, tiles, or location on a given hop distance and all the matters within the hop distance

        :todo: If nothing then everything should be scanned

        :param matter: For what matter this method should scan for. Can be either particles, tiles, locations, or (default)all
        :param hop: The hop distance from the actual position of the scanning particle
        :return: A list of the founded matters
        """

        hop_list = []
        for i in range(1, hop + 1):
            list = self.scan_for_tile_in(i)
            if list != None:
                hop_list.extend(list)
        if len(hop_list) != 0:
            return hop_list
        else:
            return None

    def scan_for_tile_in(self, hop=1):
        """
        Scanning for particles, tiles, or location on a given hop distance

        :param matter: For what matter this method should scan for. Can be either particles, tiles, locations, or (default)all
        :param hop: The hop distance from thee actual position of the scanning particle
        :return: A list of the founded matters
        """
        hop_list = []
        logging.info("particle on %s is scanning for tile in %i hops", str(self.coords), hop)
        cnt = 0
        x_offset = 0
        y_up_scan = self.coords[1] + hop
        y_down_scan = self.coords[1] - hop
        while cnt < hop:
            x_scan_pos = self.coords[0] + hop - x_offset
            x_scan_neg = self.coords[0] - hop + x_offset
            y_scan_coord_neg = self.coords[1] - cnt
            y_scan_coord_pos = self.coords[1] + cnt
            if cnt == 0:
                # if self.coords in self.sim.tile_map_coords:
                #     hop_list.append(self.sim.tile_map_coords[self.coords])
                if (x_scan_pos, y_scan_coord_neg) in self.sim.tile_map_coords:
                    hop_list.append(self.sim.tile_map_coords[(x_scan_pos, y_scan_coord_neg)])
                if (x_scan_neg, y_scan_coord_neg) in self.sim.tile_map_coords:
                    hop_list.append(self.sim.tile_map_coords[(x_scan_neg, y_scan_coord_neg)])
            else:
                if (x_scan_pos, y_scan_coord_pos) in self.sim.tile_map_coords:
                    hop_list.append(self.sim.tile_map_coords[(x_scan_pos, y_scan_coord_pos)])
                if (x_scan_pos, y_scan_coord_neg) in self.sim.tile_map_coords:
                    hop_list.append(self.sim.tile_map_coords[(x_scan_pos, y_scan_coord_neg)])
                if (x_scan_pos, y_scan_coord_neg) in self.sim.tile_map_coords:
                    hop_list.append(self.sim.tile_map_coords[(x_scan_pos, y_scan_coord_neg)])
                if (x_scan_neg, y_scan_coord_neg) in self.sim.tile_map_coords:
                    hop_list.append(self.sim.tile_map_coords[(x_scan_neg, y_scan_coord_neg)])
            cnt += 1
            x_offset += 0.5

        cnt = 0
        x_upper_scan = self.coords[0] + hop / 2
        offset_x = 0
        while cnt < hop + 1:
            x_upper_scan = x_upper_scan - offset_x
            if (x_upper_scan, y_up_scan) in self.sim.tile_map_coords:
                hop_list.append(self.sim.tile_map_coords[(x_upper_scan, y_up_scan)])
            if (x_upper_scan, y_down_scan) in self.sim.tile_map_coords:
                hop_list.append(self.sim.tile_map_coords[(x_upper_scan, y_down_scan)])
            cnt += 1
            offset_x = 1
        if len(hop_list) > 0:
            logging.info("Got %s in %s hops", str(len(hop_list)), str(hop))
            return hop_list
        else:
            logging.info("Nothing in %s hops", str(hop))
            return None


    def scan_for_location_within(self, hop=1):
        """
        Scans for particles, tiles, or location on a given hop distance and all the matters within the hop distance

        :todo: If nothing then everything should be scanned

        :param matter: For what matter this method should scan for. Can be either particles, tiles, locations, or (default)all
        :param hop: The hop distance from the actual position of the scanning particle
        :return: A list of the founded matters
        """

        hop_list = []
        for i in range(1, hop + 1):
            list = self.scan_for_location_in(i)
            if list != None:
                hop_list.extend(list)
        if len(hop_list) != 0:
            return hop_list
        else:
            return None

    def scan_for_location_in(self, hop=1):
        """
        Scanning for particles, tiles, or location on a given hop distance

        :param matter: For what matter this method should scan for. Can be either particles, tiles, locations, or (default)all
        :param hop: The hop distance from thee actual position of the scanning particle
        :return: A list of the founded matters
        """
        hop_list = []
        logging.info("particle is scanning for location in %i hops", hop)
        cnt = 0
        x_offset = 0
        y_up_scan = self.coords[1] + hop
        y_down_scan = self.coords[1] - hop
        while cnt < hop:
            x_scan_pos = self.coords[0] + hop - x_offset
            x_scan_neg = self.coords[0] - hop + x_offset
            y_scan_coord_neg = self.coords[1] - cnt
            y_scan_coord_pos = self.coords[1] + cnt
            if cnt == 0:
                # if self.coords in self.sim.location_map_coords:
                #     hop_list.append(self.sim.location_map_coords[self.coords])
                if (x_scan_pos, y_scan_coord_neg) in self.sim.location_map_coords:
                    hop_list.append(self.sim.location_map_coords[(x_scan_pos, y_scan_coord_neg)])
                if (x_scan_neg, y_scan_coord_neg) in self.sim.location_map_coords:
                    hop_list.append(self.sim.location_map_coords[(x_scan_neg, y_scan_coord_neg)])
            else:

                if (x_scan_pos, y_scan_coord_pos) in self.sim.location_map_coords:
                    hop_list.append(self.sim.location_map_coords[(x_scan_pos, y_scan_coord_pos)])
                if (x_scan_pos, y_scan_coord_neg) in self.sim.location_map_coords:
                    hop_list.append(self.sim.location_map_coords[(x_scan_pos, y_scan_coord_neg)])
                if (x_scan_neg, y_scan_coord_pos) in self.sim.location_map_coords:
                    hop_list.append(self.sim.location_map_coords[(x_scan_neg, y_scan_coord_pos)])
                if (x_scan_neg, y_scan_coord_neg) in self.sim.location_map_coords:
                    hop_list.append(self.sim.location_map_coords[(x_scan_neg, y_scan_coord_neg)])
            cnt += 1
            x_offset += 0.5

        cnt = 0
        x_upper_scan = self.coords[0] + hop / 2
        offset_x = 0
        while cnt < hop + 1:
            x_upper_scan = x_upper_scan - offset_x
            if (x_upper_scan, y_up_scan) in self.sim.location_map_coords:
                hop_list.append(self.sim.location_map_coords[(x_upper_scan, y_up_scan)])
            if (x_upper_scan, y_down_scan) in self.sim.location_map_coords:
                hop_list.append(self.sim.location_map_coords[(x_upper_scan, y_down_scan)])
            cnt += 1
            offset_x = 1
        if len(hop_list) > 0:
            logging.info("Got %s in %s hops", str(len(hop_list)), str(hop))
            return hop_list
        else:
            logging.info("Nothing in %s hops", str(hop))
            return None



    def take_me(self, coords=0):
        """
        The particle is getting taken from the the other particle on the given coordinate

        :param coords: Coordination of particle that should be taken
        :return: True: Successful taken; False: Cannot be taken or wrong Coordinates
        """

        if not self.__isCarried:
            if self.coords in self.sim.particle_map_coords:
                del self.sim.particle_map_coords[self.coords]
            self.__isCarried = True
            self.coords = coords
            self.touch()
            return True
        else:
            return False


    def drop_me(self, coords):
        """
        The actual particle is getting dropped

        :param coords: the given position
        :return: None
        """
        self.sim.particle_map_coords[coords] = self
        self.coords = coords
        self.__isCarried = False
        self.touch()

    def create_tile(self, color=gray, alpha=1):
        """
        Creates a tile on the particles actual position

        :return: None
        """
        logging.info("Going to create a tile on position %s", str(self.coords))
        self.sim.add_tile(self.coords[0], self.coords[1], color, alpha)
        self.sim.tile_map_coords[self.coords[0], self.coords[1]].created = True
        self.csv_particle_writer.write_particle(tile_created=1)
        self.sim.csv_round_writer.update_tiles_num(len(self.sim.get_tiles_list()))
        self.sim.csv_round_writer.update_metrics(tile_created=1)

    def create_tile_in(self, dir=None, color=gray, alpha=1):
        """
        Creates a tile either in a given direction

        :param dir: The direction on which the tile should be created. Options: E, SE, SW, W, NW, NE,
        :return: None
        """
        logging.info("particle with id %s is", self.get_id())
        logging.info("Going to create a tile in %s ", str(dir))
        if dir != None:
            coords = self.sim.get_coords_in_dir(self.coords, dir)
            if self.sim.add_tile(coords[0], coords[1], color, alpha) == True:
                self.sim.tile_map_coords[coords[0], coords[1]].created = True
                logging.info("Tile is created")
                self.sim.new_tile_flag = True
                self.csv_particle_writer.write_particle(tile_created=1)
                self.sim.csv_round_writer.update_tiles_num(len(self.sim.get_tiles_list()))
                self.sim.csv_round_writer.update_metrics(tile_created=1)
        else:
            logging.info("Not created tile ")

    def create_tile_on(self, x=None, y=None, color=gray, alpha=1):
        """
        Creates a tile either on a given x,y coordinates

        :param x: x coordinate
        :param y: y coordinate
        :return: None
        """

        logging.info("particle with id %s is", self.get_id())
        if x is not None and y is not None:
            coords = (x, y)
            if self.sim.check_coords(x, y):
                logging.info("Going to create a tile on position \(%i , %i\)", x, y)
                if self.sim.add_tile(coords[0], coords[1], color, alpha) == True:
                    self.sim.tile_map_coords[coords[0], coords[1]].created = True
                    self.sim.new_tile_flag = True
                    self.csv_particle_writer.write_particle(tile_created=1)
                    self.sim.csv_round_writer.update_tiles_num(len(self.sim.get_tiles_list()))
                    self.sim.csv_round_writer.update_metrics(tile_created=1)
                    return True
                else:
                    logging.info("Not created tile on coords  \(%i , %i\)", y, x)
                    return False
            else:
                logging.info("Not created tile on coords   \(%i , %i\)", y, x)

    def delete_tile(self):
        """
        Deletes a tile on current position

        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        logging.info("Particle %s is", self.get_id())
        logging.info("is going to delete a tile on current position")
        if self.coords in self.sim.get_tile_map_coords():
            if self.sim.remove_tile_on(self.coords):
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
        if self.sim.remove_tile(id):
            self.csv_particle_writer.write_particle(tile_deleted=1)
            return True
        else:
            logging.info("Could not delet tile with tile id %s", str(id))
            return False

    def delete_tile_in(self, dir=E):
        """
        Deletes a tile either in a given direction

        :param dir: The direction on which the tile should be deleted. Options: E, SE, SW, W, NW, NE,

        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        coords = ()
        if -1 < dir < 7:
            coords = self.sim.get_coords_in_dir(self.coords, dir)
            logging.info("Deleting tile in %s direction", str(dir))
            if coords is not None:
                if self.sim.remove_tile_on(coords):
                    logging.info("Deleted tile with tile on coords %s", str(coords))
                    self.csv_particle_writer.write_particle(tile_deleted=1)
                    return True
                else:
                    logging.info("Could not delet tile on coords %s", str(coords))
                    return False
        else:
            logging.info("Could not delet tile on coords %s", str(coords))
            return False

    def delete_tile_on(self, x=None, y=None):
        """
        Deletes a tile either on a given x,y coordinates
,
        :param x: x coordinate
        :param y: y coordinate
        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        coords = ()
        if x is not None and y is not None:
            coords = (x, y)
            if self.sim.remove_tile_on(coords):
                logging.info("Deleted tile with tile on coords %s", str(coords))
                self.csv_particle_writer.write_particle(tile_deleted=1)
                return True
            else:
                logging.info("Could not delet tile on coords %s", str(coords))
                return False
        else:
            logging.info("Could not delet tile on coords %s", str(coords))
            return False

    def take_tile(self):
        """
        Takes a tile on the actual position

        :param id:  The id of the tile that should be taken
        :return: True: successful taken; False: unsuccessful taken
        """
        if self.carried_particle is None and self.carried_tile is None:
            if self.coords in self.sim.tile_map_coords:
                self.carried_tile = self.sim.tile_map_coords[self.coords]
                if self.carried_tile.take(coords=self.coords):
                    logging.info("Tile has been taken")
                    self.sim.csv_round_writer.update_metrics(tiles_taken=1)
                    self.csv_particle_writer.write_particle(tiles_taken=1)
                    return True
                else:
                    logging.info("Tile could not be taken")
                    return False
            else:
                logging.info("No tile on the actual position not in the sim")
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
            if id in self.sim.tile_map_id:
                logging.info("Tile with tile id %s is in the sim", str(id))
                self.carried_tile = self.sim.tile_map_id[id]
                if self.carried_tile.take(coords=self.coords):
                    logging.info("Tile with tile id %s  has been taken", str(id))
                    self.sim.csv_round_writer.update_metrics(tiles_taken=1)
                    self.csv_particle_writer.write_particle(tiles_taken=1)
                    return True
                else:
                    logging.info("Tile with tile id %s could not be taken", str(id))
                    return False
            else:
                logging.info("Tile with tile id %s is not in the sim", str(id))
                return False
        else:
            logging.info("Tile cannot taken because particle is carrieng either a tile or a particle", str(id))
            return False

    def take_tile_in(self, dir):
        """
        Takes a tile that is in a given direction

        :param dir: The direction on which the tile should be taken. Options: E, SE, SW, W, NW, NE,
        :return: True: successful taken; False: unsuccessful taken
        """
        if self.carried_particle is None and self.carried_tile is None:
            coords = self.sim.get_coords_in_dir(self.coords, dir)
            if coords in self.sim.tile_map_coords:
                self.carried_tile = self.sim.tile_map_coords[coords]
                logging.info("Tile with tile id %s is in the sim", str(self.carried_tile.get_id()))
                if self.carried_tile.take(coords=self.coords):
                    logging.info("Tile with tile id %s  has been taken", str(self.carried_tile.get_id()))
                    self.sim.csv_round_writer.update_metrics(tiles_taken=1)
                    self.csv_particle_writer.write_particle(tiles_taken=1)
                    return True
                else:
                    logging.info("Tile with tile id %s could not be taken", str(self.carried_tile.get_id()))
                    return False
            else:
                logging.info("Tile is not in the sim")
                return False
        else:
            logging.info("Tile cannot taken because particle is carrieng either a tile or a particle")
            return False

    def take_tile_on(self, x=None, y=None):
        """
        Takes a tile that is in a given direction

        :param x: x coordinate
        :param y: y coordinate
        :return: True: successful taken; False: unsuccessful taken
        """
        if self.carried_particle is None and self.carried_tile is None:
            if self.sim.check_coords(x, y):
                coords = (x, y)
                if coords in self.sim.tile_map_coords:
                    self.carried_tile = self.sim.tile_map_coords[coords]
                    logging.info("Tile with tile id %s is in the sim", str(self.carried_tile.get_id()))
                    if self.carried_tile.take(coords=self.coords):
                        self.sim.csv_round_writer.update_metrics(tiles_taken=1)
                        self.csv_particle_writer.write_particle(tiles_taken=1)
                        logging.info("Tile with tile id %s  has been taken", str(self.carried_tile.get_id()))
                        return True
                    else:
                        logging.info("Tile with tile id %s could not be taken", str(self.carried_tile.get_id()))
                        return False
                else:
                    logging.info("Tile is not in the sim")
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
            if self.coords not in self.sim.tile_map_coords:
                try:  # cher: insert so to overcome the AttributeError
                    self.carried_tile.drop_me(self.coords)
                except AttributeError:
                    pass
                self.carried_tile = None
                logging.info("Tile has been dropped on the actual position")
                self.sim.csv_round_writer.update_metrics(tiles_dropped=1)
                self.csv_particle_writer.write_particle(tiles_dropped=1)
                return True
            else:
                logging.info("Is not possible to drop the tile on that position because it is occupied")
                return False
        else:
            return False

    def drop_tile_in(self, dir):
        """
        Drops the taken tile on a given direction

         :param dir: The direction on which the tile should be dropped. Options: E, SE, SW, W, NW, NE,
        """
        if self.carried_tile is not None:
            coords = self.sim.get_coords_in_dir(self.coords, dir)
            if coords not in self.sim.tile_map_coords:
                try:  # cher: insert so to overcome the AttributeError
                    self.carried_tile.drop_me(coords)
                except AttributeError:
                    pass
                self.carried_tile = None
                self.sim.csv_round_writer.update_metrics(tiles_dropped=1)
                self.csv_particle_writer.write_particle(tiles_dropped=1)
                logging.info("Dropped tile on %s coordinate", str(coords))
                return True
            else:
                logging.info("Is not possible to drop the tile on that position")
                return False

        else:
            logging.info("No tile taken for dropping")
            return False

    def drop_on(self, location="tile", x=None, y=None):
        """
        Drops the taken tile on a given direction

        :param x: x coordinate
        :param y: y coordinate
        """
        if self.carried_tile is not None:
            if self.sim.check_coords(x, y):
                coords = (x, y)
                if coords not in self.sim.get_tile_map_coords():
                    try:  # cher: insert so to overcome the AttributeError
                        self.carried_tile.drop_me(coords)
                    except AttributeError:
                        pass
                    self.carried_tile = None
                    self.sim.csv_round_writer.update_metrics(tiles_dropped=1)
                    self.csv_particle_writer.write_particle(tiles_dropped=1)
                    logging.info("Dropped tile on %s coordinate", str(coords))
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

    def create_tile(self, color=gray, alpha=1):
        """
        Creates a tile on the particles actual position

        :return: None
        """
        logging.info("Going to create a tile on position %s", str(self.coords))
        self.sim.add_tile(self.coords[0], self.coords[1], color, alpha)
        self.sim.tile_map_coords[self.coords[0], self.coords[1]].created = True
        self.csv_particle_writer.write_particle(tile_created=1)
        self.sim.csv_round_writer.update_tiles_num(len(self.sim.get_tiles_list()))
        self.sim.csv_round_writer.update_metrics( tile_created=1)

    def create_tile_in(self, dir=None, color=gray, alpha=1):
        """
        Creates a tile either in a given direction

        :param dir: The direction on which the tile should be created. Options: E, SE, SW, W, NW, NE,
        :return: None
        """
        logging.info("particle with id %s is", self.get_id())
        logging.info("Going to create a tile in %s ", str(dir) )
        if dir != None:
            coords = self.sim.get_coords_in_dir(self.coords, dir)
            if self.sim.add_tile(coords[0], coords[1], color, alpha) == True:
                self.sim.tile_map_coords[coords[0], coords[1]].created = True
                logging.info("Tile is created")
                self.sim.new_tile_flag = True
                self.csv_particle_writer.write_particle(tile_created=1)
                self.sim.csv_round_writer.update_tiles_num(len(self.sim.get_tiles_list()))
                self.sim.csv_round_writer.update_metrics( tile_created=1)
        else:
            logging.info("Not created tile ")

    def create_tile_on(self, x=None, y=None, color=gray, alpha=1):
        """
        Creates a tile either on a given x,y coordinates

        :param x: x coordinate
        :param y: y coordinate
        :return: None
        """

        logging.info("particle with id %s is", self.get_id())
        if x is not None and y is not None:
            coords = (x, y)
            if self.sim.check_coords(x,y):
                logging.info("Going to create a tile on position \(%i , %i\)", x,y )
                if self.sim.add_tile(coords[0], coords[1], color, alpha) == True:
                    self.sim.tile_map_coords[coords[0], coords[1]].created = True
                    self.sim.new_tile_flag = True
                    self.csv_particle_writer.write_particle(tile_created=1)
                    self.sim.csv_round_writer.update_tiles_num(len(self.sim.get_tiles_list()) )
                    self.sim.csv_round_writer.update_metrics( tile_created=1)
                    return True
                else:
                    logging.info("Not created tile on coords  \(%i , %i\)", y,x )
                    return False
            else:
                logging.info("Not created tile on coords   \(%i , %i\)", y,x )

    def delete_tile(self):
        """
        Deletes a tile on current position

        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        logging.info("Particle %s is", self.get_id())
        logging.info("is going to delete a tile on current position")
        if self.coords in self.sim.get_tile_map_coords():
            if self.sim.remove_tile_on(self.coords):
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
        if self.sim.remove_tile(id):
            self.csv_particle_writer.write_particle(tile_deleted=1)
            return True
        else:
            logging.info("Could not delet tile with tile id %s", str(id))
            return False

    def delete_tile_in(self, dir=None):
        """
        Deletes a tile either in a given direction

        :param dir: The direction on which the tile should be deleted. Options: E, SE, SW, W, NW, NE,

        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        coords = ()
        if dir is not None:
            coords = self.sim.get_coords_in_dir(self.coords, dir)
            logging.info("Deleting tile in %s direction", str(dir))
            if coords is not None:
                if self.sim.remove_tile_on(coords):
                    logging.info("Deleted tile with tile on coords %s", str(coords))
                    self.csv_particle_writer.write_particle(tile_deleted=1)
                    return True
                else:
                    logging.info("Could not delet tile on coords %s", str(coords))
                    return False
        else:
            logging.info("Could not delet tile on coords %s", str(coords))
            return False

    def delete_tile_on(self, x=None, y=None):
        """
        Deletes a tile either on a given x,y coordinates
,
        :param x: x coordinate
        :param y: y coordinate
        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        coords = ()
        if x is not None and y is not None:
            coords = (x, y)
            if self.sim.remove_tile_on(coords):
                logging.info("Deleted tile with tile on coords %s", str(coords))
                self.csv_particle_writer.write_particle(tile_deleted=1)
                return True
            else:
                logging.info("Could not delet tile on coords %s", str(coords))
                return False
        else:
            logging.info("Could not delet tile on coords %s", str(coords))
            return False


    def take_tile(self):
        """
        Takes a tile on the actual position

        :param id:  The id of the tile that should be taken
        :return: True: successful taken; False: unsuccessful taken
        """
        if self.carried_particle is None and self.carried_tile is None:
            if self.coords in self.sim.tile_map_coords:
                self.carried_tile = self.sim.tile_map_coords[self.coords]
                if self.carried_tile.take(coords=self.coords):
                    logging.info("Tile has been taken")
                    self.sim.csv_round_writer.update_metrics( tiles_taken=1)
                    self.csv_particle_writer.write_particle(tiles_taken=1)
                    return True
                else:
                    logging.info("Tile could not be taken")
                    return False
            else:
                logging.info("No tile on the actual position not in the sim")
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
            if id in self.sim.tile_map_id:
                logging.info("Tile with tile id %s is in the sim", str(id))
                self.carried_tile = self.sim.tile_map_id[id]
                if self.carried_tile.take(coords=self.coords):
                    logging.info("Tile with tile id %s  has been taken", str(id))
                    self.sim.csv_round_writer.update_metrics( tiles_taken=1)
                    self.csv_particle_writer.write_particle(tiles_taken=1)
                    return True
                else:
                    logging.info("Tile with tile id %s could not be taken", str(id))
                    return False
            else:
                logging.info("Tile with tile id %s is not in the sim", str(id))
                return False
        else:
            logging.info("Tile cannot taken because particle is carrieng either a tile or a particle", str(id))
            return False

    def take_tile_in(self, dir):
        """
        Takes a tile that is in a given direction

        :param dir: The direction on which the tile should be taken. Options: E, SE, SW, W, NW, NE,
        :return: True: successful taken; False: unsuccessful taken
        """
        if self.carried_particle is None and self.carried_tile is None:
            coords = self.sim.get_coords_in_dir(self.coords, dir)
            if coords in self.sim.tile_map_coords:
                self.carried_tile = self.sim.tile_map_coords[coords]
                logging.info("Tile with tile id %s is in the sim", str(self.carried_tile.get_id()))
                if self.carried_tile.take(coords=self.coords):
                    logging.info("Tile with tile id %s  has been taken", str(self.carried_tile.get_id()))
                    self.sim.csv_round_writer.update_metrics( tiles_taken=1)
                    self.csv_particle_writer.write_particle(tiles_taken=1)
                    return True
                else:
                    logging.info("Tile with tile id %s could not be taken", str(self.carried_tile.get_id()))
                    return False
            else:
                logging.info("Tile is not in the sim")
                return False
        else:
            logging.info("Tile cannot taken because particle is carrieng either a tile or a particle")
            return False

    def take_tile_on(self, x=None, y=None):
        """
        Takes a tile that is in a given direction

        :param x: x coordinate
        :param y: y coordinate
        :return: True: successful taken; False: unsuccessful taken
        """
        if self.carried_particle is None and self.carried_tile is None:
            if self.sim.check_coords(x, y):
                coords = (x, y)
                if coords in self.sim.tile_map_coords:
                    self.carried_tile = self.sim.tile_map_coords[coords]
                    logging.info("Tile with tile id %s is in the sim", str(self.carried_tile.get_id()))
                    if self.carried_tile.take(coords=self.coords):
                        self.sim.csv_round_writer.update_metrics( tiles_taken=1)
                        self.csv_particle_writer.write_particle(tiles_taken=1)
                        logging.info("Tile with tile id %s  has been taken", str(self.carried_tile.get_id()))
                        return True
                    else:
                        logging.info("Tile with tile id %s could not be taken", str(self.carried_tile.get_id()))
                        return False
                else:
                    logging.info("Tile is not in the sim")
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
            if self.coords not in self.sim.tile_map_coords:
                try:  # cher: insert so to overcome the AttributeError
                    self.carried_tile.drop_me(self.coords)
                except AttributeError:
                    pass
                self.carried_tile = None
                logging.info("Tile has been dropped on the actual position")
                self.sim.csv_round_writer.update_metrics( tiles_dropped=1)
                self.csv_particle_writer.write_particle(tiles_dropped=1)
                return True
            else:
                logging.info("Is not possible to drop the tile on that position because it is occupied")
                return False
        else:
            return False

    def drop_tile_in(self, dir):
        """
        Drops the taken tile on a given direction

         :param dir: The direction on which the tile should be dropped. Options: E, SE, SW, W, NW, NE,
        """
        if self.carried_tile is not None:
            coords = self.sim.get_coords_in_dir(self.coords, dir)
            if coords not in self.sim.tile_map_coords:
                try:  # cher: insert so to overcome the AttributeError
                    self.carried_tile.drop_me(coords)
                except AttributeError:
                    pass
                self.carried_tile = None
                self.sim.csv_round_writer.update_metrics( tiles_dropped=1)
                self.csv_particle_writer.write_particle(tiles_dropped=1)
                logging.info("Dropped tile on %s coordinate", str(coords))
                return True
            else:
                logging.info("Is not possible to drop the tile on that position")
                return False

        else:
            logging.info("No tile taken for dropping")
            return False

    def drop_tile_on(self, x=None, y=None):
        """
        Drops the taken tile on a given direction

        :param x: x coordinate
        :param y: y coordinate
        """
        if self.carried_tile is not None:
            if self.sim.check_coords(x, y):
                coords = (x, y)
                if coords not in self.sim.get_tile_map_coords():
                    try:  # cher: insert so to overcome the AttributeError
                        self.carried_tile.drop_me(coords)
                    except AttributeError:
                        pass
                    self.carried_tile = None
                    self.sim.csv_round_writer.update_metrics( tiles_dropped=1)
                    self.csv_particle_writer.write_particle(tiles_dropped=1)
                    logging.info("Dropped tile on %s coordinate", str(coords))
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

    def create_particle(self, color=black, alpha=1):
        """
        Creates a particle on the particles actual position

        :return: None
        """
        logging.info("Going to create on position %s", str(self.coords))
        self.sim.add_particle(self.coords[0], self.coords[1], color, alpha)
        self.sim.particle_map_coords[self.coords[0], self.coords[1]].created=True
        self.csv_particle_writer.write_particle(particle_created=1)
        self.sim.csv_round_writer.update_particle_num(len(self.sim.get_particle_list()))
        self.sim.csv_round_writer.update_metrics( particle_created=1)

    def create_particle_in(self, dir=None, color=black, alpha=1):
        """
        Creates a particle either in a given direction

        :toDo: seperate the direction and coordinates and delete state

        :param dir: The direction on which the particle should be created. Options: E, SE, SW, W, NW, NE,
        :return: None
        """
        coords = (0, 0)
        if dir is not None:
            coords = self.sim.get_coords_in_dir(self.coords, dir)
            logging.info("Going to create a particle in %s on position %s", str(dir), str(coords))
            if self.sim.add_particle(coords[0], coords[1], color, alpha) == True:
                self.sim.particle_map_coords[coords[0], coords[1]].created = True
                logging.info("Created particle on coords %s", coords)
                self.sim.csv_round_writer.update_particle_num(len(self.sim.get_particle_list()))
                self.sim.csv_round_writer.update_metrics( particle_created=1)
                self.csv_particle_writer.write_particle(particle_created=1)
        else:
            logging.info("Not created particle on coords %s", str(coords))

    def create_particle_on(self, x=None, y=None, color=black, alpha=1):
        """
        Creates a particle either on a given x,y coordinates

        :toDo: seperate the direction and coordinates and delete state

        :param x: x coordinate
        :param y: y coordinate
        :return: None
        """
        coords = (0, 0)
        if x is not None and y is not None:
            if self.sim.check_coords(x, y):
                coords = (x, y)
                logging.info("Going to create a particle on position %s", str(coords))
                if self.sim.add_particle(coords[0], coords[1], color, alpha) == True:
                    self.sim.particle_map_coords[coords[0], coords[1]].created = True
                    logging.info("Created particle on coords %s", str(coords))
                    self.sim.csv_round_writer.update_particle_num(len(self.sim.get_particle_list()))
                    self.sim.csv_round_writer.update_metrics( particle_created=1)
                    self.csv_particle_writer.write_particle(particle_created=1)
                    return True
                else:
                    return False
            else:
                return False
        else:
            logging.info("Not created particle on coords %s", str(coords))
            return False

    def delete_particle(self):
        """
        Deletes a tile on current position

        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        logging.info("Particle %s is", self.get_id())
        logging.info("is going to delete a particle on current position")
        if self.coords in self.sim.get_particle_map_coords():
            if self.sim.remove_particle_on(self.coords):
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
        if self.sim.remove_particle(id):
            self.csv_particle_writer.write_particle(particle_deleted=1)
            return
        else:
            logging.info("Could not delet particle with particle id %s", str(id))

    def delete_particle_in(self, dir=None):
        """
        Deletes a particle either in a given direction

        :param dir: The direction on which the particle should be deleted. Options: E, SE, SW, W, NW, NE,
        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        if dir is not None:
            coords = self.sim.get_coords_in_dir(self.coords, dir)
            logging.info("Deleting tile in %s direction", str(dir))
            if self.sim.remove_particle_on(coords):
                logging.info("Deleted particle with particle on coords %s", str(coords))
                self.csv_particle_writer.write_particle(particle_deleted=1)
            else:
                logging.info("Could not delet particle on coords %s", str(coords))

    def delete_particle_on(self, x=None, y=None):
        """
        Deletes a particle either on a given x,y coordinates

        :param x: x coordinate
        :param y: y coordinate
        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        if x is not None and y is not None:
            if self.sim.check_coords(x, y):
                coords = (x, y)
                if self.sim.remove_particle_on(coords):
                    logging.info("Deleted particle with particle on coords %s", str(coords))
                    self.csv_particle_writer.write_particle(particle_deleted=1)
                    return True
                else:
                    logging.info("Could not delet particle on coords %s", str(coords))
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
            if self.coords in self.sim.particle_map_coords:
                self.carried_particle = self.sim.particle_map_coords[self.coords]
                if self.carried_particle.take_me(coords=self.coords):
                    logging.info("particle has been taken")
                    self.sim.csv_round_writer.update_metrics( particles_taken=1)
                    self.csv_particle_writer.write_particle(particles_taken=1)
                    return True
                else:
                    logging.info("particle could not be taken")
                    return False
            else:
                logging.info("No particle on the actual position not in the sim")
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
            if id in self.sim.get_particle_map_id():
                logging.info("particle with particle id %s is in the sim", str(id))
                self.carried_particle = self.sim.particle_map_id[id]
                if self.carried_particle.take_me(self.coords):
                    logging.info("particle with particle id %s  has been taken", str(id))

                    self.sim.csv_round_writer.update_metrics(
                                                               particles_taken=1)
                    self.csv_particle_writer.write_particle(particles_taken=1)
                    return True
                else:
                    logging.info("particle with particle id %s could not be taken", str(id))
                    return False
            else:
                logging.info("particle with particle id %s is not in the sim", str(id))
        else:
            logging.info("particle cannot taken because particle is carrieng either a particle or a particle", str(id))

    def take_particle_in(self, dir):
        """
        Takes a particle that is in a given direction

        :param dir: The direction on which the particle should be taken. Options: E, SE, SW, W, NW, NE,
        :return: True: successful taken; False: unsuccessful taken
        """
        if self.carried_tile is None and self.carried_particle is None:
            coords = self.sim.get_coords_in_dir(self.coords, dir)
            if coords in self.sim.particle_map_coords:
                logging.info("Take particle")
                self.carried_particle = self.sim.particle_map_coords[coords]
                if self.carried_particle.take_me(coords=self.coords):
                    logging.info("particle with particle id %s  has been taken", str(self.carried_particle.get_id()))
                    self.sim.csv_round_writer.update_metrics(
                                                               particles_taken=1)
                    self.csv_particle_writer.write_particle(particles_taken=1)
                    return True
                else:
                    logging.info("particle could not be taken")
                    return False
            else:
                logging.info("particl is not in the sim")
        else:
            logging.info("particle cannot be  taken")

    def take_particle_on(self, x=None, y=None):
        """
        Takes the particle on the given coordinate if it is not taken

        :param y:
        :param x:
        :return: True: Successful taken; False: Cannot be taken or wrong Coordinates
        """
        if self.carried_particle is None and self.carried_tile is None:
            if self.sim.check_coords(x, y):
                coords = (x, y)
                if coords in self.sim.particle_map_coords:
                    self.carried_particle = self.sim.particle_map_coords[coords]
                    logging.info("Particle with id %s is in the sim", str(self.carried_particle.get_id()))
                    if self.carried_particle.take_me(coords=self.coords):
                        self.sim.csv_round_writer.update_metrics( particles_taken=1)
                        self.csv_particle_writer.write_particle(particles_taken=1)
                        logging.info("particle with tile id %s has been taken", str(self.carried_particle.get_id()))
                        return True
                    else:
                        logging.info("Particle with id %s could not be taken", str(self.carried_particle.get_id()))
                        return False
                else:
                    logging.info("Particle is not in the sim")
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
            if self.coords not in self.sim.particle_map_coords:
                try:  # cher: insert so to overcome the AttributeError
                    self.carried_particle.drop_me(self.coords)
                except AttributeError:
                    pass
            self.carried_particle = None
            self.sim.csv_round_writer.update_metrics( particles_dropped=1)
            self.csv_particle_writer.write_particle(particles_dropped=1)
            logging.info("Particle succesfull dropped")
            return True
        else:
            logging.info("No particle taken to drop")
            return False

    def drop_particle_in(self, dir):
        """
        Drops the particle tile in a given direction

         :param dir: The direction on which the particle should be dropped. Options: E, SE, SW, W, NW, NE,
        """
        if self.carried_particle is not None:
            coords = self.sim.get_coords_in_dir(self.coords, dir)
            if coords not in self.sim.particle_map_coords:
                try:  # cher: insert so to overcome the AttributeError
                    self.carried_particle.drop_me(coords)
                except AttributeError:
                    pass
                    self.carried_particle = None
                    logging.info("Dropped particle on %s coordinate", str(coords))
                    self.sim.csv_round_writer.update_metrics( particles_dropped=1)
                    self.csv_particle_writer.write_particle(particles_dropped=1)
                    return True
                else:
                    logging.info("Is not possible to drop the particle on that position")
                    return False
            else:
                logging.info("Is not possible to drop the particle on that position because it is occupied")
                return False
        else:
            logging.info("No particle taken to drop")
            return False

    def drop_particle_on(self, x=None, y=None):
        """
        Drops the particle tile on a given x and y coordination

        :param x: x coordinate
        :param y: y coordinate
        """
        if self.carried_particle is not None:
            if x is not None and y is not None:
                if self.sim.check_coords(x, y):
                    coords = (x, y)
                    if coords not in self.sim.particle_map_coords:
                        try:  # cher: insert so to overcome the AttributeError
                            self.carried_particle.drop_me(coords)
                        except AttributeError:
                            pass
                        self.carried_particle = None
                        logging.info("Dropped particle on %s coordinate", str(coords))
                        self.sim.csv_round_writer.update_metrics(
                                                                   particles_dropped=1)
                        self.csv_particle_writer.write_particle(particles_dropped=1)
                        return True
                    else:
                        logging.info("Is not possible to drop the particle on that position  because it is occupied")
                        return False
                else:
                    logging.info("Wrong coordinates for dropping particle")
                    return False
            else:
                logging.info("No coordinates for dropping particle")
                return False
        else:
            logging.info("No particle taken to drop")
            return False

    def update_particle_coords(self, particle, new_coords):
        """
        Upadting the particle with new coordinates
        Only necessary for taking and moving particles

        :param particle: The particle object
        :param new_coords: new coorindation points
        :return: None
        """
        particle.coords = new_coords
        self.particle_map_coords[new_coords] = particle

    def create_location(self, color=black, alpha=1):
        """
         Creates a location on the particles actual position

        :return: None
        """

        logging.info("Going to create on position %s", str(self.coords))
        new_location=self.sim.add_location(self.coords[0], self.coords[1], color, alpha)
        if new_location != False:
            self.csv_particle_writer.write_particle(location_created=1)
            self.sim.csv_round_writer.update_locations_num(len(self.sim.get_location_list()))
            self.sim.csv_round_writer.update_metrics( location_created=1)
            return  new_location
        else:
            return False

    def create_location_in(self, dir=None, color=black, alpha=1):
        """
        Creates a location either in a given direction

        :param dir: The direction on which the location should be created. Options: E, SE, SW, W, NW, NE,

        """
        coords = (0, 0)
        if dir is not None:
            coords = self.sim.get_coords_in_dir(self.coords, dir)
            logging.info("Going to create a location in %s on position %s", str(dir), str(coords))
            if self.sim.add_location(coords[0], coords[1], color, alpha) == True:
                logging.info("Created location on coords %s", str(coords))
                self.sim.csv_round_writer.update_locations_num(len(self.sim.get_location_list()))
                self.sim.csv_round_writer.update_metrics( location_created=1)
                return True
            else:
                return False
        else:
            logging.info("Not created location on coords %s", str(coords))
            return False

    def create_location_on(self, x=None, y=None, color=black, alpha=1):
        """
        Creates a location either on a given x,y coordinates

        :param x: x coordinate
        :param y: y coordinate
        :return: None

        """
        coords = (0, 0)
        if x is not None and y is not None:
            if self.sim.check_coords(x, y):
                coords = (x, y)
                logging.info("Going to create a location on position %s", str(coords))
                if self.sim.add_location(coords[0], coords[1], color, alpha) == True:
                    logging.info("Created location on coords %s", str(coords))
                    self.sim.csv_round_writer.update_locations_num(len(self.sim.get_location_list()))
                    self.sim.csv_round_writer.update_metrics( location_created=1)
                    return True
            else:
                return False
        else:
            logging.info("Not created location on coords %s", str(coords))
            return False

    def delete_location(self):
        """
        Deletes a location on current position

        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        logging.info("Particle %s is", self.get_id())
        logging.info("is going to delete a location on current position")
        if self.coords in self.sim.get_location_map_coords():
            if self.sim.remove_location_on(self.coords):
                self.csv_particle_writer.write_particle(location_deleted=1)
                return True
        else:
            logging.info("Could not delet location")
            return False

    def delete_location_with(self, location_id):
        """
        Deletes a location with a given location-id

        :param location_id: The id of the location that should be deleted
        :return: True: Deleting successful; False: Deleting unsuccessful
        """

        logging.info("location %s is", self.get_id())
        logging.info("is going to delete a location with id %s", str(location_id))
        if self.sim.remove_location(location_id):
            self.csv_particle_writer.write_particle(location_deleted=1)
            return
        else:
            logging.info("Could not delet location with location id %s", str(location_id))

    def delete_location_in(self, dir=None):
        """
        Deletes a location either in a given direction or on a given x,y coordinates

        :param dir: The direction on which the location should be deleted. Options: E, SE, SW, W, NW, NE,
        :param x: x coordinate
        :param y: y coordinate
        :return: True: Deleting successful; False: Deleting unsuccessful
        """

        if dir is not None:
            coords = self.sim.get_coords_in_dir(self.coords, dir)
            logging.info("Deleting tile in %s direction", str(dir))
            if self.sim.remove_location_on(coords):
                logging.info("Deleted location with location on coords %s", str(coords))
                self.csv_particle_writer.write_particle(location_deleted=1)
            else:
                logging.info("Could not delet location on coords %s", str(coords))

    def delete_location_on(self, x=None, y=None):
        """
        Deletes a particle either on a given x,y coordinates

        :param x: x coordinate
        :param y: y coordinate
        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        if x is not None and y is not None:
            if self.sim.check_coords(x, y):
                coords = (x, y)
                if self.sim.remove_location_on(coords):
                    logging.info("Deleted location  oords %s", str(coords))
                    self.csv_particle_writer.write_particle(location_deleted=1)
                    return True
                else:
                    logging.info("Could not delet location on coords %s", str(coords))
                    return False
            else:
                return False
        else:
            return False

