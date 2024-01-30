def doubleline20(sim):
    sim.add_particle(-5, 0)
    sim.add_particle(-4, 0)
    sim.add_particle(-3, 0)
    sim.add_particle(-2, 0)
    sim.add_particle(-1, 0)
    sim.add_particle(0, 0)
    sim.add_particle(1, 0)
    sim.add_particle(2, 0)
    sim.add_particle(3, 0)
    sim.add_particle(4, 0)
    sim.add_particle(-5.5, 1)
    sim.add_particle(-4.5, 1)
    sim.add_particle(-3.5, 1)
    sim.add_particle(-2.5, 1)
    sim.add_particle(-1.5, 1)
    sim.add_particle(-0.5, 1)
    sim.add_particle(0.5, 1)
    sim.add_particle(1.5, 1)
    sim.add_particle(2.5, 1)
    sim.add_particle(3.5, 1)

def line10(sim):
    sim.add_particle(-5, 0)
    sim.add_particle(-4, 0)
    sim.add_particle(-3, 0)
    sim.add_particle(-2, 0)
    sim.add_particle(-1, 0)
    sim.add_particle(0, 0)
    sim.add_particle(1, 0)
    sim.add_particle(2, 0)
    sim.add_particle(3, 0)
    sim.add_particle(4, 0)

def around37(sim):
    sim.add_particle(3, 0)
    sim.add_particle(1, 0)
    sim.add_particle(-1, 0)
    sim.add_particle(-0.5, 1)
    sim.add_particle(0.5, 1)
    sim.add_particle(-0.5, -1)
    sim.add_particle(0.5, -1)
    sim.add_particle(2, 0)
    sim.add_particle(-2, 0)
    sim.add_particle(-1.5, 1)
    sim.add_particle(1.5, 1)
    sim.add_particle(0, 2)
    sim.add_particle(-1, 2)
    sim.add_particle(1, 2)
    sim.add_particle(-1.5, -1)
    sim.add_particle(1.5, -1)
    sim.add_particle(0, -2)
    sim.add_particle(-1, -2)
    sim.add_particle(1, -2)
    sim.add_particle(-3, 0)
    sim.add_particle(-2.5, 1)
    sim.add_particle(2.5, 1)
    sim.add_particle(-2, 2)
    sim.add_particle(2, 2)
    sim.add_particle(-1.5, 3)
    sim.add_particle(1.5, 3)
    sim.add_particle(-0.5, 3)
    sim.add_particle(0.5, 3)
    sim.add_particle(-2.5, -1)
    sim.add_particle(2.5, -1)
    sim.add_particle(-2, -2)
    sim.add_particle(2, -2)
    sim.add_particle(-1.5, -3)
    sim.add_particle(1.5, -3)
    sim.add_particle(-0.5, -3)
    sim.add_particle(0.5, -3)
    sim.add_particle(0, 0)

def star50(sim):
    sim.add_particle(3,0)
    sim.add_particle(2,0)
    sim.add_particle(1,0)
    sim.add_particle(0,0)
    sim.add_particle(-1,0)
    sim.add_particle(-2,0)
    sim.add_particle(-3,0)
    sim.add_particle(-4,0)
    sim.add_particle(-5,0)
    sim.add_particle(-6,0)
    sim.add_particle(-7,0)
    sim.add_particle(-8,0)
    sim.add_particle(-9,0)
    sim.add_particle(-10,0)

    sim.add_particle(-2.5, 1)
    sim.add_particle(-2.5, -1)
    sim.add_particle(-3.5, 1)
    sim.add_particle(-3.5, -1)

    sim.add_particle(-2, 2)
    sim.add_particle(-2, -2)
    sim.add_particle(-4, 2)
    sim.add_particle(-4, -2)

    sim.add_particle(-1.5, 3)
    sim.add_particle(-1.5, -3)
    sim.add_particle(-4.5, 3)
    sim.add_particle(-4.5, -3)

    sim.add_particle(-1, 4)
    sim.add_particle(-1, -4)
    sim.add_particle(-5, 4)
    sim.add_particle(-5, -4)

    sim.add_particle(-0.5, 5)
    sim.add_particle(-0.5, -5)
    sim.add_particle(-5.5, 5)
    sim.add_particle(-5.5, -5)

    sim.add_particle(0, 6)
    sim.add_particle(0, -6)
    sim.add_particle(-6, 6)
    sim.add_particle(-6, -6)

    #38
    sim.add_particle(0.5, 7)
    sim.add_particle(0.5, -7)
    sim.add_particle(-6.5, 7)
    sim.add_particle(-6.5, -7)

    sim.add_particle(1, 8)
    sim.add_particle(1, -8)
    sim.add_particle(-7, 8)
    sim.add_particle(-7, -8)

    sim.add_particle(1.5, 9)
    sim.add_particle(1.5, -9)
    sim.add_particle(-7.5, 9)
    sim.add_particle(-7.5, -9)

    sim.add_particle(2, 10)
    sim.add_particle(2, -10)
    sim.add_particle(-8, 10)
    sim.add_particle(-8, -10)
def block100(sim, start=(0,0,0), amount=6):
    amount = int(amount /2)
    for i in range(0,amount):
        for j in range(0,amount):
            if j%2 == 0:
                sim.add_particle(-i + start[0], j + start[1])
            else:
                sim.add_particle(-i + 0.5 + start[0], j +start[1])

def hexagon(world, centre, r_max=2, exclude_centre=False):
    """
    Returns all locations of a 2d-hexagon with centre :param centre: and radius :param r_max:.
    :param exclude_centre: should the centre coordinate be included
    :type exclude_centre: boolean
    :param centre: the centre location of the hexagon
    :type centre: tuple
    :param r_max: radius of the hexagon
    :type r_max: int
    :return: list of locations
    :rtype: list
    """
    if not exclude_centre:
        world.add_particle(centre)
    displacement = - r_max + 0.5
    iteration = 0
    for y in range(1, r_max + 1):
        world.add_particle((centre[0] + y, centre[1], 0))
        world.add_particle(((centre[0] - y), centre[1], 0))
        for x in range(0, (2 * r_max) - iteration):
            world.add_particle((centre[0] + displacement + x, centre[1] + y, 0))
            world.add_particle((centre[0] + displacement + x, centre[1] - y, 0))
        iteration = iteration + 1
        displacement = displacement + 0.5


def create_matter_in_line(world, start, direction, amount, matter_type='particle'):
    current_position = start
    for _ in range(amount):
        if matter_type == 'particle':
            world.add_particle(current_position)
        elif matter_type == 'tile':
            world.add_tile(current_position)
        elif matter_type == 'location':
            world.add_location(current_position)
        else:
            print("create_matter_in_line: unknown type (allowed: particle, tile or location")
            return
        current_position = world.grid.get_coordinates_in_direction(current_position, direction)