import random
from random import randint
import math

E = 0
SE = 1
SW = 2
W = 3
NW = 4
NE = 5
# S = 6  # S for stop and not south

black = 1
gray = 2
red = 3
green = 4
blue = 5
yellow = 6
orange = 7
cyan = 8
violet = 9

dirs = [E, SE, SW, W, NW, NE]
x_offset = [0.5, 1,  0.5, -0.5, -1, -0.5]
y_offset = [1, 0, -1, -1,  0, 1]

# TODO: (OPTIMIZATION) Add more sequences in dir_coords_array to randomize particle movement and rotation direction
dirs_array = [[E, SE, SW, W, NW, NE],
              [SE, SW, W, NW, NE, E],
              [SW, W, NW, NE, E, SE],
              [W, NW, NE, E, SE, SW],
              [NW, NE, E, SE, SW, W],
              [NE, E, SE, SW, W, NW],
              [E, NE, NW, W, SW, SE],
              [NE, NW, W, SW, SE, E],
              [NW, W, SW, SE, E, NE],
              [W, SW, SE, E, NE, NW],
              [SW, SE, E, NE, NW, W],
              [SE, E, NE, NW, W, SW]]


# -1 = DFS, 0 = BFS
search_algorithms = [-1, 0]


# TODO (core):
# 1) Use move_to and move_in_dir instead of move_to_coords                              DONE
# 2) Change locations to Locations                                                      DONE
# 3) Alternative solution for get_distance and get_next_best_location                   X (Is get_distance allowed?)
# 4) When is the simulation successful? Evaluate metrics                                DONE
# 5) write down what solutions features and limitation                                  DONE
# 6) develop an automated simulation tool

# TODO (Research):
# 1) Global vs Local (graph, visited and unvisited)                                     DONE
# 2) 1 vs swarm
# 3) Memory limitations and computational power
# 4) Alternative solutions for stuck particles
# 5) What do particles do when they are done?

# TODO (Ideas):
# 1) P2P swarm idea
# 2) "Can" overload of zones (Kalman lectures)


class Location:
    def __init__(self, coords):
        self.coords = coords
        self.adjacent = []
        self.visited = False

    def __eq__(self, other):
        return self.coords == other.coords

    def __str__(self):
        return str(self.coords) + ' | Adjacent: ' + str([item.coords for item in self.adjacent])


# Checks if a location exists in a graph
def location_exists(graph, coords):
    for location in graph:
        if location.coords == coords:
            return True
    return False


# Returns the location from a graph given the coordinates
def get_location_with_coords(graph, coords):
    for location in graph:
        if location.coords == coords:
            return location
    return False


# Returns the direction of a location relative to the current location
def get_dir(current_location, target_location):
    if target_location.coords[0] == current_location.coords[0] + x_offset[0] and target_location.coords[1] == current_location.coords[1] + y_offset[0]:
        return 0

    if target_location.coords[0] == current_location.coords[0] + x_offset[1] and target_location.coords[1] == current_location.coords[1] + y_offset[1]:
        return 1

    if target_location.coords[0] == current_location.coords[0] + x_offset[2] and target_location.coords[1] == current_location.coords[1] + y_offset[2]:
        return 2

    if target_location.coords[0] == current_location.coords[0] + x_offset[3] and target_location.coords[1] == current_location.coords[1] + y_offset[3]:
        return 3

    if target_location.coords[0] == current_location.coords[0] + x_offset[4] and target_location.coords[1] == current_location.coords[1] + y_offset[4]:
        return 4

    if target_location.coords[0] == current_location.coords[0] + x_offset[5] and target_location.coords[1] == current_location.coords[1] + y_offset[5]:
        return 5


# Adds a new location to a graph
def add_location_to_graph(sim, graph, location):
    if location in graph:
        return
    graph.append(location)

    for direction in dirs:
        adjacent_location_coords = sim.get_coords_in_dir(location.coords, direction)
        if location_exists(graph, adjacent_location_coords):
            if location in get_location_with_coords(graph, adjacent_location_coords).adjacent:
                continue
            get_location_with_coords(graph, adjacent_location_coords).adjacent.append(location)


def random_walk(particle):
    dir = dirs.copy()
    new_dir = random.choice(dir)
    particle.move_to_in_bounds(new_dir)


