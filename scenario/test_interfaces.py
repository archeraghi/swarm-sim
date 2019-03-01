"""
A world is created that has particles formated in a ring structure that is up to 5 hops big
"""
def create_world(world):
    world.add_particle(0, 0, color=3)
    world.add_tile(1.0, 0.0)
    world.add_location(3.0, 2.0)

    # 1st ring
    world.add_particle(1.000000, 0.000000, color=1)
    world.add_particle(-1.000000, 0.000000, color=1)
    world.add_particle(0.500000, 1.000000, color=1)
    world.add_particle(0.500000, -1.000000, color=1)
    world.add_particle(-0.500000, 1.000000, color=1)
    world.add_particle(-0.500000, -1.000000, color=1)

    # 2nd ring
    world.add_particle(2.000000, 0.000000, color=2)
    world.add_particle(-2.000000, 0.000000, color=2)
    world.add_particle(1.500000, 1.000000, color=2)
    world.add_particle(1.500000, -1.000000, color=2)
    world.add_particle(-1.500000, 1.000000, color=2)
    world.add_particle(-1.500000, -1.000000, color=2)
    world.add_particle(1.000000, 2.000000, color=2)
    world.add_particle(1.000000, -2.000000, color=2)
    world.add_particle(0.000000, 2.000000, color=2)
    world.add_particle(0.000000, -2.000000, color=2)
    world.add_particle(-1.000000, 2.000000, color=2)
    world.add_particle(-1.000000, -2.000000, color=2)

    world.add_tile(4.00000, 6.000000)
    world.add_tile(2.500000, 7.000000)
    world.add_tile(4.00000, 8.000000)
    world.add_tile(2.500000, 9.000000)

