from lib.oppnet.communication import Message
from lib.oppnet.point import Point
from lib.oppnet.routing import RoutingParameters, next_step


def solution(sim):
    current_round = sim.get_actual_round()
    global messages
    particles = sim.get_particle_list()

    if current_round == 1:

        # initialize the routing parameters
        messages = []
        for particle in particles:
            r_params = RoutingParameters(algorithm=sim.routing_algorithm, scan_radius=sim.scan_radius,
                                         delivery_delay=sim.delivery_delay)
            r_params.set(particle)

        for receiver in particles:
            if receiver != particles[0]:
                messages.append(Message(sender=particles[0], receiver=receiver, start_round=current_round,
                                        ttl=sim.message_ttl))

        print("end init")
    next_step(particles)

