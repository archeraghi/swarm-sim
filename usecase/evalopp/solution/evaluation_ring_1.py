from lib.oppnet.communication import Message
from lib.oppnet.routing import RoutingParameters, next_step

"""
Made for scenario:
    sim.add_particle(-1, 0)
    sim.add_particle(0, 0)
    sim.add_particle(1, 0)
    
This solution is supposed to evaluate assertions for message delivery within a small network of three particles, which
are only pair wise in range, i.e. particle 1 at x=-1, y=0, can see particle 2 at x=0, y=0 but not particle 3 at x=1,
y=0. Therefore delivery from particle 1 to particle 3 and in reverse will take two hops (delivery via particle 2, that
is in between the two particles). These messages are objects m5 and m6 in the solution below.

All other possible combinations of sender and receiver, that are not particle 1 and particle 3 are in m1 through m4.
These messages can be delivered directly and thus take one hop.

We can therefore assert the delivery rounds for each of the six messages:
    delivery_round = delivery_delay * hops + starting_round
As the starting round for all six messages is 1, we can for example expect messages 1 through 4 to be delivered in round
2 with delivery_delay = 1. Messages 5 and 6 would be expected in round 3 as they take one more hop.

"""


def solution(sim):
    particles = sim.get_particle_list()

    if sim.get_actual_round() == 1:
        # initialize the particle mobility models
        for particle in particles:
            r_params = RoutingParameters(algorithm=sim.routing_algorithm, scan_radius=sim.scan_radius,
                                         delivery_delay=sim.delivery_delay)
            r_params.set(particle)

        m1 = Message(particles[-1], particles[int(len(particles)/2)], 1, sim.message_ttl)
        # middle to left
        m2 = Message(particles[int(len(particles)/2)], particles[-1], 1, sim.message_ttl)

        print("Round: {} [] SentCounter: {}".format(sim.get_actual_round(),
                                                    calculate_send_count_round(sim.get_actual_round(), len(particles))
                                                    ))
        next_step(particles)


def calculate_send_count_round(round_count, particle_count):
    return particle_count * (2 + (round_count - 1) * 4)
