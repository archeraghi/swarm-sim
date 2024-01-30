import time
from copy import deepcopy

QUICK_COATING = True
STEP_COUNTER = False

ONE_LAYER_COATING = False

CAVING = True
ORDERING = True

TRAIL = 1000
PREVIOUS = 10
FREE = 103
TOTAL_FREE = 10000
OCCUPIED = 200

ENTRANCE_1 = TOTAL_FREE + 2 * OCCUPIED + FREE + PREVIOUS + TRAIL

TRAIL_1 = 4 * OCCUPIED + TRAIL + PREVIOUS
TRAIL_2 = 3 * OCCUPIED + 1 * FREE + PREVIOUS + TRAIL
TRAIL_3 = 2 * OCCUPIED + 3 * FREE + PREVIOUS
TRAIL_4 = 3 * OCCUPIED + 2 * FREE + PREVIOUS

DEAD_END = 5 * OCCUPIED + PREVIOUS

CORNER = 4 * OCCUPIED + FREE + PREVIOUS


def next_leader(world, object_index_dictionary, subject_index_dictionary):
    leader, distance, closest_object_location = get_leader_distance_to_object(world, object_index_dictionary,
                                                                              subject_index_dictionary)
    leader.set_color((0.0, 1, 0.0, 1.0))
    setattr(leader, "own_location", leader.coordinates)
    setattr(leader, "previous_location", ())
    setattr(leader, "subject_locations", subject_index_dictionary.copy())
    if leader.own_location in leader.subject_locations:
        if isinstance(leader.subject_locations, dict):
            del leader.subject_locations[leader.own_location]
        else:
            leader.subject_locations.remove(leader.own_location)
    leader.subject_locations = sorting_list(leader.own_location, leader.subject_locations,
                                            leader.world.grid.get_distance)

    return leader, closest_object_location, distance


def solution(world):
    if world.get_actual_round() == 1:
        leader, object_location, distance = next_leader(world, world.tile_map_coordinates,
                                                        world.particle_map_coordinates)
        if leader:
            uncoated_locations = []
            if distance != 1:
                leader.own_location = go_for(object_location, leader.own_location, leader)
            while leader.subject_locations:
                uncoated_locations = scan_outside(leader)
                if QUICK_COATING:
                     beaming(leader, uncoated_locations)
                else:
                    coat(leader, uncoated_locations)
                world.csv_round.update_layer()
            coat_yourself(leader, uncoated_locations)


def move_to(direction, leader):
    leader.previous_location = leader.own_location
    leader.move_to(direction)
    refresh_screen(leader)
    return leader.coordinates


def scan_outside(leader):
    trail_locations = []
    uncoated_locations = []
    dead_end = False
    while leader.own_location not in uncoated_locations:
        environment, neighborhood = scan_environment(
            leader.matter_in,
            leader.world.grid.get_nearest_direction(leader.own_location,
                              leader.previous_location), leader.world.grid.get_directions_list())
        if trail_entrance(environment) and leader.own_location not in trail_locations:
            direction = get_trail_direction_entrance(leader, environment, neighborhood)
            trail_exit = leader.own_location
            previous_location = leader.previous_location
            trail_locations, inside_environment, neighborhood = scan_trail(leader, direction)
            if inside_environment == DEAD_END:
                dead_end = True
            else:
                # If there is an a big area than
                uncoated_locations = uncoated_locations + scan_inside(leader, inside_environment, neighborhood, trail_locations)
            get_out(leader, trail_exit)
            environment, neighborhood = get_environment_special_triangular(environment, leader, previous_location)
        else:
            uncoated_locations.append(leader.own_location)
        direction = neighborhood[FREE]
        if direction:
            leader.own_location = move_to(direction, leader)
    if not_enough_subjects(len(leader.subject_locations) + 1, len(uncoated_locations), len(trail_locations)):
        uncoated_locations = reduce_scanned_locations(leader.subject_locations, uncoated_locations, trail_locations,
                                                      dead_end)
    elif dead_end:
        uncoated_locations = uncoated_locations + trail_locations
    return uncoated_locations


