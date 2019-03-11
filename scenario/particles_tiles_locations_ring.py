"""
A sim is created that has particles formated in a ring structure that is up to 5 hops big
"""



def scenario(sim):
    sim.add_particle(0, 0, color=3)
    # 1st ring
    sim.add_particle(1.000000, 0.000000, color=1)
    sim.add_particle(-1.000000, 0.000000, color=1)
    sim.add_particle(0.500000, 1.000000, color=1)
    sim.add_particle(0.500000, -1.000000, color=1)
    sim.add_particle(-0.500000, 1.000000, color=1)
    sim.add_particle(-0.500000, -1.000000, color=1)

    # 2nd ring
    sim.add_tile(2.000000, 0.000000, color=2)
    sim.add_tile(-2.000000, 0.000000, color=2)
    sim.add_tile(1.500000, 1.000000, color=2)
    sim.add_tile(1.500000, -1.000000, color=2)
    sim.add_tile(-1.500000, 1.000000, color=2)
    sim.add_tile(-1.500000, -1.000000, color=2)
    sim.add_tile(1.000000, 2.000000, color=2)
    sim.add_tile(1.000000, -2.000000, color=2)
    sim.add_tile(0.000000, 2.000000, color=2)
    sim.add_tile(0.000000, -2.000000, color=2)
    sim.add_tile(-1.000000, 2.000000, color=2)
    sim.add_tile(-1.000000, -2.000000, color=2)

    # 3rd ring
    sim.add_location(3.000000, 0.000000, color=3)
    sim.add_location(-3.000000, 0.000000, color=3)
    sim.add_location(2.500000, 1.000000, color=3)
    sim.add_location(2.500000, -1.000000, color=3)
    sim.add_location(-2.500000, 1.000000, color=3)
    sim.add_location(-2.500000, -1.000000, color=3)
    sim.add_location(2.000000, 2.000000, color=3)
    sim.add_location(2.000000, -2.000000, color=3)
    sim.add_location(-2.000000, 2.000000, color=3)
    sim.add_location(-2.000000, -2.000000, color=3)
    sim.add_location(1.500000, 3.000000, color=3)
    sim.add_location(1.500000, -3.000000, color=3)
    sim.add_location(0.500000, 3.000000, color=3)
    sim.add_location(0.500000, -3.000000, color=3)
    sim.add_location(-0.500000, 3.000000, color=3)
    sim.add_location(-0.500000, -3.000000, color=3)
    sim.add_location(-1.500000, 3.000000, color=3)
    sim.add_location(-1.500000, -3.000000, color=3)