# Checks if the given coordinates are valid simulator coordinates
def valid_sim_location(sim, coords):
    if sim.check_coords(coords[0], coords[1]):
        sim_coord = sim.coords_to_sim(coords)
        if sim.get_sim_x_size() >= abs(sim_coord[0]) and sim.get_sim_y_size() >= abs(sim_coord[1]):
            return True

    return False


# Checks if the location at the given coordinates is a border or not
def is_border(sim, coords):
    for location in sim.get_location_list():
        if coords == location.coords:
            if location.color == [0, 0, 0]:
                return True
    return False


# Initializes the new custom particle attributes
def set_particle_attributes(particle):
    directions = dirs_array.copy()
    search_algo = search_algorithms.copy()

    direction = random.choice(directions)
    search_algorithm = random.choice(search_algo)

    setattr(particle, "direction", direction)
    setattr(particle, "search_algorithm", search_algorithm)

    setattr(particle, "unvisited_queue", [])
    setattr(particle, "visited", [])
    setattr(particle, "graph", [])

    setattr(particle, "origin_coords", particle.coords)
    setattr(particle, "start_location", Location(particle.origin_coords))

    setattr(particle, "current_location", particle.start_location)
    setattr(particle, "target_location", particle.start_location)  # just marks origin position for now

    setattr(particle, "last_visited_locations", [])
    setattr(particle, "stuck_locations", [])

    setattr(particle, "stuck", False)
    setattr(particle, "done", False)


# Discovers the adjacent (Neighbour) locations relative to the particle's current location
def discover_adjacent_locations(sim, particle):
    for direction in particle.direction:
        adjacent_location_coords = sim.get_coords_in_dir(particle.current_location.coords, direction)

        if not valid_sim_location(sim, adjacent_location_coords):
            continue

        if is_border(sim, adjacent_location_coords):
            continue

        if location_exists(particle.graph, adjacent_location_coords):
            if get_location_with_coords(particle.graph, adjacent_location_coords) in particle.current_location.adjacent:
                continue
            particle.current_location.adjacent.append(get_location_with_coords(particle.graph, adjacent_location_coords))
            continue

        new_location = Location(adjacent_location_coords)
        particle.create_location_on(adjacent_location_coords[0], adjacent_location_coords[1], color=blue)
        particle.current_location.adjacent.append(new_location)
        particle.unvisited_queue.append(new_location)
        add_location_to_graph(sim, particle.graph, new_location)


# Marks the particle's current location as visited and removes it from the particle's unvisited queue
def mark_location_as_visited(particle):
    particle.current_location.visited = True
    particle.visited.append(particle.current_location)
    particle.last_visited_locations.append(particle.current_location)
    particle.unvisited_queue = [location for location in particle.unvisited_queue if location not in particle.visited]
    particle.delete_location()
    particle.create_location(color=cyan)


# Returns the distance between 2 locations ########### IS THE USAGE OF THIS FUNCTION CONSIDERED GPS????????????????
def get_distance(location1, location2):
    x1 = location1.coords[0]
    x2 = location2.coords[0]

    y1 = location1.coords[1]
    y2 = location2.coords[1]

    return abs(math.sqrt(((x2 - x1)**2) + ((y2 - y1)**2)))


# Returns the nearest location in the particle's unvisited queue relative to the particle's current location
def get_nearest_unvisited(particle):
    possible_unvisited_locations = []
    for location in particle.unvisited_queue:
        possible_unvisited_locations.append((round(get_distance(particle.current_location, location)), location))

    return min(possible_unvisited_locations, key=lambda t: t[0])[1]


# Returns the next best possible move if the particle's target location is not adjacent to it (path generator)
def get_next_best_location(current_location, target_location, stuck_locations):
    possible_moves = []

    for location in current_location.adjacent:
        if location in stuck_locations:
            continue
        else:
            possible_moves.append((get_distance(location, target_location), location))

    if len(possible_moves) is 0:
        return current_location.adjacent[randint(0, len(current_location.adjacent) - 1)]

    best_location = min(possible_moves, key=lambda t: t[0])[1]

    return best_location


