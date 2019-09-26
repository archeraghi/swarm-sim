"""The marker module provides the interface to the markers. A marker is any point on
 the coordinate system of the simulators world"""
import uuid
from datetime import datetime
from lib.swarm_sim_header import *


class Matter:
    """In the classe marker all the methods for the characterstic of a marker is included"""
    def __init__(self, world, coordinates, color=black, transparency=1, type=None, mm_size=100):
        """Initializing the marker constructor"""
        self.coordinates = coordinates
        self.color = color_map[color]
        self.__id = str(uuid.uuid4())
        self.world = world
        self._memory={}
        self.__transparency=transparency
        self.type = type
        self.memory_limitation = world.config_data.memory_limitation
        self.mm_size = mm_size
        self.modified = False
        self.created = False

    def set_transparency(self, transparency):
        """
        Set the transparency value of the particle

        :param transparency: The transparency of the particle
        :return: None
        """
        if (0 <= transparency <= 1):
            self.__transparency = round(transparency,2)
        elif transparency < 0:
            self.__transparency = 0
        elif transparency > 1:
            self.__transparency = 1
        self.touch()

    def get_transparency(self):
        """
        Returns the transparency value of the particle

        :return: transparency
        """
        return round(self.__transparency,2)

    def read_memory_with(self, key):
        """
        Read all its own memory based on a give keywoard

        :param key: Keywoard
        :return: The founded memory; None: When nothing is written based on the keywoard
        """
        tmp_memory = None
        if key in self._memory:
            tmp_memory = self._memory[key]
            self.world.csv_round.update_metrics( memory_read=1)
        if isinstance(tmp_memory, list) and len(str(tmp_memory)) == 0:
            return None
        if isinstance(tmp_memory, str) and len(str(tmp_memory)) == 0:
            return None
        return tmp_memory

    def read_whole_memory(self):
        """
        Reads all  markers own memory based on a give keywoard

        :param key: Keywoard
        :return: The founded memory; None: When nothing is written based on the keywoard
        """
        if self._memory != None :
            self.world.csv_round.update_metrics(memory_read=1)
            return self._memory
        else:
            return None

    def write_memory_with(self, key, data):
        """
        Write on its own memory a data with a keywoard

        :param key: A string keyword for orderring the data into the memory
        :param data: The data that should be stored into the memory
        :return: True: Successful written into the memory; False: Unsuccessful
        """

        if (self.memory_limitation == True and len( self._memory) < self.mm_size) or not self.memory_limitation:
            self._memory[key] = data
            self.world.csv_round.update_metrics(memory_write=1)
            return True
        else:
            return False
            #write csv

    def write_memory(self, data):
        """
        Write on its own memory a data with a keywoard

        :param key: A string keyword for orderring the data into the memory
        :param data: The data that should be stored into the memory
        :return: True: Successful written into the memory; False: Unsuccessful
        """

        if (self.memory_limitation == True and len( self._memory) < self.mm_size) or not self.memory_limitation:
                self._memory[datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-1]] = data
                self.world.csv_round.update_metrics(memory_write=1)
                return True
        else:
            return False
            #write csv

    def delete_memeory_with(self, key):
        del self._memory[key]

    def delete_whole_memeory(self):
         self._memory.clear()

    def get_id(self):
        """
        Gets the marker id
        :return: marker id
        """
        return self.__id

    def set_color(self, color):
        """
        Sets the marker color

        :param color: marker color
        :return: None
        """
        if type (color) == int:
            self.color = color_map[color]
        else:
            self.color = color
        self.touch()

    def get_color(self):
        """
        Sets the marker color

        :param color: marker color
        :return: None
        """
        for color, code in color_map.items():    # for name, age in dictionary.iteritems():  (for Python 2.x)
         if code == self.color:
           return(color)

    def touch(self):
        """Tells the visualization that something has been modified and that it shoud changed it"""
        self.modified = True

    def untouch(self):
        """Tells the visualization that something has been modified and that it shoud changed it"""
        self.modified = False

