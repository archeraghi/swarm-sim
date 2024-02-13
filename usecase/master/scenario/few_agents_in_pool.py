

def scenario(world):

    #item_ring = world.grid.get_n_sphere_border((0, 0, 0), 9)
    #for item in item_ring:
        #world.add_item(item)

    agent_ring = world.grid.get_n_sphere_border((0, 0, 0), 3)
    for agent in agent_ring:
        world.add_agent(agent)
    agent_ring = world.grid.get_n_sphere_border((0, 0, 0), 2)
    for agent in agent_ring:
        world.add_agent(agent)




    # Causes problems:

    # world.add_item(-4, 0)
    # world.add_item(-4.5, -1)
    # world.add_item(-5, -2)
    # world.add_item(-5.5, -3)
    # world.add_item(-6, -4)
    #
    # world.add_item(4, 0)
    # world.add_item(4.5, -1)
    # world.add_item(5, -2)
    # world.add_item(5.5, -3)
    # world.add_item(6, -4)

    #

    world.add_item(-6.5, -5)
    world.add_item(-5.5, -5)
    world.add_item(-4.5, -5)
    world.add_item(-3.5, -5)
    world.add_item(-2.5, -5)
    world.add_item(-1.5, -5)
    world.add_item(-0.5, -5)
    world.add_item(0.5, -5)
    world.add_item(1.5, -5)
    world.add_item(2.5, -5)
    world.add_item(3.5, -5)
    world.add_item(4.5, -5)
    world.add_item(5.5, -5)
    world.add_item(6.5, -5)




    # world.add_item(-12.5, 1)
    # world.add_item(-12, 0)
    # world.add_item(-12.5, -1)
    # world.add_item(-12, -2)
    # world.add_item(-12.5, -3)
    # world.add_item(-12, -4)
    #
    # world.add_item(-11.5, -5)
    # world.add_item(-10.5, -5)
    # world.add_item(-9.5, -5)
    # world.add_item(-8.5, -5)
    # world.add_item(-7.5, -5)

    # world.add_item(7.5, -5)
    # world.add_item(8.5, -5)
    # world.add_item(9.5, -5)
    # world.add_item(10.5, -5)
    # world.add_item(11.5, -5)
    #
    # world.add_item(12.5, 1)
    # world.add_item(12, 0)
    # world.add_item(12.5, -1)
    # world.add_item(12, -2)
    # world.add_item(12.5, -3)
    # world.add_item(12, -4)
