from lib.std_lib import green, red


def scenario(sim):
    sim.add_particle(0, 0, red)
    x, y = 0, 0
    coordinates = {(x - 1, y), (x + 1, y), (x - 0.5, y - 1), (x + 0.5, y - 1), (x - 0.5, y + 1), (x + 0.5, y + 1)}
    for hops in range(1, 100):
        for (x, y) in coordinates:
            sim.add_particle(x * hops, y * hops, green)
