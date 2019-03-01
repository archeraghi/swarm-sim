import logging
import random


NE = 0
E = 1
SE = 2
SW = 3
W = 4
NW = 5


direction = [NE, E, SE, SW, W, NW]

ttl = 0
dir = NE
max = 0



def solution(sim, world):

    for particle in world.get_particle_list():
        global ttl
        global max
        global dir

        if sim.get_actual_round() == 0:
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

        particle.create_location()
        particle.move_to(dir)
        ttl = ttl - 1