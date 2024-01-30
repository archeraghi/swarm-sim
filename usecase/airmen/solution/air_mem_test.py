from lib.point import Point



def solution(sim):
    particles = sim.get_particle_list()
    if sim.get_actual_round() == 1:
        sim.memory.add_delta_message_on(particles[0].get_id(), "hallo", Point(100, 0), 0, 1, 1000)
        sim.memory.add_delta_message_on(particles[0].get_id(), "hallo", Point(80, 0), 0, 1, 1000)
        sim.memory.add_delta_message_on(particles[0].get_id(), "hallo", Point(60, 0), 0, 1, 1000)
        sim.memory.add_delta_message_on(particles[0].get_id(), "hallo", Point(50, 0), 0, 1, 1000)
        sim.memory.add_delta_message_on(particles[0].get_id(), "hallo", Point(20, 0), 0, 1, 1000)
        sim.memory.add_delta_message_on(particles[0].get_id(), "hallo", Point(5, 0), 0, 1, 1000)
        sim.memory.add_delta_message_on(particles[0].get_id(), "hallo", Point(0, 0), 0, 1, 1000)