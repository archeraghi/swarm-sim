from lib.std_lib import green, red


def scenario(sim):
    # bottom-left
    sim.add_particle(x=-3.5, y=-3, color=red)
    # bottom-right
    sim.add_particle(x=3.5, y=-3, color=green)
    # top-left
    sim.add_particle(x=-3.5, y=3, color=red)
    # top-right
    sim.add_particle(x=3.5, y=3, color=green)

    # bottleneck particle
    sim.add_particle(x=0, y=0)
    """
    sim.add_particle(x=-3.5, y=-3.5, color=red)
    possible bug?
    """
    # one hop particles in range
    sim.add_particle(2.0, -2.0)
    sim.add_particle(2.0, 2.0)
    sim.add_particle(-2.0, 2.0)
    sim.add_particle(-2.0, -2.0)
