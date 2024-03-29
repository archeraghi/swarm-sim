from copy import deepcopy

ONE_LAYER_COATING = False

CAVING = True
ORDERING = True

ENTRANCE_LABEL = 3
PREVIOUS_LOCATION_LABEL = 11
BESIDE_PREVIOUS_LOCATION_LABEL = 5
FREE_LOCATION_LABEL = 13
FREE_L = 17
FOUR_MATTERS = 4
FIVE_MATTERS = 5
TWO_MATTERS = 2
THREE_MATTERS = 3
PL_BP_EL_FL = PREVIOUS_LOCATION_LABEL + BESIDE_PREVIOUS_LOCATION_LABEL \
                    + ENTRANCE_LABEL + FREE_LOCATION_LABEL
PL_BP_FL_FL = PREVIOUS_LOCATION_LABEL + BESIDE_PREVIOUS_LOCATION_LABEL + 2 * FREE_LOCATION_LABEL
PL_BP_EL = BESIDE_PREVIOUS_LOCATION_LABEL + ENTRANCE_LABEL \
                                                    + PREVIOUS_LOCATION_LABEL
PL_FL_FL = PREVIOUS_LOCATION_LABEL + 2* FREE_LOCATION_LABEL

PL_BP= PREVIOUS_LOCATION_LABEL + BESIDE_PREVIOUS_LOCATION_LABEL

PL_BP_FL = BESIDE_PREVIOUS_LOCATION_LABEL + PREVIOUS_LOCATION_LABEL \
                                                    + FREE_LOCATION_LABEL

PATH_HANDLING = 1001
CAVE_HANDLING = 1002
PATH_OUTSIDE_HANDLING = 1003
TILE_HANDLING = 1004

NOT_DEAD_END_CAVE = 0

leader = None

def next_leader(world, coated_locations, subject_locations):
    global leader
    leader, distance, closest_tile_coordinates = get_leader_distance_to_object(world, coated_locations, subject_locations)
    leader.set_color((0.0, 1, 0.0, 1.0))
    setattr(leader, "directions_list", world.grid.get_directions_list())
    setattr(leader, "uncoated_locations", [])
    setattr(leader, "cave_locations", [])
    setattr(leader, "path_locations", [])
    setattr(leader, "first_level_paths_cardinality", [])
    setattr(leader, "subject_locations", subject_locations.copy())
    if leader.coordinates in leader.subject_locations:
        if isinstance(leader.subject_locations, dict):
            del leader.subject_locations[leader.coordinates]
        else:
            leader.subject_locations.remove(leader.coordinates)
    leader.subject_locations = get_sorted_list_of_particles_distances(leader, leader.subject_locations)
    setattr(leader, "coated_locations", [])
    setattr(leader, "aim", ())
    setattr(leader, "previous_location", leader.aim)
    setattr(leader, "previous_storage", [])
    setattr(leader, "shortest_path", [])
    setattr(leader, "neighbors_dict", {})
    setattr(leader, "direction_to_a_neighbor_obstacle", False)
    setattr(leader, "cave_exit_storage", [])
    setattr(leader, "first_layer", True)
    setattr(leader, "dead_end_flag", False)
    setattr(leader, "state_storage", [])
    setattr(leader, "entrance_storage", None)
    setattr(leader, "state", "toTile")
    setattr(leader, "layer", 0)
    if world.config_data.seed_value >1:
        leader.subject_locations = []
        leader.subject_locations.append(particle_generator(world).coordinates)
    if distance == 1:
        setattr(leader, "state", "scanning")
    else:
        setattr(leader, "state", "toTile")
        leader.aim = closest_tile_coordinates
        leader.shortest_path = get_shortest_path(leader.coordinates, closest_tile_coordinates, leader.world)
    return leader


def solution(world):
    global leader
    if world.get_actual_round() == 1:
        leader = next_leader(world, world.tile_map_coordinates, world.particle_map_coordinates)
    if leader:
        if leader.state == "toTile":
            handle_to_tile(leader)
        elif leader.state == "scanning":
            handle_scanning(leader)
        elif leader.state == "cave_scanning":
            handle_cave_scanning(leader)
        elif leader.state == "cave_discovery":
            handle_cave_discovery(leader)
        elif leader.state == "taking":
            handle_taking(leader)
        elif leader.state == "coating":
            handle_coating(leader)
        elif leader.state == "cave_escaping":
            handle_cave_escaping(leader)
        elif leader.state == "leader_coating":
            handle_leader_coating(leader)
        elif leader.state == "finished":
            handle_finished(leader)
            world.csv_round.update_finished()


