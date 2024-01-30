"""
A world is created that has particles formated in a ring structure that is up to 5 hops big
"""


def scenario(world):

    world.add_particle(world.grid.get_center())

    particle_ring = world.grid.get_n_sphere_border((0, 0, 0), 1)
    tile_ring = world.grid.get_n_sphere_border((0, 0, 0), 3)
    location_ring = world.grid.get_n_sphere_border((0, 0, 0), 5)

    for p in particle_ring:
        world.add_particle(p)

    for t in tile_ring:
        world.add_tile(t)

    for l in location_ring:
        world.add_location(l)
