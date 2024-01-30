from copy import deepcopy

ideal = False


def solution(world):
    global leader
    if world.get_actual_round() == 1:
        leader = handle_first_round(world)
    if leader:
        if leader.state == "scanning":
            handle_scanning(leader)
        elif leader.state == "cave_scanning":
            handle_cave_scanning(leader)
        elif leader.state == "toTile":
            handle_to_tile(leader)
        elif leader.state == "taking":
            handle_taking(leader)
        elif leader.state == "coating":
            handle_coating(leader)
        elif leader.state == "get_out_from_cave":
            handle_get_out_from_cave(leader)
            world.csv_round.update_out_of_cave()
        elif leader.state == "leader_coating":
            handle_leader_coating(leader)

        elif leader.state == "checking":
            handle_checking(leader)
            world.csv_round.update_checking()
        elif leader.state == "finished":
            handle_finished(leader.world)
            world.csv_round.update_finished()


def handle_first_round(world):
    leader, distance, closest_tile_coordinates = get_leader_distance_tile_coordinates(world)
    leader.set_color((0.0, 1, 0.0, 1.0))
    setattr(leader, "directions_list", world.grid.get_directions_list())
    setattr(leader, "free_coating_locations", [])
    setattr(leader, "cave_free_coating_locations", [])
    setattr(leader, "starting_location", ())
    setattr(leader, "uncoated_particles_list", world.particles.copy())
    leader.uncoated_particles_list.remove(leader)
    setattr(leader, "am_distances", get_sorted_list_of_particles_distances(leader))
    setattr(leader, "aim", ())
    setattr(leader, "previous_location", leader.aim)
    setattr(leader, "aim_path", [])
    setattr(leader, "path_list", [])
    setattr(leader, "neighbors", {})
    setattr(leader, "obstacle_direction", False)
    setattr(leader, "cave_entrance", None)
    setattr(leader, "cave_exit", None)
    setattr(leader, "cave_coating", False)
    setattr(leader, "cave_found", False)
    setattr(leader, "first_level", True)
    setattr(leader, "level", 1)
    setattr(leader, "scanning", True)
    setattr(leader, "cave_1st_location", None)

    if distance == 1:
        leader.starting_location = leader.coordinates
        setattr(leader, "state", "scanning")
        # print("Start with scanning")
    else:
        setattr(leader, "state", "toTile")
        leader.aim = closest_tile_coordinates
        leader.aim_path = find_way_to_aim(leader.coordinates, closest_tile_coordinates, leader.world)
        # print("Start with going to Tile")
    return leader


def handle_scanning(leader):
    direction, dire_exit = checking_for_a_cave(leader)
    if direction:
        leader.state = "cave_scanning"
        # print("scanning --> caving")
    elif leader.first_level:
        direction = first_level_scanning(leader)
    else:
        direction = other_level_scanning(leader)
    leader.previous_location = leader.coordinates
    leader.move_to(direction)
    leader.world.csv_round.update_scanning()
    if leader.coordinates in leader.free_coating_locations:
        leader.state = "checking"
        delete_cave_entrances(leader)
        if leader.first_level:
            # print("1st_level_scanning --> checking")
            leader.first_level = False
        # print("scanning --> checking")


def checking_for_a_cave(leader):
    get_neighbors(leader)
    direction_entry, direction_exit = check_cave_entrance(leader)
    if direction_entry and direction_exit:
        found_cave_while_scanning(leader, direction_entry, direction_exit)
    return direction_entry, direction_exit


