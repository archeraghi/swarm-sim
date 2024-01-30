def scenario(world):

    # Ants
    part_num = 0
    while part_num < 32:
        ant = world.add_particle(0, 0)
        setattr(ant, "way_home_list", [])
        setattr(ant, "phero_counter", 1)
        part_num += 1

    # Food
    world.add_tile(-5.0, -0.0)
    world.add_tile(-2.5, 5.0)
    world.add_tile(2.5, 5.0)
    world.add_tile(5.0, -0.0)
    world.add_tile(-2.5, -5.0)
    world.add_tile(2.5, -5.0)

    # Base
    world.add_marker(0, 0, 1)