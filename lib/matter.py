
import uuid
from datetime import datetime

from lib.swarm_sim_header import eprint


class Matter:
    def __init__(self, world, coordinates, color, type=None, mm_size=100):
        """Initializing the matter constructor"""
        self.coordinates = coordinates
        self.color = color
        self.__id = str(uuid.uuid4())
        self.world = world
        self._memory = {}
        self.type = type
        self.memory_limitation = world.config_data.memory_limitation
        self.mm_size = mm_size
        self.created = False

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
        Reads all  matters own memory based on a give keywoard

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
        Gets the matter id
        :return: matter id
        """
        return self.__id

    def set_color(self, color: tuple):
        """
        Sets the matter color

        :param color: matter color
        :return: None
        """
        if len(color) != 4:
            eprint("invalid color format!\ncolor has to be in rgba format => (float, float, float, float)")
        else:
            self.color = color

    def get_color(self):
        """
        :return: color
        """
        return self.color
