#self.sim.csv_round_writer.update_metrics( steps=1)
#                self.csv_particle_writer.write_particle(steps=1)
import random

NE = 0
E = 1
SE = 2
SW = 3
W = 4
NW = 5

#Topological or distance interaction: topological_interaction=1 -> if particles have topological interactions and 0 otherwise.
topological_interaction=0
# maximum number of Neighbors to observe
number_of_neighbors=20

#if noise=1 than in predefined time intervals the particle will move undependently of his observation
noise=0
noise_interval=10

# define minimum and maximum distance
min_distance = 2
max_distance = 7

# visual range
vr = 7

#set the initial radius to calculate density
#initialRadius=10
density_radius=5

direction = [NE, E, SE, SW, W, NW]

def density(particles):
    density_list = []
    for particle in particles:
       DensityNeighbors=particle.scan_for_particle_within(hop=density_radius)
        if DensityNeighbors is not None:
            density_list.append(len(DensityNeighbors))
        else:
            density_list.append(0)
    min_density=density_list[0]
    max_density = density_list[0]
    sum_density=density_list[0]
    for i in range(1,len(density_list)-1):
        if min_density>density_list[i]:
            min_density=density_list[i]
        if max_density<density_list[i]:
            max_density=density_list[i]
        sum_density+=density_list[i]
    avg_density=sum_density/len(particles)
    return(avg_density,min_density,max_density)


def neighbor_topological_metric_random(particle):
    neighbors=particle.scan_for_particle_within(hop=vr)
    if len(neighbors)<=number_of_neighbors:
        return neighbors
    list_neig=[]
    list_neig.append(random.choice(neighbors))
    while len(list_neig)<number_of_neighbors:
        particle1=random.choice(neighbors)
        if particle1 not in list_neig:
            list_neig.append(particle1)
    return list_neig


def solution(sim):
    safe=0
    uncomfortable=0
    critical=0
    print(len(sim.particles))
    calculated_dir=0
    sim.set_calculated_dir(0)
    sim.set_calculated_dis(0)
    sim.set_mems(0)
    [avg_density,min_density,max_density] = density(sim.particles)
    sim.set_density(avg_density)
    #density radius zu fluctuation ändern
    sim.set_densityFluctuation(max_density-min_density)
    print("round=",sim.get_actual_round())

    #check for termination
    check_termination(sim)

    for particle in sim.particles:
        # Initialisation
        init(critical, particle, safe, sim, uncomfortable)

        neighbor_in_vr = particle.scan_for_particle_within(hop=vr)
        # a lonely particle moves randomly
        if neighbor_in_vr is None:
            move_lonely_particle(particle)
        else:
            # make neighbors list based of interaction type
            nearest_neighbors = []
            middle_neighbors = []
            farthest_neighbors = []
            if topological_interaction == 1:
                '''if sim.get_actual_round()<10:
                    list_of_neighbors = neighbor_topological_metric(particle)
                else:
                    list_of_neighbors = neighbor_topological_metric_random(particle)
                '''
                list_of_neighbors = neighbor_topological_metric(particle)
                sim.set_calculated_dis(sim.get_calculated_dis() + len(list_of_neighbors))
            else:
                list_of_neighbors = neighbor_in_vr
                sim.set_calculated_dis(sim.get_calculated_dis() + len(list_of_neighbors))

            # classify your neighbors in 3 lists depending on how far they are
            classify_neighbors(particle, list_of_neighbors, nearest_neighbors, middle_neighbors,
                               farthest_neighbors, neighbor_in_vr)

            # **************** applicate flocking rules with your neighbors****************
            # seperation rule with nearest neighbors
            # uncomfortable situation
            if len(nearest_neighbors) > 0:
                calculated_dir, uncomfortable = seperation_rule(calculated_dir, nearest_neighbors, particle,
                                                                uncomfortable)

            # Alignement rule with middle neighbors
            # safe situation (interaction with all observed neighbors)
            # particle moves like middle neighbors and toward farthest neighbors
            elif len(middle_neighbors) > 0:
                calculated_dir, safe = alignment_rule(calculated_dir, farthest_neighbors, middle_neighbors, particle,
                                                      safe, sim)

            # cohesion rule with farthest neighbors
            # critical situation
            else:
                calculated_dir, critical = cohesion_rule(calculated_dir, critical, farthest_neighbors, particle)
            sim.set_calculated_dir(calculated_dir)
    sim.set_critical(critical)
    sim.set_safe(safe)
    sim.set_uncomfortable(uncomfortable)


