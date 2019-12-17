
def scenario(world):

    tile_ring = world.grid.get_n_sphere_border((0, 0, 0), 2)
    for location in tile_ring:
        world.add_tile(location)

    particle_ring = world.grid.get_n_sphere_border((0, 0, 0), 4)
    for location in particle_ring:
        world.add_particle(location)
