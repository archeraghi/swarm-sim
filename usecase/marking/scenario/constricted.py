black = 1
gray = 2
red = 3
green = 4
blue = 5
yellow = 6
orange = 7
cyan = 8
violett = 9


start_positions = {"TopLeft": [(-9.5, 11), (-10, 10), (-9, 10), (-8.5, 11), (-10.5, 11), (-11, 10)],
                   "TopRight": [(9.5, 11.0), (10.5, 11.0), (11.0, 10.0), (10.0, 10.0), (10.5, 9.0), (9.0, 10.0)],
                   "BottomLeft": [(-10.5, -11.0), (-9.5, -11.0), (-10.0, -10.0), (-11.0, -10.0), (-10.5, -9.0), (-9.0, -10.0)],
                   "BottomRight": [(10.5, -11.0), (11.0, -10.0), (9.5, -11.0), (10.0, -10.0), (10.5, -9.0), (9.0, -10.0)],
                   "Random1": [(-6.5, 5.0), (-7.0, 4.0), (-6.0, 4.0), (-5.5, 3.0), (-6.5, 3.0), (-6.0, 2.0)],
                   "Random2": [(10.5, 1.0), (11.0, 0.0), (10.5, -1.0), (9.5, -1.0), (10.0, 0.0), (9.0, -0.0)]}


def scenario(sim):
    draw_terrain(sim)

    for i in range(0, sim.config_data.particles_num):
        sim.add_particle((start_positions[sim.config_data.start_position][i][0]), (start_positions[sim.config_data.start_position][i][1]))


def get_starting_positions():
    return list(start_positions.keys())


def draw_terrain(sim):
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

    sim.add_location(-11.0, 12.0)
    sim.add_location(-10.0, 12.0)
    sim.add_location(-9.0, 12.0)
    sim.add_location(-8.0, 12.0)
    sim.add_location(-7.0, 12.0)
    sim.add_location(-6.0, 12.0)
    sim.add_location(-5.5, 11.0)
    sim.add_location(-5.0, 10.0)
    sim.add_location(-4.5, 9.0)
    sim.add_location(-4.0, 8.0)
    sim.add_location(-3.5, 7.0)
    sim.add_location(-3.0, 6.0)
    sim.add_location(-2.5, 5.0)
    sim.add_location(-2.0, 4.0)
    sim.add_location(-1.5, 3.0)
    sim.add_location(-1.0, 2.0)
    sim.add_location(-0.5, 1.0)
    sim.add_location(0.5, 1.0)
    sim.add_location(1.0, 2.0)
    sim.add_location(1.5, 3.0)
    sim.add_location(2.0, 4.0)
    sim.add_location(2.5, 5.0)
    sim.add_location(3.0, 6.0)
    sim.add_location(3.5, 7.0)
    sim.add_location(4.0, 8.0)
    sim.add_location(4.5, 9.0)
    sim.add_location(5.0, 10.0)
    sim.add_location(5.5, 11.0)
    sim.add_location(6.0, 12.0)
    sim.add_location(7.0, 12.0)
    sim.add_location(8.0, 12.0)
    sim.add_location(9.0, 12.0)
    sim.add_location(10.0, 12.0)
    sim.add_location(11.0, 12.0)
    sim.add_location(-11.0, -12.0)
    sim.add_location(-10.0, -12.0)
    sim.add_location(-9.0, -12.0)
    sim.add_location(-8.0, -12.0)
    sim.add_location(-7.0, -12.0)
    sim.add_location(-6.0, -12.0)
    sim.add_location(-5.5, -11.0)
    sim.add_location(-5.0, -10.0)
    sim.add_location(-4.5, -9.0)
    sim.add_location(-4.0, -8.0)
    sim.add_location(-3.5, -7.0)
    sim.add_location(-3.0, -6.0)
    sim.add_location(-2.5, -5.0)
    sim.add_location(-2.0, -4.0)
    sim.add_location(-1.5, -3.0)
    sim.add_location(-1.0, -2.0)
    sim.add_location(-0.5, -1.0)
    sim.add_location(0.5, -1.0)
    sim.add_location(1.0, -2.0)
    sim.add_location(1.5, -3.0)
    sim.add_location(2.0, -4.0)
    sim.add_location(2.5, -5.0)
    sim.add_location(3.0, -6.0)
    sim.add_location(3.5, -7.0)
    sim.add_location(4.0, -8.0)
    sim.add_location(4.5, -9.0)
    sim.add_location(5.0, -10.0)
    sim.add_location(5.5, -11.0)
    sim.add_location(6.0, -12.0)
    sim.add_location(7.0, -12.0)
    sim.add_location(8.0, -12.0)
    sim.add_location(9.0, -12.0)
    sim.add_location(10.0, -12.0)
    sim.add_location(11.0, -12.0)