def get_environment_special_triangular(environment_type, leader, previous_location):
    if environment_type == ENTRANCE_1:
        environment, neighborhood = scan_environment(
            leader.matter_in,
            leader.world.grid.get_nearest_direction(leader.own_location,
                              previous_location), leader.world.grid.get_directions_list())
    else:
        environment, neighborhood = scan_environment(
            leader.matter_in,
            leader.world.grid.get_nearest_direction(leader.own_location,
                              leader.previous_location), leader.world.grid.get_directions_list())
    return environment, neighborhood


def not_enough_subjects(subjects_cardinality, uncoated_cardinality, trail_cardinality):
    if subjects_cardinality < uncoated_cardinality + trail_cardinality:
        return True
    return False


def reduce_scanned_locations(subject_locations, uncoated_locations, trail_locations, dead_end):
    subjects_cardinality = len(subject_locations) + 1  # for the leader
    trail_cardinality = len(trail_locations)
    if subjects_cardinality < trail_cardinality:
        if not dead_end:
            trail_locations.pop()
        uncoated_locations = reduce_trail_locations(trail_locations, subjects_cardinality)
    else:
        uncoated_locations = uncoated_locations[0:subjects_cardinality - trail_cardinality] + trail_locations
    return uncoated_locations


def reduce_trail_locations(trail_locations, subjects_cardinality):
    i = 0
    while  len(trail_locations) > subjects_cardinality and trail_locations:
        if i % 2 == 0:
            trail_locations.pop(0)
        elif i % 2 == 1:
            trail_locations.pop()
        i += 1
    return trail_locations


def remove_trail_ending(uncoated_locations, trail_locations):
    uncoated_locations.insert(0, trail_locations.pop())
    trail_cardinality = len(trail_locations)
    return trail_cardinality


def trail_entrance(environment_type):
    if environment_type == TRAIL_2 or environment_type == TRAIL_3 \
            or environment_type == ENTRANCE_1:
        return True


def get_trail_direction_entrance(leader, environment, neighborhood):

    if environment == TRAIL_2 or environment == TRAIL_3:
        direction_to_trail_entrance = handle_special_case_between_trail_entrance(leader)
    elif environment == ENTRANCE_1:
        direction_to_trail_entrance = neighborhood[TRAIL]
    return direction_to_trail_entrance


def handle_special_case_between_trail_entrance(leader):
    direction_exit_from_trail = get_exit_direction(leader)
    own = leader.own_location
    leader.move_to(direction_exit_from_trail)
    leader.own_location = leader.coordinates
    leader.world.csv_round.update_metrics(steps=- 1)
    direction_to_trail_entrance = leader.world.grid.get_nearest_direction(leader.own_location, own)
    return direction_to_trail_entrance


def get_exit_direction(leader):
    direction_exit_from_trail = ()
    directions_list = leader.world.grid.get_directions_list()
    for idx in range(len(directions_list)):
        if leader.world.grid.get_coordinates_in_direction(leader.own_location,
                                         directions_list[idx % len(directions_list)]) \
                == leader.previous_location:
            direction_left = directions_list[(idx + 1) % len(directions_list)]
            direction_right = directions_list[(idx - 1) % len(directions_list)]
            if leader.matter_in(direction_right) is False:
                direction_exit_from_trail = direction_right
            else:
                direction_exit_from_trail = direction_left
    return direction_exit_from_trail


