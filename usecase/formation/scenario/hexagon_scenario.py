import random
import math

def scenario(sim):
	created = 0
	amount = sim.config_data.p_amount

	positions = [[0,0]]

	i = 0

	while created < amount:
		current_pos = positions[i]

		dir = 0
		while dir < 6:
			new_coords = sim.get_coords_in_dir(current_pos, dir)
			positions.append(new_coords)
			dir = dir + 1

		try:
			sim.get_particle_map_coords()[(current_pos[0]), current_pos[1]]
		except KeyError:
			sim.add_particle(current_pos[0], current_pos[1])
			created = created + 1
		i = i + 1