def scanning(leader, uncoated_storage):
    get_neighbors(leader)
    finished=False
    if not cave_entrance(leader):
        if len(leader.neighbors_dict) == FIVE_MATTERS:
            direction = leader.world.grid.get_nearest_direction(leader.coordinates, leader.previous_location)
        else:
            direction = other_level_scanning(leader)
        if leader.coordinates not in leader.uncoated_locations and leader.coordinates not in leader.cave_locations \
                and leader.coordinates not in leader.path_locations  and leader.coordinates != leader.aim:
            uncoated_storage.append(leader.coordinates)
        leader.previous_location = leader.coordinates
        if direction:
            leader.move_to(direction)
        elif leader.state != "cave_scanning":
            finished = True
        leader.world.csv_round.update_scanning()
    return uncoated_storage, finished


def handle_scanning(leader):
    leader.uncoated_locations, finished  = scanning(leader, leader.uncoated_locations )
    if leader.coordinates in leader.uncoated_locations or finished:
        finished_scanning(leader)

def particle_generator(world):
    return world.add_particle((3-leader.layer, 0, 0,) )

def beaming(leader):
    leader.uncoated_locations = list(dict.fromkeys(leader.uncoated_locations))
    while leader.uncoated_locations:
        uncoated_location = leader.uncoated_locations.pop()
        if leader.subject_locations:
            if leader.coordinates == uncoated_location:
                direction = next_direction(leader,True)
                leader.move_to(direction)
                leader.world.csv_round.update_metrics(steps=-1)
            subject_location =leader.subject_locations.pop(0)
            # shortest_path = get_shortest_path(leader.coordinates, subject_location, leader.world)
            # leader.world.csv_round.update_metrics(steps=len(shortest_path)-1)
            leader.take_particle_on(subject_location)
            #shortest_path = get_shortest_path(subject_location, uncoated_location, leader.world)
            # leader.world.csv_round.update_metrics(steps=len(shortest_path)-1)
            leader.drop_particle_on(uncoated_location)
            leader.coated_locations.append(uncoated_location)
        else:
            leader.aim = uncoated_location
            return
    if ONE_LAYER_COATING:
        delete_cave_entrances(leader)
        handle_finished(leader)


def handle_scanned_locations(leader):
    if not ONE_LAYER_COATING:
        if CAVING:
            if enough_particles(leader):
                if leader.dead_end_flag:
                    if leader.path_locations:
                        leader.uncoated_locations.extend(leader.path_locations)
                    if leader.cave_locations:
                        leader.uncoated_locations.extend(leader.cave_locations)
                    leader.cave_locations.clear()
                    leader.path_locations.clear()
                    leader.dead_end_flag = False
                else:
                    if leader.cave_locations:
                        leader.uncoated_locations.extend(leader.cave_locations)
                    leader.cave_locations.clear()
    else:
        if leader.path_locations:
            leader.uncoated_locations.extend(leader.path_locations)
        if leader.cave_locations:
            leader.uncoated_locations.extend(leader.cave_locations)
            leader.cave_locations.clear()
        leader.uncoated_locations = list(dict.fromkeys(leader.uncoated_locations))


