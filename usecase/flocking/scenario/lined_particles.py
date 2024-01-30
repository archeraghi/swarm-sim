def scenario(sim):
    for i in range (0,6):
        sim.add_particle(i,0)
        sim.add_particle(-i,0)
