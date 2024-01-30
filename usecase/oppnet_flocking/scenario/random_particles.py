import csv
import os
import random


def scenario(world):
    x_min, x_max = int(-world.get_world_x_size()), int(world.get_world_x_size())
    y_min, y_max = int(-world.get_world_y_size()), int(world.get_world_y_size())

    particle_count = 50

    csv_file = open(world.config_data.directory_name + '/particle_coordinates.csv', 'w', newline='')
    writer = csv.writer(csv_file)
    writer.writerow(["x", "y"])

    scenario_file = open(os.getcwd() + '/scenario/random_{}.py'.format(particle_count), 'w', newline='\n')
    scenario_file.writelines(['from lib.swarm_sim_header import red, blue\n', '\n\n', 'def scenario(world):\n'])

    # add borders
    scenario_file.writelines(['    # add borders as tiles\n'])
    for x in range(round(x_min - 2), round(x_max + 2)):
        for y in [y_min - 2, y_max + 2]:
            world.add_tile((x, y, 0))
            scenario_file.writelines(['    world.add_tile(({}, {}, 0))\n'.format(x, y)])
            if x != y:
                world.add_tile((y, x, 0))
                scenario_file.writelines(['    world.add_tile(({}, {}, 0))\n'.format(y, x)])

    coordinates = []
    for _ in range(particle_count):
        x, y = random.randint(x_min, x_max), random.randrange(y_min, y_max, 2)
        while [x, y] in coordinates:
            x, y = random.randint(x_min, x_max), random.randrange(y_min, y_max, 2)
        world.add_particle((x, y, 0))

        coordinates.append([x, y])

        writer.writerow([x, y])
        scenario_file.writelines(['    world.add_particle(({}, {}, 0))\n'.format(x, y)])

    csv_file.close()
    scenario_file.close()


