import random
import math

def scenario(sim):
	amount = sim.config_data.p_amount
	created = 0

	n = math.ceil(math.sqrt(amount))
	print(n)
	j = 0
	while created < amount:
		i = 0
		while i < n:
			x = 0 - (j*0.5) + (i*1)
			y = 0 - (j*1)
			if created < amount:
				sim.add_particle(x, y)
				created = created+1
			else:
				return
			i = i+1
		j = j+1