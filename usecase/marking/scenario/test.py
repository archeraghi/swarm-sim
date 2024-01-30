black = 1
gray = 2
red = 3
green = 4
blue = 5
yellow = 6
orange = 7
cyan = 8
violett = 9

start_positions = {"Center": [(0, 0)]}


def scenario(sim, start_position, particles_num):
    draw_terrain(sim)

    for i in range(0, particles_num):
        sim.add_particle((start_positions[start_position][i][0]), (start_positions[start_position][i][1]))


def get_starting_positions():
    return list(start_positions.keys())


def draw_terrain(sim):
    sim.add_location(0.0, 4.0)
    sim.add_location(-0.0, -4.0)
    sim.add_location(4.0, 0.0)
    sim.add_location(-4.0, 0.0)
    sim.add_location(-3.5, 1.0)
    sim.add_location(-4.0, 2.0)
    sim.add_location(-3.5, 3.0)
    sim.add_location(-4.0, 4.0)
    sim.add_location(-3.0, 4.0)
    sim.add_location(-2.0, 4.0)
    sim.add_location(-1.0, 4.0)
    sim.add_location(1.0, 4.0)
    sim.add_location(2.0, 4.0)
    sim.add_location(3.5, 1.0)
    sim.add_location(4.0, 2.0)
    sim.add_location(3.5, 3.0)
    sim.add_location(4.0, 4.0)
    sim.add_location(3.0, 4.0)
    sim.add_location(-3.5, -1.0)
    sim.add_location(-4.0, -2.0)
    sim.add_location(-3.5, -3.0)
    sim.add_location(-4.0, -4.0)
    sim.add_location(-3.0, -4.0)
    sim.add_location(-2.0, -4.0)
    sim.add_location(-1.0, -4.0)
    sim.add_location(1.0, -4.0)
    sim.add_location(2.0, -4.0)
    sim.add_location(3.0, -4.0)
    sim.add_location(4.0, -4.0)
    sim.add_location(3.5, -3.0)
    sim.add_location(4.0, -2.0)
    sim.add_location(3.5, -1.0)



