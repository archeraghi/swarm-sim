

# initialize the memory of the particles
def init_particles(particle_list):
    for particle in particle_list:
        init_particle(particle)


def init_particle(particle):
    particle.write_memory_with("Leader", 0)
    particle.write_memory_with("Mark", 0)
    particle.write_memory_with("AnnounceNext", None)
    particle.write_memory_with("Order", None)
    particle.write_memory_with("Direction", None)
    particle.write_memory_with("Moving", 0)
    particle.write_memory_with("WayForN", None)
    particle.write_memory_with("UpdateState", None)


def set_nbs_announce_next_false(particle):
    nbs = particle.scan_for_particle_within(1)
    for nb in nbs:
        if nb.read_memory_with("Leader") == 1 and nb.read_memory_with("AnnounceNext") != 0:
            particle.write_to_with(nb,"AnnounceNext", 0)
            set_nbs_announce_next_false(nb)

def neighbour_of_leader(particle):
    if particle.read_memory_with("Leader") == 0:
        for nb in particle.scan_for_particle_within(1):
            if nb.read_memory_with("Leader") >= 1 and nb.read_memory_with("WayForN") == None:
                particle.write_to_with(nb, "WayForN", calc_dir(particle, nb))
                spread_way(nb)

# spreads a way between the leaders/placed to the non-leader
def spread_way(particle):
    if particle.read_memory_with("Leader") >= 1 and particle.read_memory_with("Mark") == 0:
        particle.write_memory_with("Mark", 1)
        for nb in particle.scan_for_particle_within(1):
            if nb.read_memory_with("Leader") >= 1 and nb.read_memory_with("WayForN") == None:
                particle.write_to_with(nb, "WayForN", calc_dir(particle, nb))
        for nb in particle.scan_for_particle_within(1):
            if nb.read_memory_with("Leader") >= 1 and nb.read_memory_with("WayForN") != None:
                spread_way(nb)

# calcs how p2 has to move to replace p1
def calc_dir(p1, p2):
    i = 0
    while i < 6:
        tmp = p2.get_particle_in(i)
        if tmp == p1:
            return i
        i = i + 1

def spread_moving(particle):
    if particle.read_memory_with("Moving") == 0:
        particle.write_memory_with("Moving", 1)
        for nb in particle.scan_for_particle_within(1):
            if nb.read_memory_with("Leader") >= 1 and nb.read_memory_with("Moving") == 0:
                spread_moving(nb)

def replacement(particle):
    order = particle.read_memory_with("Order")
    order = order+1

    if particle.read_memory_with("Leader") >= 1:
        dir_for_next = particle.read_memory_with("WayForN")
        next = particle.get_particle_in(dir_for_next)

        particle.write_to_with(next, "Order", order)
        particle.write_to_with(next, "Direction", calc_dir(particle, next))
        particle.write_to_with(next, "UpdateState", particle.read_memory_with("Leader"))

        next.set_color(3)

        return replacement(next)

    else:
        for nb in particle.scan_for_particle_within(1):
            if nb.read_memory_with("Leader") == 0 and nb.read_memory_with("Direction") == None:

                particle.write_to_with(nb, "Order", order)
                particle.write_to_with(nb, "Direction", calc_dir(particle, nb))
                particle.write_to_with(nb, "UpdateState", particle.read_memory_with("Leader"))

                nb.set_color(3)

                return replacement(nb)

def get_first_to_move(particle):
    if particle.read_memory_with("Order") == 1:
        particle.write_memory_with("UpdateState", 2)
        move_in_right_order(particle, 1)

def move_in_right_order(particle, order):
    if particle.read_memory_with("Order") != order:
        return

    next = None
    nbs = particle.scan_for_particle_within(1)
    if nbs != None:
        for nb in particle.scan_for_particle_within(1):
            if nb.read_memory_with("Order") == (order+1):
                next = nb
                break

    dir = particle.read_memory_with("Direction")
    particle.move_to(dir)
    particle.set_color(1)

    if next != None:
        move_in_right_order(next, (order+1))

def update_state(particle):
    if particle.read_memory_with("UpdateState") != None:
        state = particle.read_memory_with("UpdateState")
        particle.write_memory_with("Leader", state)

def refresh_mem(particle):
    particle.write_memory_with("Order", None)
    particle.write_memory_with("Mark", 0)
    particle.write_memory_with("Direction", None)
    particle.write_memory_with("AnnounceNext", None)
    particle.write_memory_with("Moving", 0)
    particle.write_memory_with("WayForN", None)
    particle.write_memory_with("UpdateState", None)
    if particle.read_memory_with("Leader") == 1:
        particle.set_color(4)
    if particle.read_memory_with("Leader") == 2:
        particle.set_color(5)

def is_formed(sim):
    for particle in sim.get_particle_list():
        if particle.read_memory_with("Leader") != 1:
            return
    sim.success_termination()

def add_random_particle(sim):
    for particle in sim.get_particle_list():
        i = 0
        while i < 6:
            if particle.get_particle_in(i) is None:
                pos = sim.get_coords_in_dir(particle.coords, i)
                new = sim.add_particle(pos[0], pos[1])
                return new
            i = i+1