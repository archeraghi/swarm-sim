import random
import numpy
import numpy as np
import matplotlib.pylab as plt
import itertools


from lib.particle import Particle

NE = 0
E = 1
SE = 2
SW = 3
W = 4
NW = 5



direction = [NE, E, SE, SW, W, NW]
#choose leader_count which will have a start value
#leader_count=2
info_plot=[[]]
filler_actual_count=[]
calc_count=0
table_calcs= ""
def solution(world):
    global calc_count
    global table_calcs
    #max count for plots and table size
    table_size_max=16
    # configurations for Gossip
    threshold_limit = 0.00001
    #config protocol : remember last x particles
    remember_count=10

    #initializes particles with attributes sum =0, weight=1, particle_count=0 and check_term=0
    #besides one particle which gets a sum value =1
    if world.get_actual_round()==1:
        for rnd_particle in world.get_particle_list():
            setattr(rnd_particle, "sum", 0)
            setattr(rnd_particle, "weight", 1)
            setattr(rnd_particle, "particle_count",0)
            setattr(rnd_particle, "check_term" , 0)
            #protocol
            setattr(rnd_particle, "knows_the_particle", 0)
            setattr(rnd_particle, "replace_index",0)
            for i in range(0,remember_count):
                s = str(i)
                setattr(rnd_particle, "already_calc_with_"+s,-1)

        random.choice(world.get_particle_list()).sum =1
        for i in range(len(world.get_particle_list())):
            info_plot.append([0])

    if world.get_actual_round() == 1 and len(world.get_particle_list()) <= table_size_max:
        table_calcs = "|rounds  |"
        for i in range(0, len(world.get_particle_list())):
            table_calcs = table_calcs + "___p" + '{:_<4d}'.format(i) + "|"

        table_calcs = table_calcs + "\n" + "|round:_0|"
        helper_sum_list=[]
        for i in range(0, len(world.get_particle_list())):
            helper_sum_list.append(0)
        for particle in world.get_particle_list():
            print(particle.number)
            helper_sum_list[particle.number-1]=particle.sum
        for i in helper_sum_list:
            table_calcs=table_calcs+'{:_>8.4f}'.format(i)+"|"
        table_calcs+="\n|round:_1"


    #helper to terminate the progamm
    checklist_for_threshold = []

    #helper variables
    counter1=0
    helper_particle_list=world.get_particle_list().copy()
    #print(len(helper_particle_list))

    if world.get_actual_round() > 1 and len(world.get_particle_list()) <= table_size_max:
        table_calcs+="\n|round:" +'{:_>2d}'.format(world.get_actual_round()) + "|"

    while(len(helper_particle_list)!=0):
        #choose a random particle
        rnd_particle=random.choice(helper_particle_list)
        current_sum = rnd_particle.sum
        #the random chosen particle searches for a neighbour
        neighbour_found_in_dir=search_any_neighbour(rnd_particle)
        #protocol: checks if the found neighbour is in the last x remembered particles
        if(neighbour_found_in_dir!=-1):
            for i in range(0,remember_count):
                s=str(i)
                remember_attribute="already_calc_with_"+s
                if(getattr(rnd_particle,remember_attribute)==rnd_particle.get_particle_in(neighbour_found_in_dir).number):
                    rnd_particle.knows_the_particle=1
        #if the the random chosen particle has a sumvalue above 0
        #he will reach for the searched neighbour
        if (neighbour_found_in_dir) != -1 and (rnd_particle.sum!=0 and rnd_particle.knows_the_particle==0):
            if(rnd_particle.check_term==0 or rnd_particle.get_particle_in(neighbour_found_in_dir).check_term!=1):
                #or rnd_particle.get_particle_in(neighbour_found_in_dir).sum!=0 ):
                print("current_sum:",current_sum)
                print("other particle's current_sum", rnd_particle.get_particle_in(neighbour_found_in_dir).sum)
                other_par_cur_sum=rnd_particle.get_particle_in(neighbour_found_in_dir).sum
                #adds the particle sum value with his neighbour's sum value and halves it eventually
                new_sum=transfer_sum(rnd_particle,rnd_particle.get_particle_in(neighbour_found_in_dir))
                #both particle get the new_sum
                rnd_particle.sum = new_sum
                rnd_particle.get_particle_in(neighbour_found_in_dir).sum= new_sum
                #protocol
                remember_attribute="already_calc_with_"+str(rnd_particle.replace_index)
                setattr(rnd_particle,remember_attribute, rnd_particle.get_particle_in(neighbour_found_in_dir).number)
                rnd_particle.replace_index=(rnd_particle.replace_index+1)%remember_count

                remember_attribute="already_calc_with_"+str(rnd_particle.get_particle_in(neighbour_found_in_dir).replace_index)
                setattr(rnd_particle.get_particle_in(neighbour_found_in_dir), remember_attribute, rnd_particle.number)
                rnd_particle.get_particle_in(neighbour_found_in_dir).replace_index= (rnd_particle.get_particle_in(neighbour_found_in_dir).replace_index+1)%remember_count

                #both partcle calculate the estimated amout of particles in the system
                rnd_particle.particle_count= calculate_particle_count(rnd_particle)
                rnd_particle.get_particle_in(neighbour_found_in_dir).particle_count = calculate_particle_count(rnd_particle.get_particle_in(neighbour_found_in_dir))
                #check
                print("after calc:",rnd_particle.sum)
                print("N:after calc:",rnd_particle.get_particle_in(neighbour_found_in_dir).sum)
                print("particle aprox:", rnd_particle.particle_count)
                print("N:particle aprox:", rnd_particle.get_particle_in(neighbour_found_in_dir).particle_count)
                #termination helper
                print("difference: old/new sum:",abs(current_sum-rnd_particle.sum))
                #checks if it has already calculates with that neighbour in the last round
                table_calcs+=next_line_table(world.get_particle_list())
                calc_count+=1
                table_calcs+="  "+str(rnd_particle.number-1)+"-->"+str(rnd_particle.get_particle_in(neighbour_found_in_dir).number-1)
                if(abs(current_sum-rnd_particle.sum)> 0):
                    # checks if the threshold was not reached
                    if (abs(current_sum-rnd_particle.sum)<threshold_limit):
                        rnd_particle.check_term=1

                    if(abs(other_par_cur_sum-rnd_particle.get_particle_in(neighbour_found_in_dir).sum)<threshold_limit):
                        rnd_particle.get_particle_in(neighbour_found_in_dir).check_term=1

        checklist_for_threshold.append(rnd_particle.check_term)
        #print(checklist_for_threshold)
        counter1 += 1
        helper_particle_list.remove(rnd_particle)
        #print(len(helper_particle_list))
        #protocol
        rnd_particle.knows_the_particle=0

    for particle in world.get_particle_list():
        info_plot[particle.number].append(particle.particle_count)

    for particle in world.get_particle_list():
        farbe=set_color_g(particle)
        particle.set_color(farbe)


    #terminates when all particles had a new_sum with a difference belove the threshold in compersion to the round before
    if 0 not in checklist_for_threshold or world.get_actual_round()== world.get_max_round():
        print("Terminated in round : ", world.get_actual_round())
        i=0
        for particle in world.get_particle_list():
            print("partikel_nr:",i)
            print("schätzt partikelanzahl im system auf:",particle.particle_count)
            i+=1

        for i in range(0, world.get_actual_round() + 1):
            filler_actual_count.append(len(world.get_particle_list()))

        if len(world.get_particle_list()) <= table_size_max:
            for particle in world.get_particle_list():
                x = np.arange(0, world.get_actual_round() + 1, 1)
                #print(x)
                y = info_plot[particle.number]
                #print(y)
                #plt.figure(1)
                fig1,ax1 = plt.subplots()
                ax1.plot(x, y)
                ax1.plot(x, filler_actual_count)
                particle_number='Particle Number : '+ str(particle.number)
                ax1.set(xlabel='rounds',ylabel='Estimation of particles', title=particle_number)

        #average estimation per round
        average_plotter=[]

        for i in range(0, world.get_actual_round() + 1):
            average = 0
            for particle in world.get_particle_list():
                average+=info_plot[particle.number][i]
            average_plotter.append(average / len(world.get_particle_list()))
        x2 = np.arange(0, world.get_actual_round() + 1, 1)
        #print(x2)
        y2 = average_plotter
        #print(y2)
        fig2,ax2=plt.subplots()
        ax2.plot(x2,y2)
        ax2.plot(x2,filler_actual_count)
        ax2.set(xlabel='rounds', ylabel='Average', title='Average estimation of all particles ')


        if world.get_actual_round() > 1 and len(world.get_particle_list()) <= table_size_max:
            table_calcs+=next_line_table(world.get_particle_list())
            print(table_calcs)
        print("Calculation count between particles", calc_count)
        print("Average estimation:", average / len(world.get_particle_list()))
        plt.show()
        world.set_end()



    if world.get_actual_round() > 0:
        for particle in world.get_particle_list():
            free_space_in_dir=search_personal_space(particle)
            if free_space_in_dir != -1:
                particle.move_to(free_space_in_dir)


