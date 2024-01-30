import csv
import random

from lib.std_lib import red, blue, black


def scenario(sim):
    x_min, x_max = int(-sim.get_sim_x_size()), int(sim.get_sim_x_size())
    y_min, y_max = int(-sim.get_sim_y_size()), int(sim.get_sim_y_size())

    particle_count = 400

    csv_file = open(sim.directory + '/particle_coords.csv', 'w', newline='')
    writer = csv.writer(csv_file)
    writer.writerow(["x", "y"])

    scenario_file = open(sim.directory + '/random_{}.py'.format(particle_count), 'w', newline='\n')
    scenario_file.writelines(['from lib.std_lib import red, blue, black\n', '\n\n', 'def scenario(sim):\n'])

    # add borders
    scenario_file.writelines(['    # add borders as tiles\n'])
    for x in range(x_min - 2, x_max + 2):
        for y in [y_min - 2, y_max + 2]:
            sim.add_tile(x, y, red)
            scenario_file.writelines(['    sim.add_tile({}, {}, red)\n'.format(x, y)])
            if x != y:
                sim.add_tile(y, x, blue)
                scenario_file.writelines(['    sim.add_tile({}, {}, blue)\n'.format(x, y)])

    coords = []
    for _ in range(particle_count):
        x, y = random.randint(x_min, x_max), random.randrange(y_min, y_max, 2)
        while [x, y] in coords:
            x, y = random.randint(x_min, x_max), random.randrange(y_min, y_max, 2)
        sim.add_particle(x, y, black)

        coords.append([x, y])

        writer.writerow([x, y])
        scenario_file.writelines(['    sim.add_particle({}, {}, black)\n'.format(x, y)])

    csv_file.close()
    scenario_file.close()