def scan_inside(leader, environment, neighborhood, trail_locations):
    uncoated_locations = []
    trail_locations = special_case_corner_triangular_graph(leader, environment, trail_locations)
    leader.previous_location = leader.own_location
    leader.move_to(neighborhood[FREE])
    leader.own_location = leader.coordinates
    while leader.own_location not in trail_locations:
        environment, neighborhood = scan_environment(leader.matter_in, leader.world.grid.get_nearest_direction(leader.own_location,
                                                                           leader.previous_location), leader.world.grid.get_directions_list())

        uncoated_locations.append(leader.own_location)
        direction = neighborhood[FREE]
        if direction:
            leader.own_location = move_to(direction, leader)
    return uncoated_locations


def special_case_corner_triangular_graph(leader, environment_type, trail_locations):
    if environment_type == CORNER:
        if leader.own_location in trail_locations:
            trail_locations.remove(leader.own_location)
    return trail_locations


def scan_trail(leader, direction):
    trail_locations=[leader.own_location]
    leader.own_location = move_to(direction, leader)
    trail_locations.append(leader.own_location)
    environment, neighborhood = scan_environment(leader.matter_in,
                                                 leader.world.grid.get_nearest_direction(leader.own_location,
                                                                                         leader.previous_location),
                                                 leader.world.grid.get_directions_list())
    environment_type = environment
    while environment_type < TOTAL_FREE \
            and environment_type != DEAD_END and environment_type != CORNER:
        direction = get_next_direction_in_trail(leader, environment, neighborhood)
        leader.own_location = move_to(direction, leader)
        trail_locations.append(leader.own_location)
        environment, neighborhood = scan_environment(leader.matter_in,
                                       leader.world.grid.get_nearest_direction
                                       (leader.own_location, leader.previous_location),
                                                     leader.world.grid.get_directions_list())
        environment_type = environment
    return trail_locations, environment, neighborhood


def get_next_direction_in_trail(leader, environment, neighborhood):
    direction = ()
    if environment == TRAIL_1 or environment == TRAIL_2:
        direction = neighborhood[TRAIL]
    elif environment == TRAIL_3 or environment == TRAIL_4:
        direction = special_case_tg_in_trail(direction, leader, neighborhood[FREE])

    return direction


def special_case_tg_in_trail(direction, leader, neighbor_direction):
    exit_direction = get_exit_direction(leader)
    if exit_direction != neighbor_direction:
        direction = neighbor_direction
    return direction


def get_direction_for(source, destiny):
    if destiny and source:
        new_direction = []
        for i in range(len(source)):
            new_direction.append(destiny[i] - source[i])
        return tuple(new_direction)
    else:
        return False


# def get_location_in_direction(position, direction):
#     new_pos = []
#     for i in range(len(position)):
#         new_pos.append(position[i] + direction[i])
#     return tuple(new_pos)


def scan_environment(matter_in, previous_direction, directions_list):
    sum_of_neighbors_labels = 0
    directions_maps_neighbors = {}
    neighborType_maps_direction = {}

    for idx in range(len(directions_list)):
        direction_view = directions_list[idx % len(directions_list)]
        if direction_view == previous_direction:
            type_number = PREVIOUS
        else:
            direction_left = directions_list[(idx - 1) % len(directions_list)]
            direction_right = directions_list[(idx + 1) % len(directions_list)]
            type_number = label_neighbor( matter_in(direction_view),matter_in(direction_left), matter_in(direction_right))
        sum_of_neighbors_labels += type_number
        directions_maps_neighbors[direction_view] = type_number
        neighborType_maps_direction[type_number] = direction_view
    return  sum_of_neighbors_labels, neighborType_maps_direction


def label_neighbor(matter_in_view, matter_in_left, matter_in_right):
    if matter_in_view is False:
        if matter_in_left is True and matter_in_right is True:
            return TRAIL
        elif matter_in_left is True and matter_in_right is False \
                or matter_in_right is True and matter_in_left is False:
            return FREE
        elif matter_in_left is False and matter_in_right is False:
            return TOTAL_FREE
    else:
        return OCCUPIED


