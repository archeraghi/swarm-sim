from lib.std_lib import green, red


def scenario(sim):
    # 4 communicating particles
    # bottom-left
    sim.add_particle(x=-35, y=-30, color=red)
    # bottom-right
    sim.add_particle(x=35, y=-30, color=green)
    # top-left
    sim.add_particle(x=-35, y=30, color=red)
    # top-right
    sim.add_particle(x=35, y=30, color=green)

    # moving bottleneck particle
    sim.add_particle(x=0, y=0)

    # one hop particles in range
    sim.add_particle(20.0, -20.0)
    sim.add_particle(20.0, 20.0)
    sim.add_particle(-20.0, 20.0)
    sim.add_particle(-20.0, -20.0)

    # right border
    sim.add_particle(20.0, 18.0)
    sim.add_particle(20.0, 16.0)
    sim.add_particle(20.0, 14.0)
    sim.add_particle(20.0, 12.0)
    sim.add_particle(20.0, 10.0)
    sim.add_particle(20.0, 8.0)
    sim.add_particle(20.0, 6.0)
    sim.add_particle(20.0, 4.0)
    sim.add_particle(20.0, 2.0)
    sim.add_particle(20.0, 0.0)
    sim.add_particle(20.0, -2.0)
    sim.add_particle(20.0, -4.0)
    sim.add_particle(20.0, -6.0)
    sim.add_particle(20.0, -8.0)
    sim.add_particle(20.0, -10.0)
    sim.add_particle(20.0, -12.0)
    sim.add_particle(20.0, -14.0)
    sim.add_particle(20.0, -16.0)
    sim.add_particle(20.0, -18.0)

    # left border
    sim.add_particle(-20.0, 18.0)
    sim.add_particle(-20.0, 16.0)
    sim.add_particle(-20.0, 14.0)
    sim.add_particle(-20.0, 12.0)
    sim.add_particle(-20.0, 10.0)
    sim.add_particle(-20.0, 8.0)
    sim.add_particle(-20.0, 6.0)
    sim.add_particle(-20.0, 4.0)
    sim.add_particle(-20.0, 2.0)
    sim.add_particle(-20.0, 0.0)
    sim.add_particle(-20.0, -2.0)
    sim.add_particle(-20.0, -4.0)
    sim.add_particle(-20.0, -6.0)
    sim.add_particle(-20.0, -8.0)
    sim.add_particle(-20.0, -10.0)
    sim.add_particle(-20.0, -12.0)
    sim.add_particle(-20.0, -14.0)
    sim.add_particle(-20.0, -16.0)
    sim.add_particle(-20.0, -18.0)

    # left diagonal
    sim.add_particle(-33.5, -29.0)
    sim.add_particle(-32.0, -28.0)
    sim.add_particle(-30.5, -27.0)
    sim.add_particle(-29.0, -26.0)
    sim.add_particle(-27.5, -25.0)
    sim.add_particle(-26.0, -24.0)
    sim.add_particle(-24.5, -23.0)
    sim.add_particle(-23.0, -22.0)
    sim.add_particle(-21.5, -21.0)

    sim.add_particle(-33.5, 29.0)
    sim.add_particle(-32.0, 28.0)
    sim.add_particle(-30.5, 27.0)
    sim.add_particle(-29.0, 26.0)
    sim.add_particle(-27.5, 25.0)
    sim.add_particle(-26.0, 24.0)
    sim.add_particle(-24.5, 23.0)
    sim.add_particle(-23.0, 22.0)
    sim.add_particle(-21.5, 21.0)

    # right diagonal
    sim.add_particle(33.5, -29.0)
    sim.add_particle(32.0, -28.0)
    sim.add_particle(30.5, -27.0)
    sim.add_particle(29.0, -26.0)
    sim.add_particle(27.5, -25.0)
    sim.add_particle(26.0, -24.0)
    sim.add_particle(24.5, -23.0)
    sim.add_particle(23.0, -22.0)
    sim.add_particle(21.5, -21.0)

    sim.add_particle(33.5, 29.0)
    sim.add_particle(32.0, 28.0)
    sim.add_particle(30.5, 27.0)
    sim.add_particle(29.0, 26.0)
    sim.add_particle(27.5, 25.0)
    sim.add_particle(26.0, 24.0)
    sim.add_particle(24.5, 23.0)
    sim.add_particle(23.0, 22.0)
    sim.add_particle(21.5, 21.0)
