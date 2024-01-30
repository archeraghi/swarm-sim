from enum import Enum

from lib.oppnet.communication import send_message
from lib.oppnet.meta import EventType, process_event


class Algorithm(Enum):
    Epidemic = 0
    Epidemic_MANeT = 1


class MANeTRole(Enum):
    Router = 0
    Node = 1


class SendEvent:

    def __init__(self, messages, start_round, delay, store, sender, receiver):
        """
        :param messages: Iterable of :class:`~comms.Message` to be send.
        :type messages: Iterable
        :param start_round: The simulator round the SendEvent was created in.
        :type start_round: int
        :param delay: The number of rounds to wait until the message is delivered.
        :type delay: int
        :param store: The store the messages originate from.
        :type store: :class:`~messagestore.MessageStore`
        :param sender: The sender of the message.
        :type sender: :class:`~particle.Particle`
        :param receiver: The receiver of the message.
        :type receiver: :class:`~particle.Particle`
        """
        self.messages = messages
        self.start_round = start_round
        self.delay = delay
        self.store = store
        self.sender = sender
        self.receiver = receiver

    def fire_event(self):
        """
        Sends the actual messages
        """
        for m in self.messages:
            send_message(self.store, self.sender, self.receiver, m)

    def check_delay(self, current_round):
        """
        Checks whether the message is ready to be delivered.
        :param current_round: Current simulator round
        :type current_round: int.
        :return: If message is ready to be delivered
        :rtype: bool
        """
        return self.start_round + self.delay == current_round

    @staticmethod
    def create_net_events(messages, current_round, store, sender, receiver):
        """
        Creates NetworkEvents in the simulators EventQueue for each message to be send
        :param messages: Iterable of messages.
        :type messages: Iterable
        :param current_round: Current round of the simulator.
        :type current_round: int
        :param store: The store the :param messages: originate from.
        :type store: :class:`~messagestore.MessageStore`
        :param sender: Sender of the messages.
        :type sender: :class:`~particle.Particle`
        :param receiver: Receiver of the messages
        :type receiver: :class:`~particle.Particle`
        :return: The SendEvent for the iterable of messages
        :rtype: :class:`~routing.SendEvent`
        """
        delivery_delay = RoutingParameters.get(sender).delivery_delay
        for message in messages:
            process_event(EventType.MessageSent, sender, receiver, message)
        return SendEvent(messages, current_round, delivery_delay, store, sender, receiver)


class RoutingParameters:

    def __init__(self, algorithm, scan_radius, manet_role=None, manet_group=0, delivery_delay=2):
        """
        :param algorithm: The routing algorithm to be used.
        :type algorithm: :class:`~routing.Algorithm`
        :param scan_radius: Scan radius for particle scanning.
        :type scan_radius: int
        :param manet_role: Role of the particle in an MANeT island.
        :type manet_role: :class:`~routing.MANeTRole`
        :param manet_group: Group the particle belongs to.
        :type manet_group: int
        :param delivery_delay: The number of rounds to wait until the message is delivered.
        :type delivery_delay: int
        """
        if type(algorithm) == str:
            self.algorithm = Algorithm[algorithm]
        else:
            self.algorithm = algorithm
        self.manet_role = manet_role
        self.manet_group = manet_group
        if manet_role is None:
            self.manet_role = MANeTRole.Node
        self.scan_radius = scan_radius
        self.delivery_delay = delivery_delay
        self.send_events = []

    def add_events(self, events):
        """
        Adds SendEvents to the RoutingParameter object.
        :param events: Iterable of :class:`~routing.SendEvent`
        :type events: Iterable
        """
        self.send_events.append(events)

    def get_next_events(self, current_round):
        """
        Gets the next list of SendEvents that are due, i.e. which are ready to be delivered. Events are then popped
        from the list.
        :param current_round: The current simulator round
        :type current_round: int
        :return: List of next due SendEvents
        :rtype: List
        """
        if not self.send_events:
            return []
        send_events = self.send_events[0]
        try:
            if send_events[0][0].check_delay(current_round):
                self.send_events.pop(0)
                return send_events
        except IndexError:
            pass
        try:
            if send_events[1][0].check_delay(current_round):
                self.send_events.pop(0)
                return send_events
        except IndexError:
            return []

    def set(self, particle):
        setattr(particle, "routing_params", self)

    @staticmethod
    def get(particle):
        """
        Gets the routing_params attribute of :param particle:.
        :param particle: The particle to get the attribute from.
        :type particle: :class:`~particle.Particle`
        :return: MobilityModel of :param particle:.
        :rtype: :class:`~mobility_model.MobilityModel`
        """
        return getattr(particle, "routing_params")

    @staticmethod
    def same_manet_group(particle1, particle2):
        """
        Compares the MANeT groups of two particles :param particle1: and :param particle2:.
        :param particle1: First particle
        :type particle1: :class:`~particle.Particle`
        :param particle2: Second particle
        :type particle2: :class:`~particle.Particle`
        :return: If :param particle1: and :param particle2: are in the same MANeT group.
        :rtype: bool
        """
        rp1, rp2 = RoutingParameters.get(particle1), RoutingParameters.get(particle2)
        return rp1.manet_group == rp2.manet_group


