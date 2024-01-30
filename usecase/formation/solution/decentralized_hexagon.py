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
        w = particle.get_particle_in(W)
        se = particle.get_particle_in(SE)
        sw = particle.get_particle_in(SW)
        ne = particle.get_particle_in(NE)
        nw = particle.get_particle_in(NW)

        if e is not None and w is not None and sw is not None and se is not None and nw is not None and ne is not None:
            particle.write_memory_with("AnnounceNext", 1)
        else:
            particle.write_memory_with("AnnounceNext", 0)
            hm.set_nbs_announce_next_false(particle)

def update_leaders(particle):
    if particle.read_memory_with("Leader") == 1:
        e = particle.get_particle_in(E)
        w = particle.get_particle_in(W)
        se = particle.get_particle_in(SE)
        sw = particle.get_particle_in(SW)
        ne = particle.get_particle_in(NE)
        nw = particle.get_particle_in(NW)

        update_leader_hexagon(particle, w, e, se, sw, ne, nw)
        update_placed_hexagon(particle, w, e, se, sw, ne, nw)

def update_leader_hexagon(particle, w, e, se, sw, ne, nw):
    if particle.read_memory_with("AnnounceNext") == 1:
        particle.write_to_with(w, "Leader", 1)
        particle.write_to_with(e, "Leader", 1)
        particle.write_to_with(sw, "Leader", 1)
        particle.write_to_with(se, "Leader", 1)
        particle.write_to_with(nw, "Leader", 1)
        particle.write_to_with(ne, "Leader", 1)
        w.set_color(4)
        e.set_color(4)
        sw.set_color(4)
        se.set_color(4)
        nw.set_color(4)
        ne.set_color(4)
def update_placed_hexagon(particle, w, e, se, sw, ne, nw):
    if particle.read_memory_with("AnnounceNext") == 0:
        update_to_placed(particle, w, e, se, sw, ne, nw)
def update_to_placed(particle, w, e, se, sw, ne, nw):
    if w is not None and w.read_memory_with("Leader") == 0:
        particle.write_to_with(w, "Leader", 2)
        w.set_color(5)
    if e is not None and e.read_memory_with("Leader") == 0:
        particle.write_to_with(e, "Leader", 2)
        e.set_color(5)
    if se is not None and se.read_memory_with("Leader") == 0:
        particle.write_to_with(se, "Leader", 2)
        se.set_color(5)
    if sw is not None and sw.read_memory_with("Leader") == 0:
        particle.write_to_with(sw, "Leader", 2)
        sw.set_color(5)
    if ne is not None and ne.read_memory_with("Leader") == 0:
        particle.write_to_with(ne, "Leader", 2)
        ne.set_color(5)
    if nw is not None and nw.read_memory_with("Leader") == 0:
        particle.write_to_with(nw, "Leader", 2)
        nw.set_color(5)

def calc_move(particle):
    if particle.read_memory_with("Leader") == 1 and particle.read_memory_with("WayForN") is not None and particle.read_memory_with("Moving") == 0:
        e = particle.get_particle_in(E)
        w = particle.get_particle_in(W)
        se = particle.get_particle_in(SE)
        sw = particle.get_particle_in(SW)
        ne = particle.get_particle_in(NE)
        nw = particle.get_particle_in(NW)

        if e is None or w is None or se is None or sw is None or ne is None or nw is None:
            hm.spread_moving(particle)
        else:
            return

        if w is None:
            particle.write_memory_with("Direction", W)
        elif e is None:
            particle.write_memory_with("Direction", E)
        elif se is None:
            particle.write_memory_with("Direction", SE)
        elif sw is None:
            particle.write_memory_with("Direction", SW)
        elif ne is None:
            particle.write_memory_with("Direction", NE)
        elif nw is None:
            particle.write_memory_with("Direction", NW)

        particle.write_memory_with("Order", 1)
        hm.replacement(particle)
        particle.set_color(3)

def announce_right_placed_to_leaders(particle):
    if particle.read_memory_with("Leader") == 1 and particle.read_memory_with("Moving") == 0:
        e = particle.get_particle_in(E)
        w = particle.get_particle_in(W)
        se = particle.get_particle_in(SE)
        sw = particle.get_particle_in(SW)
        ne = particle.get_particle_in(NE)
        nw = particle.get_particle_in(NW)

        placed_to_leaders_hexagon(particle, e, w, se, sw, ne, nw)

def placed_to_leaders_hexagon(particle, e, w, se, sw, ne, nw):
    if w is not None and w.read_memory_with("Leader") == 2:
        particle.write_to_with(w, "Leader", 1)
        w.set_color(4)
    if e is not None and e.read_memory_with("Leader") == 2:
        particle.write_to_with(e, "Leader", 1)
        e.set_color(4)
    if sw is not None and sw.read_memory_with("Leader") == 2:
        particle.write_to_with(sw, "Leader", 1)
        sw.set_color(4)
    if se is not None and se.read_memory_with("Leader") == 2:
        particle.write_to_with(se, "Leader", 1)
        se.set_color(4)
    if nw is not None and nw.read_memory_with("Leader") == 2:
        particle.write_to_with(nw, "Leader", 1)
        nw.set_color(4)
    if ne is not None and ne.read_memory_with("Leader") == 2:
        particle.write_to_with(ne, "Leader", 1)
        ne.set_color(4)