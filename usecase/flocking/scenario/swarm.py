def scenario(sim):
    sim.add_particle(0.0, 0.0)
    for y in range(0,10):
        for x in range(0,10):
            sim.add_particle(x+0.5,2*y+1.0)
            sim.add_particle(-(x + 0.5), 2 * y + 1.0)
            sim.add_particle(x + 0.5,-(2 * y + 1.0))
            sim.add_particle(-(x + 0.5), -(2 * y + 1.0))
            sim.add_particle(x,2*y)
            sim.add_particle(-x, 2 * y)
            sim.add_particle(x, -2 * y)
            sim.add_particle(-x,-  2 * y)
    print("Particle amount", len(sim.particles))