def enough_particles(leader):
    #subjects_cardinality = leader.world.config_data.seed_value - particle_cnt +1
    subjects_cardinality = len(leader.world.particles)
    locations_cardinality = len(leader.uncoated_locations)
    paths_cardinality = 0
    caves_cardinality = 0
    location_tile = 0
    if leader.path_locations:
        paths_cardinality = len(leader.path_locations)
    if leader.cave_locations:
        caves_cardinality = len(leader.cave_locations)
    if leader.first_level_paths_cardinality:
        location_tile = len(leader.first_level_paths_cardinality)
    if subjects_cardinality < locations_cardinality+caves_cardinality+paths_cardinality:

        if caves_cardinality > NOT_DEAD_END_CAVE and leader.path_locations and leader.path_locations[-1] not in leader.first_level_paths_cardinality:
            leader.cave_locations.insert(0, leader.path_locations.pop())
            paths_cardinality = len(leader.path_locations)

        if subjects_cardinality <= location_tile:
            leader.uncoated_locations.clear()
            leader.uncoated_locations.extend(leader.first_level_paths_cardinality)
        elif subjects_cardinality < paths_cardinality:
            leader.uncoated_locations.clear()
            i = 0
            while i < paths_cardinality - subjects_cardinality:
                if leader.path_locations:
                    if i %2 == 0:
                        leader.path_locations.pop(0)
                    elif i %2 == 1:
                        leader.path_locations.pop()
                    i += 1
            # if lt and leader.path_locations:
            #     while lt:
            #         if leader.path_locations:
            #             # leader.path_locations.insert(0, lt.pop())
            #             leader.path_locations.append(lt.pop())

            leader.uncoated_locations.extend(leader.path_locations)

        else:
            if leader.path_locations:
                leader.uncoated_locations.extend(leader.path_locations)
            for _ in range(0, locations_cardinality + paths_cardinality - subjects_cardinality):
                if leader.cave_locations:
                    leader.cave_locations.pop()
            leader.uncoated_locations.extend(leader.cave_locations)
        return False

    return True


def finished_scanning(leader):
    if leader.first_layer:
        leader.first_layer = False
    handle_scanned_locations(leader)
    leader.aim = None
    if leader.subject_locations and leader.uncoated_locations:
        go_taking_particles(leader)
        # beaming(leader)
        # if not leader.subject_locations and (leader.uncoated_locations or leader.aim):
        #     it_is_leader_turn_to_coat(leader)
        # else:
        #     go_scanning(leader)
    elif leader.uncoated_locations:
        it_is_leader_turn_to_coat(leader)


def found_cave_entrance_go_for_cave_discovery(leader, direction_entrance):
    if leader.state == "cave_scanning":
        leader.state_storage.append("cave_scanning")
    leader.path_locations.append(leader.coordinates)
    leader.cave_exit_storage.append(leader.coordinates)
    leader.directions_entrance = direction_entrance
    leader.state = "cave_discovery"
    leader.previous_location = leader.coordinates
    leader.move_to(direction_entrance)
    leader.world.csv_round.update_cave_discovery()


def cave_entrance(leader):
    sum_of_neighbors_labels, neighbor_number_map_direction = label_neighbors(
        leader)
    if sum_of_neighbors_labels == PL_BP_FL_FL or sum_of_neighbors_labels == PL_BP_EL:
        direction_exit = neighbor_number_map_direction[BESIDE_PREVIOUS_LOCATION_LABEL]
        if leader.state != "cave_scanning":
            leader.entrance_storage = PL_BP_FL_FL
        own = leader.coordinates
        leader.move_to(direction_exit)
        if leader.coordinates in leader.uncoated_locations:
            leader.uncoated_locations.remove(leader.coordinates)
        leader.world.csv_round.update_metrics(steps=- 1)
        direction_entrance = leader.world.grid.get_nearest_direction(leader.coordinates, own)
        found_cave_entrance_go_for_cave_discovery(leader, direction_entrance)
        return True
    elif sum_of_neighbors_labels == PL_BP_EL_FL:
        if leader.state != "cave_scanning":
            leader.entrance_storagea = PL_BP_EL_FL
        direction_entrance = neighbor_number_map_direction[ENTRANCE_LABEL]
        direction_exit = neighbor_number_map_direction[BESIDE_PREVIOUS_LOCATION_LABEL]
        found_cave_entrance_go_for_cave_discovery(leader, direction_entrance)
        return True


def handle_cave_discovery(leader):
    get_neighbors(leader)
    if len(leader.neighbors_dict) == FIVE_MATTERS:
        handling_dead_end(leader)
    else:
        sum_of_neighbors_labels, neighbor_number_map_direction = label_neighbors(
            leader)
        if len(leader.neighbors_dict) < FOUR_MATTERS:
            if len(leader.neighbors_dict) == THREE_MATTERS and (sum_of_neighbors_labels == PL_FL_FL or sum_of_neighbors_labels ==  PL_BP_FL):
                direction = neighbor_number_map_direction[FREE_LOCATION_LABEL]
                store_location_in_path_list(leader, direction)
            elif len(leader.neighbors_dict) == THREE_MATTERS and sum_of_neighbors_labels == PL_BP_EL:
                direction = neighbor_number_map_direction[ENTRANCE_LABEL]
                store_location_in_path_list(leader, direction)
            elif len(leader.neighbors_dict) == TWO_MATTERS and sum_of_neighbors_labels == PL_BP_FL_FL:
                direction = neighbor_number_map_direction[FREE_LOCATION_LABEL]
                store_location_in_path_list(leader, direction)
            else:
                go_cave_scanning(leader)
        elif len(leader.neighbors_dict) == FOUR_MATTERS and sum_of_neighbors_labels == PL_BP:
            go_cave_scanning(leader)
        else:
            direction = next_direction(leader)
            store_location_in_path_list(leader, direction)


