from lib.tile import gray, blue, red, black
import math
from math import sqrt

NE = 0
E = 1
SE = 2
SW = 3
W = 4
NW = 5


def directions():
    return {"NE": (0.5, 1),
            "E": (1, 0),
            "SE": (0.5, -1),
            "SW": (-0.5, -1),
            "W": (-1, 0),
            "NW": (-0.5, 1)}


def scenario(sim):
    sim.add_location(0, 0)

    # This value determines the length of the hexagon's sides
    hexagon_scale_factor = 12
    outer_hexagon_radius = hexagon_scale_factor * 2

    # This sets the out-most tiles of the hexagon
    sim.add_tile(outer_hexagon_radius/2, outer_hexagon_radius, color=gray)
    #sim.add_tile(outer_hexagon_radius, 0, color=blue)
    sim.add_tile(outer_hexagon_radius/2, -outer_hexagon_radius, color=gray)
    sim.add_tile(-outer_hexagon_radius/2, -outer_hexagon_radius, color=gray)
    sim.add_tile(-outer_hexagon_radius, 0, color=red)
    sim.add_tile(-outer_hexagon_radius/2, outer_hexagon_radius, color=gray)

    # This constructs all the six sides of the hexagon
    for i in range(1, outer_hexagon_radius):
        sim.add_tile(-outer_hexagon_radius/2 + i, outer_hexagon_radius, color=gray)
        # sim.add_tile(outer_hexagon_radius/2 + (0.5*i), outer_hexagon_radius - i, color=blue)
        # sim.add_tile(outer_hexagon_radius/2 + (0.5*i), -outer_hexagon_radius + i, color=blue)
        sim.add_tile(-outer_hexagon_radius/2 + i, -outer_hexagon_radius, color=gray)
        sim.add_tile(-outer_hexagon_radius/2 - (0.5*i), -outer_hexagon_radius + i, color=red)
        sim.add_tile(-outer_hexagon_radius/2 - (0.5*i), outer_hexagon_radius - i, color=red)

    # This adds the location for the finishing line
    sim.add_location(outer_hexagon_radius/2, 0, color=blue)
    for i in range(1, int(outer_hexagon_radius/2)):
        sim.add_location(outer_hexagon_radius / 2, i * 2, color=blue)
        sim.add_location(outer_hexagon_radius / 2, i * -2, color=blue)

    for tile in sim.tiles:
        if tile.color == [0.8, 0.0, 0.0]:
            tile.write_memory_with("light_emission", 1)

    # radius = 1  # This value determines the radius of the particle hexagon that is to be created
    # sim.add_particle(0, 0, color=red)
    # displacement = - radius + 0.5
    # iteration = 0
    # for i in range(1, radius+1):
    #     sim.add_particle( i, 0)
    #     sim.add_particle(-i, 0)
    # for i in range(1, radius+1):
    #     for j in range(0, (2*radius) - iteration):
    #         sim.add_particle(displacement + j, i)
    #         sim.add_particle(displacement + j, -i)
    #     iteration = iteration + 1
    #     displacement = displacement + 0.5
    #sim.param_lambda=2
    hexagon(sim, (0.0, 0.0), sim.param_lambda)
    #hexagon(sim, (0.0, 0.0), 128)

def hexagon(world, center, amount):
    created = 1
    amount = amount

    positions = [(center[0],center[1])]
    pp= [(center[0],center[1])]
    i = 0
    n=[]
    dirs = list(directions().values())
    while created < amount:
        for current_pos in positions:
            dir = 0
            while dir < 6 and created < amount:
                new_coords = (current_pos[0] + dirs[dir][0], current_pos[1]+ dirs[dir][1])
                dir = dir + 1
                if new_coords not in pp:
                    # if world.add_particle(current_pos):
                    #world.add_particle(current_pos)
                    pp.append(new_coords)
                    n.append(new_coords)
                    #     world.remove_particle_on(current_pos)
                    created = created + 1
            if created > amount:
                break
        positions = list(n)
        n.clear()
    layer = 0
    if created > 6:
        layer = math.ceil(-1/2 + sqrt( pow(-1/2, 2) - (1-created/3)) )
    for current_pos in pp:
        world.add_particle(current_pos[0], current_pos[1])



