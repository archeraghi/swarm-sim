
def scenario(sim):

    for i in range(-1,1):
        sim.add_particle(i, 0)
    for i in range(-1,0):
        sim.add_particle(i+0.5, 1)
    #for i in range(-1,1):
    #    sim.add_particle(i+0.5,-1)

    for particle in sim.get_particle_list():
        print(particle.coords)

    print("Particle amount", len(sim.get_particle_list()))