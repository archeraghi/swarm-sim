def scenario(sim):
    sim.add_particle(0, 0)
    index = 0
    while len(sim.particles) <= 168:
        coords = sim.particles[index].coords
        index += 1
        particles = sim.get_particle_map_coords()
        for i in range(0, 6):
            new_coords = sim.get_coords_in_dir(coords, i)
            if new_coords not in particles.keys():
                sim.add_particle(new_coords[0], new_coords[1])
