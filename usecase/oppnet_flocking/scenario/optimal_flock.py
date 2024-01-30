from lib.swarm_sim_header import get_hexagon_coordinates, black
from lib.world import World


def scenario(world: World):
    radius = world.config_data.flock_radius
    centre = (0, 0)
    hexagon = get_hexagon_coordinates(centre, radius)

    if world.config_data.particle_color is None:
        particle_color = black
    else:
        particle_color = world.config_data.particle_color

    for location in hexagon:
        world.add_particle(coordinates=location, color=particle_color)

    if world.config_data.border:
        # add borders
        x_min, x_max = int(-world.get_world_x_size()), int(world.get_world_x_size())
        y_min, y_max = int(-world.get_world_y_size()), int(world.get_world_y_size())
        for x in range(round(x_min - 2), round(x_max + 2)):
            for y in [y_min - 2, y_max + 2]:
                world.add_tile((x, y, 0))
                if x != y:
                    world.add_tile((y, x, 0))
