import solution.leader as l
import solution.help_methods as hm
import solution.decentralized_hexagon as d_hex
import solution.decentralized_square as d_squ
import solution.decentralized_triangle as d_tri
import solution.decentralized_line as d_line

NE = 0
E = 1
SE = 2
SW = 3
W = 4
NW = 5

form = 1

direction = [NE, E, SE, SW, W, NW]

def solution(sim):
    global form
    print("Runde", sim.get_actual_round())

    if sim.get_actual_round() == 1:
        hm.init_particles(sim.get_particle_list())
        l.elect(sim.get_particle_list())
        form = sim.config_data.formation

    add_new_particle(sim)

    for particle in sim.get_particle_list():
        if sim.get_actual_round() % 7 == 1:
            announce_next(particle)
        elif sim.get_actual_round() % 7 == 2:
            update_leaders(particle)
        elif sim.get_actual_round() % 7 == 3:
            hm.neighbour_of_leader(particle)
        elif sim.get_actual_round() % 7 == 4:
            calc_move(particle)
        elif sim.get_actual_round() % 7 == 5:
            if particle.read_memory_with("Moving") == 0:
                announce_right_placed_to_leaders(particle)
            else:
                hm.get_first_to_move(particle)
        elif sim.get_actual_round() % 7 == 6:
            hm.update_state(particle)
        elif sim.get_actual_round() % 7 == 0:
            hm.refresh_mem(particle)
            hm.is_formed(sim)

def announce_next(particle):
    if form == 1:
        d_hex.announce_next(particle)
    elif form == 2:
        d_squ.announce_next(particle)
    elif form == 3:
        d_tri.announce_next(particle)
    elif form == 4:
        d_line.announce_next(particle)

def update_leaders(particle):
    if form == 1:
        d_hex.update_leaders(particle)
    elif form == 2:
        d_squ.update_leaders(particle)
    elif form == 3:
        d_tri.update_leaders(particle)
    elif form == 4:
        d_line.update_leaders(particle)

def calc_move(particle):
    if form == 1:
        d_hex.calc_move(particle)
    elif form == 2:
        d_squ.calc_move(particle)
    elif form == 3:
        d_tri.calc_move(particle)
    elif form == 4:
        d_line.calc_move(particle)

def announce_right_placed_to_leaders(particle):
    if form == 1:
        d_hex.announce_right_placed_to_leaders(particle)
    elif form == 2:
        d_squ.announce_right_placed_to_leaders(particle)
    elif form == 3:
        d_tri.announce_right_placed_to_leaders(particle)
    elif form == 4:
        d_line.announce_right_placed_to_leaders(particle)

def add_new_particle(sim):
    if sim.config_data.dynamic == 1 and sim.get_actual_round() == 8:
        new = hm.add_random_particle(sim)
        hm.init_particle(new)