def found_cave_while_scanning(leader, direction_entry, direction_exit):
    leader.cave_1st_location = leader.world.grid.get_coordinates_in_direction(leader.coordinates, direction_entry)
    leader.cave_entrance = leader.coordinates
    leader.cave_exit = leader.world.grid.get_coordinates_in_direction(leader.coordinates, direction_exit)
    if not ideal:
        leader.cave_found = True
        if leader.cave_entrance in leader.free_coating_locations:
            leader.free_coating_locations.remove(leader.cave_entrance)
        if leader.cave_exit in leader.free_coating_locations:
            leader.free_coating_locations.remove(leader.cave_exit)
        if leader.cave_1st_location in leader.free_coating_locations:
            leader.free_coating_locations.remove(leader.cave_1st_location)
    else:
        if leader.cave_entrance not in leader.free_coating_locations:
            leader.free_coating_locations.append(leader.cave_entrance)
        if leader.cave_exit not in leader.free_coating_locations:
            leader.free_coating_locations.append(leader.cave_exit)
        if leader.cave_1st_location not in leader.free_coating_locations:
            leader.free_coating_locations.append(leader.cave_1st_location)

    if leader.level > 1:
        if leader.cave_exit not in leader.cave_free_coating_locations:
            leader.cave_free_coating_locations.append(leader.cave_exit)
        if leader.cave_entrance not in leader.cave_free_coating_locations:
            leader.cave_free_coating_locations.append(leader.cave_entrance)
        if leader.cave_1st_location not in leader.cave_free_coating_locations:
            leader.cave_free_coating_locations.append(leader.cave_1st_location)


dead_end = 5


def handle_cave_scanning(leader):
    get_neighbors(leader)

    if len(leader.neighbors) == dead_end:
        handling_dead_end(leader)
    elif get_an_adjacent_obstacle_directions(leader, ignore_particle=True):
        direction = obstacles_free_direction(leader)
        # if get_an_adjacent_tile_directions_scanning(leader):
        if leader.coordinates != leader.cave_exit and leader.coordinates != leader.cave_entrance \
                and leader.coordinates != leader.cave_1st_location:
            leader.cave_free_coating_locations.append(leader.coordinates)
        if ideal and leader.coordinates not in leader.free_coating_locations:
            leader.free_coating_locations.append(leader.coordinates)
        # if leader.coordinates in leader.free_coating_locations and not ideal:
        #     leader.free_coating_locations.remove(leader.coordinates)
        leader.previous_location = leader.coordinates
        leader.move_to(direction)
        leader.world.csv_round.update_cave_scanning()
        if leader.coordinates == leader.cave_exit \
                or leader.coordinates == leader.cave_entrance \
                or leader.coordinates == leader.cave_1st_location:
            leader.aim = leader.cave_exit
            if leader.coordinates == leader.aim:
                # print("from caving --> scanning")
                leader.state = "scanning"
                return
            leader.aim_path = find_way_to_aim(leader.coordinates, leader.aim, leader.world)
            # print("from caving -->get out of the cave")
            leader.state = "get_out_from_cave"


def delete_cave_entrances(leader):
    if not ideal:
        if leader.cave_exit and leader.cave_exit in leader.free_coating_locations:
            leader.free_coating_locations.remove(leader.cave_exit)
        if leader.cave_1st_location and leader.cave_1st_location in leader.free_coating_locations:
            leader.free_coating_locations.remove(leader.cave_1st_location)
        if leader.cave_entrance and leader.cave_entrance in leader.free_coating_locations:
            leader.free_coating_locations.remove(leader.cave_entrance)


def other_level_scanning(leader):
    direction = obstacles_free_direction(leader)
    if leader.coordinates not in leader.free_coating_locations:
        leader.free_coating_locations.append(leader.coordinates)
    return direction


def first_level_scanning(leader):
    if get_an_adjacent_obstacle_directions(leader, ignore_particle=True):
        direction = obstacles_free_direction(leader)
        if get_an_adjacent_tile_directions_scanning(leader) and leader.coordinates not in leader.free_coating_locations:
            leader.free_coating_locations.append(leader.coordinates)
    return direction


def check_cave_entrance(leader):
    sum_of_neighbors_numbers, free_location_neighborhood_counter, neighbor_direction_map_number = give_neighbors_numbers(
        leader)
    direction_entry, direction_exit = get_cave_entry_and_exit(leader, sum_of_neighbors_numbers,
                                                              free_location_neighborhood_counter,
                                                              neighbor_direction_map_number)

    return direction_entry, direction_exit


