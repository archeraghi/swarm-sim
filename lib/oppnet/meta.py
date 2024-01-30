from enum import Enum

from lib.std_lib import green, blue, orange, yellow, red


class EventType(Enum):
    MessageSent = 0
    MessageDelivered = 1
    MessageDeliveredDirect = 2
    MessageForwarded = 3
    MessageDeliveredFirst = 4
    MessageDeliveredFirstDirect = 5
    MessageTTLExpired = 6
    #
    ReceiverOutOfMem = 10


def process_event(event_type, sender, receiver, message):
    """
    :param event_type: The type of event
    :type event_type: :class:`~meta.EventType`
    :param sender: The particle sending the Message.
    :type sender: :class:`~particle.Particle`
    :param receiver: The intended receiver of the message.
    :type receiver: :class:`~particle.Particle`
    :param message: The message to send.
    :type message: :class:`~comms.Message`
    """
    if event_type == EventType.MessageSent:
        sender.csv_particle_writer.write_particle(messages_sent=1)
        sender.sim.csv_round_writer.update_metrics(messages_sent=1)
        # add to message data
        sender.sim.csv_round_writer.csv_msg_writer.update_metrics(message, sent=1)
    elif event_type == EventType.MessageDeliveredFirst:
        # update round metrics
        sender.sim.csv_round_writer.update_metrics(messages_delivered_unique=1, messages_received=1)
        # update particle metrics for both sender and receiver
        sender.csv_particle_writer.write_particle(messages_delivered=1)
        receiver.csv_particle_writer.write_particle(messages_received=1)
        # update message data
        sender.sim.csv_round_writer.csv_msg_writer.update_metrics(message, delivered=1,
                                                                  delivery_round=sender.sim.get_actual_round())
        # color receiver
        receiver.set_color(green)
        sender.set_color(blue)
    elif event_type == EventType.MessageDeliveredFirstDirect:
        # update round metrics
        sender.sim.csv_round_writer.update_metrics(messages_delivered_directly_unique=1,
                                                   messages_received=1)
        # update particle metrics for both sender and receiver
        sender.csv_particle_writer.write_particle(messages_delivered=1)
        receiver.csv_particle_writer.write_particle(messages_received=1)
        # update message data
        sender.sim.csv_round_writer.csv_msg_writer.update_metrics(message, delivered_direct=1, delivered=1,
                                                                  delivery_round=sender.sim.get_actual_round())
        # color receiver
        receiver.set_color(green)
        sender.set_color(blue)
    elif event_type == EventType.MessageDeliveredDirect:
        # update round metrics
        sender.sim.csv_round_writer.update_metrics(messages_delivered_directly=1,
                                                   messages_received=1)
        # update particle metrics for both sender and receiver
        sender.csv_particle_writer.write_particle(messages_delivered_directly=1)
        receiver.csv_particle_writer.write_particle(messages_received=1)
        # update message data
        sender.sim.csv_round_writer.csv_msg_writer.update_metrics(message, delivered_direct=1,
                                                                  delivery_round=sender.sim.get_actual_round())
        # color receiver
        receiver.set_color(green)
        sender.set_color(blue)
    elif event_type == EventType.MessageDelivered:
        # update round metrics
        sender.sim.csv_round_writer.update_metrics(messages_delivered=1, messages_received=1)
        # update particle metrics for both sender and receiver
        sender.csv_particle_writer.write_particle(messages_delivered=1)
        receiver.csv_particle_writer.write_particle(messages_received=1)
        # update message data
        sender.sim.csv_round_writer.csv_msg_writer.update_metrics(message, delivered=1,
                                                                  delivery_round=sender.sim.get_actual_round())
        # color receiver
        receiver.set_color(green)
        sender.set_color(blue)
    elif event_type == EventType.MessageForwarded:
        # update round metrics
        sender.sim.csv_round_writer.update_metrics(messages_forwarded=1, messages_received=1)
        # update particle metrics for both sender and receiver
        sender.csv_particle_writer.write_particle(messages_forwarded=1)
        receiver.csv_particle_writer.write_particle(messages_received=1)
        # update message data
        sender.sim.csv_round_writer.csv_msg_writer.update_metrics(message, forwarded=1)
        # color receiver
        receiver.set_color(yellow)
    elif event_type == EventType.MessageTTLExpired:
        # update round metrics
        sender.sim.csv_round_writer.update_metrics(message_ttl_expired=1)
        # update particle metrics for the sender
        sender.csv_particle_writer.write_particle(messages_ttl_expired=1)
        # color receiver
        sender.set_color(orange)
    elif event_type == EventType.ReceiverOutOfMem:
        # update round metrics
        sender.sim.csv_round_writer.update_metrics(receiver_out_of_mem=1)
        # update particle metrics for the receiver
        receiver.csv_particle_writer.write_particle(out_of_mem=1)
        # color receiver
        receiver.set_color(red)