def next_step(particles, current_round, scan_radius=None):
    """
    Executest the next routing steps for each particle in order.
    :param particles: List of particles
    :type particles: list
    :param current_round: Current simulator round.
    :type current_round: int
    :param scan_radius: Particle scan radius.
    :type scan_radius: int
    """
    # execute the SendEvents for each particle
    for particle in particles:
        routing_params = RoutingParameters.get(particle)
        if scan_radius is not None:
            routing_params.scan_radius = scan_radius

        if routing_params.algorithm == Algorithm.Epidemic_MANeT:
            __create_send_events_manet__(particle, current_round)
        elif routing_params.algorithm == Algorithm.Epidemic:
            __next_step_epidemic(particle, current_round)


def __execute_send_events__(routing_params, current_round):
    """
    Gets the next step send events and executest them.
    :param routing_params: The routing parameters of :param particle:.
    :type routing_params: :class:`~routing.RoutingParameters`
    :param current_round: Current simulator round.
    :type current_round: int
    """
    # check for messages to send
    send_events = routing_params.get_next_events(current_round)
    if send_events:
        for send_event in send_events:
            if isinstance(send_event, SendEvent):
                send_event.fire_event()
            else:
                for event in send_event:
                    event.fire_event()


def __next_step_epidemic(sender, current_round, nearby=None):
    """
    Creates SendEvents for a :param particle:.
    :param particle: The particle which creates SendEvents.
    :type particle: :class:`~particle.Particle`
    :param current_round: Current simulator round.
    :type current_round: int
    """

    routing_params = RoutingParameters.get(sender)
    if nearby is None:
        nearby = sender.scan_for_particle_within(hop=routing_params.scan_radius)
        if nearby is None:
            return

    for msg in list(sender.send_store):
        for neighbour in nearby:
            send_message(sender, neighbour, msg)


def __create_send_events_manet__(particle, current_round):
    """
    Creates SendEvents for a :param particle: depending on MANeT role.
    :param particle: The particle which routing model should be executed.
    :type particle: :class:`~particle.Particle`
    :param current_round: Current simulator round.
    :type current_round: int
    """
    routing_params = RoutingParameters.get(particle)
    nearby = particle.scan_for_particle_within(hop=routing_params.scan_radius)
    if nearby is None:
        return

    if routing_params.manet_role == MANeTRole.Node:
        nearby = [neighbour for neighbour in nearby if RoutingParameters.same_manet_group(particle, neighbour)]
        __next_step_epidemic(particle, current_round, nearby)

    elif routing_params.manet_role == MANeTRole.Router:
        __next_step_epidemic(particle, current_round)
