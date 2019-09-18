
#Standard Lib that has to be in each solution
from solution.std_lib import *

def solution(world):

    for particle in world.get_particle_list():
        global ttl
        global max
        global direction

        if world.get_actual_round() == 1:
            max = 0
            ttl = 0
            direction = NE

        if (ttl==0 and (direction==NE or direction==SW)):
            max = max+1

        if ttl==0:
            print("Round ", world.get_actual_round())
            ttl=max
            if direction==NE:
                direction=NW
            elif direction==NW:
                direction=SW
            elif direction==SW:
                direction=SE
            elif direction==SE:
                direction=NE

        particle.create_marker()
        particle.move_to(direction)
        ttl = ttl - 1