import configparser
from datetime import datetime
from ast import literal_eval as make_tuple
import importlib


class ConfigData:

    def __init__(self):
        config = configparser.ConfigParser(allow_no_value=True)
        config.read("config.ini")
        self.directory_name = ""
        self.seed_value = config.getint("Simulator", "seedvalue")
        self.max_round = config.getint("Simulator", "max_round")
        self.particle_random_order = config.getboolean("Simulator", "particle_random_order")
        self.particle_random_order_always = config.getboolean("Simulator", "particle_random_order_always")
        self.window_size_x = config.getint("Simulator", "window_size_x")
        self.window_size_y = config.getint("Simulator", "window_size_y")
        self.close_at_end = config.getboolean("Simulator", "close_at_end")

        self.visualization = config.getint("Visualization", "visualization")
        try:
            self.gui = config.get("Visualization", "gui")
        except configparser.NoOptionError:
            print("no gui option given. setting to default \"gui.py\"")
            self.gui = "gui.py"

        try:
            self.grid_class = config.get("Visualization", "grid_class")
        except configparser.NoOptionError:
            raise RuntimeError("Fatal Error: no grid class defined in config.ini!")

        try:
            self.grid_size = config.getint("Visualization", "grid_size")
        except configparser.NoOptionError:
            raise RuntimeError("Fatal Error: no grid size defined in config.ini!")

        test = getattr(importlib.import_module("grids.%s" % self.grid_class), self.grid_class)
        self.grid = test(self.grid_size)

        self.particle_model_file = config.get("Visualization", "particle_model_file")
        self.tile_model_file = config.get("Visualization", "tile_model_file")
        self.location_model_file = config.get("Visualization", "location_model_file")

        self.particle_color = make_tuple(config.get("Visualization", "particle_color"))
        self.tile_color = make_tuple(config.get("Visualization", "tile_color"))
        self.location_color = make_tuple(config.get("Visualization", "location_color"))
        self.particle_scaling = make_tuple(config.get("Visualization", "particle_scaling"))
        self.tile_scaling = make_tuple(config.get("Visualization", "tile_scaling"))
        self.location_scaling = make_tuple(config.get("Visualization", "location_scaling"))
        self.grid_color = make_tuple(config.get("Visualization", "grid_color"))
        self.cursor_color = make_tuple(config.get("Visualization", "cursor_color"))
        self.background_color = make_tuple(config.get("Visualization", "background_color"))
        self.center_color = make_tuple(config.get("Visualization", "center_color"))
        self.line_color = make_tuple(config.get("Visualization", "line_color"))
        self.line_scaling = make_tuple(config.get("Visualization", "line_scaling"))
        self.show_lines = config.getboolean("Visualization", "show_lines")
        self.coordinates_color = make_tuple(config.get("Visualization", "coordinates_color"))
        self.coordinates_scaling = make_tuple(config.get("Visualization", "coordinates_scaling"))
        self.show_coordinates = config.getboolean("Visualization", "show_coordinates")
        self.show_center = config.getboolean("Visualization", "show_center")
        self.focus_color = make_tuple(config.get("Visualization", "focus_color"))
        self.show_focus = config.getboolean("Visualization", "show_focus")

        self.look_at = make_tuple(config.get("Visualization", "look_at"))
        self.phi = config.getint("Visualization", "phi")
        self.theta = config.getint("Visualization", "theta")
        self.radius = config.getint("Visualization", "radius")
        self.fov = config.getint("Visualization", "fov")
        self.cursor_offset = config.getint("Visualization", "cursor_offset")
        self.render_distance = config.getint("Visualization", "render_distance")

        self.show_border = config.getboolean("Visualization", "show_border")
        self.border_color = make_tuple(config.get("Visualization", "border_color"))

        self.animation = config.getboolean("Visualization", "animation")
        self.auto_animation = config.getboolean("Visualization", "auto_animation")
        self.manual_animation_speed = config.getint("Visualization", "manual_animation_speed")

        self.size_x = config.getfloat("World", "size_x")
        self.size_y = config.getfloat("World", "size_y")
        self.size_z = config.getfloat("World", "size_z")
        self.border = config.getboolean("World", "border")
        self.type = config.getboolean("World", "type")
        self.max_particles = config.getint("World", "max_particles")

        self.memory_limitation = config.getboolean("Matter", "memory_limitation")
        self.particle_mm_size = config.getint("Matter", "particle_mm_size")
        self.tile_mm_size = config.getint("Matter", "tile_mm_size")
        self.location_mm_size = config.getint("Matter", "location_mm_size")

        try:
            self.scenario = config.get("File", "scenario")
        except configparser.NoOptionError:
            self.scenario = "init_scenario.py"

        try:
            self.solution = config.get("File", "solution")
        except configparser.NoOptionError:
            self.solution = "solution.py"

        self.local_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')[:-1]
        self.multiple_sim = 0
