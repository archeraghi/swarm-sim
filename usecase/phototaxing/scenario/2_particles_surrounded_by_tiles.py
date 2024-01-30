from lib.tile import blue, red


def scenario(sim):
    # Adding all the tiles to make the boundaries for the scenario
    # Red tiles emit light, blue tiles will later be used as a success condition
    sim.add_tile(-5, 0, color=red)
    sim.add_tile(15, 0, color=blue)
    for i in range(1, 3):
        sim.add_tile(-5, 2*i, color=red)
        sim.add_tile(-5, -2*i, color=red)
        sim.add_tile(-5.5, 2 * i - 1, color=red)
        sim.add_tile(-5.5, -2 * i + 1, color=red)

        sim.add_tile(15, 2 * i, color=blue)
        sim.add_tile(15, -2 * i, color=blue)
        sim.add_tile(15.5, 2 * i - 1, color=blue)
        sim.add_tile(15.5, -2 * i + 1, color=blue)

    sim.add_tile(-5.5, 5)
    sim.add_tile(-5.5, -5)

    for i in range(1, 21):
        sim.add_tile(-5.5 + i, 5)
        sim.add_tile(-5.5 + i, -5)

    # value represents direction:
    # 2 = East
    for tile in sim.tiles:
        if tile.get_color() == red:
            tile.write_memory_with("light_emission", 1)

    # Now we add the particles
    sim.add_particle(0, 0)
    sim.add_particle(-1, 0)
