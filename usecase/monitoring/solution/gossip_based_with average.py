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
    #config protocol : remember last x particles
    remember_count=10
    #max deviation in % from local(particles) average
    deviation=0.01

    #initializes particles with attributes sum =0, particle_count=0 and check_term=0
    #besides one particle which gets a sum value =1
    if world.get_actual_round()==1:
        for rnd_particle in world.get_particle_list():
            setattr(rnd_particle, "sum", 0)
            setattr(rnd_particle, "particle_count",0)
            setattr(rnd_particle, "check_term" , 0)
            #index counter | max = remember_count
            setattr(rnd_particle, "replace_index", 0)
            #protocol
            setattr(rnd_particle, "knows_the_particle", 0)
            for i in range(0,remember_count):
                s = str(i)
                setattr(rnd_particle, "already_calc_with_"+s,-1)
            #for average|min|max calc
            setattr(rnd_particle, "current_min", 0)
            setattr(rnd_particle, "current_max", 0)
            setattr(rnd_particle, "current_average", 0)
            for i in range(0,remember_count):
                s = str(i)
                setattr(rnd_particle, "neighbours_particle_count_"+s, 0)
        #Graph
        random.choice(world.get_particle_list()).sum =1
        for i in range(len(world.get_particle_list())):
            info_plot.append([0])

    #Table
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
    #helper variable
    helper_particle_list=world.get_particle_list().copy()

    #Table
    if world.get_actual_round() > 1 and len(world.get_particle_list()) <= table_size_max:
        table_calcs+="\n|round:" +'{:_>2d}'.format(world.get_actual_round()) + "|"

    #Main Loop
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
                other_par_cur_sum=rnd_particle.get_particle_in(neighbour_found_in_dir).sum
                #adds the particle sum value with his neighbour's sum value and halves it eventually
                new_sum=transfer_sum(rnd_particle,rnd_particle.get_particle_in(neighbour_found_in_dir))
                #both particle get the new_sum
                rnd_particle.sum = new_sum
                rnd_particle.get_particle_in(neighbour_found_in_dir).sum= new_sum
                #protocol
                remember_attribute="already_calc_with_"+str(rnd_particle.replace_index)
                setattr(rnd_particle,remember_attribute, rnd_particle.get_particle_in(neighbour_found_in_dir).number)
                #protocol for neigbhour particle
                remember_attribute="already_calc_with_"+str(rnd_particle.get_particle_in(neighbour_found_in_dir).replace_index)
                setattr(rnd_particle.get_particle_in(neighbour_found_in_dir), remember_attribute, rnd_particle.number)
                #both partcle calculate the estimated amout of particles in the system
                rnd_particle.particle_count= calculate_particle_count(rnd_particle)
                rnd_particle.get_particle_in(neighbour_found_in_dir).particle_count = calculate_particle_count(rnd_particle.get_particle_in(neighbour_found_in_dir))
                #prints information about the calculation
                print_information(rnd_particle,neighbour_found_in_dir, current_sum)
                #Table
                table_calcs+=next_line_table(world.get_particle_list())
                table_calcs += "  " + str(rnd_particle.number - 1) + "-->" + str(rnd_particle.get_particle_in(neighbour_found_in_dir).number - 1)
                #Amount of calculations between particles increased by 1
                calc_count+=1
                #Termination
                average_attribute="neighbours_particle_count_"+str(rnd_particle.replace_index)
                setattr(rnd_particle,average_attribute, rnd_particle.get_particle_in(neighbour_found_in_dir).particle_count)
                average_array=[]
                for i in range(0,remember_count):
                    average_attribute="neighbours_particle_count_"+str(i)
                    average_array.append(getattr(rnd_particle,average_attribute))
                rnd_particle.current_average=sum(average_array)/remember_count
                rnd_particle.current_min=min(average_array)
                rnd_particle.current_max=max(average_array)

                average_attribute="neighbours_particle_count_"+str(rnd_particle.get_particle_in(neighbour_found_in_dir).replace_index)
                setattr(rnd_particle.get_particle_in(neighbour_found_in_dir), average_attribute, rnd_particle.particle_count)
                average_array = []
                for i in range(0, remember_count):
                    average_attribute = "neighbours_particle_count_" + str(i)
                    average_array.append(getattr(rnd_particle.get_particle_in(neighbour_found_in_dir), average_attribute))
                rnd_particle.get_particle_in(neighbour_found_in_dir).current_average = sum(average_array) / remember_count
                rnd_particle.get_particle_in(neighbour_found_in_dir).current_min = min(average_array)
                rnd_particle.get_particle_in(neighbour_found_in_dir).current_max = max(average_array)

                rnd_particle.check_term=check_termination(rnd_particle,deviation)
                rnd_particle.get_particle_in(neighbour_found_in_dir).check_term=check_termination(rnd_particle.get_particle_in(neighbour_found_in_dir),deviation)
                #increase index for the next neighbour
                rnd_particle.replace_index = (rnd_particle.replace_index + 1) % remember_count
                rnd_particle.get_particle_in(neighbour_found_in_dir).replace_index= (rnd_particle.get_particle_in(neighbour_found_in_dir).replace_index+1)%remember_count
        checklist_for_threshold.append(rnd_particle.check_term)
        #print(checklist_for_threshold)
        helper_particle_list.remove(rnd_particle)
        #protocol
        rnd_particle.knows_the_particle=0


    #Graph
    for particle in world.get_particle_list():
        info_plot[particle.number].append(particle.particle_count)

    #Color
    for particle in world.get_particle_list():
        farbe=set_color_g(particle)
        particle.set_color(farbe)


    #terminates when all particles have their check_term=1 or max_round is reached
    #
    #
    #

    if 0 not in checklist_for_threshold or world.get_actual_round()== world.get_max_round:
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
            sum_avg = 0
            for particle in world.get_particle_list():
                sum_avg+=info_plot[particle.number][i]
            average_plotter.append(sum_avg / len(world.get_particle_list()))
        #min
        min_all_per_round=[]
        for i in range(0, world.get_actual_round() + 1):
            min_all_particle = []
            for particle in world.get_particle_list():
                min_all_particle.append(info_plot[particle.number][i])
            min_all_per_round.append(min(min_all_particle))
        #max
        max_all_per_round = []
        for i in range(0, world.get_actual_round() + 1):
            max_all_particle = []
            for particle in world.get_particle_list():
                #if(info_plot[particle.number][i]<=len(world.get_particle_list())*5):
                max_all_particle.append(info_plot[particle.number][i])
                #else:
                #    max_all_particle.append(len(world.get_particle_list()*5))
            max_all_per_round.append(max(max_all_particle))
        #standard deviation
        standard_deviation_per_round = []
        for i in range(0, world.get_actual_round() + 1):
            all_particle = 0
            for particle in world.get_particle_list():
                all_particle+=(info_plot[particle.number][i]-average_plotter[i])*(info_plot[particle.number][i]-average_plotter[i])
            standard_deviation_per_round.append(np.sqrt(all_particle) / len(world.get_particle_list()))


        x2 = np.arange(0, world.get_actual_round() + 1, 1)
        fig2,ax2=plt.subplots()
        ax2.plot(x2,average_plotter)
        ax2.plot(x2,filler_actual_count)
        ax2.plot(x2,min_all_per_round)
        ax2.plot(x2,max_all_per_round)
        ax2.set(xlabel='rounds', ylabel='Average', title='Rot:Max | Blau:Durchschnitt | Grün:Min | Orange:Echter Wert')

        fig3, ax3 = plt.subplots()
        ax3.plot(x2,standard_deviation_per_round)
        ax3.set(xlabel='rounds', ylabel='standard deviation', title='Standard deviation')

        if world.get_actual_round() > 1 and len(world.get_particle_list()) <= table_size_max:
            table_calcs+=next_line_table(world.get_particle_list())
            print(table_calcs)
        print("Calculation count between particles", calc_count)
        print("Calculations per node", calc_count / (world.get_world_y_size() * world.get_world_x_size()))
        print("Average estimation:", average_plotter[len(average_plotter)-1])
        # Abweichung : Tatsächlicher Wert / Durchschnittswert | Min | Max ( all particle ) | Standardabweichung
        # absolut/relativ
        absolute_deviation=  average_plotter[len(average_plotter)-1]-len(world.get_particle_list())
        relative_deviation= (average_plotter[len(average_plotter)-1] / len(world.get_particle_list()) - 1) * 100
        max_all_time= max(max_all_per_round)
        min_all_time= min(min_all_per_round)
        max_last_round= max_all_per_round[len(max_all_per_round)-1]
        min_last_round= min_all_per_round[len(min_all_per_round)-1]

        standard_deviation_last_round = standard_deviation_per_round[len(standard_deviation_per_round)-1]
        relative_standard_deviation = (standard_deviation_last_round/average_plotter[len(average_plotter)-1])*100

        difference_max_average_last_round=max_last_round-average_plotter[len(average_plotter)-1]
        difference_min_average_last_round=min_last_round-average_plotter[len(average_plotter)-1]

        print("Deviation : Average estimation - Particles (absolute): ",absolute_deviation, " (relativ:)",relative_deviation,"%")
        print("(all rounds): Max: ",max_all_time, " Min: ", min_all_time)
        print("(last round): Max: ",max_last_round, "Min: ", min_last_round)
        print("difference Max-average: ", difference_max_average_last_round, " Min-average: ", difference_min_average_last_round)
        print("Standard deviation (last round): ", standard_deviation_last_round, "(relativ:)",relative_standard_deviation ,"%"  )
        print(standard_deviation_per_round)




        #for rnd_particle in world.get_particle_list():
        #    print("partikel number:", rnd_particle.number)
        #    print("curr average:", rnd_particle.current_average)
        #    print("curr min:", rnd_particle.current_min)
        #    print("curr max:", rnd_particle.current_average)
        #    print("curr count:", rnd_particle.particle_count)
        plt.show()
        world.set_end()



    #every particle moves after exchanging information
    if world.get_actual_round() > 0:
        for particle in world.get_particle_list():
            free_space_in_dir=search_personal_space(particle)
            if free_space_in_dir != -1:
                particle.move_to(free_space_in_dir)


def check_termination(particle,deviation):
    if(abs(particle.current_max-particle.current_average)<=np.ceil(2*deviation*particle.current_average)) \
            and (abs(particle.current_min-particle.current_average)<=np.ceil(2*deviation*particle.current_average))\
            and (abs(particle.particle_count-particle.current_average)<=np.ceil(deviation*particle.current_average)):
        return 1
    else:
        return 0

def print_information(rnd_particle, neighbour_found_in_dir, current_sum):
    print("current_sum:", current_sum)
    print("other particle's current_sum", rnd_particle.get_particle_in(neighbour_found_in_dir).sum)
    print("after calc:", rnd_particle.sum)
    print("N:after calc:", rnd_particle.get_particle_in(neighbour_found_in_dir).sum)
    print("particle aprox:", rnd_particle.particle_count)
    print("N:particle aprox:", rnd_particle.get_particle_in(neighbour_found_in_dir).particle_count)
    print("difference: old/new sum:", abs(current_sum - rnd_particle.sum))


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

