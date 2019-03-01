"""
A world is created that has two particles, two locations, and two tiles.
"""

def create_world(world):
    world.add_particle(0, 0)
    world.add_particle(-1, 0)
    world.add_tile(1, 0)