def init(critical, particle, safe, sim, uncomfortable):
    if sim.get_actual_round() == 1:
        sim.set_critical(critical)
        sim.set_safe(safe)
        sim.set_uncomfortable(uncomfortable)
        dir = random.choice(direction)
        particle.write_memory_with(key=particle.get_id(), data=get_direction_data(dir))


def check_termination(sim):
    if size_of_one_flock(sim.particles[0], len(sim.particles)) < len(sim.particles) or \
            sim.get_actual_round() == sim.get_max_round():
        print('There is more than one Flock, Flock size=', size_of_one_flock(sim.particles[0], len(sim.particles)))
        sim.set_end()


def move_lonely_particle(particle):
    dir = random.choice(direction)
    particle.write_memory_with(key=particle.get_id(), data=get_direction_data(dir))
    particle.move_to(dir)


def cohesion_rule(calculated_dir, critical, farthest_neighbors, particle):
    critical += 1
    if len(farthest_neighbors) > 0:
        # find the direction in witch the most neighbours are reachable
        count = count_particle_in_dir(particle, farthest_neighbors)
        calculated_dir += len(farthest_neighbors)
        dir = get_max_dir(count)
        if particle.get_particle_in(dir) is None:
            particle.write_memory_with(key=particle.get_id, data=get_direction_data(dir))
            particle.move_to(dir)
            # particle.move_to_in_bounds(dir)
    return calculated_dir, critical


def alignment_rule(calculated_dir, farthest_neighbors, middle_neighbors, particle, safe, sim):
    safe += 1
    neighbors = middle_neighbors
    # get the direction in which the most of your neighbors are moving
    count = count_dir_from_memory(particle, neighbors)
    sim.set_mems(sim.get_mems() + len(neighbors))
    if len(farthest_neighbors) > 0:
        calculated_dir += len(farthest_neighbors)
        count1 = count_particle_in_dir(particle, farthest_neighbors)
        for i in range(0, 6):
            count[i] += count1[i]
    dir = get_max_dir(count)
    if particle.get_particle_in(dir) is None:
        particle.write_memory_with(key=particle.get_id, data=get_direction_data(dir))
        particle.move_to(dir)
        # particle.move_to_in_bounds(dir)
    return calculated_dir, safe


def seperation_rule(calculated_dir, nearest_neighbors, particle, uncomfortable):
    uncomfortable += 1
    calculated_dir += len(nearest_neighbors)
    # count how many particles there are in every direction
    count = count_particle_in_dir(particle, nearest_neighbors)
    dir = get_min_dir(count)
    if particle.get_particle_in(dir) is None:
        particle.write_memory_with(key=particle.get_id, data=get_direction_data(dir))
        particle.move_to(dir)
        # particle.move_to_in_bounds(dir)
    return calculated_dir, uncomfortable


#Output: the direction in which the fewest neighbors are reachable
def get_min_dir(count):
    minimum = count[0]
    for i in range(1, 5):
        if count[i] < minimum:
            minimum = count[i]
    dir_choice = []
    for i in range(0, 6):
        if count[i] == minimum:
            dir_choice.append(i)
    return random.choice(dir_choice)


#Number of particles who are reachable in each direction. e.g count[0] is the number of particles to reach by going in direction[0].
#Input: the main particle and a list of his neighbors
def count_particle_in_dir(particle, neighbours):
    count = [0, 0, 0, 0, 0, 0]
    for particle1 in neighbours:
        for dir in proportional_directions(particle.coords, particle1.coords):
            count[dir] += 1
    return count

#Output: the direction in which the most neighbors are reachable
def get_max_dir(count):
    maximum = count[0]
    for i in range(1, 6):
        if count[i] > maximum:
            maximum = count[i]
    dir_choice = []
    for i in range(0, 6):
        if count[i] == maximum:
            dir_choice.append(i)
    return random.choice(dir_choice)


#Reading from neighbors memories teh function counts how many particles are going in a direction.
#count[0] is the number of particles who went in the previous round in direction[0].
def count_dir_from_memory(particle, neighbors):
    count = [0, 0, 0, 0, 0, 0]
    for particle1 in neighbors:
        data=particle.read_from_with(matter=particle1, key=particle1.get_id())
        count[get_direction_integer(data)] += 1
    return count


