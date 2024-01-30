import random

def scenario(sim):
	amount = sim.config_data.p_amount
	created = 0

	while created < amount:
		x = 0 + (created*1)
		sim.add_particle(x, 0)
		created = created + 1