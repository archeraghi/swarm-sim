"""
A world is created that has particles formated in a ring structure that is up to 5 hops big
"""
import numpy

def scenario(world):

    #c = world.grid.get_circle((-1,0,0),4)
#
 #   for i in c:
  #      world.add_particle(*i)

    world.add_particle(0,0,0)
    world.add_tile(1,0,0)
    world.add_marker(2,0,0)