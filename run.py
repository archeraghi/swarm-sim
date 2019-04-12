"""This is the main module of the Opportunistic Robotics Network Simulator"""


import configparser
import getopt
import logging
import os
import sys
from datetime import datetime

from lib import  sim

class ConfigData():

    def __init__(self, config):
        self.seedvalue = config.getint("Simulator", "seedvalue")
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
        self.size_x = config.getint("Simulator", "size_x")
        self.size_y = config.getint("Simulator", "size_y")
        self.window_size_x = config.getint("Simulator", "window_size_x")
        self.window_size_y = config.getint("Simulator", "window_size_y")
        self.border = config.getint("Simulator", "border")
        self.max_particles = config.getint("Simulator", "max_particles")
        self.mm_limitation = config.getboolean("Matter", "mm_limitation")
        self.particle_mm_size = config.getint("Matter", "particle_mm_size")
        self.tile_mm_size = config.getint("Matter", "tile_mm_size")
        self.location_mm_size = config.getint("Matter", "location_mm_size")
        self.dir_name = None
def swarm_sim( argv ):
    """In the main function first the config is getting parsed and than
    the simulator and the sim object is created. Afterwards the run method of the simulator
    is called in which the simlator is going to start to run"""
    config = configparser.ConfigParser(allow_no_value=True)

    config.read("config.ini")
    config_data=ConfigData(config)

    multiple_sim=0
    local_time = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')[:-1]
    try:
        opts, args = getopt.getopt(argv, "hs:w:r:n:m:d:v:", ["solution=", "scenario="])
    except getopt.GetoptError:
        print('Error: run.py -r <randomeSeed> -w <scenario> -s <solution> -n <maxRounds>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('run.py -r <randomeSeed> -w <scenario> -s <solution> -n <maxRounds>')
            sys.exit()
        elif opt in ("-s", "--solution"):
            config_data.solution = arg
        elif opt in ("-w", "--scenario"):
            config_data.scenario = arg
        elif opt in ("-r", "--seed"):
            config_data.seedvalue = int(arg)
        elif opt in ("-n", "--maxrounds"):
           config_data.max_round = int(arg)
        elif opt in ("-m"):
           multiple_sim = int(arg)
        elif opt in ("-v"):
            config_data.visualization = int(arg)
        elif opt in ("-d"):
            local_time = str(arg)


    #logging.basicConfig(filename='myapp.log', filemode='w', level=logging.INFO, format='%(asctime)s %(message)s')
    logging.basicConfig(filename='system.log', filemode='w', level=logging.INFO, format='%(message)s')


    if multiple_sim == 1:
        config_data.dir_name= local_time + "_" + config_data.scenario.rsplit('.', 1)[0] + \
               "_" + config_data.solution.rsplit('.', 1)[0] + "/" + \
               str(config_data.seedvalue)

        config_data.dir_name = "./outputs/mulitple/"+ config_data.dir_name

    else:
        config_data.dir_name= local_time + "_" + config_data.scenario.rsplit('.', 1)[0] + \
               "_" + config_data.solution.rsplit('.', 1)[0] + "_" + \
               str(config_data.seedvalue)
        config_data.dir_name = "./outputs/" + config_data.dir_name
    if not os.path.exists(config_data.dir_name):
        os.makedirs(config_data.dir_name)

    logging.info('Started')
    simulator = sim.Sim( config_data )
    simulator.run()
    logging.info('Finished')


if __name__ == "__main__":
    swarm_sim(sys.argv[1:])

