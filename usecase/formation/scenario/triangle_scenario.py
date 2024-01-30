import random
import math

def scenario(sim):
	d = 0

	created = 0
	amount = sim.config_data.p_amount

	start_pos = [0, 0]
	pos = [0, 0]
	while True:
		i = 0
		start_pos[0] = pos[0] - (0.5 * d)
		start_pos[1] = pos[1] - (1 * d)

		while i <= d:
			x = start_pos[0] + (1 * i)
			y = start_pos[1]
			if created < amount:
				sim.add_particle(x, y)
				print(sim.get_particle_map_coords()[0,0])
				created = created+1
			else:
				return
			i = i + 1
		d = d + 1

