import configparser
from datetime import datetime


class ConfigData:

    def __init__(self):
        config = configparser.ConfigParser(allow_no_value=True)
        config.read("config.ini")
        self.seed_value = config.getint("Simulator", "seedvalue")
        self.max_round = config.getint("Simulator", "max_round")
        self.particle_random_order = config.getboolean("Simulator", "particle_random_order")
        self.visualization = config.getint("Simulator", "visualization")
        self.window_size_x = config.getint("Simulator", "window_size_x")
        self.window_size_y = config.getint("Simulator", "window_size_y")

        self.size_x = config.getfloat("World", "size_x")
        self.size_y = config.getfloat("World", "size_y")
        self.border = config.getboolean("World", "border")
        self.max_particles = config.getint("World", "max_particles")

        self.memory_limitation = config.getboolean("Matter", "memory_limitation")
        self.particle_mm_size = config.getint("Matter", "particle_mm_size")
        self.tile_mm_size = config.getint("Matter", "tile_mm_size")
        self.marker_mm_size = config.getint("Matter", "marker_mm_size")

        try:
            self.scenario = config.get("File", "scenario")
        except configparser.NoOptionError as noe:
            self.scenario = "init_scenario.py"

        try:
            self.solution = config.get("File", "solution")
        except configparser.NoOptionError as noe:
            self.solution = "solution.py"

        self.local_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')[:-1]
        self.multiple_sim = 0