def store_location_in_path_list(leader, direction):
    if leader.coordinates not in leader.path_locations:
        leader.path_locations.append(leader.coordinates)
        if adjacent_tile(leader):
            leader.first_level_paths_cardinality.append(leader.coordinates)
    leader.previous_location = leader.coordinates
    leader.move_to(direction)


def go_cave_scanning(leader):
    if leader.coordinates not in leader.path_locations:
        leader.path_locations.append(leader.coordinates)
        if adjacent_tile(leader):
            leader.first_level_paths_cardinality.append(leader.coordinates)
    leader.state = "cave_scanning"


def handle_cave_scanning(leader):
    leader.cave_locations, finished = scanning(leader, leader.cave_locations)
    if leader.coordinates in leader.cave_locations or leader.coordinates in leader.path_locations or finished:
        go_cave_escaping(leader)


def delete_cave_entrances(leader):
    if not ONE_LAYER_COATING:
        if leader.cave_exit_storage and leader.cave_exit_storage in leader.uncoated_locations:
            leader.uncoated_locations.remove(leader.cave_exit_storage)
    leader.path_locations.clear()
    leader.cave_locations.clear()
    leader.first_level_paths_cardinality.clear()
    leader.cave_exit_storage.clear()


def other_level_scanning(leader):
    direction = next_direction(leader)
    return direction


def check_cave_entrance(leader):
    sum_of_neighbors_labels, neighbor_number_map_direction = label_neighbors(
        leader)
    if sum_of_neighbors_labels == PL_BP_FL_FL:
        direction_exit = neighbor_number_map_direction[BESIDE_PREVIOUS_LOCATION_LABEL]
        own=leader.coordinates
        leader.move_to(direction_exit)
        direction_entrance = leader.world.grid.get_nearest_direction(leader.coordinates, own )
    else:
        direction_entrance, direction_exit = get_cave_entry_and_exit( sum_of_neighbors_labels, neighbor_number_map_direction)

    return direction_entrance, direction_exit


def label_neighbors(leader):
    sum_of_neighbors_labels = 0
    neighbor_number_map_direction = {}
    for idx in range(len(leader.directions_list)):
        facing_direction = leader.directions_list[idx % len(leader.directions_list)]
        if leader.matter_in(facing_direction) is False:
            direction_left = leader.directions_list[(idx - 1) % len(leader.directions_list)]
            direction_right = leader.directions_list[(idx + 1) % len(leader.directions_list)]
            number = get_location_label(direction_left, direction_right, leader, facing_direction)
            sum_of_neighbors_labels += number
            neighbor_number_map_direction[number] = facing_direction
    return sum_of_neighbors_labels,  neighbor_number_map_direction


def get_location_label(direction_left, direction_right, leader, facing_direction):
    number = 0
    if leader.matter_in(direction_left) is True and leader.matter_in(direction_right) is True:
        number = ENTRANCE_LABEL

    elif leader.matter_in(direction_left) is True and  leader.matter_in(direction_right) is False\
            or leader.matter_in(direction_right) is True and  leader.matter_in(direction_left) is False:
        number = FREE_LOCATION_LABEL

    if leader.previous_location == leader.world.grid.get_coordinates_in_direction(leader.coordinates,
                                                                                  facing_direction):
        number = PREVIOUS_LOCATION_LABEL

    elif (leader.previous_location == leader.world.grid.get_coordinates_in_direction(leader.coordinates,
                                                                                     direction_left)
          and leader.matter_in(direction_left) is False) \
            or (leader.previous_location == leader.world.grid.get_coordinates_in_direction(leader.coordinates,
                                                                                           direction_right)
                and leader.matter_in(direction_right) is False):
        number = BESIDE_PREVIOUS_LOCATION_LABEL
    return number


