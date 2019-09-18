import math
import random
from enum import Enum


class Colors(Enum):
    black = 1
    gray = 2
    red = 3
    green = 4
    blue = 5
    yellow = 6
    orange = 7
    cyan = 8
    violett = 9
    dark_green = 10


black = 1
gray = 2
red = 3
green = 4
blue = 5
yellow = 6
orange = 7
cyan = 8
violett = 9
dark_green = 10


color_map = {
    black: [0.0, 0.0, 0.0],
    gray: [0.3, 0.3, 0.3],
    red: [0.8, 0.0, 0.0],
    green: [0.0, 0.8, 0.0],
    dark_green: [0.2, 1, 0.6],
    blue: [0.0, 0.0, 0.8],
    yellow: [0.8, 0.8, 0.0],
    orange: [0.8, 0.3, 0.0],
    cyan: [0.0, 0.8, 0.8],
    violett: [0.8, 0.2, 0.6]
}


NE=0
E = 1
SE = 2
SW = 3
W = 4
NW = 5


direction_list = [NE, E, SE, SW, W, NW]

x_offset = [0.5, 1,  0.5,   -0.5,   -1, -0.5 ]
y_offset = [ 1, 0, -1,   -1,    0,  1]


def direction_number_to_string(direction):
    """
    :param direction: the direction that should get converted to a string
    :return: the string of the direction
    """
    if direction == 0:
        return "NE"
    elif direction == 1:
        return "E"
    elif direction == 2:
        return "SE"
    elif direction == 3:
        return "SW"
    elif direction == 4:
        return "W"
    elif direction == 5:
        return "NW"
    else:
        return "Error"


def get_the_invert(direction):
    return (direction + 3) % 6


def direction_in_range(direction):
    return direction % 6


def check_coords(coords_x, coords_y):
    """
    Checks if the given coordinates are matching the
    hexagon coordinates

    :param coords_x: proposed x coordinate
    :param coords_y: proposed y coordinate
    :return: True: Correct x and y coordinates; False: Incorrect coordinates
    """

    if (coords_x / 0.5) % 2 == 0:
        if coords_y % 2 != 0:
            return False
        else:
            return True
    else:
        if coords_y % 2 == 0:
            return False
        else:
            return True


def coords_to_sim(coords):
    return coords[0], coords[1] * math.sqrt(3 / 4)


def sim_to_coords(x, y):
    return x, round(y / math.sqrt(3 / 4), 0)


def get_coords_in_direction(coords, direction):
    """
    Returns the coordination data of the pointed directions

    :param coords: particles actual staying coordination
    :param direction: The direction. Options:  E, SE, SW, W, NW, or NE
    :return: The coordinaiton of the pointed directions
    """
    return coords[0] + x_offset[direction], coords[1] + y_offset[direction]