def get_out(leader, exit_location):
    if leader.own_location != exit_location:
        leader.own_location = go_for(exit_location, leader.own_location, leader)
        leader.own_location = move_to(leader.world.grid.get_nearest_direction(leader.own_location, exit_location), leader)
    return


def coat(leader, uncoated_locations):
    while uncoated_locations and leader.subject_locations:
        subject_location = leader.subject_locations.pop(0)
        leader.own_location = go_for(subject_location, leader.own_location, leader)
        leader.take_particle_on(subject_location)
        uncoated_location = uncoated_locations.pop()
        leader.own_location = go_for(uncoated_location, leader.own_location, leader)
        leader.drop_particle_on(uncoated_location)


def coat_yourself(leader, uncoated_locations):
    if not uncoated_locations:
        uncoated_locations = scan_outside(leader)
        leader.world.csv_round.update_layer()

    aim = uncoated_locations.pop()
    shortest_path = get_shortest_path(leader.own_location, aim, leader.world)

    while leader.own_location != aim:
        next_location = shortest_path.pop(0)
        leader.own_location = move_to(leader.world.grid.get_nearest_direction(leader.own_location, next_location), leader)
        # print("Finished")
    finished(leader)


def finished(leader):
    particle_distance_list = []
    locations_distance_list = []
    coated_objects = get_coated_objects_list(leader)
    create_locations(coated_objects, leader, particle_distance_list)
    for location in leader.world.locations:
        locations_distance_list.append(get_distance_to_closest_tile(location.coordinates, leader.world))
    if particle_distance_list and locations_distance_list:
        check_valid_type(locations_distance_list, particle_distance_list, leader)


def create_locations(coated_objects, leader, particle_distance_list):
    for particle in coated_objects:
        for direction in leader.world.grid.get_directions_list():
            if not particle.matter_in(direction):
                particle.create_location_in(direction)
        particle_distance_list.append(get_distance_to_closest_tile(particle.coordinates, leader.world))


def get_coated_objects_list(leader):
    for particle in leader.subject_locations:
        leader.world.particles.remove(leader.world.particle_map_coordinates[particle])
    if leader.world.particles:
        listi = leader.world.particles
    else:
        listi = leader.coated_particles
    return listi


def check_valid_type(locations_distance_list, particle_distance_list, leader):
    if max(particle_distance_list) <= min(locations_distance_list):
        leader.world.csv_round.update_valid(1)
        print("Valid")
        leader.state = "End"
        leader.world.set_successful_end()
    else:
        leader.world.csv_round.update_valid(0)
        leader.world.set_unsuccessful_end()


def sorting_list(source_location, destiny_locations_list, get_distance, reverse=False):
    distances = []
    tmp_dict = {}
    sorted_list = []
    for destiny_location in destiny_locations_list:
        calculated_distance = get_distance(source_location, destiny_location)
        distances.append(calculated_distance)
        tmp_dict[destiny_location] = calculated_distance
    distances.sort(reverse=reverse)
    for distance in distances:
        for coords, dist in tmp_dict.items():
            if distance == dist and coords not in sorted_list:
                sorted_list.append(coords)
    return sorted_list


def get_leader_distance_to_object(world, objact_list, am_list):
    minimum_distance = None
    closest_subject = None
    closest_object_coordinate = []
    for am_location in am_list:
        for object_location in objact_list:
            value = world.grid.get_distance(am_location, object_location)
            if minimum_distance is None or (value < minimum_distance):
                minimum_distance = value
                if am_location in world.particle_map_coordinates:
                    closest_subject = world.particle_map_coordinates[am_location]
                closest_object_coordinate = object_location
    return closest_subject, minimum_distance, closest_object_coordinate


