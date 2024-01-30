from lib.oppnet.communication import Message
from lib.oppnet.routing import RoutingParameters, next_step


def solution(sim):
    global particles
    current_round = sim.get_actual_round()
    global expected_delivery_round
    global messages

    if current_round == 1:

        # initialize the routing parameters
        particles = sim.get_particle_list()
        messages = []
        for particle in particles:
            r_params = RoutingParameters(algorithm=sim.routing_algorithm, scan_radius=sim.scan_radius,
                                         delivery_delay=sim.delivery_delay)
            r_params.set(particle)
        # create the messages
        sender = particles[0]
        receiver = particles[round(len(particles) / 2)]
        # send a message from the left most particle, to the right most particle
        messages.append(Message(sender=sender, receiver=receiver, start_round=current_round,
                                ttl=sim.message_ttl))

        expected_delivery_round = len(sim.get_particle_list())/2 + 1

    # execute the next routing step
    next_step(particles)

    # check the assertions
    check_round_message_assertions(sim.csv_round_writer, current_round, len(messages))
    check_message_assertions(sim.csv_round_writer.csv_msg_writer, current_round)

    if current_round == expected_delivery_round:
        sim.set_end()


def calculate_send_count_round(round_count, msgcount):
    return msgcount * (2 + (round_count - 1) * 4)


def check_message_assertions(csv_msg_writer, current_round):
    for message in messages:
        message_data = csv_msg_writer.get_csv_message_data(message)
        try:
            assert_message_sent_count(message_data.get_sent_count(), current_round)
        except AssertionError:
            print("Sent Count assertion failed in round {} for message no. {}"
                  .format(current_round, message.seq_number))

        try:
            assert_message_forwarding_count(message_data.get_forwarding_count(), current_round)
        except AssertionError:
            print("Forwarding Count assertion failed in round {} for message no. {}"
                  .format(current_round, message.seq_number))

        try:
            assert_message_delivery_count(message_data.get_delivery_count(), current_round)
        except AssertionError:
            print("Delivery Count assertion failed in round {} for message no. {}"
                  .format(current_round, message.seq_number))

        try:
            assert_message_delivery_round(message_data.get_delivery_round(), current_round)
        except AssertionError:
            print("Delivery Round assertion failed in round {} for message no. {}"
                  .format(current_round, message.seq_number))

        try:
            assert_message_delivery_hops(message_data.get_first_delivery_hops(), current_round)
        except AssertionError:
            print("First Delivery Hops assertion failed in round {} for message no. {}"
                  .format(current_round, message.seq_number))


def assert_message_sent_count(sent_count, current_round):
    particle_with_msg = []
    for i in range(1, current_round + 1):
        particle_with_msg.append(1 + ((i - 1) * 2))
    expected = 0
    for i in particle_with_msg:
        expected += i * 2
    if current_round == expected_delivery_round:
        expected -= 3*2
    assert expected == sent_count


def assert_message_forwarding_count(forwarding_count, current_round):
    expected = (current_round - 1) * 2
    if current_round == expected_delivery_round:
        expected -= 1
    assert expected == forwarding_count


def assert_message_delivery_count(delivery_count, current_round):
    expected = 2 if current_round == expected_delivery_round else 0
    assert expected == delivery_count


def assert_message_delivery_round(delivery_round, current_round):
    if not delivery_round:
        delivery_round = 0
    expected = expected_delivery_round if current_round == expected_delivery_round else 0
    assert expected == delivery_round


def assert_message_delivery_hops(delivery_hops, current_round):
    if not delivery_hops:
        delivery_hops = 0
    expected = expected_delivery_round - 1 if current_round == expected_delivery_round else 0
    assert expected == delivery_hops


def check_round_message_assertions(csv_round_writer, current_round, message_amount):
    try:
        assert_round_sent_count(csv_round_writer.get_messages_sent(), current_round, message_amount)
    except AssertionError:
        print("Sent Count assertion failed in round {}"
              .format(current_round))

    try:
        assert_round_forwarding_count(csv_round_writer.get_messages_forwarded(), current_round, message_amount)
    except AssertionError:
        print("Forwarding Count assertion failed in round {}"
              .format(current_round))

    try:
        assert_round_delivery_count(csv_round_writer.get_messages_delivered(), current_round, message_amount)
    except AssertionError:
        print("Delivery Count assertion failed in round {}"
              .format(current_round))


def assert_round_sent_count(sent_count, current_round, message_amount):
    expected = calculate_send_count_round(current_round, message_amount)
    if current_round == expected_delivery_round:
        expected -= (3 * 2)
    assert sent_count == expected


def assert_round_forwarding_count(forwarding_count, current_round, message_amount):
    expected = 0
    if current_round != expected_delivery_round and current_round != 1:
        expected = message_amount * 2
    elif current_round == expected_delivery_round:
        expected = 1
    assert forwarding_count == expected


def assert_round_delivery_count(delivery_round, current_round, message_amount):

    expected = message_amount * 2 if expected_delivery_round == current_round else 0
    assert delivery_round == expected


def assert_round_received_count(received_count, current_round, message_amount):
    expected = message_amount * 2 if expected_delivery_round == current_round else 0
    assert received_count == expected

