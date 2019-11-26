"""This is the main module of the Opportunistic Robotics Network Simulator"""
import importlib
import getopt
import logging
import os
import sys
import time
import random
from lib import world, config
from lib.gnuplot_generator import gnuplot_generator


def swarm_sim(argv):
    """In the main function first the config is getting parsed and than
    the swarm_sim_world and the swarm_sim_world object is created. Afterwards the run method of the swarm_sim_world
    is called in which the simlator is going to start to run"""
    logging.basicConfig(filename='system.log', filemode='w', level=logging.INFO, format='%(message)s')
    logging.info('Started')

    config_data = config.ConfigData()
    
    read_cmd_args(argv, config_data)

    create_direction_for_data(config_data)

    random.seed(config_data.seed_value)

    swarm_sim_world = world.World(config_data)

    while swarm_sim_world.get_actual_round() <= config_data.max_round and swarm_sim_world.get_end() is False:
        round_start_timestamp = time.perf_counter()
        if config_data.visualization:
            swarm_sim_world.vis.run(round_start_timestamp)
        run_solution(swarm_sim_world)

    logging.info('Finished')

    # generate_data(config_data, swarm_sim_world)

    while True:
        round_start_timestamp = time.perf_counter()
        swarm_sim_world.vis.run(round_start_timestamp)


def read_cmd_args(argv, config_data):
    try:
        opts, args = getopt.getopt(argv, "hs:w:r:n:m:d:v:", ["solution=", "scenario="])
    except getopt.GetoptError:
        print('Error: swarm-swarm_sim_world.py -r <seed> -w <scenario> -s <solution> -n <maxRounds>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('swarm-swarm_sim_world.py -r <seed> -w <scenario> -s <solution> -n <maxRounds>')
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


def create_direction_for_data(config_data):
    if config_data.multiple_sim == 1:
        config_data.direction_name = config_data.local_time + "_" + config_data.scenario.rsplit('.', 1)[0] + \
                               "_" + config_data.solution.rsplit('.', 1)[0] + "/" + \
                               str(config_data.seed_value)

        config_data.direction_name = "./outputs/mulitple/" + config_data.direction_name

    else:
        config_data.direction_name = config_data.local_time + "_" + config_data.scenario.rsplit('.', 1)[0] + \
                               "_" + config_data.solution.rsplit('.', 1)[0] + "_" + \
                               str(config_data.seed_value)
        config_data.direction_name = "./outputs/" + config_data.direction_name
    if not os.path.exists(config_data.direction_name):
        os.makedirs(config_data.direction_name)


def run_solution(swarm_sim_world):
    mod = importlib.import_module('solution.' + swarm_sim_world.config_data.solution)
    mod.solution(swarm_sim_world)
    swarm_sim_world.csv_round.next_line(swarm_sim_world.get_actual_round())
    swarm_sim_world.inc_round_counter_by(number=1)


def generate_data(config_data, swarm_sim_world):
    swarm_sim_world.csv_aggregator()
    gnuplot_generator(config_data.direction_name)


if __name__ == "__main__":
    swarm_sim(sys.argv[1:])