def global_scanning(matter_map_coords_dict, hop, starting_x, starting_y):
    hop_list = []
    if (hop / 2 + starting_x, hop + starting_y) in matter_map_coords_dict:
        hop_list.append(matter_map_coords_dict[(hop / 2 + starting_x, hop + starting_y)])
    if (hop + starting_x, starting_y) in matter_map_coords_dict:
        hop_list.append(matter_map_coords_dict[(hop + starting_x, starting_y)])
    if (hop / 2 + starting_x, -hop + starting_y) in matter_map_coords_dict:
        hop_list.append(matter_map_coords_dict[(hop / 2 + starting_x, -hop + starting_y)])
    if (-hop / 2 + starting_x, -hop + starting_y) in matter_map_coords_dict:
        hop_list.append(matter_map_coords_dict[(-hop / 2 + starting_x, -hop + starting_y)])
    if (-hop + starting_x, starting_y) in matter_map_coords_dict:
        hop_list.append(matter_map_coords_dict[(-hop + starting_x, starting_y)])
    if (-hop / 2 + starting_x, hop + starting_y) in matter_map_coords_dict:
        hop_list.append(matter_map_coords_dict[(-hop / 2 + starting_x, hop + starting_y)])
    for i in range(1, hop):
        if (-hop / 2 + i + starting_x, hop + starting_y) in matter_map_coords_dict:
            hop_list.append(matter_map_coords_dict[(-hop / 2 + i + starting_x, hop + starting_y)])
        if (hop / 2 + (0.5 * i) + starting_x, hop - i + starting_y) in matter_map_coords_dict:
            hop_list.append(
                matter_map_coords_dict[(hop / 2 + (0.5 * i) + starting_x, hop - i + starting_y)])
        if (hop / 2 + (0.5 * i) + starting_x, -hop + i + starting_y) in matter_map_coords_dict:
            hop_list.append(
                matter_map_coords_dict[(hop / 2 + (0.5 * i) + starting_x, -hop + i + starting_y)])
        if (-hop / 2 + i + starting_x, -hop + starting_y) in matter_map_coords_dict:
            hop_list.append(matter_map_coords_dict[(-hop / 2 + i + starting_x, -hop + starting_y)])
        if (-hop / 2 - (0.5 * i) + starting_x, -hop + i + starting_y) in matter_map_coords_dict:
            hop_list.append(
                matter_map_coords_dict[(-hop / 2 - (0.5 * i) + starting_x, -hop + i + starting_y)])
        if (-hop / 2 - (0.5 * i) + starting_x, hop - i + starting_y) in matter_map_coords_dict:
            hop_list.append(
                matter_map_coords_dict[(-hop / 2 - (0.5 * i) + starting_x, hop - i + starting_y)])
    return hop_list



# Helping Methods for creating scenarios

def generating_random_spraded_particles (world, max_size_particle):
    for _ in range(0, max_size_particle):
        x = random.randrange(-world.get_world_x_size(), world.get_world_x_size())
        y = random.randrange(-world.get_world_y_size(), world.get_world_y_size())
        if y % 2 == 1:
            x = x + 0.5
        if (x, y) not in world.tile_map_coords:
            world.add_particle(x, y)
        else:
            print(" x and y ", (x, y))
    print("Max Size of created Particle", len(world.particles))


def create_particle_in_line(world, max_size_particle, start_coords):
    if start_coords[0] % 1 != 0:
        start_i = int(start_coords[0] - 0.5)
        for i in range(start_i, start_i+max_size_particle):
            world.add_particle(i + 1.5, start_coords[1])

    else:
        for i in range(int(start_coords[0] + 1), int(start_coords[0] + 1) + max_size_particle):
            world.add_particle(i, start_coords[1])


def create_particle_in_square(world, max_size_particle, start_coords):

    for y in range(start_coords[1], round(max_size_particle/2)):
        for x in range(start_coords[0], round(max_size_particle/2)):
            world.add_particle(x + 0.5, 2 * y + 1.0)
            world.add_particle(-(x + 0.5), 2 * y + 1.0)
            world.add_particle(x + 0.5, -(2 * y + 1.0))
            world.add_particle(-(x + 0.5), -(2 * y + 1.0))
            world.add_particle(x, 2 * y)
            world.add_particle(-x, 2 * y)
            world.add_particle(x, -2 * y)
            world.add_particle(-x, -  2 * y)


def add_particles_as_hexagon(world, radius, color=black):
    world.add_particle(0, 0, color)
    displacement = - radius + 0.5
    iteration = 0
    for i in range(1, radius + 1):
        world.add_particle(i, 0, color)
        world.add_particle(-i, 0, color)
    for i in range(1, radius + 1):
        for j in range(0, (2 * radius) - iteration):
            world.add_particle(displacement + j, i, color)
            world.add_particle(displacement + j, -i, color)
        iteration = iteration + 1
        displacement = displacement + 0.5


def add_tiles_as_hexagon(world, radius, color=black):
    world.add_tile(0, 0, color)
    displacement = - radius + 0.5
    iteration = 0
    for i in range(1, radius + 1):
        world.add_tile(i, 0, color)
        world.add_tile(-i, 0, color)
    for i in range(1, radius + 1):
        for j in range(0, (2 * radius) - iteration):
            world.add_tile(displacement + j, i, color)
            world.add_tile(displacement + j, -i, color)
        iteration = iteration + 1
        displacement = displacement + 0.5