def get_cave_entry_and_exit(sum_of_neighbors_labels, neighbor_number_map_direction):
    direction_entrance = None
    direction_exit = None
    if sum_of_neighbors_labels == PL_BP_EL_FL:
        direction_entrance = neighbor_number_map_direction[ENTRANCE_LABEL]
        direction_exit = neighbor_number_map_direction[FREE_LOCATION_LABEL]
    elif sum_of_neighbors_labels == PL_BP_FL_FL:
        direction_entrance = neighbor_number_map_direction[FREE_LOCATION_LABEL]
        direction_exit = neighbor_number_map_direction[BESIDE_PREVIOUS_LOCATION_LABEL]
    elif sum_of_neighbors_labels == PL_BP_EL:
        direction_entrance = neighbor_number_map_direction[ENTRANCE_LABEL]
        direction_exit = neighbor_number_map_direction[BESIDE_PREVIOUS_LOCATION_LABEL]
    if direction_entrance and direction_exit:
        return direction_entrance, direction_exit
    else:
        return None, None


def get_neighbors(leader):
    leader.neighbors_dict = {}
    leader.direction_to_a_neighbor_obstacle = None
    for dir in leader.directions_list:
        if leader.matter_in(dir):
            leader.neighbors_dict[dir] = leader.get_matter_in(dir)
            leader.direction_to_a_neighbor_obstacle = dir


def adjacent_tile(leader):
    for dir in leader.directions_list:
        if leader.matter_in(dir) and leader.get_matter_in(dir).type=="tile":
            return True
    return False


def go_cave_escaping(leader):
    leader.aim = leader.cave_exit_storage.pop()
    leader.shortest_path = get_shortest_path(leader.coordinates, leader.aim, leader.world)
    leader.state = "cave_escaping"


def handling_dead_end(leader):
    if leader.coordinates not in leader.path_locations:
        leader.path_locations.append(leader.coordinates)
        if adjacent_tile(leader):
            leader.first_level_paths_cardinality.append(leader.coordinates)
    leader.aim = leader.cave_exit_storage.pop()
    leader.shortest_path = get_shortest_path(leader.coordinates, leader.aim, leader.world)
    leader.dead_end_flag = True
    leader.state = "cave_escaping"


def handle_cave_escaping(leader):
    if reached_aim(leader.aim, leader):
        leader.previous_location = leader.coordinates
        leader.move_to(leader.world.grid.get_nearest_direction(leader.coordinates, leader.aim))
        if leader.state_storage:
            leader.state = leader.state_storage.pop()
        else:
            leader.state = "scanning"
        return


def handle_to_tile(leader):
    if reached_aim(leader.aim, leader):
        if leader.subject_locations:
            leader.previous_location = leader.coordinates
            leader.state = "scanning"
        else:
            leader.state = "finished"
    else:
        leader.world.csv_round.update_to_tile()


def handle_taking(leader):
    if reached_aim(leader.aim, leader):
        go_coating(leader)
    else:
        leader.world.csv_round.update_taking()


def go_coating(leader):
    leader.take_particle_on(leader.aim)
    leader.aim = leader.uncoated_locations.pop()
    leader.shortest_path = get_shortest_path(leader.coordinates, leader.aim, leader.world)
    leader.state = "coating"


def handle_coating(leader):
    if reached_aim(leader.aim, leader):
        leader.drop_particle_on(leader.aim)
        get_neighbors(leader)
        global particle_cnt
        if not leader.subject_locations and leader.world.config_data.seed_value>2 and  particle_cnt < leader.world.config_data.seed_value:
            leader.subject_locations.append(particle_generator(leader.world).coordinates)
            particle_cnt += 1
        if leader.uncoated_locations and leader.subject_locations:
            if ONE_LAYER_COATING and len(leader.uncoated_locations) == 1:
                it_is_leader_turn_to_coat(leader)
            else:
                go_taking_particles(leader)
        elif (not leader.uncoated_locations and leader.subject_locations and not ONE_LAYER_COATING)\
                or (not leader.uncoated_locations and not leader.subject_locations and not ONE_LAYER_COATING):
            go_scanning(leader)
        else:
            leader.aim = None
            it_is_leader_turn_to_coat(leader)


