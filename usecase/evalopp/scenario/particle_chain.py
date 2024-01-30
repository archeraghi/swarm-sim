from lib.std_lib import black


def scenario(sim):
    n = 50
    for i in range(n):
        sim.add_particle(i, 0, black)
