import copy
import random
from lib.point import Point


from lib.oppnet.meta import EventType, process_event


class Message:
    seq_number = 0

    def __init__(self, sender, receiver, start_round: int, ttl: int, content=None, is_copy=False, actual_receiver=None):
        """
        Initializes a Message instance and puts it in the sender's MessageStore.
        :param sender: The particle sending the message.
        :type sender: :class:`~particle.Particle`
        :param receiver: The intended receiving particle of the message.
        :type receiver: :class:`~particle.Particle`
        :param start_round: The round when the message was created.
        :type start_round: int
        :param ttl: Time-to-live value of the message.
        :type ttl: int
        :param content: The content of the message.
        :type content: any
        """
        self.original_sender = sender
        self.sender = sender
        if is_copy:
            self.actual_receiver = actual_receiver
        else:
            self.actual_receiver = receiver
        self.receiver = receiver
        self.seq_number = Message.seq_number
        self.key = self.__create_msg_key__()
        self.delivered = 0
        self.start_round = start_round
        self.delivery_round = 0
        self.forwarder = None
        self.ttl = ttl
        self.hops = 0
        self.content = content

        Message.seq_number += 1


    def get_receiver(self):
        return self.receiver

    def set_receiver(self, receiver):
        self.receiver = receiver

    def get_actual_receiver(self):
        return self.actual_receiver

    def set_actual_receiver(self, receiver):
        self.actual_receiver = receiver

    def __append_to_store__(self):
        try:
            self.sender.send_store.append(self)
        except OverflowError:
            process_event(EventType.ReceiverOutOfMem, self.sender, self.receiver, self)

    def get_sender(self):
        return self.sender


    def __copy__(self):
        new = type(self)(self.sender, self.receiver, self.start_round, self.ttl, self.content, is_copy=True,
                         actual_receiver=self.get_actual_receiver())
        new.key = self.key
        new.seq_p = self.seq_number
        new.hops = self.hops
        Message.seq_number -= 1
        return new

    def __create_msg_key__(self):
        """
        :return: the builtin identity of message.
        """
        return id(self)

    def inc_hops(self):
        """
        Increments message hop count
        """
        self.hops += 1

    def set_sender(self, sender):
        """
        Updates the sender.
        :param sender: The new sender
        :type sender: :class:`~particle.Particle`
        """
        self.sender = sender

    def update_delivery(self, delivery_round):
        if self.delivery_round == 0:
            self.delivery_round = delivery_round
        self.delivered += 1


def send_message(sender, receiver, message: Message):
    """
    Puts the :param message: object in the receiver's corresponding MessageStore. Depending on if the message is
    delivered to the sender or forwarded.
    :param msg_store: The MessageStore of the sender the message originates from.
    :type msg_store: :class:`~messagestore.MessageStore`
    :param sender: The particle sending the Message.
    :type sender: :class:`~particle.Particle`
    :param receiver: The intended receiver of the message.
    :type receiver: :class:`~particle.Particle`
    :param message: The message to send.
    :type message: :class:`~comms.Message`
    """

    current_round = sender.sim.get_actual_round()

    original = message
    message = copy.copy(original)
    message.set_sender(sender)
    message.set_receiver(receiver)
    message.inc_hops()  # TODO : move to coppy function ????
    msg_store = sender.send_store

    if message.hops == message.ttl:
        ttl_expired(original, msg_store, sender, receiver)
        return
    memory = sender.sim.memory


    # remove from original store if ttl expired after this send
    memory.add_delta_message_on(receiver.get_id(), message, Point(sender.coords[0], sender.coords[1]), current_round, sender.signal_velocity, 5)  # TODO: add attributes to particles
    if receiver.get_id() == message.get_actual_receiver().get_id():
        # remove original upon delivery
        msg_store.remove(original)


