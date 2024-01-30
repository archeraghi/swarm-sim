from lib import world, particle as particle_class
import copy
from lib.swarm_sim_header import *
import solution.p_max_lifetime.distance_calculation as distance_calc_mod
import solution.p_max_lifetime.read_write as read_write_mod
import solution.p_max_lifetime.p_max_calculation as p_max_calc_mod
import solution.p_max_lifetime.coating_alg as coating_mod
import solution.goal_test as goal_test

cycle_no = 3


def solution(sim: world) -> None:
    """
    Main solution function that is called each round
    @param sim: the current world state
    """
    # code for deleting particles to test robustness
    if sim.config_data.particle_fail_quote > 0 and sim.get_actual_round() == 300:
        for to_delete in list(filter(lambda x: x.willfail, sim.particles)):
            to_delete.delete_particle()

    if sim.get_actual_round() == 1:
        initialize_particles(sim)

    for particle in sim.particles:
        # resets all particles last movement direction every 10 cycles
        if sim.get_actual_round() % (cycle_no * 10) == 1:
            if len(particle.prev_direction) > 0:
                particle.prev_direction.pop(0)

        if sim.get_actual_round() % cycle_no == 1:
            if particle.wait:
                particle.wait = False
            else:
                move_cycle(particle)

        elif sim.get_actual_round() % cycle_no == 2:
            read_cycle(particle)

        elif sim.get_actual_round() % cycle_no == 0:
            write_cycle(particle)

    goal_test.end_sim(sim)


def initialize_particles(sim: world) -> None:
    """
    handles initialization for all particles in round 1
    @param sim: the current world state
    """
    for particle in sim.particles:
        coating_mod.initialize_particle(particle)
        if random.random() < sim.config_data.particle_fail_quote:
            particle.willfail = True
        particle.dest_t = random.choice(sim.get_tiles_list()).coordinates


def write_cycle(particle: particle_class) -> None:
    """
    lets the current particle send messages to its neighbors
    @param particle: the particle whose turn it is
    """
    particle.next_direction = coating_mod.coating_alg(particle)
    if particle.own_dist != math.inf:
        if len(particle.p_max.ids) > 0 and particle.p_max.dist > 0 and particle.next_direction is False:
            # particle.p_max_table.update({particle.p_max.id: particle.p_max.dist})
            read_write_mod.send_p_max_to_neighbors(particle)
        else:
            read_write_mod.send_own_dist_to_neighbors(particle)
    else:
        next_dir = get_next_direction_to(particle.coordinates[0], particle.coordinates[1],
                                         particle.dest_t[0], particle.dest_t[1])
        if particle.particle_in(next_dir):
            read_write_mod.send_target_tile(particle, next_dir)


def read_cycle(particle: particle_class) -> None:
    """
    Lets the current particle read messages from its neighbors and calculate distances for each neighbor location
    @param particle: the particle whose turn it is
    """
    if debug and debug_read:
        print("reading memory of particle", particle.number)
    particle.rcv_buf = read_write_mod.read_and_clear(particle.read_whole_memory())
    particle.nh_list = distance_calc_mod.calculate_distances(particle)
    p_max_calc_mod.find_p_max(particle)
    if particle.own_dist is math.inf:
        read_write_mod.check_for_new_target_tile(particle)
    particle.rcv_buf_dbg = copy.deepcopy(particle.rcv_buf)
    particle.rcv_buf.clear()


def move_cycle(particle: particle_class) -> None:
    """
    Lets the current particle move
    @param particle: the particle whose turn it is
    """
    if particle.next_direction is False and particle.own_dist > 1:
        if debug and debug_movement:
            print("moving closer to target tile")
        move_to_target_tile(particle)
    elif particle.next_direction is not False and not particle.particle_in(particle.next_direction) \
            and not particle.tile_in(particle.next_direction):
        move_to_next_dir(particle)
    coating_mod.reset_p_max(particle)


def move_to_next_dir(particle: particle_class) -> None:
    """
    Moves the particle to the next direction calculated by the algorithm
    @param particle: the particle whose turn it is
    """
    if len(particle.prev_direction) >= particle.max_prev_dirs:
        particle.prev_direction.pop(0)
    particle.prev_direction.append(get_the_invert(particle.next_direction))
    particle.move_to(particle.next_direction)
    if debug:
        print("dist list before moving", [str(neighbor) for neighbor in particle.nh_list])
        print("\n P", particle.number, " coates to", direction_number_to_string(particle.next_direction))
    new_own_dist = particle.nh_list[particle.next_direction].dist
    neighbor_left = particle.nh_list[direction_in_range(particle.next_direction - 1)]
    neighbor_right = particle.nh_list[direction_in_range(particle.next_direction + 1)]
    coating_mod.reset_attributes(particle)
    coating_mod.reset_p_max(particle)
    particle.wait = True
    particle.own_dist = new_own_dist
    particle.nh_list[direction_in_range(particle.prev_direction[-1] + 1)] = neighbor_left
    particle.nh_list[direction_in_range(particle.prev_direction[-1] - 1)] = neighbor_right


def move_to_target_tile(particle: particle_class) -> None:
    """
    Moves the particle in the global direction of it's target tile
    This method uses information from the world class
    @param particle: the particle whose turn it is
    """
    hit_a_matter = move_to_dest_step_by_step(particle, particle.dest_t, particle.prev_direction)
    if hit_a_matter or hit_a_matter is None:
        # reset_attributes(particle)
        if hit_a_matter is not None:
            if particle.own_dist > distance_calc_mod.calc_own_dist_t(hit_a_matter):
                particle.own_dist = distance_calc_mod.calc_own_dist_t(hit_a_matter)
            if hit_a_matter.type == "tile" and debug:
                print("got a distance from a tile")
    else:
        coating_mod.reset_attributes(particle)
        coating_mod.reset_p_max(particle)
        particle.wait = True
