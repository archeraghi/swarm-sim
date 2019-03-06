"""This is the main module of the Opportunistic Robotics Network Simulator"""


import configparser
import getopt
import logging
import os
import sys
from datetime import datetime

from lib import world, sim, vis, csv_generator
from lib.gnuplot_generator import generate_gnuplot


#visualization=True

def core(argv):
    """In the main function first the config is getting parsed and than
    the simulator and the world object is created. Afterwards the run method of the simulator
    is called in which the simlator is going to start to run"""
    config = configparser.ConfigParser(allow_no_value=True)

    config.read("config.ini")
    seedvalue = config.getint("Simulator", "seedvalue")
    max_round = config.getint("Simulator", "max_round")
    random_order = config.getboolean("Simulator", "random_order")
    visualization = config.getint("Simulator", "visualization")
    try:
        world_file = config.get ("File", "scenario")
    except (configparser.NoOptionError) as noe:
        world_file = "lonely_particle.py"

    try:
        solution_file = config.get("File", "solution")
    except (configparser.NoOptionError) as noe:
        solution_file = "random_walk.py"
    size_x = config.getint("World", "size_x")
    size_y = config.getint("World", "size_y")
    window_size_x = config.getint("World", "window_size_x")
    window_size_y = config.getint("World", "window_size_y")
    max_particles = config.getint("World", "max_particles")
    mm_limitation = config.getboolean("matter", "mm_limitation")
    mm_particle = config.getint("matter", "particle_mm_size")
    mm_tile= config.getint("matter", "tile_mm_size")
    mm_location=config.getint("matter", "location_mm_size")

    multiple_sim=0

    try:
        opts, args = getopt.getopt(argv, "hs:w:r:n:m:d:v:", ["solution=", "world="])
    except getopt.GetoptError:
        print('Error: run.py -r <randomeSeed> -s <solution> -w <world> -n <maxRounds>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('run.py -r <randomeSeed> -s <solution> -w <world> -n <maxRounds>')
            sys.exit()
        elif opt in ("-s", "--solution"):
            solution_file = arg
        elif opt in ("-w", "--world"):
            world_file = arg
        elif opt in ("-r", "--seed"):
            seedvalue = int(arg)
        elif opt in ("-n", "--maxrounds"):
           max_round = int(arg)
        elif opt in ("-m"):
           multiple = int(arg)
        elif opt in ("-v"):
            visualization = arg


    #logging.basicConfig(filename='myapp.log', filemode='w', level=logging.INFO, format='%(asctime)s %(message)s')
    logging.basicConfig(filename='system.log', filemode='w', level=logging.INFO, format='%(message)s')


    nTime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')[:-1]
    dir_name =  nTime + "_" + solution_file.rsplit('.',1)[0] + "_" + \
                         str(seedvalue)
    if multiple_sim == 1:
        directory = "./outputs/mulitple/" + dir_name + "/" + str(seedvalue)
    else:
        directory = "./outputs/" + dir_name
    if not os.path.exists(directory):
        os.makedirs(directory)


    simulator = sim.Sim(seed=seedvalue, max_round=max_round, solution=solution_file.rsplit('.',1)[0])

    logging.info('Started')

    csv_round_writer = csv_generator.CsvRoundData(sim=simulator, solution=solution_file.rsplit('.', 1)[0],
                                                  seed=seedvalue,
                                                  tiles_num=0, particle_num=0,
                                                  steps=0, directory=directory)

    sim_world=world.World( size_x=size_x, size_y=size_y, world_name=world_file,
                           sim=simulator, max_particles=max_particles, mm_limitation=mm_limitation,
                           particle_mm_size=mm_particle, tile_mm_size=mm_tile, location_mm_size=mm_location, dir=directory,
                           csv_round=csv_round_writer, random_order=random_order)



    if visualization==1:
        window = vis.VisWindow(window_size_x, window_size_y, sim_world, simulator)
        window.run()
    else:
        simulator.run(sim_world)

    csv_round_writer.aggregate_metrics()  # After simulation is finished, aggregate everything
    particleFile = csv_generator.CsvParticleFile(directory)
    for particle in sim_world.init_particles:
        particleFile.write_particle(particle)
    particleFile.csv_file.close()
    generate_gnuplot(directory)
    logging.info('Finished')


if __name__ == "__main__":
    core(sys.argv[1:])