def give_neighbors_numbers(leader):
    free_location_neighborhood_counter = 0
    sum_of_neighbors_numbers = 0
    neighbor_direction_map_number = {}
    starting_number = 0
    entrance_number = 2
    previous_location_number = 10
    exit_location_number = 5
    free_location_number = 1
    for idx in range(len(leader.directions_list)):
        direction = leader.directions_list[(idx) % len(leader.directions_list)]
        if leader.matter_in(direction) is False:
            dire_left = leader.directions_list[(idx - 1) % len(leader.directions_list)]
            dire_right = leader.directions_list[(idx + 1) % len(leader.directions_list)]
            number = starting_number
            if leader.matter_in(dire_left) is True and leader.matter_in(dire_right) is True:
                number = entrance_number
            elif leader.matter_in(dire_left) is True or leader.matter_in(dire_right) is True:
                number = free_location_number
            if leader.previous_location == leader.world.grid.get_coordinates_in_direction(leader.coordinates,
                                                                                          direction):
                number = previous_location_number
            elif (leader.previous_location == leader.world.grid.get_coordinates_in_direction(leader.coordinates,
                                                                                             dire_left) \
                  and leader.matter_in(dire_left) is False) \
                    or (leader.previous_location == leader.world.grid.get_coordinates_in_direction(leader.coordinates,
                                                                                                   dire_right) \
                        and leader.matter_in(dire_right) is False):
                number = exit_location_number
            sum_of_neighbors_numbers += number
            neighbor_direction_map_number[direction] = number
            free_location_neighborhood_counter += 1
    return sum_of_neighbors_numbers, free_location_neighborhood_counter, neighbor_direction_map_number


def get_cave_entry_and_exit(leader, sum_of_neighbors_numbers, free_location_neighborhood_counter,
                            neighbor_direction_map_number):
    direction_entry = None
    direction_exit = None
    two_free_location_in_neighborhood = 2
    three_free_location_in_neighborhood = 3
    four_free_location_in_neighborhood = 4
    entrance_number = 2
    previous_location_number = 10
    exit_location_number = 5
    free_location_number = 1
    if free_location_neighborhood_counter == two_free_location_in_neighborhood:
        for direction in neighbor_direction_map_number:
            if neighbor_direction_map_number[direction] == previous_location_number:
                direction_exit = direction
            elif neighbor_direction_map_number[direction] == entrance_number:
                direction_entry = direction
    elif free_location_neighborhood_counter == three_free_location_in_neighborhood:
        for direction in neighbor_direction_map_number:
            if neighbor_direction_map_number[direction] == entrance_number:
                direction_entry = direction
            elif neighbor_direction_map_number[direction] == exit_location_number:
                direction_exit = direction
    elif free_location_neighborhood_counter == four_free_location_in_neighborhood \
            and sum_of_neighbors_numbers == previous_location_number + exit_location_number + entrance_number + free_location_number:
        for direction in neighbor_direction_map_number:
            if neighbor_direction_map_number[direction] == entrance_number:
                direction_entry = direction
            if neighbor_direction_map_number[direction] == free_location_number:
                direction_exit = direction
    elif free_location_neighborhood_counter == four_free_location_in_neighborhood \
            and sum_of_neighbors_numbers == previous_location_number + exit_location_number + 2 * free_location_number:
        for direction in neighbor_direction_map_number:
            if neighbor_direction_map_number[direction] == exit_location_number:
                direction_exit = direction
            elif neighbor_direction_map_number[direction] == free_location_number:
                if leader.matter_in(direction) is False:
                    direction_entry = direction
    return direction_entry, direction_exit


def scan_adjacent_locations(leader):
    index_direction = leader.directions_list.index(leader.obstacle_direction)
    neighbors_string = ""
    for idx in range(len(leader.directions_list)):
        direction = leader.directions_list[(idx + index_direction) % len(leader.directions_list)]
        if leader.matter_in(direction) is True:
            neighbors_string = neighbors_string + "M"
        else:
            neighbors_string = neighbors_string + "L"
    return index_direction, neighbors_string


def get_neighbors(leader):
    leader.neighbors = {}
    leader.obstacle_direction = None
    for dir in leader.directions_list:
        if leader.matter_in(dir):
            leader.neighbors[dir] = leader.get_matter_in(dir)
            leader.obstacle_direction = dir


