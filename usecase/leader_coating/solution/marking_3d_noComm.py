import random
import math



class Location:
    def __init__(self, coords):
        self.coords = coords
        self.adjacent = {}
        self.visited = False
        self.next_to_wall = False

    def __eq__(self, other):
        return self.coords == other.coords

    def __str__(self):
        return str(self.coords) + ' | Adjacent: ' + str(
            [(direction, location.coords, location.next_to_wall) for direction, location in self.adjacent.items()])


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


# Returns the direction of an adjacent location relative to the current location
def get_dir(current_location, target_location):
    return target_location.coords[0] - current_location.coords[0], \
           target_location.coords[1] - current_location.coords[1], \
           target_location.coords[2] - current_location.coords[2]


# Adds a new location to a graph
def add_location_to_graph(world, graph, location, directions):
    if location in graph:
        return

    graph.append(location)
    location.visited = True

    for direction in directions:

        adjacent_location_coords = world.grid.get_coordinates_in_direction(location.coords,
                                                                           world.grid.get_directions_list()[direction])
        if location_exists(graph, adjacent_location_coords):
            if location in get_location_with_coords(graph, adjacent_location_coords).adjacent.values():
                continue
            get_location_with_coords(graph, adjacent_location_coords).adjacent[
                get_opposite_bearing(world, direction)] = location

        if is_border(world, adjacent_location_coords):
            if location.next_to_wall is True:
                continue

            location.next_to_wall = True
            continue


# Checks if the given coordinates are valid simulator coordinates
def valid_sim_coords(world, coords):
    return world.grid.are_valid_coordinates(coords)


# Checks if the location at the given coordinates is a border or not
def is_border(world, coords):
    for tile in world.get_tiles_list():
        if coords == tile.coordinates:
            return True
    return False


# Initializes the new custom particle attributes
def set_particle_attributes(world, particle, search_alg):
    directions = list(range(len(world.grid.get_directions_list())))
    search_algo = []

    if search_alg == 0:
        search_algo.append(0)
    elif search_alg == 1:
        search_algo.append(-1)
    elif search_alg == 2:
        search_algo.append(-1)
        search_algo.append(0)

    search_algorithm = random.choice(search_algo)

    setattr(particle, "direction", directions)
    setattr(particle, "search_algorithm", search_algorithm)

    setattr(particle, "unvisited_queue", [])
    setattr(particle, "visited", [])
    setattr(particle, "graph", [])

    setattr(particle, "origin_coords", particle.coordinates)
    setattr(particle, "start_location", Location(particle.origin_coords))

    setattr(particle, "current_location", None)
    setattr(particle, "next_location", None)
    setattr(particle, "target_location", particle.start_location)
    setattr(particle, "stuck_location", None)
    setattr(particle, "alternative_location", None)
    setattr(particle, "bearing", None)

    setattr(particle, "previous_location", None)
    setattr(particle, "last_visited_locations", [])
    setattr(particle, "alternative_locations", [])
    setattr(particle, "reverse_path", [])

    setattr(particle, "stuck", False)
    setattr(particle, "alternative_reached", True)
    setattr(particle, "target_reached", True)
    setattr(particle, "done", False)


# Discovers the adjacent (Neighbour) locations relative to the particle's current location
def discover_adjacent_locations(world, particle):
    for direction in particle.direction:

        adjacent_location_coords = world.grid.get_coordinates_in_direction(particle.current_location.coords,
                                                                           world.grid.get_directions_list()[direction])

        if not valid_sim_coords(world, adjacent_location_coords):
            continue

        if is_border(world, adjacent_location_coords):
            if particle.current_location.next_to_wall is True:
                continue
            particle.current_location.next_to_wall = True
            continue

        if location_exists(particle.graph, adjacent_location_coords):
            if get_location_with_coords(particle.graph,
                                        adjacent_location_coords) in particle.current_location.adjacent.values():
                continue
            particle.current_location.adjacent[direction] = get_location_with_coords(particle.graph,
                                                                                    adjacent_location_coords)
            continue

        new_location = Location(adjacent_location_coords)
        particle.create_location_on(adjacent_location_coords)
        world.new_location.set_color((0.0, 0.0, 1.0, 1.0))
        particle.current_location.adjacent[direction] = new_location
        particle.unvisited_queue.append(new_location)
        add_location_to_graph(world, particle.graph, new_location, particle.direction)


