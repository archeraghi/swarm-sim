"""The marker module provides the interface to the markers. A marker is any point on
 the coordinate system of the simulators sim"""


import uuid
import logging
from datetime import datetime


black = 1
gray = 2
red = 3
green = 4
blue = 5
yellow = 6
orange = 7
cyan = 8
violett = 9

color_map = {
    black: [0.0, 0.0, 0.0],
    gray: [0.3, 0.3, 0.3],
    red: [0.8, 0.0, 0.0],
    green: [0.0, 0.8, 0.0],
    blue: [0.0, 0.0, 0.8],
    yellow: [0.8, 0.8, 0.0],
    orange: [0.8, 0.3, 0.0],
    cyan: [0.0, 0.8, 0.8],
    violett: [0.8, 0.2, 0.6]
}


class Matter():
    """In the classe marker all the methods for the characterstic of a marker is included"""

    def __init__(self, sim, coords, color=black, alpha=1, type=None, mm_size=100):
        """Initializing the marker constructor"""
        self.coords = coords
        self.color = color_map[color]
        self.__id = str(uuid.uuid4())
        self.memory_delay_time=3
        self.memory_delay=True
        self.memory_buffer=[]
        self._tmp_memory=[]
        self.sim = sim
        self._memory={}
        self.__modified=False
        self.__alpha=alpha
        self.type = type
        self.mm_limit = sim.config_data.mm_limitation
        self.mm_size = mm_size

    def set_alpha(self, alpha):
        """
        Set the alpha value of the particle

        :param alpha: The alpha of the particle
        :return: None
        """
        if (0 <= alpha <= 1):
            self.__alpha = round(alpha,2)
        elif alpha < 0:
            self.__alpha = 0
        elif alpha > 1:
            self.__alpha = 1
        self.touch()
    def get_alpha(self):
        """
        Returns the alpha value of the particle

        :return: alpha
        """
        return round(self.__alpha,2)

    def read_memory_with(self, key):
        """
        Read all its own memory based on a give keywoard

        :param key: Keywoard
        :return: The founded memory; None: When nothing is written based on the keywoard
        """
        tmp_memory = None
        # if self.memory_delay == True:
        #     for key in self._tmp_memory:
        #         if key ==
        if key in self._memory:
            tmp_memory = self._memory[key]
            self.sim.csv_round_writer.update_metrics( memory_read=1)
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
            self.sim.csv_round_writer.update_metrics(memory_read=1)
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

        if (self.mm_limit == True and len( self._memory) < self.mm_size) or not self.mm_limit:
            self._memory[key] = data
            self.sim.csv_round_writer.update_metrics(memory_write=1)
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

        if (self.mm_limit == True and len( self._memory) < self.mm_size) or not self.mm_limit:
                self._memory[datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-1]] = data
                self.sim.csv_round_writer.update_metrics(memory_write=1)
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

