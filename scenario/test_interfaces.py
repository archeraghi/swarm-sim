
from lib.swarm_sim_header import get_coordinates_in_direction, get_multiple_steps_in_direction


def scenario(world):

    dirs = world.grid.get_directions_list()

    world.add_particle(world.grid.get_center(), color=(1.0, 0.0, 0.0, 1.0))
    tile_pos = get_coordinates_in_direction(world.grid.get_center(), dirs[0])
    world.add_tile(tile_pos)
    loc_pos = get_coordinates_in_direction(tile_pos, dirs[1])
    world.add_location(loc_pos)

    # 1st ring
    ring1 = world.grid.get_n_sphere_border(world.grid.get_center(), 1)

    for m in ring1:
        world.add_particle(m, color=(0.2, 0.2, 0.2, 1.0))

    # 2nd ring
    ring2 = world.grid.get_n_sphere_border(world.grid.get_center(), 2)

    for m in ring2:
        world.add_particle(m, color=(0.5, 0.5, 0.5, 1.0))

    tile_pos1 = get_multiple_steps_in_direction(world.grid.get_center(), dirs[0], 4)
    tile_pos2 = get_multiple_steps_in_direction(tile_pos1, dirs[1], 2)
    tile_pos3 = get_multiple_steps_in_direction(tile_pos2, dirs[2], 2)
    tile_pos4 = get_multiple_steps_in_direction(tile_pos3, dirs[3], 2)

    world.add_tile(tile_pos1)
    world.add_tile(tile_pos2)
    world.add_tile(tile_pos3)
    world.add_tile(tile_pos4)