def add_markers_as_hexagon(world, radius, color=black):
    world.add_marker(0, 0, color)
    displacement = - radius + 0.5
    iteration = 0
    for i in range(1, radius + 1):
        world.add_marker(i, 0, color)
        world.add_marker(-i, 0, color)
    for i in range(1, radius + 1):
        for j in range(0, (2 * radius) - iteration):
            world.add_marker(displacement + j, i, color)
            world.add_marker(displacement + j, -i, color)
        iteration = iteration + 1
        displacement = displacement + 0.5


def create_tiles_formed_as_hexagons_border(world, radius, starting_x = 0, starting_y = 0):
    offset_x = 0
    if starting_y % 2 != 0:
        offset_x = 0.5
    world.add_tile(radius/2 + starting_x + offset_x, radius + starting_y)
    world.add_tile(radius + starting_x + offset_x, starting_y)
    world.add_tile(radius/2 + starting_x + offset_x, -radius  + starting_y)
    world.add_tile(-radius/2 + starting_x + offset_x, -radius + starting_y)
    world.add_tile(-radius + starting_x + offset_x, starting_y)
    world.add_tile(-radius/2 + starting_x + offset_x, radius + starting_y)

    for i in range(1, radius):
        world.add_tile(-radius/2 + i + starting_x + offset_x, radius + starting_y)
        world.add_tile(radius/2 + (0.5 * i ) + starting_x + offset_x, radius - i + starting_y)
        world.add_tile(radius/2 + (0.5 * i) + starting_x + offset_x, -radius + i + starting_y)
        world.add_tile(-radius/2 + i + starting_x + offset_x, -radius + starting_y)
        world.add_tile(-radius/2 - (0.5 * i) + starting_x + offset_x, -radius + i + starting_y)
        world.add_tile(-radius/2 - (0.5 * i) + starting_x + offset_x, radius - i + starting_y)


# Helping methods for Solution


def scan_neighborhood(particle):
    """
    :param particle:
    :return: a dictionary with the direction and the founded matter
    """
    nh_dict={}
    for direction in direction_list:
        nh_dict[direction] = particle.get_matter_in(direction)


def move_to_dest_in_one_rnd(particle, destiny):
    if move_to_dest_step_by_step(particle, destiny):
        return True
    move_to_dest_in_one_rnd(particle, destiny)


def move_to_dest_step_by_step(particle, destiny):
    """

    :param particle:
    :param destiny:
    :return: True if movement occured, False if not movment and a Matter if the next direction point has a matter on it
    """
    next_dir = get_next_direction_to(particle.coords[0], particle.coords[1], destiny.coords[0], destiny.coords[1])
    if particle.matter_in(next_dir):
        particle.get_matter_in(next_dir)
        return particle.get_matter_in(next_dir)
    particle.move_to(next_dir)
    print("\n P", particle.number, " moves to", direction_number_to_string(next_dir))
    return False


def get_next_direction_to(src_x, src_y, dest_x, dest_y):
    """
    :param src_x: x coordinate of the source
    :param src_y: y coordinate of the source
    :param dest_x: x coordinate of the destiny
    :param dest_y: y coordinate of the destiny
    :return: the next direction that brings the matter closer to the destiny
    """
    next_dir = -1
    if (src_x < dest_x or src_x == dest_x) and src_y < dest_y:
        next_dir = NE
    elif src_y < dest_y and src_x > dest_x:
        next_dir = NW
    elif src_y > dest_y and src_x < dest_x:
        next_dir = SE
    elif (src_x > dest_x or src_x == dest_x) and src_y > dest_y :
        next_dir = SW
    elif src_y == dest_y and src_x > dest_x:
        next_dir = W
    elif src_y == dest_y and src_x < dest_x:
        next_dir = E
    return next_dir
