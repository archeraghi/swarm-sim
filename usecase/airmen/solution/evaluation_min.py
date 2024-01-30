import lib.oppnet.routing
from lib.oppnet.communication import Message
from lib.oppnet.mobility_model import MobilityModel


def solution(sim):
    particles = sim.get_particle_list()

    if sim.get_actual_round() == 1:
        # initialize the particle mobility models
        for particle in particles:
            m_model = MobilityModel(particle.coords[0], particle.coords[1], sim.mobility_model_mode)
            m_model.set(particle)
            r_params = lib.oppnet.routing.RoutingParameters(algorithm=sim.routing_algorithm,
                                                            scan_radius=sim.scan_radius,
                                                            delivery_delay=sim.delivery_delay)
            r_params.set(particle)

        # expected hop count 1
        # expected delivery round 2
        start_round = 1
        hops = 1
        # left to middle

        m1 = Message(particles[0], particles[2], 1, sim.message_ttl)
        particles[0].send_store.append(m1)

    lib.oppnet.routing.next_step(particles, sim.get_actual_round())
