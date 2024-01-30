previous_location =  None
def solution(world):
    global previous_location
    if world.get_actual_round() ==1:
        leader = world.particles[0]
        leader.previous_location = (1, 0.0, 0.0)
        leader.create_location_on(leader.previous_location).set_color((1.0, 1.0, 0.0, 1.0))
    # if len(world.particles) > 0:
    #     leader = world.particles[0]
    #     leader.previous_location = (1, 0.0, 0.0)
    #     leader.create_location_on(direction_exit).set_color((1.0, 1.0, 0.0, 1.0))
    #     # if not previous_location:
    #     #     previous_location = leader.create_location_on((-0.5, 1.0, 0.0))
    #     #     previous_location.set_color((1.0, 0.0, 1.0, 1.0))
    #     if len(world.locations) > 1:
    #         for location in world.locations[:]:
    #                 world.remove_location(location.get_id())
    #                 world.vis.remove_location(location)
    #     leader.directions_list = world.grid.get_directions_list()
    #     check_for_cave(leader)


def check_for_cave(leader):
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
    if direction_entry is not None and direction_exit is not None:
        leader.create_location_in(direction_entry)
        leader.create_location_in(direction_exit).set_color((1.0, 1.0, 0.0, 1.0))
        previous_location = leader.create_location_on(leader.previous_location)
        if previous_location:
            previous_location.set_color((1.0, 0.0, 0.0, 1.0))
    return direction_entry, direction_exit