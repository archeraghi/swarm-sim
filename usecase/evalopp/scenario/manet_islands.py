from lib.std_lib import violett, yellow, green, red

num_part_per = 5
left = -2.5
right = -left
top = 3.0
bottom = -top


def scenario(world):
    # add tile boundaries
    for x in range(int(abs(world.get_sim_x_size()))):
        world.add_tile(x, 0)
        world.add_tile(-x, 0)
    for y in range(0, int(abs(world.get_sim_y_size())), 2):
        world.add_tile(0, y)
        world.add_tile(0, -y)
    # top-left
    world.add_particle(left, top, color=violett)

    world.add_particle(left + 1, top, color=violett)
    world.add_particle(left + 0.5, top - 1, color=violett)
    world.add_particle(left - 0.5, top - 1, color=violett)

    # bottom-left
    world.add_particle(left, bottom, color=yellow)
    world.add_particle(left + 1, bottom, color=yellow)
    world.add_particle(left + 0.5, bottom + 1, color=yellow)
    world.add_particle(left - 0.5, bottom + 1, color=yellow)
    # top-right
    world.add_particle(right, top, color=green)
    world.add_particle(right - 1, top, color=green)
    world.add_particle(right - 0.5, top - 1, color=green)
    world.add_particle(right + 0.5, top - 1, color=green)
    # bottom-right
    world.add_particle(right - 1, bottom, color=red)
    world.add_particle(right - 0.5, bottom + 1, color=red)
    world.add_particle(right + 0.5, bottom + 1, color=red)
    world.add_particle(right, bottom, color=red)
