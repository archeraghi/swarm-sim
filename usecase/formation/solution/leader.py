import random
# elects leader with the highest id
def elect(particle_list):
    particle = get_random_particle(particle_list)
    particle.write_memory_with("Leader", 1)
    particle.set_color(4)

def get_random_particle(particle_list):
    return random.choice(particle_list)
