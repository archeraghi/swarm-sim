from lib.tile import gray, blue, red, black


def scenario(sim):
    # This creates the initial tiles in the middle (y-axis)
    sim.add_tile(-10, 0, color=red)
    sim.add_tile(10, 0, color=blue)
    for i in range(1, 10):
        # Red tiles will emit light
        sim.add_tile(-10, 2*i, color=red)
        sim.add_tile(-10, -2*i, color=red)
        sim.add_tile(-10.5, 2 * i - 1, color=red)
        sim.add_tile(-10.5, -2 * i + 1, color=red)

        # Blue tiles will be goal tiles
        sim.add_tile(10, 2 * i, color=blue)
        sim.add_tile(10, -2 * i, color=blue)
        sim.add_tile(10.5, 2 * i - 1, color=blue)
        sim.add_tile(10.5, -2 * i + 1, color=blue)

    # Gray tiles are just boundaries, so that the particles can't escape the field
    for i in range(1, 21):
        sim.add_tile(-10.5 + i, 19, color=gray)
        sim.add_tile(-10.5 + i, -19, color= gray)

    for tile in sim.tiles:
        if tile.color == [0.8, 0.0, 0.0]:
            tile.write_memory_with("light_emission", 1)

    # Now we add the particles
    sim.add_particle(0, 0)
    sim.add_particle(-1, 0)
    sim.add_particle(-2, 0)
    sim.add_location(0, 0)