def ttl_expired(message, store, sender, receiver):
    """
    Handle expiry of TTL. Delete the message from :param store: and append a corresponding NetworkEvent in the
    simulator EventQueue.
    :param message: The message that expired.
    :type message: :class:`~comms.Message`
    :param store: The MessageStore containing the :param message:.
    :type store: :class:`~messagestore.MessageStore`
    :param sender: The sender of the message.
    :type sender: :class:`~particle.Particle`
    :param receiver: The intended receiver of the message.
    :type receiver: :class:`~particle.Particle`
    """
    try:
        store.remove(message)
    except ValueError:
        pass
    finally:
        process_event(EventType.MessageTTLExpired, sender, receiver, message)


def __deliver_message__(message, sender, receiver, current_round):
    """
    Delivers :param message: from :param sender: to :param receiver:.
    Also creates corresponding NetworkEvent in simulator EventQueue.
    :param message: The message to send.
    :type message: :class:`~comms.Message`
    :param sender: The sender of :param message:.
    :type sender: :class:`~particle.Particle`
    :param receiver: The receiving particle of :param message:.
    :type receiver: :class:`~particle.Particle`
    :param current_round: The current simulator round.
    :type current_round: int
    :return: The corresponding NetworkEvent depending on whether the message was delivered directly
             and/or for the first time.
    :rtype: :class:`~meta.NetworkEvent`
    """
    store = receiver.rcv_store

    message.update_delivery(current_round)
    message.inc_hops()

    if sender.get_id() == message.original_sender.get_id():
        if not store.contains_key(message.key):
            process_event(EventType.MessageDeliveredFirstDirect, sender, receiver, message)
        else:
            process_event(EventType.MessageDeliveredDirect, sender, receiver, message)
    else:
        if not store.contains_key(message.key):
            process_event(EventType.MessageDeliveredFirst, sender, receiver, message)
        else:
            process_event(EventType.MessageDelivered, sender, receiver, message)
    if not store.contains_key(message.key):
        store_message(store, message, sender, receiver)


def store_message(message, sender, receiver):
    """
    Puts the :param message: in the :param receiver:'s :param store: and handles OverflowError by creating
    a ReceiverOutOfMem NetworkEvent. The actual overflow is handled internally in the :param store:
    :param store: The store :param message: is to be put in.
    :type store: :class:`~messagestore.MessageStore`
    :param message: The message to store.
    :type message: :class:`~comms.Message`
    :param sender: The sender of the message.
    :type sender: :class:`~particle.Particle`
    :param receiver: The receiver of the message.
    :type receiver: :class:`~particle.Particle`
    """
    if message.get_actual_receiver().number == message.get_receiver().number:  # TODO: ???
        print("{} :: {}".format(message.actual_receiver.number, message.receiver.number))
        store = receiver.rcv_store
        process_event(EventType.MessageDelivered, message.sender, message.receiver, message)
        if message.original_sender == message.sender:
            process_event(EventType.MessageDeliveredDirect, message.sender, message.receiver, message)
    else:
        store = receiver.send_store
        if not(store.contains_key(message.key)):
            process_event(EventType.MessageForwarded, message.sender, message.receiver, message)  # TODO: remove receiver sender
    try:
        store.append(message)
    except OverflowError:
        process_event(EventType.ReceiverOutOfMem, sender, receiver, message)


def generate_random_messages(particle_list, amount, sim, ttl_range=None):
    """
    Creates :param amount: many messages for each particle in :param particle_list: with a TTL randomly picked from
    :param ttl_range.

    :param particle_list: The list of particles messages should be generated for.
    :type particle_list: list
    :param amount: The amount of messages to be created for each particle.
    :type amount: number
    :param sim: The simulator instance.
    :type sim: :class:`~sim.Sim`
    :param ttl_range: Min and max value for the TTL value to be randomly drawn from for each message.
    :type ttl_range: tuple
    :return: list of generated messages
    """
    messages = []
    if ttl_range is not None:
        if ttl_range is not tuple:
            ttl_range = (1, round(sim.get_max_round() / 10))
    else:
        ttl_range = (sim.message_ttl, sim.message_ttl)
    for sender in particle_list:
        for _ in range(0, amount):
            receiver = random.choice([particle for particle in particle_list if particle != sender])
            messages.append(Message(sender, receiver, start_round=sim.get_actual_round(),
                                    ttl=random.randint(ttl_range[0], ttl_range[1])))
    return messages
