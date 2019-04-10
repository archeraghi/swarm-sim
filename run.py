"""This is the main module of the Opportunistic Robotics Network Simulator"""


import configparser
import getopt
import logging
import os
import sys
from datetime import datetime

from lib import  sim

def swarm_sim(argv):
    """In the main function first the config is getting parsed and than
    the simulator and the sim object is created. Afterwards the run method of the simulator
    is called in which the simlator is going to start to run"""
    config = configparser.ConfigParser(allow_no_value=True)

    config.read("config.ini")
    seedvalue = config.getint("Simulator", "seedvalue")
    max_round = config.getint("Simulator", "max_round")
    random_order = config.getboolean("Simulator", "random_order")
    visualization = config.getint("Simulator", "visualization")
    try:
        scenario_file = config.get ("File", "scenario")
    except (configparser.NoOptionError) as noe:
        scenario_file = "init_scenario.py"

    try:
        solution_file = config.get("File", "solution")
    except (configparser.NoOptionError) as noe:
        solution_file = "solution.py"
    size_x = config.getint("Simulator", "size_x")
    size_y = config.getint("Simulator", "size_y")
    window_size_x = config.getint("Simulator", "window_size_x")
    window_size_y = config.getint("Simulator", "window_size_y")
    border = config.getint("Simulator", "border")
    max_particles = config.getint("Simulator", "max_particles")
    mm_limitation = config.getboolean("Matter", "mm_limitation")
    mm_particle = config.getint("Matter", "particle_mm_size")
    mm_tile= config.getint("Matter", "tile_mm_size")
    mm_location=config.getint("Matter", "location_mm_size")

    multiple_sim=0

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
            solution_file = arg
        elif opt in ("-w", "--scenario"):
            scenario_file = arg
        elif opt in ("-r", "--seed"):
            seedvalue = int(arg)
        elif opt in ("-n", "--maxrounds"):
           max_round = int(arg)
        elif opt in ("-m"):
           multiple_sim = int(arg)
        elif opt in ("-v"):
            visualization = int(arg)
        elif opt in ("-d"):
            act_date = arg


    #logging.basicConfig(filename='myapp.log', filemode='w', level=logging.INFO, format='%(asctime)s %(message)s')
    logging.basicConfig(filename='system.log', filemode='w', level=logging.INFO, format='%(message)s')


    nTime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')[:-1]
    dir_name =  nTime + "_" + solution_file.rsplit('.',1)[0] + "_" + \
                         str(seedvalue)
    if multiple_sim == 1:
        directory = "./outputs/mulitple/"+ act_date + "_" + scenario_file.rsplit('.',1)[0] + \
                     "_"+solution_file.rsplit('.',1)[0] + "/" + str(seedvalue)
    else:
        directory = "./outputs/" + dir_name
    if not os.path.exists(directory):
        os.makedirs(directory)



    logging.info('Started')



    simulator=sim.Sim(seed=seedvalue, max_round=max_round, solution=solution_file.rsplit('.',1)[0],
                          size_x=size_x, size_y=size_y, scenario_name=scenario_file,
                           max_particles=max_particles, mm_limitation=mm_limitation,
                           particle_mm_size=mm_particle, tile_mm_size=mm_tile, location_mm_size=mm_location,
                           dir=directory, random_order=random_order,
                          visualization=visualization,  border=border, window_size_x=window_size_x, window_size_y=window_size_y,)

    simulator.run()
    logging.info('Finished')


if __name__ == "__main__":
    swarm_sim(sys.argv[1:])