def handling_dead_end(leader):
    leader.aim = leader.cave_exit
    leader.aim_path = find_way_to_aim(leader.coordinates, leader.aim, leader.world)
    if leader.coordinates not in leader.cave_free_coating_locations:
        leader.cave_free_coating_locations.append(leader.coordinates)
    if ideal and leader.coordinates not in leader.free_coating_locations:
        leader.free_coating_locations.append(leader.coordinates)
    # print("from caving --> get out of the cave")
    leader.state = "get_out_from_cave"


def handle_get_out_from_cave(leader):
    if reached_aim(leader.aim, leader):
        leader.cave_coating = False
        leader.previous_location = leader.coordinates
        leader.move_to(leader.world.grid.get_nearest_direction(leader.coordinates, leader.aim))
        if leader.scanning:
            # print("from  get out of the cave --> scanning")
            leader.state = "scanning"
            return
        # print("from  get out of the cave --> checking")
        leader.state = "checking"


def handle_to_tile(leader):
    if reached_aim(leader.aim, leader):
        # print("from toTile --> 1st level scanning")
        leader.state = "scanning"
    else:
        leader.world.csv_round.update_to_tile()


def handle_taking(leader):
    if reached_aim(leader.aim, leader):
        leader.take_particle_on(leader.aim)
        if leader.cave_free_coating_locations and leader.cave_coating:
            leader.aim = leader.cave_free_coating_locations.pop()
            leader.aim_path = find_way_to_aim(leader.coordinates, leader.aim, leader.world)
        else:
            leader.cave_coating = False
            leader.aim = leader.free_coating_locations.pop()
            leader.aim_path = find_way_to_aim(leader.coordinates, leader.aim, leader.world)

        # print("from taking --> dropping")
        leader.state = "coating"
    else:
        leader.world.csv_round.update_taking()


def handle_coating(leader):
    if reached_aim(leader.aim, leader):
        leader.drop_particle_on(leader.aim)
        if leader.get_particle_in(leader.world.grid.get_nearest_direction(leader.coordinates,
                                                                          leader.aim)) in leader.uncoated_particles_list:
            leader.uncoated_particles_list.remove(
                (leader.get_particle_in(leader.world.grid.get_nearest_direction(leader.coordinates, leader.aim))))
        elif not leader.cave_free_coating_locations and leader.cave_coating:
            leader.cave_coating = False
            leader.aim = leader.cave_exit
            leader.aim_path = find_way_to_aim(leader.coordinates, leader.aim, leader.world)
            leader.state = "get_out_from_cave"
            # print("from dropping -->  to get out from cave")
            return
        get_neighbors(leader)
        dir, direction_exit = check_cave_entrance(leader)
        if dir and direction_exit and 3 <= len(leader.neighbors) < 5 and not leader.cave_found and not ideal:
            handle_cave_entrance_while_coating(dir, direction_exit, leader)
        leader.state = "checking"
        # print("from dropping -->  checking")
    else:
        if leader.cave_coating:
            leader.world.csv_round.update_cave_coating()
        else:
            leader.world.csv_round.update_coating()


def handle_cave_entrance_while_coating(dir, direction_exit, leader):
    # print("Im infront of cave")
    leader.cave_entrance = leader.coordinates
    leader.cave_1st_location = leader.world.grid.get_coordinates_in_direction(leader.coordinates, dir)
    leader.cave_exit = leader.world.grid.get_coordinates_in_direction(leader.coordinates, direction_exit)
    if leader.cave_entrance in leader.free_coating_locations and not ideal:
        leader.free_coating_locations.remove(leader.cave_entrance)
    if leader.cave_exit in leader.free_coating_locations:
        leader.free_coating_locations.remove(leader.cave_exit)
    if leader.cave_1st_location in leader.free_coating_locations:
        leader.free_coating_locations.remove(leader.cave_1st_location)


