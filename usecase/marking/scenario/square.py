black = 1
gray = 2
red = 3
green = 4
blue = 5
yellow = 6
orange = 7
cyan = 8
violett = 9

start_positions = {"TopLeft": [(-9.5, 11), (-10, 10), (-11, 12), (-11, 10), (-10, 12), (-10.5, 11)],
                   "TopRightEnclosed": [(10.5, 11), (11, 12), (10, 12), (11, 10), (10, 10), (9.5, 11)],
                   "TopRight": [(11, 8), (10, 8), (9, 8), (8, 8), (10.5, 7), (9.5, 7)],
                   "BottomLeft": [(-10.5, -11), (-11, -12), (-10, -12), (-9.5, -11), (-10, -10), (-9, -12)],
                   "BottomRight": [(10.5, -11), (11, -12), (10, -12), (11, -10), (10, -10), (9.5, -11)],
                   "Center": [(0, 0), (1, 0), (0.5, -1), (-0.5, -1), (-1, 0), (-0.5, 1)],
                   "Random1": [(8, -2), (7.5, -1), (7, -2), (8.5, -1), (8, 0), (6.5, -1)],
                   "Random2": [(-5.5, 1), (-5, 2), (-7.5, 3), (-6.5, 1), (-4.5, 1), (-6.0, 2.0)]}


def scenario(sim):
    draw_terrain(sim)

    for i in range(0, sim.config_data.particles_num):
        sim.add_particle((start_positions[sim.config_data.start_position][i][0]), (start_positions[sim.config_data.start_position][i][1]))


def get_starting_positions():
    return list(start_positions.keys())


def draw_terrain(sim):
    # Top Border
    sim.add_location(-11.5, 13)
    sim.add_location(-10.5, 13)
    sim.add_location(-9.5, 13)
    sim.add_location(-8.5, 13)
    sim.add_location(-7.5, 13)
    sim.add_location(-6.5, 13)
    sim.add_location(-5.5, 13)
    sim.add_location(-4.5, 13)
    sim.add_location(-3.5, 13)
    sim.add_location(-2.5, 13)
    sim.add_location(-1.5, 13)
    sim.add_location(-0.5, 13)
    sim.add_location(0.5, 13)
    sim.add_location(1.5, 13)
    sim.add_location(2.5, 13)
    sim.add_location(3.5, 13)
    sim.add_location(4.5, 13)
    sim.add_location(5.5, 13)
    sim.add_location(6.5, 13)
    sim.add_location(7.5, 13)
    sim.add_location(8.5, 13)
    sim.add_location(9.5, 13)
    sim.add_location(10.5, 13)
    sim.add_location(11.5, 13)

    # Bottom Border
    sim.add_location(-11.5, -13)
    sim.add_location(-10.5, -13)
    sim.add_location(-9.5, -13)
    sim.add_location(-8.5, -13)
    sim.add_location(-7.5, -13)
    sim.add_location(-6.5, -13)
    sim.add_location(-5.5, -13)
    sim.add_location(-4.5, -13)
    sim.add_location(-3.5, -13)
    sim.add_location(-2.5, -13)
    sim.add_location(-1.5, -13)
    sim.add_location(-0.5, -13)
    sim.add_location(0.5, -13)
    sim.add_location(1.5, -13)
    sim.add_location(2.5, -13)
    sim.add_location(3.5, -13)
    sim.add_location(4.5, -13)
    sim.add_location(5.5, -13)
    sim.add_location(6.5, -13)
    sim.add_location(7.5, -13)
    sim.add_location(8.5, -13)
    sim.add_location(9.5, -13)
    sim.add_location(10.5, -13)
    sim.add_location(11.5, -13)

    # Left Border
    sim.add_location(-12, 12)
    sim.add_location(-11.5, 11)
    sim.add_location(-12, 10)
    sim.add_location(-11.5, 9)
    sim.add_location(-12, 8)
    sim.add_location(-11.5, 7)
    sim.add_location(-12, 6)
    sim.add_location(-11.5, 5)
    sim.add_location(-12, 4)
    sim.add_location(-11.5, 3)
    sim.add_location(-12, 2)
    sim.add_location(-11.5, 1)
    sim.add_location(-12, 0)
    sim.add_location(-12, -12)
    sim.add_location(-11.5, -11)
    sim.add_location(-12, -10)
    sim.add_location(-11.5, -9)
    sim.add_location(-12, -8)
    sim.add_location(-11.5, -7)
    sim.add_location(-12, -6)
    sim.add_location(-11.5, -5)
    sim.add_location(-12, -4)
    sim.add_location(-11.5, -3)
    sim.add_location(-12, -2)
    sim.add_location(-11.5, -1)

    # Right Border
    sim.add_location(12, 12)
    sim.add_location(11.5, 11)
    sim.add_location(12, 10)
    sim.add_location(11.5, 9)
    sim.add_location(12, 8)
    sim.add_location(11.5, 7)
    sim.add_location(12, 6)
    sim.add_location(11.5, 5)
    sim.add_location(12, 4)
    sim.add_location(11.5, 3)
    sim.add_location(12, 2)
    sim.add_location(11.5, 1)
    sim.add_location(12, 0)
    sim.add_location(12, -12)
    sim.add_location(11.5, -11)
    sim.add_location(12, -10)
    sim.add_location(11.5, -9)
    sim.add_location(12, -8)
    sim.add_location(11.5, -7)
    sim.add_location(12, -6)
    sim.add_location(11.5, -5)
    sim.add_location(12, -4)
    sim.add_location(11.5, -3)
    sim.add_location(12, -2)
    sim.add_location(11.5, -1)

    ###################################################

    # Obstacles
    # sim.add_location(-2, 0)
    sim.add_location(0, -2)
    sim.add_location(1, -2)
    sim.add_location(1.5, 3)
    sim.add_location(0.5, 3)

    sim.add_location(-7.0, 8.0)
    sim.add_location(-6.5, 7.0)
    sim.add_location(-6.0, 6.0)
    sim.add_location(-5.5, 5.0)
    sim.add_location(-5.0, 4.0)
    sim.add_location(-4.5, 3.0)
    sim.add_location(-4.0, 2.0)
    sim.add_location(-3.5, 1.0)
    sim.add_location(-3.0, 0.0)

    sim.add_location(0.5, 1)
    sim.add_location(0, 2)
    sim.add_location(-0.5, 3)
    sim.add_location(-0.5, 0)
    sim.add_location(1.5, -1)

    sim.add_location(5.5, -5)
    sim.add_location(6.5, -5)
    sim.add_location(6.5, -7)
    sim.add_location(6, -6)
    sim.add_location(5, -6)
    sim.add_location(7, -6)
    sim.add_location(5.5, -7)

    sim.add_location(8.5, 11)
    sim.add_location(9, 10)
    sim.add_location(9.5, 9)
    sim.add_location(10.5, 9)
    sim.add_location(7.5, 11)
    sim.add_location(6.5, 11)
    sim.add_location(5.5, 11)
    sim.add_location(4.5, 11)
    sim.add_location(3.5, 11)
    sim.add_location(2.5, 11)
    sim.add_location(1.5, 11)
    sim.add_location(1, 0)