# test weather a target can be reached in only one direction
def target_on_dir(x, y):
    if (y == 0) or (abs(x) == abs(y) * 0.5):
        return True
    else:
        return False


# when a target can be reached in only one direction, the function gives back this direction
def direction_of_target(x, y):
    if y == 0:
        if x > 0:
            return [E]
        return [W]
    else:
        if x == 0.5 * y:
            if x > 0:
                return [NE]
            return [SW]
        else:
            if x > 0:
                return [SE]
            return [NW]


# gives the directions in witch a target can be reached when the target by going in more than one direction as quickly
def directions_of_target(x, y):
    if y > 0:
        if x >= 1 + 0.5 * y:
            return [NE, E]
        elif x <= 0 - (1 + 0.5 * y):
            return [NW, W]
        return [NE, NW]
    else:
        if x >= 1 + 0.5 * abs(y):
            return [SE, E]
        elif x <= 0 - (1 + 0.5 * abs(y)):
            return [SW, W]
        return [SE, SW]


# gives a list of directions in witch a target-Point could be reached from an origin Point
def proportional_directions(origin, target_point):
    x = target_point[0] - origin[0]
    y = target_point[1] - origin[1]
    if target_on_dir(x, y):
        return direction_of_target(x, y)
    else:
        return directions_of_target(x, y)


# Converts the value of direction in a string in order to write it in a memory
def get_direction_data(dir):
    if dir == 0:
        return "NE"
    elif dir == 1:
        return "E"
    elif dir == 2:
        return "SE"
    elif dir == 3:
        return "SW"
    elif dir == 4:
        return "W"
    elif dir == 5:
        return "NW"


# converts the direction to its integer value
def get_direction_integer(dirr):
    if dirr == "NE":
        return 0
    elif dirr == "E":
        return 1
    elif dirr == "SE":
        return 2
    elif dirr == "SW":
        return 3
    elif dirr == "W":
        return 4
    elif dirr == "NW":
        return 5


#check if a particle is in a list
def neighbor_not_in_list(n_list, random_neighbor):
    for i in range(0,len(n_list)):
        if n_list[i]==random_neighbor:
            return 0
    return 1


#add neighbors from temp lists to the neighbors list with respecting the number of observed neighbors
def add_neighbors_to_list(particle, radius, n_list):
    temp_list=particle.scan_for_particle_in(hop=radius)
    if temp_list is not None:
        if len(temp_list)<number_of_neighbors-len(n_list):
            n_list.extend(temp_list)
        else:
            for i in range(0,number_of_neighbors-len(n_list)):
                n_list.append(temp_list[i])


#create list of neighbors to observe in a topological interaction
def neighbor_topological_metric(particle):
    n_list=[]
    radius=0
    stop=0
    while len(n_list)<number_of_neighbors and stop==0:
        if radius<vr:
            radius+=1
            add_neighbors_to_list(particle,radius,n_list)
        else:
            stop=1
    return n_list


# classify your neighbors in 3 lists: nearest neighbors (within min_distance) middle_neighbors
# (between min and max_ distance) farthest neighbors are in a distance greater than max-distance.
def classify_neighbors(particle,list_of_neighbors, nearest_neighbors, middle_neighbors, farthest_neighbors, list_vr):
    list_min = particle.scan_for_particle_within(hop=min_distance)
    list_max = particle.scan_for_particle_within(hop=max_distance)
    for particle1 in list_of_neighbors:
        if list_min is not None and particle1 in list_min:
            nearest_neighbors.append(particle1)
        elif list_max is not None and particle1 in list_max:
            middle_neighbors.append(particle1)
        elif list_vr is not None and particle1 in list_vr:
            farthest_neighbors.append(particle1)


#this function counts how many flocks there are in the world.
def size_of_one_flock(particle,n):
    flock_list = [particle]
    for i in range(0,n):
        if i>len(flock_list)-1:
            return len(flock_list)
        temp_list=flock_list[i].scan_for_particle_within(hop=vr)
        if temp_list is not None:
            for j in range(0, len(temp_list)):
                if temp_list[j] not in flock_list:
                    flock_list.append(temp_list[j])
    return len(flock_list)


