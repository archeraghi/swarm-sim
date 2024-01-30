def scenario(sim):
    for y in range(0, 10):
        for x in range(0, 10):
            if y%2 == 0:
                sim.add_particle(x, y)
            else:
                sim.add_particle(x+0.5, y)


