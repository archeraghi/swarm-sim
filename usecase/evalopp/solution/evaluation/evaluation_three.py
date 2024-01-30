import lib.oppnet.routing
from lib.oppnet.communication import Message
from lib.oppnet.mobility_model import MobilityModel

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


class DeliveryAssertions:
    def __init__(self, message, delivery_round, hops):
        self.message = message
        self.delivery_round = delivery_round
        self.hops = hops

    def execute(self, message):
        assert message.delivery_round == self.delivery_round
        assert message.hops == self.hops


def solution(sim):
    particles = sim.get_particle_list()
    global delivery_assertions

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
        m1 = Message(particles[0], particles[1], 1, sim.message_ttl)
        # middle to left
        m2 = Message(particles[1], particles[0], 1, sim.message_ttl)
        # middle to right
        m3 = Message(particles[1], particles[2], 1, sim.message_ttl)
        # right to middle
        m4 = Message(particles[2], particles[1], 1, sim.message_ttl)
        delivery_assertions = []

        for m in [m1, m2, m3, m4]:
            delivery_assertions.append(DeliveryAssertions(m, delivery_round=sim.delivery_delay * hops + start_round,
                                                          hops=hops))

        # expected hop count 2
        # expected delivery round 3
        hops = 2
        # left to right
        m5 = Message(particles[0], particles[2], 1, sim.message_ttl)
        delivery_assertions.append(DeliveryAssertions(m5, delivery_round=sim.delivery_delay * hops + start_round,
                                                      hops=hops))

        # expected hop count 2
        # expected delivery round 3
        # right to left
        m6 = Message(particles[2], particles[0], 1, sim.message_ttl)
        delivery_assertions.append(DeliveryAssertions(m6, delivery_round=sim.delivery_delay * hops + start_round,
                                                      hops=hops))

    for particle in particles:
        m_model = MobilityModel.get(particle)
        next_direction = m_model.next_direction(current_x_y=particle.coords)
        if next_direction is not False:
            particle.move_to_in_bounds(next_direction)

    lib.oppnet.routing.next_step(particles)

    # check the assertions
    if sim.get_actual_round() == sim.get_max_round():
        for assertion in delivery_assertions:
            m = assertion.message
            rcv_store = m.receiver.rcv_store
            try:
                assertion.execute(rcv_store.get_by_key(m.key))
            except AssertionError:
                print("Assertion for message {} failed".format(m.seq_number))
            except KeyError:
                print("Message {} not delivered".format(m.seq_number))
