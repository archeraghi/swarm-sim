#colors
black = 1
gray = 2
red = 3
green = 4
blue = 5
yellow = 6
orange = 7
cyan = 8
violett = 9


#directions
NE = 0
E = 1
SE = 2
SW = 3
W = 4
NW = 5

direction = [NE, E, SE, SW, W, NW]


#standard libaries

def scan_neighborhood(particle):
    """
    :param particle:
    :return: a dictionary with the direction and the founded matter
    """
    nh_dict={}
    for dir in direction:
        nh_dict[dir] = particle.get_matter_in(dir)

def move_to_dest_in_one_rnd(particle, destiny):
    if move_to_dest_step_by_step(particle, destiny):
        return True
    move_to_dest_in_one_rnd(particle, destiny)

def move_to_dest_step_by_step(particle, destiny):
    """

    :param particle:
    :param destiny:
    :return: True if movement occured, False if not movment and a Matter if the next dir point has a matter on it
    """
    next_dir = get_next_dir_to(particle.coords[0], particle.coords[1], destiny.coords[0], destiny.coords[1])
    if particle.matter_in(next_dir):
        particle.get_matter_in(next_dir)
        return particle.get_matter_in(next_dir)
    particle.move_to(next_dir)
    print("\n P", particle.number, " moves to", dir_to_str(next_dir))
    return False
def get_next_dir_to(src_x, src_y, dest_x, dest_y):
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


def dir_to_str(dir):
    """
    :param dir: the direction that should get converted to a string
    :return: the string of the direction
    """
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
    else:
        return "Error"


def get_the_invert(dir):
    return (dir + 3) % 6


def dir_in_range(dir):
    return dir % 6