def handle_checking(leader):
    if ideal and bool(leader.free_coating_locations) and len(leader.free_coating_locations) == 1:
        leader.state = "leader_coating"
        if leader.cave_coating and leader.cave_free_coating_locations:
            leader.aim = leader.cave_free_coating_locations.pop()
        else:
            leader.aim = leader.free_coating_locations.pop()

        leader.aim_path = find_way_to_aim(leader.coordinates, leader.aim, leader.world)
        for particle in leader.uncoated_particles_list:
            leader.world.particles.remove(particle)


    elif not leader.free_coating_locations and not leader.cave_free_coating_locations:
        # print("from checking -->  scanning")
        leader.level += 1
        leader.world.csv_round.update_layer()
        leader.starting_location = leader.coordinates
        if get_an_adjacent_obstacle_directions(leader):
            leader.scanning = True
        if not leader.cave_coating:
            leader.cave_found = False
        leader.state = "scanning"


    elif leader.cave_free_coating_locations and not leader.cave_coating:
        # print("active vs locations ", (len(leader.uncoated_particles_list) + 1),
        # len(leader.cave_free_coating_locations))
        quantity_of_uncoated_particles = len(leader.uncoated_particles_list) + 1  # for the leader
        if quantity_of_uncoated_particles < len(leader.cave_free_coating_locations):
            if abs(len(leader.uncoated_particles_list) + 1 - len(leader.cave_free_coating_locations)) == 1:
                inner_cave_free_coating_location = leader.cave_free_coating_locations[-1]
                outside__cave_free_coating_location = leader.cave_free_coating_locations[0]
                distance_inner_cave_free_coating_location_to_tile = get_closest_tile_distance(
                    inner_cave_free_coating_location, leader.world)
                distance_outside_cave_free_coating_location_to_tile = get_closest_tile_distance(
                    outside__cave_free_coating_location, leader.world)
                if distance_inner_cave_free_coating_location_to_tile == distance_outside_cave_free_coating_location_to_tile:
                    leader.cave_free_coating_locations.pop(0)
                else:
                    leader.cave_free_coating_locations.pop()
            else:
                leader.cave_free_coating_locations.pop()

        leader.cave_coating = True
    else:
        # print("from checking -->  fill_up_cave", leader.cave_free_coating_locations)
        if leader.uncoated_particles_list:
            # print("from checking -->  taking")
            leader.scanning = False
            leader.am_distances = get_sorted_list_of_particles_distances(leader)
            leader.aim = leader.am_distances.pop(0)
            leader.aim_path = find_way_to_aim(leader.coordinates, leader.aim, leader.world)
            leader.previous_location = leader.coordinates
            leader.state = "taking"
        else:
            # print("It is my turn")
            leader.state = "leader_coating"
            if leader.cave_coating and leader.cave_free_coating_locations:
                leader.aim = leader.cave_free_coating_locations.pop()
            else:
                leader.aim = leader.free_coating_locations.pop()
            # if leader.coordinates == leader.aim:
            #     leader.state = "finished"
            #     #print("Finished immediatly")
            #     return
            leader.aim_path = find_way_to_aim(leader.coordinates, leader.aim, leader.world)


def handle_leader_coating(leader):
    if reached_aim(leader.aim, leader, True):
        leader.state = "finished"
        leader.world.csv_round.update_leader_coating()
    else:
        leader.world.csv_round.update_leader_coating()
        # print("Finished")


def handle_finished(world):
    particle_distance_list = []
    locations_distance_list = []
    for particle in world.particles:
        for direction in world.grid.get_directions_list():
            if not particle.matter_in(direction):
                particle.create_location_in(direction)
        particle_distance_list.append(get_closest_tile_distance(particle.coordinates, world))
    for location in world.locations:
        locations_distance_list.append(get_closest_tile_distance(location.coordinates, world))
    if particle_distance_list and locations_distance_list:
        if max(particle_distance_list) < min(locations_distance_list):
            # print ("Valid state")
            if leader.level == 1:
                leader.world.csv_round.update_valid(1)  # Ideal without Layer
            else:
                leader.world.csv_round.update_valid(3)  # Ideal Layered
            leader.world.csv_round.update_layer()
            world.set_successful_end()
        elif max(particle_distance_list) == min(locations_distance_list):
            if leader.level == 1:
                leader.world.csv_round.update_valid(2)  # Legal without Layer
            else:
                leader.world.csv_round.update_valid(4)  # Legal Layered
            world.set_successful_end()
        else:
            # print("Invalid State")
            world.set_unsuccessful_end()


