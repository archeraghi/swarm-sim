"""This is the main module of the Opportunistic Robotics Network Simulator"""
import getopt
import importlib
import logging
import os
import random
import sys
import time

from lib import world, config


#from lib.gnuplot_generator import plot_generator


def swarm_sim(argv):
    """In the main function first the config is getting parsed and than
    the swarm_sim_world and the swarm_sim_world object is created. Afterwards the run method of the swarm_sim_world
    is called in which the simlator is going to start to run"""
    logging.basicConfig(filename='system.log', filemode='w', level=logging.INFO, format='%(message)s')
    logging.info('Started')

    config_data = config.ConfigData()
    read_cmd_args(argv, config_data)

    create_folder_for_data(config_data)

    random.seed(config_data.seed_value)
    swarm_sim_world = world.World(config_data)

    round_start_timestamp = time.perf_counter()
    while (config_data.max_round == 0 or swarm_sim_world.get_actual_round() <= config_data.max_round) \
            and swarm_sim_world.get_end() is False:

        if config_data.visualization:
            swarm_sim_world.vis.run(round_start_timestamp)
            round_start_timestamp = time.perf_counter()

        run_solution(swarm_sim_world)
    if config_data.visualization:
        swarm_sim_world.vis.run(round_start_timestamp)
    logging.info('Finished')

    generate_data(config_data, swarm_sim_world)


def draw_scenario(config_data, swarm_sim_world):
    mod = importlib.import_module('scenario.' + config_data.scenario)
    mod.scenario(swarm_sim_world)
    if config_data.particle_random_order:
        random.shuffle(swarm_sim_world.particles)


def read_cmd_args(argv, config_data):
    try:
        opts, args = getopt.getopt(argv, "h:s:w:r:n:m:d:v:b:", ["solution=", "scenario="])
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
        elif opt == "-m":
            config_data.multiple_sim = int(arg)
        elif opt == "-v":
            config_data.visualization = int(arg)
        elif opt == "-d":
            config_data.local_time = str(arg)
        elif opt == "-b":
            config_data.folder_name = str(arg)


def  create_folder_for_data(config_data):
    if config_data.multiple_sim == 1:
        # config_data.folder_name = config_data.local_time + "_" + config_data.scenario.rsplit('.', 1)[0] + \
        #                              "_" + config_data.solution.rsplit('.', 1)[0]

        config_data.folder_name =  config_data.folder_name

    else:
        config_data.folder_name = config_data.local_time + "_" + config_data.scenario.rsplit('.', 1)[0] + \
                                     "_" + config_data.solution.rsplit('.', 1)[0] + "_" + \
                                     str(config_data.seed_value)
        config_data.folder_name = "./outputs/" + config_data.folder_name
    if not os.path.exists(config_data.folder_name):
        os.makedirs(config_data.folder_name)


def run_solution(swarm_sim_world):
    if swarm_sim_world.config_data.particle_random_order_always:
        random.shuffle(swarm_sim_world.particles)
    mod = importlib.import_module('solution.' + swarm_sim_world.config_data.solution)
    mod.solution(swarm_sim_world)
    swarm_sim_world.csv_round.next_line(swarm_sim_world.get_actual_round())
    swarm_sim_world.inc_round_counter_by(number=1)


def generate_data(config_data, swarm_sim_world):
    swarm_sim_world.csv_aggregator()
    #plot_generator("rounds.csv" ,config_data.folder_name, 5, 4,"Round")
    #plot_generator("particle.csv", config_data.folder_name, 2, 1,"Particle")


if __name__ == "__main__":
    swarm_sim(sys.argv[1:])
