import random
import numpy
import numpy as np
import matplotlib.pylab as plt
import itertools


black = 1
gray = 2
red = 3
green = 4
blue = 5
yellow = 6
orange = 7
cyan = 8
violett = 9

color_map = {
    black: [0.0, 0.0, 0.0],
    gray: [0.3, 0.3, 0.3],
    red: [0.8, 0.0, 0.0],
    green: [0.0, 0.8, 0.0],
    blue: [0.0, 0.0, 0.8],
    yellow: [0.8, 0.8, 0.0],
    orange: [0.8, 0.3, 0.0],
    cyan: [0.0, 0.8, 0.8],
    violett: [0.8, 0.2, 0.6]
    }


check=0
def solution(sim):
    global check
    wait_var=10
    term_list=[]
    if sim.get_actual_round()==1:
        for particle in sim.get_particle_list():
            #setattr(particle, "connected_from_dir")[0]=-1
            setattr(particle, "max", 0)
            setattr(particle, "push", 1)
            setattr(particle, "prev_push",0)
            setattr(particle, "prev_max", 0)
            #setattr(particle, "getting_pushed_buffer", 0)
            setattr(particle, "connected_to_dir",-1)
            setattr(particle, "leader", 0)
            setattr(particle, "connected_to_leader", 0)
            setattr(particle, "term_counter",0)
            setattr(particle, "ready_to_term",0)
            setattr(particle, "connected_from_dir",[])
            particle.connected_from_dir.append(-1)
        leader_particle=random.choice(sim.get_particle_list())
        leader_particle.leader = 1
        leader_particle.connected_to_leader=1
        leader_particle.set_color(red)
        print("leader_particle is particle_nr:", leader_particle.number)
        print("round nr:", sim.get_actual_round())

    #for particle in sim.get_particle_list():
    #    particle.getting_pushed_buffer=0
    # if sim.get_actual_round()==0:
    #     for particle in sim.get_particle_list():
    #             particle.connected_to_dir=search_any_neighbour(particle)
    #             if particle.get_particle_in(particle.connected_to_dir).connected_from_dir[0]==-1:
    #                 particle.connected_from_dir[0]=(particle.connected_to_dir+3)%6
    #             else:
    #                 particle.get_particle_in(particle.connected_to_dir).connected_from_dir.append((particle.connected_to_dir+3)%6)
    #
    #
    # for particle in sim.get_particle_list():
    #     particle.has_pushed=0
    #
    # while(0 in has_pushed_list):
    #     for particle in sim.get_particle_list():
    #         if particle.has_pushed == 0 and particle.push == 1:


    for particle in sim.get_particle_list():
        print("actuall particle_nr:", particle.number)
        print("actuall particle pushes:", particle.push)
        if (particle.leader == 0 and particle.connected_to_dir == -1) or particle.connected_to_leader == 0 :
            #print("Particle_nr is connecting:", particle.number)
            particle.connected_to_dir=search_any_neighbour(particle)
            # print("connected to particle_nr:", particle.get_particle_in(particle.connected_to_dir).number)
        if particle.get_particle_in(particle.connected_to_dir):
            if particle.get_particle_in(particle.connected_to_dir).leader == 1 or particle.get_particle_in(particle.connected_to_dir).connected_to_leader==1:
                particle.connected_to_leader=1
                if len(particle.get_particle_in(particle.connected_to_dir).connected_from_dir)==1 and (particle.connected_to_dir+3)%6!=particle.get_particle_in(particle.connected_to_dir).connected_from_dir[0]:
                    particle.get_particle_in(particle.connected_to_dir).connected_from_dir[0]=(particle.connected_to_dir+3)%6
                elif (particle.connected_to_dir+3)%6 not in particle.get_particle_in(particle.connected_to_dir).connected_from_dir:
                    particle.get_particle_in(particle.connected_to_dir).connected_from_dir.append((particle.connected_to_dir+3)%6)
        if particle.connected_to_leader==1 and particle.leader==0 and not particle.get_particle_in(particle.connected_to_dir) or particle.get_particle_in(particle.connected_to_dir).get_color()==yellow:
            particle.connected_to_leader=0
            particle.push=1
            particle.prev_push=0
            particle.set_color(yellow)
            for i in particle.connected_from_dir:
                particle.get_particle_in(i).connected_to_leader=0
                particle.get_particle_in(i).set_color(yellow)
                particle.get_particle_in(i).push=1
                particle.get_particle_in(i).prev_push=0
        if particle.connected_to_leader==1 and particle.leader !=1:
            if particle.prev_push>particle.push:
                check = 1
            particle.get_particle_in(particle.connected_to_dir).push+=(particle.push-particle.prev_push)
            particle.prev_push=particle.push
            if particle.max!=particle.get_particle_in(particle.connected_to_dir).max:
                particle.max=particle.get_particle_in(particle.connected_to_dir).max
                particle.set_color(5)
                particle.term_counter = 0
                particle.ready_to_term  = 0
            elif particle.max!=0:
                particle.term_counter+=1
                if particle.term_counter==wait_var:
                    particle.ready_to_term=1
                    particle.set_color(3)
            for particle in sim.get_particle_list():
                if particle.leader == 1:
                    print("leader_push:",particle.push)
                    print("leader_prev_push:", particle.prev_push)
            #print("pushes to particle_nr:", particle.get_particle_in(particle.connected_to_dir).number)
            #print("connected particle pushes:", particle.get_particle_in(particle.connected_to_dir).push)

    for particle in sim.get_particle_list():
        if particle.leader==1:
            particle.max=particle.push
            if particle.prev_max == particle.max and particle.max!=0:
                particle.term_counter+=1
                print("leader_term_count", particle.term_counter)
                if particle.term_counter==wait_var:
                    particle.ready_to_term=1
            else:
                particle.term_counter=0
                particle.ready_to_term=0
            particle.prev_max=particle.max
            print("max:" , particle.max)

    for particle in sim.get_particle_list():
        term_list.append(particle.ready_to_term)

    print(term_list)

    if 0 not in term_list:
        for particle in sim.get_particle_list():
            print("particle_nr:", particle.number)
            print("has max:", particle.max)
            print("has term_count:", particle.term_counter)
        print("particle in map:", len(sim.get_particle_list()))
        print("check:",check)
        sim.set_end()


    # if sim.get_actual_round()==10:
    #     a_particle=random.choice(sim.get_particle_list())
    #     print("deleted particle_nr:", a_particle.number)
    #     a_particle.delete_particle()
    #     a_particle = random.choice(sim.get_particle_list())
    #     print("deleted particle_nr:", a_particle.number)
    #     a_particle.delete_particle()



    print("round nr:", sim.get_actual_round()+1)


def search_deeper(particle_start, current_push_search):
    if particle_start.push > current_push_search:
        return search_deeper(particle_start.get_particle_in(random.choice(particle_start.connected_from_dir)), current_push_search)
    else:
        return particle_start


def search_any_neighbour(particle) -> int:
    # searches for any neighbour to transfer sum afterwards
    dir = [0, 1, 2, 3, 4, 5]
    while len(dir) != 0:
        rnd_dir = random.choice(dir)
        if particle.particle_in(rnd_dir):
            return rnd_dir
        else:
            dir.remove(rnd_dir)
    return -1