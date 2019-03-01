How to add a solution
===============

A solution tells the ORN simulator what to do while using the provided interfaces of the ORN simulator.
The solution module is called from the sim.py. That means that it can use all the instances of
sim.py. The most important one is the __max_round, __round_counter and __seed.

For adding a solutionn create a in the folder lib/solutions a python file e.g. yoursolution.py
and instert the following code inside:


	import logging  #just needed for printing outputs in the log file


	#the provided directions
	E = 0
	SE = 1
	SW = 2
	W = 3
	NW = 4
	NE = 5
	S = 6 # S for stop and not south

	direction = [E, SE, SW, W, NW, NE]  #direction list

	def solution(self, world):
    	"""
    	All the magic starts from here
    
    	:param self: The object instance of the sim.py 
    	:param world: The object instance of the created world
    	"""


	  