def it_is_leader_turn_to_coat(leader):
    leader.state = "leader_coating"
    if leader.aim is None:
        leader.aim = leader.uncoated_locations.pop()
    leader.shortest_path = get_shortest_path(leader.coordinates, leader.aim, leader.world)

particle_cnt=2

def go_taking_particles(leader):
    leader.scanning = False
    leader.aim = leader.subject_locations.pop(0)
    leader.shortest_path = get_shortest_path(leader.coordinates, leader.aim, leader.world)
    leader.previous_location = leader.coordinates
    leader.state = "taking"


def go_scanning(leader):
    delete_cave_entrances(leader)
    leader.layer+=1
    leader.world.csv_round.update_layer()
    leader.state = "scanning"


def handle_leader_coating(leader):
    if leader.coordinates == leader.aim:
        leader.state = "finished"
        leader.world.csv_round.update_leader_coating()
    elif reached_aim(leader.aim, leader):
        leader.state = "finished"
        leader.world.csv_round.update_leader_coating()
    else:
        leader.world.csv_round.update_leader_coating()
        # print("Finished")


def handle_finished(leader):
    particle_distance_list = []
    locations_distance_list = []
    for particle in leader.subject_locations:
        leader.world.particles.remove(leader.world.particle_map_coordinates[particle])
    if leader.world.particles:
        listi = leader.world.particles
    else:
        listi = leader.coated_particles
    for particle in listi:
        for direction in leader.world.grid.get_directions_list():
            if not particle.matter_in(direction):
                particle.create_location_in(direction)
        particle_distance_list.append(get_distance_to_closest_tile(particle.coordinates, leader.world))
    for location in leader.world.locations:
        locations_distance_list.append(get_distance_to_closest_tile(location.coordinates,leader.world))
    if particle_distance_list and locations_distance_list:
        check_valid_type(locations_distance_list, particle_distance_list, leader.world)


def check_valid_type(locations_distance_list, particle_distance_list, world):
    if max(particle_distance_list) <= min(locations_distance_list):
        leader.world.csv_round.update_valid(1)
        print ("Valid")
        world.set_successful_end()
    else:
        leader.world.csv_round.update_valid(0)
        world.set_unsuccessful_end()


def get_sorted_list_of_particles_distances(leader, listi):
    distances = []
    tmp_dict = {}
    sorted_list_of_particles_coordinates = []
    for particle in listi:
        calculated_distance = leader.world.grid.get_distance(leader.coordinates, particle)
        distances.append(calculated_distance)
        tmp_dict[particle] = calculated_distance
    distances.sort()
    for distance in distances:
        for coords, dist in tmp_dict.items():
            if distance == dist and coords not in sorted_list_of_particles_coordinates:
                sorted_list_of_particles_coordinates.append(coords)
    return sorted_list_of_particles_coordinates


def get_sorted_list_of_locations_distances(leader, location_list):
    distances = []
    tmp_dict = {}
    sorted_list_of_locations_coordinates = []
    for location in location_list:
        distance = get_distance_to_closest_tile(location, leader.world)
        distances.append(distance)
        tmp_dict[location] = distance
    distances.sort(reverse=True)
    for distance in distances:
        for coords, dist in tmp_dict.items():
            if distance == dist and coords not in sorted_list_of_locations_coordinates:
                sorted_list_of_locations_coordinates.append(coords)
    return sorted_list_of_locations_coordinates


def next_direction(leader, flagi = False):
    for idx in range(len(leader.directions_list)):
        facing_direction = leader.directions_list[idx % len(leader.directions_list)]
        direction_left = leader.directions_list[(idx - 1) % len(leader.directions_list)]
        direction_right = leader.directions_list[(idx + 1) % len(leader.directions_list)]
        if leader.matter_in(facing_direction) is True:
            if not leader.matter_in(direction_right) and \
                leader.previous_location != leader.world.grid.get_coordinates_in_direction(
                    leader.coordinates, direction_right) and leader.world.grid.get_coordinates_in_direction(
                leader.coordinates, direction_right) not in leader.uncoated_locations \
                    and leader.world.grid.get_coordinates_in_direction(leader.coordinates, direction_right) not in leader.cave_locations \
                    and leader.world.grid.get_coordinates_in_direction(leader.coordinates, direction_right) not in leader.path_locations \
                    and not flagi:
                return direction_right
            elif not leader.matter_in(direction_left) and \
                leader.previous_location != leader.world.grid.get_coordinates_in_direction(
                    leader.coordinates, direction_left) and leader.world.grid.get_coordinates_in_direction(
                    leader.coordinates, direction_left) not in leader.uncoated_locations \
                    and leader.world.grid.get_coordinates_in_direction(leader.coordinates, direction_left) not in leader.cave_locations \
                    and leader.world.grid.get_coordinates_in_direction(leader.coordinates, direction_left) not in leader.path_locations \
                    and not flagi:
                return direction_left
        elif flagi and not leader.matter_in(facing_direction) and not  leader.matter_in(direction_right) and not leader.matter_in(direction_left):
            return facing_direction