# Returns the next closest unvisited location relative to the particle's current location
def get_next_unvisited(particle, search_algorithm):
    if particle.unvisited_queue[search_algorithm] not in particle.current_location.adjacent:
        return get_next_best_location(particle.current_location, get_nearest_unvisited(particle), particle.stuck_locations)

    else:
        return particle.unvisited_queue[search_algorithm]


# Enables the particles to create packets with their own data and send them to one another if they are within range
def communicate(particle, communication_range):
    # TODO(OPTIMIZATION) should the particles exchange unvisited locations as well? What would be the benefit?
    packet = (particle.graph, particle.visited, particle.unvisited_queue)
    # TODO(OPTIMIZATION) What should the communication range be?
    found_particles = particle.scan_for_particle_within(hop=communication_range)

    if found_particles is None:
        return

    for particle in found_particles:
        particle.write_to_with(particle, particle.get_id(), packet)


# Enables the particle to extend its own data with the data recieved from other particles
def analyse_memory(sim, particle):
    if particle.read_whole_memory():
        for particle_id in particle.read_whole_memory():
            for location in particle.read_whole_memory()[particle_id][0]:
                if location not in particle.graph:
                    add_location_to_graph(sim, particle.graph, location)
            particle.visited.extend([location for location in particle.read_whole_memory()[particle_id][1] if
                                     location not in particle.visited])
        particle.delete_whole_memory()


# Checks if the particle's next location is in a stuck cycle or not
def next_location_in_stuck_nodes(particle, next_location):
    if next_location in particle.last_visited_locations:
        if next_location in particle.stuck_locations:
            particle.stuck = True
            return True
        else:
            # if len(particle.stuck_locations) >= 10:
            particle.stuck_locations.append(next_location)
            # particle.stuck_locations.pop(0)
            return False
    else:
        particle.last_visited_locations.append(next_location)
        return False


def solution(sim):
    done_particles = 0

    for particle in sim.get_particle_list():

        if sim.get_actual_round() == 1:
            set_particle_attributes(particle)
            particle.create_location_on(particle.origin_coords[0], particle.origin_coords[1], color=blue)
            add_location_to_graph(sim, particle.graph, particle.current_location)
            discover_adjacent_locations(sim, particle)

        else:
            # TODO(OPTIMIZATION) How often should the particles communicate if they are within range?
            if sim.get_actual_round() > 30:
                if sim.get_actual_round() % 15 == 0:
                    communicate(particle, 5)
                    # pass

            analyse_memory(sim, particle)

            # TODO(OPTIMIZATION) How many locations should form the stuck cycle? Is there a better solution?
            # if len(particle.stuck_locations) >= 20:
            if sim.get_actual_round() % 20 == 0:
                particle.stuck_locations.clear()

            try:
                next_location = get_next_unvisited(particle, particle.search_algorithm)  # 0 for BFS, -1 for DFS

                if next_location_in_stuck_nodes(particle, next_location):
                    next_location = particle.current_location.adjacent[
                        randint(0, len(particle.current_location.adjacent) - 1)]

                next_direction = get_dir(particle.current_location, next_location)
                particle.current_location = next_location
                discover_adjacent_locations(sim, particle)
                mark_location_as_visited(particle)
                particle.move_to(next_direction)

            except IndexError:
                mark_location_as_visited(particle)
                particle.current_location = get_location_with_coords(particle.graph, particle.coords)
                discover_adjacent_locations(sim, particle)

                if particle.current_location is particle.target_location:
                    particle.stuck_locations.clear()
                    done_particles += 1
                    particle.done = True
                    continue

                else:
                    particle.current_location = get_location_with_coords(particle.graph, particle.coords)

                    try:
                        next_location = get_next_best_location(particle.current_location, particle.target_location, particle.stuck_locations)

                        if next_location_in_stuck_nodes(particle, next_location):
                            next_location = particle.current_location.adjacent[
                                randint(0, len(particle.current_location.adjacent) - 1)]

                        next_direction = get_dir(particle.current_location, next_location)
                        particle.current_location = next_location

                        if location_exists(particle.graph, next_location.coords):
                            particle.move_to(next_direction)

                    except ValueError:
                        discover_adjacent_locations(sim, particle)

    if done_particles == len(sim.get_particle_list()):
        print(sim.get_actual_round())
        sim.csv_round_writer.success()
        sim.set_end()