def get_sorted_list_of_particles_distances(leader):
    distances = []
    tmp_dict = {}
    sorted_list_of_particles_coordinates = []
    for particle in leader.uncoated_particles_list:
        calculated_distance = leader.world.grid.get_distance(leader.coordinates, particle.coordinates)
        distances.append(calculated_distance)
        tmp_dict[particle.coordinates] = calculated_distance
    distances.sort()
    for distance in distances:
        for coords, dist in tmp_dict.items():
            if distance == dist and coords not in sorted_list_of_particles_coordinates:
                sorted_list_of_particles_coordinates.append(coords)
    return sorted_list_of_particles_coordinates


def get_sorted_list_of_locations_distances(leader):
    distances = []
    tmp_dict = {}
    sorted_list_of_locations_coordinates = []
    for location in leader.free_coating_locations:
        calculated_distance = leader.world.grid.get_distance(leader.coordinates, location)
        distances.append(calculated_distance)
        tmp_dict[location] = calculated_distance
    distances.sort()
    for distance in distances:
        for coords, dist in tmp_dict.items():
            if distance == dist and coords not in sorted_list_of_locations_coordinates:
                sorted_list_of_locations_coordinates.append(coords)
    return sorted_list_of_locations_coordinates


def obstacles_free_direction(leader):
    index_direction = leader.directions_list.index(leader.obstacle_direction)
    for idx in range(len(leader.directions_list)):
        direction = leader.directions_list[(idx + index_direction) % len(leader.directions_list)]
        if leader.matter_in(
                direction) is False and leader.previous_location == leader.world.grid.get_coordinates_in_direction(
                leader.coordinates, direction):
            idx_2 = len(leader.directions_list)
            while idx_2 >= 0:
                direction = leader.directions_list[(idx_2 + index_direction) % len(leader.directions_list)]
                if leader.matter_in(
                        direction) is False and leader.previous_location != leader.world.grid.get_coordinates_in_direction(
                    leader.coordinates, direction):
                    return direction
                idx_2 -= 1
        if leader.matter_in(
                direction) is False and leader.previous_location != leader.world.grid.get_coordinates_in_direction(
                leader.coordinates, direction):
            return direction
    return direction


def get_an_adjacent_obstacle_directions(leader, ignore_particle=False):
    leader.obstacle_direction = None
    for dir in leader.directions_list:
        if leader.matter_in(dir):
            if ignore_particle and leader.get_matter_in(dir).type == "particle" \
                    and leader.get_matter_in(dir) in leader.uncoated_particles_list:
                leader.uncoated_particles_list.remove(leader.get_matter_in(dir))
            leader.obstacle_direction = dir
    if bool(leader.obstacle_direction):
        return True
    return False


def get_an_adjacent_tile_directions_scanning(leader):
    leader.obstacle_direction = None
    for dir in leader.directions_list:
        if leader.matter_in(dir) and leader.get_matter_in(dir).type == "tile":
            return True
    return False


def get_leader_distance_tile_coordinates(world):
    closest_particle = world.get_particle_list()[0]
    min = None
    for particle in world.get_particle_list():
        for tile in world.get_tiles_list():
            value = world.grid.get_distance(particle.coordinates, tile.coordinates)
            if min is None or (value < min):
                min = value
                closest_particle = particle
                closest_tile_coordinate = tile.coordinates
    return closest_particle, min, closest_tile_coordinate


def find_way_to_aim(lcoordinates, tcoordinates, world):
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


def get_closest_tile_distance(source, world):
    min = None
    for tile in world.get_tiles_list():
        value = world.grid.get_distance(source, tile.coordinates)
        if min is None or (value < min):
            min = value
    return min


def reached_aim(aim, leader, leader_positioning=False):
    if leader.aim_path:
        next_direction = leader.world.grid.get_nearest_direction(leader.coordinates, leader.aim_path.pop(0))
        next_coords = leader.world.grid.get_coordinates_in_direction(leader.coordinates, next_direction)
        if aim == next_coords and leader_positioning is False:
            return True
        leader.previous_location = leader.coordinates
        leader.move_to(next_direction)
        if leader_positioning and leader.coordinates == aim:
            return True
        return False
    return True