"""
A world is created that has two particles, two markers, and two tiles.
"""


def scenario(world):
    world.add_particle(0, 0)
    world.add_particle(1, 0)
    world.add_marker(0.5, 1)
    world.add_tile(-1, 0)
    world.add_tile(1, 0)
