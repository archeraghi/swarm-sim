import random
import array
import numpy
import math



def scenario(sim):

    ##Generator settings
    sim_count_particle=140
    prio_setx1 = 12
    prio_setx2 = 12
    prio_setx3 = 12
    prio_setx4 = 12
    prio_setx5 = 12
    prio_setx6 = 12
    prio_sety1 = 12
    prio_sety2 = 12
    prio_sety3 = 12
    prio_sety4 = 12
    prio_sety5 = 12
    prio_sety6 = 12

    #Denisty settings
    min_connection = 1  # 1 - 6
    max_connection = 2  # min - 6
    global_density_factor = 0.9  # 0-0.9 / 0-90%


    #prio_map example

    ##x 1 2 3 3 2 1
    #y# # # # # # #
    #1# 2 3 4 4 3 2
    #2# 3 4 5 5 4 3
    #3# 4 5 6 6 5 4
    #3# 4 5 6 6 5 4
    #2# 3 4 5 5 4 3
    #1# 2 3 4 4 3 2

    ##########################################################
    #Help : min/max-connection

    ## setting: min = 1 , max = 2 --> connectied in a line
    ## setting: min = 2 , max = 2 --> lowest density
    ## setting: min = 2 , max = 5 --> low chance for high density
    ## setting: min = 5 , max = 5 --> high chance for high density
    ## setting: min = 4 , max = 4 --> medium density
    ## setting: min = 6 , max = 6 --> max density

    if min_connection == 0:
        global_density_factor=0.5

    def prio_sim_size(global_density_factor):
        if global_density_factor > 0.9:
            global_density_factor = 0.9
        prio_sim_size_length=6
        while(prio_sim_size_length < int((math.sqrt( sim.get_sim_y_size() * sim.get_sim_x_size())))):
            if (sim_count_particle > (prio_sim_size_length*prio_sim_size_length)/int((1/global_density_factor))):
                prio_sim_size_length+=6
                #
                #
            else:
                print("Sim_size_lenth",prio_sim_size_length)
                break
        return prio_sim_size_length

    count_particle = prio_sim_size(global_density_factor)
    prio_x = numpy.empty(count_particle, dtype=object)
    prio_y = numpy.empty(count_particle, dtype=object)

    def prio_mapping_x(vx1,vx2,vx3,vx4,vx5,vx6,prio_x,count_particle):
        halv=int(count_particle/2)
        var_a=int(halv/3)
        for x1 in range(0,var_a):
            prio_x[x1]= vx1
        for x2 in range(var_a,var_a*2):
            prio_x[x2]= vx2
        for x3 in range(var_a*2,halv):
            prio_x[x3]= vx3
        for x4 in range(halv,halv+var_a):
            prio_x[x4]= vx4
        for x5 in range(halv+var_a,halv+var_a*2):
            prio_x[x5]= vx5
        for x6 in range(halv+var_a*2,halv*2):
            prio_x[x6]= vx6
        return prio_x

    def prio_mapping_y(vy1,vy2,vy3,vy4,vy5,vy6,prio_y,count_particle):
        halv = int(count_particle / 2)
        var_a =int(halv / 3)
        for y1 in range(0, var_a):
            prio_y[y1] = vy1
        for y2 in range(var_a, var_a * 2):
            prio_y[y2] = vy2
        for y3 in range(var_a*2, halv):
            prio_y[y3] = vy3
        for y4 in range(halv , halv + var_a):
            prio_y[y4] = vy4
        for y5 in range(halv + var_a, halv + var_a * 2):
            prio_y[y5] = vy5
        for y6 in range(halv + var_a * 2, halv * 2):
            prio_y[y6] = vy6
        return prio_y

    prio_x_map=  prio_mapping_x(prio_setx1,
                 prio_setx2,
                 prio_setx3,
                 prio_setx4,
                 prio_setx5,
                 prio_setx6,
                 prio_x,
                 count_particle)

    prio_y_map = prio_mapping_y(prio_sety1,
                 prio_sety2,
                 prio_sety3,
                 prio_sety4,
                 prio_sety5,
                 prio_sety6,
                 prio_y,
                 count_particle)

    def prio_sum_map(prio_x_map,prio_y_map):
        prio_counter=0
        prio_sum = numpy.empty(len(prio_x_map)*len(prio_y_map), dtype=object)
        for prio_var1 in range(0, len(prio_x)):
            for prio_var2 in range(0, len(prio_y)):
                prio_sum[prio_counter] = prio_x_map[prio_var2] + prio_y_map[prio_var1]
                prio_counter+=1
        return prio_sum


    prio_sum_value_map=prio_sum_map(prio_x_map,prio_y_map)
    showmap = numpy.split(prio_sum_value_map,count_particle)

    def print_prio_map(showmap):
        for x in range(0,len(showmap)):
            print("\n",showmap[x])# [0]=x1+y2 ,[1]=x1+y2 ... [6]=x2+y1..

    print_prio_map(showmap)
    print("max :",max(prio_sum_value_map))
    print("Sum :",sum(prio_sum_value_map))

    def max_prio_sum_value_map(prio_sum_value_map):
        x = prio_sum_value_map
        get_indexes = lambda x, xs: [i for (y, i) in zip(xs, range(len(xs))) if x == y]
        max_prio_sum_value_map = get_indexes(max(prio_sum_value_map), x)
        return max_prio_sum_value_map

    max_prio_sum_value_map = max_prio_sum_value_map(prio_sum_value_map)
    print(max_prio_sum_value_map)

    def find_start(max_prio_sum_value_map):
        return random.choice(max_prio_sum_value_map)

    def position_in_prio_map_x(position, count_particle):
        posi_x=0
        while(position>=count_particle):
            posi_x+=1
            position-=count_particle
        return posi_x

    def position_in_prio_map_y(position, count_particle):
        while(position>=count_particle):
            if(position-count_particle>=0):
                position-=count_particle
        posi_y=count_particle-position
        return posi_y

    def sim_positioning_adjustment_x(count_particle,posi_x):
        halv = int(count_particle/2)
        adjustment= posi_x - halv
        return adjustment

    def sim_positioning_adjustment_y(count_particle, posi_y):
        halv = int(count_particle / 2)
        adjustment = posi_y - halv
        return adjustment

    def place_particle_randomizer(prio_sum_value_map, counter):
       a=random.choice(range(1, len(prio_sum_value_map)))
       if prio_sum_value_map[counter]>=a:
           return 1
       else:
           return 0

    def start_random_placment(sim_count_particle,prio_sum_value_map,count_particle):
        counter1 = 0
        positions_used= []

        while(len(sim.get_particle_list())<sim_count_particle):
                if(counter1 not in positions_used):
                    if place_particle_randomizer(prio_sum_value_map,counter1)==1:
                       posi_x_sim=position_in_prio_map_x(counter1,count_particle)
                       posi_y_sim=position_in_prio_map_y(counter1,count_particle)
                       posi_x_sim=sim_positioning_adjustment_x(count_particle,posi_x_sim)
                       posi_y_sim=sim_positioning_adjustment_y(count_particle,posi_y_sim)
                       if(posi_x_sim% 2 == 1):
                           posi_y_sim -= 0.5
                       sim.add_particle(-posi_y_sim,-posi_x_sim)
                       positions_used.append(counter1)
                       # if (len(sim.get_particle_list())==1):
                       #     print(len(sim.get_particle_list()))
                       #     first_particle=sim.get_particle_list()
                       #     print(first_particle[0].get_sum())
                       #     first_particle[0].set_sum(1)
                       #     print(first_particle[0].get_sum())

                counter1=(counter1+1)%(count_particle*count_particle)


    #splitter = numpy.split(prio_sum_value_map,count_particle)


    start_random_placment(sim_count_particle,prio_sum_value_map,count_particle)