def get_an_adjacent_obstacle_directions(leader, remove_particle=False):
    leader.direction_to_a_neighbor_obstacle = None
    for dir in leader.directions_list:
        if leader.matter_in(dir):
            if remove_particle and leader.get_matter_in(dir).type == "particle" \
                    and leader.get_matter_in(dir) in leader.subject_locations:
                leader.subject_locations.remove(leader.get_matter_in(dir))
            elif remove_particle and leader.matter_in(dir) and leader.get_matter_in(dir).type == "tile":
                leader.direction_to_a_neighbor_obstacle = dir
                return True
            leader.direction_to_a_neighbor_obstacle = dir
    if bool(leader.direction_to_a_neighbor_obstacle):
        return True
    return False


def get_leader_distance_to_object(world, objact_list, am_list):
    closest_particle = None
    min = None
    for am_coordinates in am_list:
         for object_coordinates in objact_list:
            value = world.grid.get_distance(am_coordinates, object_coordinates)
            if min is None or (value < min):
                min = value
                if am_coordinates in world.particle_map_coordinates:
                    closest_particle = world.particle_map_coordinates[am_coordinates]
                closest_object_coordinate = object_coordinates
    return closest_particle, min, closest_object_coordinate


def get_shortest_path(lcoordinates, tcoordinates, world):
    coord_lists = [[lcoordinates]]
    visited_coordinates = [lcoordinates]
    while len(coord_lists) > 0:
        current_list = coord_lists.pop(0)
        length = len(current_list)
        if are_aim_coordinates_reachable(tcoordinates, current_list[length - 1], world):
            if current_list[0] == lcoordinates:
                current_list.pop(0)
            current_list.append(tcoordinates)
            return current_list
        else:
            around_last = get_all_surounding_coordinates(current_list[length - 1], world)
            for tmp in around_last:
                if is_coord_unvisited_and_free(tmp, visited_coordinates, world):
                    new_list = deepcopy(current_list)
                    new_list.append(tmp)
                    coord_lists.append(new_list)
                    visited_coordinates.append(tmp)


def are_aim_coordinates_reachable(acoordinates, bcoordinates, world):
    if acoordinates == bcoordinates:
        return True
    around = get_all_surounding_coordinates(acoordinates, world)
    for tmp in around:
        if tmp == bcoordinates:
            return True
    return False


def is_coord_unvisited_and_free(coord, visited_coordinates, world):
    if coord in visited_coordinates:
        return False
    if coord in world.get_particle_map_coordinates():
        return False
    if coord in world.get_tile_map_coordinates():
        return False
    return True


def get_all_surounding_coordinates(pcoordinates, world):
    surrounding_coordinates = []
    for direction in world.grid.get_directions_list():
        surrounding_coordinates.append(world.grid.get_coordinates_in_direction(pcoordinates, direction))
    return surrounding_coordinates


def get_distance_to_closest_tile(source, world):
    distance = None
    for tile in world.get_tiles_list():
        value = world.grid.get_distance(source, tile.coordinates)
        if distance is None or (value < distance):
            distance = value
    return distance


def reached_aim(aim, leader):
    if leader.shortest_path:
        get_neighbors(leader)
        next_location = leader.shortest_path.pop(0)
        if next_location == aim and leader.state != "leader_coating":
            return True
        else:
            next_direction = leader.world.grid.get_nearest_direction(leader.coordinates, next_location)
            next_coords = leader.world.grid.get_coordinates_in_direction(leader.coordinates, next_direction)
            if aim == next_coords and leader.state != "leader_coating":
                return True
            leader.previous_location = leader.coordinates
            leader.move_to(next_direction)
            if leader.state == "leader_coating" and leader.coordinates == aim:
                return True
            return False
    return True