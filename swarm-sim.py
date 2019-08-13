"""This is the main module of the Opportunistic Robotics Network Simulator"""

import importlib
import configparser
import getopt
import logging
import os
import sys
from datetime import datetime
from lib import world
from lib.gnuplot_generator import gnuplot_generator


class ConfigData:

    def __init__(self, config):
        self.seed_value = config.getint("Simulator", "seedvalue")
        self.max_round = config.getint("Simulator", "max_round")
        self.random_order = config.getboolean("Simulator", "random_order")
        self.visualization = config.getint("Simulator", "visualization")
        try:
            self.scenario = config.get("File", "scenario")
        except (configparser.NoOptionError) as noe:
            self.scenario = "init_scenario.py"

        try:
            self.solution = config.get("File", "solution")
        except (configparser.NoOptionError) as noe:
            self.solution = "solution.py"
        self.size_x = config.getfloat("Simulator", "size_x")
        self.size_y = config.getfloat("Simulator", "size_y")
        self.window_size_x = config.getint("Simulator", "window_size_x")
        self.window_size_y = config.getint("Simulator", "window_size_y")
        self.border = config.getfloat("Simulator", "border")
        self.max_particles = config.getint("Simulator", "max_particles")
        self.mm_limitation = config.getboolean("Matter", "mm_limitation")
        self.particle_mm_size = config.getint("Matter", "particle_mm_size")
        self.tile_mm_size = config.getint("Matter", "tile_mm_size")
        self.marker_mm_size = config.getint("Matter", "marker_mm_size")
        self.local_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')[:-1]
        self.multiple_sim = 0


def swarm_sim( argv ):
    """In the main function first the config is getting parsed and than
    the swarm_world and the swarm_world object is created. Afterwards the run method of the swarm_world
    is called in which the simlator is going to start to run"""
    logging.basicConfig(filename='system.log', filemode='w', level=logging.INFO, format='%(message)s')
    logging.info('Started')

    config_data = init_swarm_sim(argv)

    swarm_world = world.World(config_data)

    while swarm_world.get_actual_round() <= swarm_world.get_max_round() and swarm_world.get_end() is False:
        solution(swarm_world)
        if config_data.visualization and swarm_world.window.window_active is False:
            break
    swarm_world.csv_aggregator()
    gnuplot_generator(config_data.dir_name)
    logging.info('Finished')


def init_swarm_sim(argv):
    config_data = read_config_file()
    read_cmd_args(argv, config_data)
    create_dir(config_data)
    return config_data


def read_config_file():
    config = configparser.ConfigParser(allow_no_value=True)
    config.read("config.ini")
    config_data = ConfigData(config)
    return config_data


def create_dir(config_data):
    if config_data.multiple_sim == 1:
        config_data.dir_name = config_data.local_time + "_" + config_data.scenario.rsplit('.', 1)[0] + \
                               "_" + config_data.solution.rsplit('.', 1)[0] + "/" + \
                               str(config_data.seed_value)

        config_data.dir_name = "./outputs/mulitple/" + config_data.dir_name

    else:
        config_data.dir_name = config_data.local_time + "_" + config_data.scenario.rsplit('.', 1)[0] + \
                               "_" + config_data.solution.rsplit('.', 1)[0] + "_" + \
                               str(config_data.seed_value)
        config_data.dir_name = "./outputs/" + config_data.dir_name
    if not os.path.exists(config_data.dir_name):
        os.makedirs(config_data.dir_name)


def solution(swarm_world):
    if swarm_world.config_data.visualization:
        swarm_world.window.draw_world()
    mod = importlib.import_module('solution.' + swarm_world.config_data.solution)
    mod.solution(swarm_world)
    swarm_world.csv_round.next_line(swarm_world.get_actual_round())
    swarm_world.inc_round_cnter()


def read_cmd_args(argv, config_data):
    try:
        opts, args = getopt.getopt(argv, "hs:w:r:n:m:d:v:", ["solution=", "scenario="])
    except getopt.GetoptError:
        print('Error: swarm-swarm_world.py -r <seed> -w <scenario> -s <solution> -n <maxRounds>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('swarm-swarm_world.py -r <seed> -w <scenario> -s <solution> -n <maxRounds>')
            sys.exit()
        elif opt in ("-s", "--solution"):
            config_data.solution = arg
        elif opt in ("-w", "--scenario"):
            config_data.scenario = arg
        elif opt in ("-r", "--seed"):
            config_data.seed_value = int(arg)
        elif opt in ("-n", "--maxrounds"):
            config_data.max_round = int(arg)
        elif opt in "-m":
            config_data.multiple_sim = int(arg)
        elif opt in "-v":
            config_data.visualization = int(arg)
        elif opt in "-d":
            config_data.local_time = str(arg)


if __name__ == "__main__":
    swarm_sim(sys.argv[1:])

