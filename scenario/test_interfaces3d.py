"""
A world is created that has particles formated in a ring structure that is up to 5 hops big
"""


def scenario(world):
    world.add_particle(0, 0, 0)
    world.add_particle(-1, 0, 0)
    world.add_tile(1, 0.0, 0.0)
    world.add_tile(1, 0.0, 2.0)
    world.add_marker(-1, 0.0, 0.0)
    world.add_marker(-1, 0.0, -3.0)

    print(world.particles[0])
