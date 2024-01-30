def scenario(world):

    # Ants
    part_num = 0
    while part_num < 31:
        ant = world.add_particle(0, 0)
        setattr(ant, "way_home_list", [])
        part_num += 1

    # Food
    world.add_tile(-13.0, 2.0)
    world.add_tile(-12.5, 1.0)
    world.add_tile(-13.5, 1.0)
    world.add_tile(-14.0, 0.0)
    world.add_tile(-13.0, 0.0)
    world.add_tile(-1.5, 13.0)
    world.add_tile(1.0, 14.0)
    world.add_tile(0.5, 13.0)
    world.add_tile(-0.5, 13.0)
    world.add_tile(-1.0, 14.0)
    world.add_tile(14.5, 1.0)
    world.add_tile(15.0, -0.0)
    world.add_tile(16.0, -0.0)
    world.add_tile(16.5, 1.0)
    world.add_tile(15.5, 1.0)
    world.add_tile(-2.5, -11.0)
    world.add_tile(-1.0, -12.0)
    world.add_tile(-1.5, -11.0)
    world.add_tile(-2.0, -12.0)
    world.add_tile(11.5, -11.0)
    world.add_tile(11.0, -10.0)
    world.add_tile(10.5, -11.0)

    # Base
    world.add_marker(0, 0, 1)