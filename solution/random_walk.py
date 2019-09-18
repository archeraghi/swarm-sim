import random
#Standard Lib that has to be in each solution
from solution.std_lib import *


def solution(world):
    for particle in world.get_particle_list():
        particle.move_to(random.choice(direction))