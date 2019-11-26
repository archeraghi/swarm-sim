"""
A world is created that has particles formated in a ring structure that is up to 5 hops big
"""
import random

def scenario(world):

    #c = world.grid.get_centered_circle(5)
    c = world.grid.get_centered_ring(5)
    #print(c)
    for p in c:
        world.add_particle(*p)
    #world.addtile(0,0,0)

    for particle in world.get_particle_list():
            particle.move_to(random.choice(list(world.grid.get_directions_dictionary().values())))

