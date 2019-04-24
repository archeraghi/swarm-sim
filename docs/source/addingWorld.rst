How to add a sim
===============

Before the ORN Simulator can be started, its simulation sim has to be created.
At lease one particle should be created that takse the action of the sim.
For creating a particle just create a python file e.g. one_particle_sim.py
in the folder robtotsOnTiles/sims/ and insert the  following code:


def scenario(self):

	self.add_particle(0,0)


That is all and you created a particle.


The same thing you can do it with creating locations and tiles. E.g creating two particles, tiles, and locations.
You have to create a python file e.g. two_particles_tiles_locations.py in robtotsOnTiles/sims/ and insert the  following code:


def scenario(self):
    self.add_particle(0, 0)
    self.add_particle(1, 0)
    self.add_location(2, 0)
    self.add_tile(-1, 0)




