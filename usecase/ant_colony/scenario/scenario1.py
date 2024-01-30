def scenario(world):

    # Ants
    part_num = 0
    while part_num <= 40:
        ant = world.add_particle(0, 0)
        setattr(ant, "way_home_list", [])
        part_num += 1

    # Food
    # world.add_tile(6.0, 8.0)
    # world.add_tile(-6.5, 7.0)
    # world.add_tile(6.0, -8.0)
    # world.add_tile(-6.5, -7.0)
    world.add_tile(0.5, 7.0)
    # world.add_tile(6.5, -1.0)
    # world.add_tile(-4.5, 1.0)
    # world.add_tile(-0.5, -7.0)

    # Base
    world.add_marker(0, 0, 1)