def next_line_table(p_list):
    helper_sum_list=[]
    global table_calcs
    next_line="\n|calc:" + '{:_>3d}'.format(calc_count) + "|"
    for i in range(0, len(p_list)):
        helper_sum_list.append(0)
    for particle in p_list:
        helper_sum_list[particle.number - 1] = particle.sum
    for i in helper_sum_list:
        next_line+= '{:_>8.4f}'.format(i) + "|"
    return next_line


def search_personal_space(particle):
    dir = [0, 1, 2, 3, 4, 5]
    while len(dir) != 0:
        rnd_dir = random.choice(dir)
        if particle.particle_in(rnd_dir):
            dir.remove(rnd_dir)
        else:
            return rnd_dir
    return -1

def search_any_neighbour(particle: Particle) -> int:
    #searches for any neighbour to transfer sum afterwards
    dir = [0,1,2,3,4,5]
    while len(dir)!=0:
        rnd_dir=random.choice(dir)
        if particle.particle_in(rnd_dir):
            return rnd_dir
        else:
            dir.remove(rnd_dir)
    return -1


def transfer_sum(particle1,particle2):
    return (particle1.sum+particle2.sum)/(2)


def calculate_particle_count(particle):
    #berechnet den Kehrwert der Summe um die geschätzte Anzahl der Partikel im System zu berechnen
    return round(1/particle.sum)

def set_color_g(particle):
    #colour =1 : <10
    #colour =2 : <20
    #colour =3 : <50
    #colour =4 : <100
    #colour =5 : <200
    #colour =6 : >=200
    # black = 1
    # gray = 2
    # red = 3
    # green = 4
    # blue = 5
    # yellow = 6
    # orange = 7
    # cyan = 8
    # violett = 9
    if particle.particle_count>=200:
        return 6
    elif particle.particle_count>=100:
        return 5
    elif particle.particle_count>=50:
        return 4
    elif particle.particle_count>=20:
        return 3
    elif particle.particle_count>=10:
        return 2
    else:
        return 1


