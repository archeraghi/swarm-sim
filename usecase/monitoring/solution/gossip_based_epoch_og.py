import csv
import datetime
import random
import numpy
import numpy as np
import matplotlib.pylab as plt
import itertools
from mpl_toolkits import mplot3d
import matplotlib.tri as mtri
from mpl_toolkits.mplot3d import Axes3D
import os

from lib.particle import Particle

NE = 0
E = 1
SE = 2
SW = 3
W = 4
NW = 5


x_offset = [0.5, 1,  0.5,   -0.5,   -1, -0.5 ]
y_offset = [ 1, 0, -1,   -1,    0,  1]
direction = [NE, E, SE, SW, W, NW]
info_plot=[[]]
filler_actual_count=[]
calc_count = 0
filler_actual_count=[]
filler_actual_count.append(0)
message_count=0
u_message_count=0
info_plot_dir = './outputs/gossip_based_standard/' + datetime.datetime.now().strftime('%Y_%m_%d_%H') + '/'
# configurations for Gossip

def solution(sim):
    global map_exchange
    global map_exchange_u
    global info_plot_dir
    global calc_count
    global table_calcs
    global message_count
    global u_message_count
    threshold_limit = 0.000002
    table_calcs = ""
    # max count for plots and table size
    table_size_max = 1
    #initializes particles with attributes sum =0, weight=1, particle_count=0 and check_term=0
    #besides one particle which gets a sum value =1
    if sim.get_actual_round()==1:
        for rnd_particle in sim.get_particle_list():
            setattr(rnd_particle, "sum", 0)
            setattr(rnd_particle, "weight", 1)
            setattr(rnd_particle, "particle_count",0)
            #setattr(rnd_particle, "check_term" , 0)
            setattr(rnd_particle, "version_number", 1)
            setattr(rnd_particle, "min_rounds", 100)
            setattr(rnd_particle, "actual_round", 0)
        master = random.choice(sim.get_particle_list())
        master.sum = 1
        master.version_number = 2
        for i in range(len(sim.get_particle_list())):
            info_plot.append([0])

        rows, cols = (1 + 2 * int(sim.get_world_y_size()), 1 + 4 * int(sim.get_world_x_size()))
        map_exchange = [[int(0) for i in range(cols)] for j in range(rows)]
        map_exchange_u = [[int(0) for i in range(cols)] for j in range(rows)]

    if sim.get_actual_round() == 1 and len(sim.get_particle_list()) <= table_size_max:
        table_calcs = "|rounds  |"
        for i in range(0, len(sim.get_particle_list())):
            table_calcs = table_calcs + "___p" + '{:_<4d}'.format(i) + "|"

        table_calcs = table_calcs + "\n" + "|round:_0|"
        helper_sum_list=[]
        for i in range(0,len(sim.get_particle_list())):
            helper_sum_list.append(0)
        for particle in sim.get_particle_list():
            print(particle.number)
            helper_sum_list[particle.number-1]=particle.sum
        for i in helper_sum_list:
            table_calcs=table_calcs+'{:_>8.4f}'.format(i)+"|"
        table_calcs+="\n|round:_1"


    #helper to terminate the progamm
    checklist_for_threshold = []

    #helper variables
    counter1=0
    helper_particle_list=sim.get_particle_list().copy()
    #print(len(helper_particle_list))

    if sim.get_actual_round() > 1 and len(sim.get_particle_list()) <= table_size_max:
        table_calcs+="\n|round:"+'{:_>2d}'.format(sim.get_actual_round())+"|"

    while(len(helper_particle_list)!=0):
        #choose a random particle
        rnd_particle=random.choice(helper_particle_list)
        neighbour_found_in_dir = search_any_neighbour(rnd_particle)

        if (neighbour_found_in_dir != -1):
            if rnd_particle.actual_round >= rnd_particle.min_rounds:
                reset_to_master(rnd_particle)
                #print("master reset in round:" + sim.get_actual_round())

            if rnd_particle.version_number < rnd_particle.get_particle_in(neighbour_found_in_dir).version_number:
                reset_particle(rnd_particle,rnd_particle.get_particle_in(neighbour_found_in_dir))

            if rnd_particle.version_number > rnd_particle.get_particle_in(neighbour_found_in_dir).version_number:
                reset_particle(rnd_particle.get_particle_in(neighbour_found_in_dir), rnd_particle)

        current_sum = rnd_particle.sum

        #if the the random chosen particle has a sumvalue above 0
        #he will reach for the searched neighbour
        if (neighbour_found_in_dir) != -1 and (rnd_particle.sum!=0):
            #if(rnd_particle.check_term==0 or rnd_particle.get_particle_in(neighbour_found_in_dir).check_term!=1):
                #or rnd_particle.get_particle_in(neighbour_found_in_dir).sum!=0 ):
            r_p_old_count = rnd_particle.particle_count
            r_p_n_old_count = rnd_particle.get_particle_in(neighbour_found_in_dir).particle_count
            #adds the particle sum value with his neighbour's sum value and halves it eventually
            new_sum=transfer_sum(rnd_particle,rnd_particle.get_particle_in(neighbour_found_in_dir))
            #both particle get the new_sum
            rnd_particle.sum = new_sum
            rnd_particle.get_particle_in(neighbour_found_in_dir).sum= new_sum
            #both partcle calculate the estimated amout of particles in the system
            rnd_particle.particle_count= calculate_particle_count(rnd_particle)
            rnd_particle.get_particle_in(neighbour_found_in_dir).particle_count = calculate_particle_count(rnd_particle.get_particle_in(neighbour_found_in_dir))

            if (r_p_old_count==rnd_particle.particle_count):
                map_exchange_u[abs(int(rnd_particle.coords[1]) - int(sim.get_world_y_size()))][int(2 * rnd_particle.coords[0]) + 2 * int(sim.get_world_x_size())] += 1
                u_message_count+=1
            if (r_p_n_old_count==rnd_particle.get_particle_in(neighbour_found_in_dir).particle_count):
                map_exchange_u[abs(int(rnd_particle.get_particle_in(neighbour_found_in_dir).coords[1]) - int(sim.get_world_y_size()))][int(2 * rnd_particle.get_particle_in(neighbour_found_in_dir).coords[0]) + 2 * int(sim.get_world_x_size())] += 1
                u_message_count+=1
            #check
            #print("after calc:",rnd_particle.sum)
            #print("N:after calc:",rnd_particle.get_particle_in(neighbour_found_in_dir).sum)
            #print("particle aprox:", rnd_particle.particle_count)
            #print("N:particle aprox:", rnd_particle.get_particle_in(neighbour_found_in_dir).particle_count)
            #termination helper
            #print("difference: old/new sum:",abs(current_sum-rnd_particle.sum))
            #checks if it has already calculates with that neighbour in the last round
            #table_calcs+=next_line_table(sim.get_particle_list())
            calc_count+=1
            message_count=calc_count*2
            print(sim.get_world_y_size())
            map_exchange[abs(int(rnd_particle.coords[1]) - int(sim.get_world_y_size()))][int(2 * rnd_particle.coords[0]) + 2 * int(sim.get_world_x_size())] += 1
            map_exchange[abs(int(rnd_particle.get_particle_in(neighbour_found_in_dir).coords[1]) - int(sim.get_world_y_size()))][int(2 * rnd_particle.get_particle_in(neighbour_found_in_dir).coords[0]) + 2 * int(sim.get_world_x_size())] +=1
            rnd_particle.actual_round += 1


        #table_calcs+="  "+str(rnd_particle.number-1)+"-->"+str(rnd_particle.get_particle_in(neighbour_found_in_dir).number-1)
            #if(abs(current_sum-rnd_particle.sum)> 0):
                # checks if the threshold was not reached
            #    if (abs(current_sum-rnd_particle.sum)<threshold_limit):
            #        rnd_particle.check_term=1

            #    if(abs(other_par_cur_sum-rnd_particle.get_particle_in(neighbour_found_in_dir).sum)<threshold_limit):
            #        rnd_particle.get_particle_in(neighbour_found_in_dir).check_term=1


    #checklist_for_threshold.append(rnd_particle.check_term)
        #print(checklist_for_threshold)
        counter1 += 1
        helper_particle_list.remove(rnd_particle)
        #print(len(helper_particle_list))

    for particle in sim.get_particle_list():
        info_plot[particle.number].append(particle.particle_count)

    #for particle in sim.get_particle_list():
    #    farbe=set_color_g(particle)
    #    particle.set_color(farbe)

    filler_actual_count.append(len(sim.get_particle_list()))

    #terminates when all particles had a new_sum with a difference belove the threshold in compersion to the round before
    if sim.get_actual_round()== sim.get_max_round():
        print("Terminiert in Runde: ", sim.get_actual_round())
        i = 0
        for particle in sim.get_particle_list():
            print("Partikel_nr:", i)
            print("Schätzt Partikelanzahl im System auf:", particle.particle_count)
            i += 1

        if len(sim.get_particle_list()) <= table_size_max:
            for particle in sim.get_particle_list():
                x = np.arange(0, sim.get_actual_round() + 1, 1)
                # print(x)
                y = info_plot[particle.number]
                # print(y)
                # plt.figure(1)
                fig1, ax1 = plt.subplots()
                ax1.plot(x, y, label='Einschätzung')
                ax1.plot(x, filler_actual_count, label='Tatsächliche Anzahl im System')
                particle_number = 'Einschätzung der Anzahl der Partikel im System von Partikel_Nr: ' + str(
                    particle.number)
                ax1.set(xlabel='Runde', ylabel='Partikel', title=particle_number)
                ax1.legend(loc='best')

        # average estimation per round
        average_plotter = []

        for i in range(0, sim.get_actual_round() + 1):
            average = 0
            for particle in sim.get_particle_list():
                average += info_plot[particle.number][i]
            average_plotter.append(average / len(sim.get_particle_list()))
        x2 = np.arange(0, sim.get_actual_round() + 1, 1)
        # print(x2)
        y2 = average_plotter
        # print(y2)
        fig2, ax2 = plt.subplots()
        ax2.plot(x2, y2, label='Durchschnittliche Einschätzung')
        ax2.plot(x2, filler_actual_count, label='Tatsächliche Anzahl im System')
        ax2.set(xlabel='Runde', ylabel='Partikel', title='Durchschnittliche Einschätzung aller Partikel')
        ax2.legend(loc='best')
        ax2.set_yscale('log')


        standard_deviation_per_round = []
        for i in range(0, sim.get_actual_round() + 1):
            all_particle = 0
            for particle in sim.get_particle_list():
                all_particle += (info_plot[particle.number][i] - average_plotter[i]) * (
                        info_plot[particle.number][i] - average_plotter[i])

            standard_deviation_per_round.append(
                (np.sqrt(all_particle) / len(sim.get_particle_list())) / average_plotter[i] * 100)


        y3 = []
        for i in x2:
            y3.append(5)

        fig3, ax3 = plt.subplots()
        ax3.plot(x2, standard_deviation_per_round, label='relative Standardabweichung')
        ax3.plot(x2, y3, label='5% - Linie')
        ax3.set(xlabel='Runde', ylabel='relative Standardabweichung in %',
                title='Standardabweichung der Einschätzungen der Partikel')
        ax3.legend(loc='best')

        if sim.get_actual_round() > 1 and len(sim.get_particle_list()) <= table_size_max:
            table_calcs += next_line_table(sim.get_particle_list())
            print(table_calcs)
        print("Austausche zwischen Partikel: ", calc_count)
        print("Durchschnittliche Einschätzung aller Partikel: ", average / len(sim.get_particle_list()))

        ###############################################################
        y = np.arange(sim.get_world_y_size(), -sim.get_world_y_size() - 1, -1)
        x = np.arange(-sim.get_world_x_size(), sim.get_world_x_size() + 0.5, 0.5)

        Y, X = np.meshgrid(x, y)

        map_exchange_2 = np.copy(map_exchange)

        for i in range(0, len(map_exchange)):
            for j in range(0, len(map_exchange[i])):
                if map_exchange[i][j] == 0:
                    map_exchange[i][j] = None
        map_exchange = np.array(map_exchange)
        print(map_exchange)
        fig4, ax4 = plt.subplots()
        a5 = ax4.scatter(Y, X, c=map_exchange_2, cmap='Reds')
        fig4.colorbar(a5)

        ax4.set_xlabel('X coord')
        ax4.set_ylabel('Y coord')

        # Graph 4

        x = []
        y = []
        z = []
        dx = []
        dy = []
        dz = []
        for i in range(0, len(Y)):
            for j in range(0, len(Y[i])):
                if map_exchange_2[i][j] > 0:
                    x.append(Y[i][j])
                    dx.append(0.2)
        for i in range(0, len(X)):
            for j in range(0, len(X[i])):
                if map_exchange_2[i][j] > 0:
                    y.append(X[i][j])
                    dy.append(0.2)
        for i in range(0, len(map_exchange)):
            for j in range(0, len(map_exchange[i])):
                if map_exchange_2[i][j] > 0:
                    z.append(0)
                    dz.append(map_exchange_2[i][j])

        fig5 = plt.figure()
        ax5 = fig5.add_subplot(111, projection='3d')

        dzc = np.array(dz)
        colors = plt.cm.Reds(dzc / float(map_exchange_2.max()))

        ax5.bar3d(x, y, z, dx, dy, dz, color=colors)
        ax5.set_xlabel('X coord')
        ax5.set_ylabel('Y coord')
        ax5.set_zlabel('Nachrichten')

        map_exchange_u_2 = np.copy(map_exchange_u)

        for i in range(0, len(map_exchange_u)):
            for j in range(0, len(map_exchange_u[i])):
                if map_exchange_u[i][j] == 0:
                    map_exchange_u[i][j] = None
        map_exchange_u = np.array(map_exchange_u)
        print(map_exchange_u)
        fig7, ax7 = plt.subplots()
        a7 = ax7.scatter(Y, X, c=map_exchange_u_2, cmap='Reds')
        fig7.colorbar(a7)

        ax7.set_xlabel('X coord')
        ax7.set_ylabel('Y coord')

        # Graph 7
        x = []
        y = []
        z = []
        dx = []
        dy = []
        dz = []
        for i in range(0, len(Y)):
            for j in range(0, len(Y[i])):
                if map_exchange_u_2[i][j] > 0:
                    x.append(Y[i][j])
                    dx.append(0.2)
        for i in range(0, len(X)):
            for j in range(0, len(X[i])):
                if map_exchange_u_2[i][j] > 0:
                    y.append(X[i][j])
                    dy.append(0.2)
        for i in range(0, len(map_exchange_u)):
            for j in range(0, len(map_exchange_u[i])):
                if map_exchange_u_2[i][j] > 0:
                    z.append(0)
                    dz.append(map_exchange_u_2[i][j])

        fig8 = plt.figure()
        ax8 = fig8.add_subplot(111, projection='3d')

        dzc = np.array(dz)
        colors = plt.cm.Reds(dzc / float(map_exchange_u_2.max()))
        a8 = ax8.bar3d(x, y, z, dx, dy, dz, color=colors)
        ax8.set_xlabel('X coord')
        ax8.set_ylabel('Y coord')
        ax8.set_zlabel('Redundante Nachrichten')

        ##############################################################
        ##csv

        csv_information=[average_plotter[len(average_plotter)-1], standard_deviation_per_round[len(standard_deviation_per_round)-1], calc_count, sim.get_actual_round(), u_message_count ]
        print(csv_information)
        print("unnötige Nachrichten: ", u_message_count)
        print("nachrichten: ",message_count)

        if not os.path.exists(info_plot_dir):
            os.makedirs(info_plot_dir)
        csv_name = get_free_csv_name()

        with open(csv_name, 'w') as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow(csv_information)
        plt.show()
        sim.set_end()

    ###################################################################################

    if sim.get_actual_round() > 0:
        for particle in sim.get_particle_list():
            free_space_in_dir=search_personal_space(particle,sim)
            if free_space_in_dir != -1:
                particle.move_to(free_space_in_dir)

    #if sim.get_actual_round()==200:
    #    for i in range(0,30):
    #        rnd_particle=random.choice(sim.get_particle_list())
    #        sim.remove_particle(rnd_particle.get_id())
    #        print("removed and its now:", len(sim.get_particle_list()))


def reset_to_master(particle):
    particle.sum=1
    particle.version_number=int(particle.version_number+random.randint(1,round(particle.particle_count)))
    particle.particle_count = 1
    particle.actual_round=0

def reset_particle(rnd_particle, rnd_particle_neighbour):
    rnd_particle.sum = 0
    rnd_particle.particle_count= 0
    rnd_particle.version_number= rnd_particle_neighbour.version_number
    rnd_particle.actual_round = 0

def get_free_csv_name() -> str:
    i = 0
    while(os.path.isfile(info_plot_dir+'info_plot_'+str(i)+'.csv')):
        i+=1
    return info_plot_dir+'info_plot_'+str(i)+'.csv'

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


def search_personal_space(particle, sim):
    dir = [0, 1, 2, 3, 4, 5]
    while len(dir) != 0:
        rnd_dir = random.choice(dir)
        if particle.particle_in(rnd_dir) or\
                abs(particle.coords[0]+x_offset[rnd_dir])>sim.get_world_x_size() or\
                abs(particle.coords[1]+y_offset[rnd_dir])>sim.get_world_y_size():
            dir.remove(rnd_dir)
        else:
            return rnd_dir
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


