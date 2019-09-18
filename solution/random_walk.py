import random
#Standard Lib that has to be in each solution
from lib.swarm_sim_header import *

def solution(world):

    if world.get_actual_round() % 1 == 0:
        for particle in world.get_particle_list():
            particle.move_to(random.choice(direction))