# Marks the particle's current location as visited and removes it from the particle's unvisited queue
def mark_location(world, particle):
    particle.current_location.visited = True
    particle.visited.append(particle.current_location)
    particle.unvisited_queue = [location for location in particle.unvisited_queue if location not in particle.visited]
    current_location = world.location_map_coordinates[particle.coordinates]

    if current_location.color == (0.0, 0.8, 0.8, 1.0):
        return

    particle.delete_location()
    particle.create_location()
    world.new_location.set_color((0.0, 0.8, 0.8, 1.0))


# Returns the distance between 2 locations
def get_distance(location1, location2):
    x1 = location1.coords[0]
    x2 = location2.coords[0]

    y1 = location1.coords[1]
    y2 = location2.coords[1]

    z1 = location1.coords[2]
    z2 = location2.coords[2]

    return abs(math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2) + ((z2 - z1) ** 2)))


# Returns the nearest location in the particle's unvisited queue relative to the particle's current location
def get_nearest_unvisited(particle):
    possible_unvisited_locations = []
    for location in particle.unvisited_queue:
        possible_unvisited_locations.append((round(get_distance(particle.current_location, location)), location))

    return min(possible_unvisited_locations, key=lambda t: t[0])[1]


# Returns the next best possible move if the particle's target location is not adjacent to it (path generator)
def get_best_location(particle, target_location):
    possible_moves = []

    for location in particle.current_location.adjacent.values():
        possible_moves.append((get_distance(location, target_location), location))

    best_location = min(possible_moves, key=lambda t: t[0])[1]

    return best_location


# Follows wall
def follow_wall(world, particle, target_location):
    possible_moves = []

    for location in particle.current_location.adjacent.values():

        if location in particle.last_visited_locations:
            continue

        if location.next_to_wall or not location.visited:
            possible_moves.append((get_distance(location, target_location), location))
            particle.alternative_locations.append((get_distance(location, target_location), location))

    if len(possible_moves) == 0:
        for location in particle.current_location.adjacent.values():

            if location in particle.last_visited_locations:
                continue

            if not is_border(world, location.coords):
                possible_moves.append((get_distance(location, target_location), location))
                particle.alternative_locations.append((get_distance(location, target_location), location))

    best_location = min(possible_moves, key=lambda t: t[0])[1]

    return best_location


# Returns the next closest unvisited location relative to the particle's current location
def get_next_unvisited(particle):
    if particle.unvisited_queue[particle.search_algorithm] not in particle.current_location.adjacent.values():
        return get_best_location(particle, get_nearest_unvisited(particle))

    else:
        return particle.unvisited_queue[particle.search_algorithm]


# Returns the direction of the target location relative to the current location
def get_bearing(world, current_location, target_location):
    dirs = world.grid.get_directions_list()

    if current_location == target_location:
        return 0

    d = world.grid.get_nearest_direction(current_location.coords, target_location.coords)

    index = 0
    for direction in dirs:
        if d == direction:
            break
        else:
            index += 1

    return index


# Checks if the path to the target is obstructed by a wall or obstacle
def path_blocked(world, current_location, target_location):
    if target_location in current_location.adjacent.values():
        return False

    ndb = get_bearing(world, current_location, target_location)

    if ndb not in current_location.adjacent.keys():
        return True


# Reverses particle bearing. This is used to terminate the wall following algorithm.
def get_opposite_bearing(world, bearing):

    direction = world.grid.get_directions_list()[bearing]

    return get_bearing(world, Location(direction), Location(world.grid.get_center()))


# Checks if a particle's way is blocked by a wall or obstacle
def check_stuck(world, particle, target_location):
    if path_blocked(world, particle.current_location, target_location):
        return True

    return False


# Returns the next location to move to
def get_next_location(world, particle, target_location):
    if target_location in particle.current_location.adjacent.values():
        particle.target_reached = True
        return target_location

    else:
        if check_stuck(world, particle, target_location):
            particle.stuck = True
            particle.bearing = get_bearing(world, particle.current_location, particle.target_location)
            particle.stuck_location = particle.current_location
            particle.last_visited_locations.append(particle.current_location)
            return follow_wall(world, particle, target_location)

        else:
            return get_best_location(particle, target_location)


# Handles the movement of the particle through the terrain
def move(world, particle, next_location):
    particle.previous_location = particle.current_location
    next_direction = get_dir(particle.current_location, next_location)
    particle.current_location = next_location
    mark_location(world, particle)
    particle.move_to(next_direction)
    particle.current_location = get_location_with_coords(particle.graph, particle.coordinates)
    discover_adjacent_locations(world, particle)