def get_shortest_path(lown_location, town_location, world):
    coord_lists = [[lown_location]]
    visited_location = [lown_location]
    counter = 10000
    while len(coord_lists) > 0 and counter > 0:
        current_list = coord_lists.pop(0)
        length = len(current_list)
        if are_aim_location_reachable(town_location, current_list[length - 1],world.grid.get_directions_list(), world.grid.get_coordinates_in_direction):
            if current_list[0] == lown_location:
                current_list.pop(0)
            current_list.append(town_location)
            return current_list
        else:
            around_last = get_all_surounding_location(current_list[length - 1], world.grid.get_directions_list(), world.grid.get_coordinates_in_direction)
            for tmp in around_last:
                if is_coord_unvisited_and_free(tmp, visited_location, world):
                    new_list = deepcopy(current_list)
                    new_list.append(tmp)
                    coord_lists.append(new_list)
                    visited_location.append(tmp)
        counter -= 1
    if counter <= 0:
        world.csv_round.update_valid(0)
        print("Time Out Breadth Search ", " from ", lown_location, " to ", town_location)
        world.set_unsuccessful_end()


def are_aim_location_reachable(own_location, bown_location, directions_list, get_location_for_direction):
    if own_location == bown_location:
        return True
    around = get_all_surounding_location(own_location, directions_list, get_location_for_direction)
    for tmp in around:
        if tmp == bown_location:
            return True
    return False


def is_coord_unvisited_and_free(coord, visited_location, world):
    if coord in visited_location:
        return False
    if coord in world.get_particle_map_coordinates():
        return False
    if coord in world.get_tile_map_coordinates():
        return False
    return True


def get_directions_list():
    directions = [(0.5, 1, 0),
                  (1, 0, 0),
                  (0.5, -1, 0),
                  (-0.5, -1, 0),
                  (-1, 0, 0),
                  (-0.5, 1, 0)]
    return directions


def get_all_surounding_location(own_location, directions_list, get_location_in_direction):
    environment_location = []
    for direction in directions_list:
        environment_location.append(get_location_in_direction(own_location, direction))
    return environment_location


def get_distance_to_closest_tile(source, world):
    distance = None
    for tile in world.get_tiles_list():
        value = world.grid.get_distance(source, tile.coordinates)
        if distance is None or (value < distance):
            distance = value
    return distance


def go_for(aim, own_location, leader):
    shortest_path = get_shortest_path(own_location, aim, leader.world)
    next_location = shortest_path.pop(0)
    while next_location != aim:
        own_location = move_to(leader.world.grid.get_nearest_direction(own_location, next_location), leader)
        if shortest_path:
            next_location = shortest_path.pop(0)
    return own_location


def refresh_screen(leader):
    if leader.world.config_data.visualization:
        round_start_timestamp = time.perf_counter()
        leader.world.vis.run(round_start_timestamp)


def beaming(leader, uncoated_locations):
    while uncoated_locations and leader.subject_locations:
        uncoated_location = uncoated_locations.pop()
        if leader.own_location == uncoated_location:
            environment, neighborhood = scan_environment(leader.matter_in,
                                                         leader.world.grid.get_nearest_direction
                                                         (leader.own_location, leader.previous_location),
                                                         leader.world.grid.get_directions_list())
            direction = neighborhood[FREE]
            if (environment == 1006 or environment == 816) and not direction:
                direction = neighborhood[FREE]
            leader.own_location = move_to(direction, leader)
            leader.world.csv_round.update_metrics(steps=-1)
        subject_location = leader.subject_locations.pop(0)
        leader.take_particle_on(subject_location)
        if STEP_COUNTER:
            shortest_path = get_shortest_path(leader.own_location, subject_location, leader.world)
            shortest_path.pop()
            leader.world.csv_round.update_metrics(steps=len(shortest_path)-1)
            refresh_screen(leader)
        leader.drop_particle_on(uncoated_location)
        if STEP_COUNTER:
            shortest_path = get_shortest_path(subject_location, uncoated_location, leader.world)
            leader.world.csv_round.update_metrics(steps=len(shortest_path)-1)
            refresh_screen(leader)


