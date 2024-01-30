import solution.help_methods as hm

NE = 0
E = 1
SE = 2
SW = 3
W = 4
NW = 5

def announce_next(particle):
    if particle.read_memory_with("Leader") == 1 and particle.read_memory_with("AnnounceNext") is None:

        e = particle.get_particle_in(E)
        sw = particle.get_particle_in(SW)
        se = particle.get_particle_in(SE)
        if sw is not None and se is not None and e is not None:
            particle.write_memory_with("AnnounceNext", 1)
        else:
            particle.write_memory_with("AnnounceNext", 0)
            hm.set_nbs_announce_next_false(particle)

def update_leaders(particle):
    if particle.read_memory_with("Leader") == 1:
        e = particle.get_particle_in(E)
        sw = particle.get_particle_in(SW)
        se = particle.get_particle_in(SE)
        update_leaders_square(particle, e, sw, se)

def update_leaders_square(particle, e, sw, se):
    if particle.read_memory_with("AnnounceNext") == 1:
        particle.write_to_with(e, "Leader", 1)
        particle.write_to_with(sw, "Leader", 1)
        particle.write_to_with(se, "Leader", 1)
        e.set_color(4)
        sw.set_color(4)
        se.set_color(4)

    if particle.read_memory_with("AnnounceNext") == 0:
        if e is not None and e.read_memory_with("Leader") == 0:
            particle.write_to_with(e, "Leader", 2)
            e.set_color(5)
        if sw is not None and sw.read_memory_with("Leader") == 0:
            particle.write_to_with(sw, "Leader", 2)
            sw.set_color(5)
        if se is not None and se.read_memory_with("Leader") == 0:
            particle.write_to_with(se, "Leader", 2)
            se.set_color(5)

def calc_move(particle):
    if particle.read_memory_with("Leader") == 1 and particle.read_memory_with("WayForN") != None and particle.read_memory_with("Moving") == 0:
        e = particle.get_particle_in(E)
        se = particle.get_particle_in(SE)
        sw = particle.get_particle_in(SW)

        if se is None or sw is None or e is None:
            hm.spread_moving(particle)
        else:
            return

        if sw is None:
            particle.write_memory_with("Direction", SW)
        elif se is None:
            particle.write_memory_with("Direction", SE)
        elif e is None:
            particle.write_memory_with("Direction", E)

        particle.write_memory_with("Order", 1)
        hm.replacement(particle)
        particle.set_color(3)

def announce_right_placed_to_leaders(particle):
    if particle.read_memory_with("Leader") == 1 and particle.read_memory_with("Moving") == 0:
        e = particle.get_particle_in(E)
        sw = particle.get_particle_in(SW)
        se = particle.get_particle_in(SE)

        if e is not None and e.read_memory_with("Leader") == 2:
            particle.write_to_with(e, "Leader", 1)
            e.set_color(4)
        if sw is not None and sw.read_memory_with("Leader") == 2:
            particle.write_to_with(sw, "Leader", 1)
            sw.set_color(4)
        if se is not None and se.read_memory_with("Leader") == 2:
            particle.write_to_with(se, "Leader", 1)
            se.set_color(4)
