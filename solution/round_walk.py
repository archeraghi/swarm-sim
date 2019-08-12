
#Standard Lib that has to be in each solution
from solution.std_lib import *

def solution(sim):

    for particle in sim.get_particle_list():
        global ttl
        global max
        global dir

        if sim.get_actual_round() == 1:
            max = 0
            ttl = 0
            dir = NE

        if (ttl==0 and (dir==NE or dir==SW)):
            max = max+1

        if ttl==0:
            print("Round ", sim.get_actual_round())
            ttl=max
            if dir==NE:
                dir=NW
            elif dir==NW:
                dir=SW
            elif dir==SW:
                dir=SE
            elif dir==SE:
                dir=NE

        particle.create_marker()
        particle.move_to(dir)
        ttl = ttl - 1