def solution(world):

    if world.config_data.max_round == world.get_actual_round():
        print("last round! (if not yet finished = max_round to small)")

    # 0 = BFS, 1 = DFS, 2 = MIXED
    search_algorithm = 2

    for particle in world.get_particle_list():

        if world.get_actual_round() == 1:
            set_particle_attributes(world, particle, search_algorithm)
            particle.current_location = particle.start_location
            particle.create_location_on(particle.origin_coords)
            world.new_location.set_color((0.0, 0.0, 1.0, 1.0))
            add_location_to_graph(world, particle.graph, particle.current_location, particle.direction)
            discover_adjacent_locations(world, particle)
            continue

        else:

            if not particle.alternative_reached:

                if particle.alternative_location in particle.current_location.adjacent.values():
                    particle.alternative_reached = True
                    particle.alternative_locations.clear()
                    particle.reverse_path.clear()
                    particle.next_location = particle.alternative_location
                    move(world, particle, particle.next_location)
                    if len(particle.unvisited_queue) <= 0:
                        mark_location(world, particle)
                        world.success_termination()
                        return
                    continue

                particle.next_location = particle.reverse_path.pop()
                move(world, particle, particle.next_location)
                if len(particle.unvisited_queue) <= 0:
                    mark_location(world, particle)
                    world.success_termination()
                    return
                continue

            if particle.stuck:
                particle.alternative_locations = [item for item in particle.alternative_locations
                                                  if item[1].coords != particle.current_location.coords]

                if particle.current_location not in particle.last_visited_locations:
                    particle.last_visited_locations.append(particle.current_location)

                if particle.current_location.coords != particle.stuck_location.coords:

                    if get_bearing(world, particle.current_location, particle.stuck_location) == \
                            get_opposite_bearing(world, particle.bearing):
                        particle.stuck = False
                        particle.last_visited_locations.clear()
                        particle.alternative_locations.clear()
                        continue

                if particle.target_location in particle.current_location.adjacent.values():
                    particle.stuck = False
                    particle.target_reached = True
                    particle.last_visited_locations.clear()
                    particle.alternative_locations.clear()
                    particle.next_location = particle.target_location
                    move(world, particle, particle.next_location)
                    if len(particle.unvisited_queue) <= 0:
                        mark_location(world, particle)
                        return
                    continue

                try:
                    next_location = follow_wall(world, particle, particle.target_location)
                    particle.next_location = next_location
                    move(world, particle, particle.next_location)
                    if len(particle.unvisited_queue) <= 0:
                        mark_location(world, particle)
                        return
                    continue

                except ValueError:
                    particle.reverse_path = particle.last_visited_locations.copy()
                    del particle.reverse_path[-1]
                    particle.alternative_location = min(particle.alternative_locations, key=lambda t: t[0])[1]
                    particle.alternative_reached = False
                    continue

            if not particle.target_reached:
                particle.next_location = get_next_location(world, particle, particle.target_location)
                move(world, particle, particle.next_location)
                if len(particle.unvisited_queue) <= 0:
                    mark_location(world, particle)
                    return
                continue

            if len(particle.unvisited_queue) > 0:

                if particle.unvisited_queue[particle.search_algorithm] in particle.current_location.adjacent.values():
                    particle.target_reached = True
                    particle.next_location = particle.unvisited_queue[particle.search_algorithm]
                    move(world, particle, particle.next_location)
                    if len(particle.unvisited_queue) <= 0:
                        mark_location(world, particle)
                        return
                    continue

                else:
                    nearest_unvisited = get_nearest_unvisited(particle)

                    if nearest_unvisited in particle.current_location.adjacent.values():
                        particle.target_reached = True
                        particle.next_location = nearest_unvisited
                        move(world, particle, particle.next_location)
                        if len(particle.unvisited_queue) <= 0:
                            mark_location(world, particle)
                            return
                        continue

                    else:
                        particle.target_reached = False
                        particle.target_location = nearest_unvisited
                        particle.next_location = get_next_location(world, particle, particle.target_location)
                        move(world, particle, particle.next_location)
                        if len(particle.unvisited_queue) <= 0:
                            mark_location(world, particle)
                            return
                        continue

            if len(particle.unvisited_queue) <= 0:
                mark_location(world, particle)
                return
