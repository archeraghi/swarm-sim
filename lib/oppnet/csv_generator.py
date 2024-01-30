"""

TODO:
1- Order the names based on particles, locations, and tiles and alphabetic
2- A new column called round_success
3- On demand extenstion of the metrics.


"""

import csv
import logging
import os

import pandas as pd

from lib.oppnet.communication import Message


class CsvParticleFile:
    def __init__(self, directory):
        self.file_name = directory + '/particle.csv'
        file_exists = os.path.isfile(self.file_name)
        if not file_exists:
            self.csv_file = open(self.file_name, 'w', newline='')
            self.writer = csv.writer(self.csv_file)
            self.writer.writerow(['Particle ID', 'Particle Number',
                                  'Location Created', 'Location Deleted',
                                  'Location Read', 'Location Write',
                                  'Memory Read', 'Memory Write',
                                  'Particles Created', 'Particles Deleted',
                                  'Particles Dropped',
                                  'Particle Read', 'Particle Steps',
                                  'Particles Taken', 'Particle Write',
                                  'Tiles Created', 'Tiles Deleted',
                                  'Tiles Dropped',
                                  'Tile Read', 'Tiles Taken',
                                  'Tile Write', 'Success',
                                  'Messages Sent', 'Messages Forwarded', 'Messages Delivered',
                                  'Messages Delivered Directly', 'Messages Received',
                                  'Messages TTL Expired', 'Out of Memory'
                                  ])

    def write_particle(self, particle):
        csv_iterator = [particle.csv_particle_writer.id, particle.csv_particle_writer.number,
                        particle.csv_particle_writer.location_created, particle.csv_particle_writer.location_deleted,
                        particle.csv_particle_writer.location_read, particle.csv_particle_writer.location_write,
                        particle.csv_particle_writer.memory_read, particle.csv_particle_writer.memory_write,
                        particle.csv_particle_writer.particle_created, particle.csv_particle_writer.particles_dropped,
                        particle.csv_particle_writer.particle_deleted, particle.csv_particle_writer.particle_read,
                        particle.csv_particle_writer.steps, particle.csv_particle_writer.particles_taken,
                        particle.csv_particle_writer.particle_write,
                        particle.csv_particle_writer.tile_created, particle.csv_particle_writer.tile_deleted,
                        particle.csv_particle_writer.tiles_dropped,
                        particle.csv_particle_writer.tile_read, particle.csv_particle_writer.tiles_taken,
                        particle.csv_particle_writer.tile_write,
                        particle.csv_particle_writer.success,
                        particle.csv_particle_writer.messages_sent, particle.csv_particle_writer.messages_forwarded,
                        particle.csv_particle_writer.messages_delivered,
                        particle.csv_particle_writer.messages_delivered_directly,
                        particle.csv_particle_writer.messages_received,
                        particle.csv_particle_writer.messages_ttl_expired,
                        particle.csv_particle_writer.out_of_mem,
                        ]
        self.writer.writerow(csv_iterator)


class CsvParticleData:
    def __init__(self, particle_id, particle_number):
        self.id = particle_id
        self.number = particle_number
        self.steps = 0
        self.particle_created = 0
        self.particle_deleted = 0
        self.particles_dropped = 0
        self.particle_read = 0
        self.particles_taken = 0
        self.particle_write = 0
        self.tile_created = 0
        self.tile_deleted = 0
        self.tile_read = 0
        self.tile_write = 0
        self.location_read = 0
        self.location_write = 0
        self.location_created = 0
        self.location_deleted = 0
        self.memory_read = 0
        self.memory_write = 0
        self.tiles_taken = 0
        self.tiles_dropped = 0
        self.success = 0
        self.messages_sent = 0
        self.messages_forwarded = 0
        self.messages_delivered = 0
        self.messages_delivered_directly = 0
        self.messages_received = 0
        self.messages_ttl_expired = 0
        self.out_of_mem = 0

    def write_particle(self, steps=0, particle_read=0, particle_created=0, particle_deleted=0, particles_dropped=0,
                       particles_taken=0,
                       particle_write=0, tile_created=0, tile_deleted=0, tile_read=0, tile_write=0, location_read=0,
                       location_write=0, location_created=0, location_deleted=0, memory_read=0, memory_write=0,
                       tiles_taken=0, tiles_dropped=0, success=0, messages_sent=0, messages_forwarded=0,
                       messages_delivered=0, messages_delivered_directly=0, messages_received=0,
                       messages_ttl_expired=0, out_of_mem=0):
        self.steps = self.steps + steps
        self.particle_created = self.particle_created + particle_created
        self.particle_deleted = self.particle_deleted + particle_deleted
        self.particles_dropped = self.particles_dropped + particles_dropped
        self.particles_taken = self.particles_taken + particles_taken
        self.particle_read = self.particle_read + particle_read
        self.particle_write = self.particle_write + particle_write
        self.tile_created = self.tile_created + tile_created
        self.tile_deleted = self.tile_deleted + tile_deleted
        self.tile_read = self.tile_read + tile_read
        self.tile_write = self.tile_write + tile_write
        self.location_read = self.location_read + location_read
        self.location_write = self.location_write + location_write
        self.location_created = self.location_created + location_created
        self.location_deleted = self.location_deleted + location_deleted
        self.memory_read = self.memory_read + memory_read
        self.memory_write = self.memory_write + memory_write
        self.tiles_taken = self.tiles_taken + tiles_taken
        self.tiles_dropped = self.tiles_dropped + tiles_dropped
        self.success = self.success + success
        self.messages_sent += messages_sent
        self.messages_forwarded += messages_forwarded
        self.messages_delivered += messages_delivered
        self.messages_delivered_directly += messages_delivered_directly
        self.messages_received += messages_received
        self.messages_ttl_expired += messages_ttl_expired
        self.out_of_mem += out_of_mem


class CsvRoundData:
    def __init__(self, sim, task=0, solution=0, seed=20, particle_num=0, tiles_num=0, locations_num=0,
                 steps=0, directory='outputs/'):
        self.sim = sim

        self.csv_msg_writer = CsvMessageData(directory)
        self.task = task
        self.solution = solution
        self.actual_round = sim.get_actual_round()
        self.seed = seed
        self.steps = steps
        self.steps_sum = steps
        self.particle_created = 0
        self.particle_deleted = 0
        self.particle_num = particle_num
        self.particle_read = 0
        self.particle_write = 0
        self.tile_created = 0
        self.tile_deleted = 0
        self.tile_num = tiles_num
        self.tile_read = 0
        self.tile_write = 0
        self.locations_num = locations_num
        self.location_read = 0
        self.location_write = 0
        self.location_created = 0
        self.location_deleted = 0
        self.memory_read = 0
        self.memory_write = 0
        self.particle_created_sum = 0
        self.particle_deleted_sum = 0
        self.particle_read_sum = 0
        self.particle_write_sum = 0
        self.particles_taken = 0
        self.particles_dropped = 0
        self.particles_taken_sum = 0
        self.particles_dropped_sum = 0
        self.tile_created_sum = 0
        self.tile_deleted_sum = 0
        self.tile_read_sum = 0
        self.tile_write_sum = 0
        self.location_read_sum = 0
        self.location_write_sum = 0
        self.location_created_sum = 0
        self.location_deleted_sum = 0
        self.memory_read_sum = 0
        self.memory_write_sum = 0
        self.success_round = None
        self.success_counter = 0
        self.tiles_taken = 0
        self.tiles_dropped = 0
        self.tiles_taken_sum = 0
        self.tiles_dropped_sum = 0
        self.messages_sent = 0
        self.messages_forwarded = 0
        self.messages_delivered = 0
        self.messages_delivered_directly = 0
        self.messages_received = 0
        self.message_ttl_expired = 0
        self.messages_delivered_unique = 0
        self.messages_delivered_directly_unique = 0
        self.receiver_out_of_mem = 0

        self.directory = directory
        self.file_name = '%s%s' % (self.directory, '/rounds.csv')
        self.csv_file = open(self.file_name, 'w', newline='')
        self.writer_round = csv.writer(self.csv_file)
        self.writer_round.writerow(['',
                                    'Round Number', 'Seed', 'solution',
                                    'Location Counter',
                                    'Location Created', 'Location Created Sum',
                                    'Location Deleted', 'Location Deleted Sum',
                                    'Location Read', 'Location Read Sum',
                                    'Location Write', 'Location Write Sum',
                                    'Memory Read', 'Memory Read Sum',
                                    'Memory Write', 'Memory Write Sum',
                                    'Particle Counter',
                                    'Particles Created', 'Particles Created Sum',
                                    'Particles Deleted', 'Particles Deleted Sum',
                                    'Particles Dropped', 'Particles Dropped Sum',
                                    'Particle Read', 'Particle Read Sum',
                                    'Particle Steps', 'Particle Steps Sum',
                                    'Particles Taken', 'Particles Taken Sum',
                                    'Particle Write', 'Particle Write Sum',
                                    'Success Counter', 'Success Round',
                                    'Tile Counter',
                                    'Tiles Created', 'Tiles Created Sum',
                                    'Tiles Deleted', 'Tiles Deleted Sum',
                                    'Tiles Dropped', 'Tiles Dropped Sum',
                                    'Tile Read', 'Tile Read Sum',
                                    'Tiles Taken', 'Tiles Taken Sum',
                                    'Tile Write', 'Tile Write Sum',
                                    'Messages Sent', 'Messages Forwarded',
                                    'Messages Delivered', 'Messages Delivered Directly',
                                    'Messages Received', 'Messages TTL Expired',
                                    'Messages Delivered Unique', 'Messages Delivered Directly Unique',
                                    'Receiver Out Of Mem'
                                    ])

    def update_particle_num(self, particle):
        self.particle_num = particle

    def update_tiles_num(self, tile):
        self.tile_num = tile

    def update_locations_num(self, act_locations_num):
        self.locations_num = act_locations_num

    def success(self):
        self.success_counter = self.success_counter + 1

    def update_metrics(self, steps=0,
                       particle_read=0, tile_read=0, location_read=0, memory_read=0,
                       particle_write=0, tile_write=0, location_write=0, memory_write=0,
                       particle_created=0, tile_created=0, location_created=0,
                       particle_deleted=0, tile_deleted=0, location_deleted=0, tiles_taken=0, tiles_dropped=0,
                       particles_taken=0, particles_dropped=0, messages_sent=0, messages_forwarded=0,
                       messages_delivered=0, messages_delivered_directly=0, messages_received=0,
                       messages_delivered_unique=0, messages_delivered_directly_unique=0,
                       message_ttl_expired=0, receiver_out_of_mem=0):
        logging.debug("CSV: Starting writing_rounds")
        self.location_created_sum = self.location_created_sum + location_created
        self.location_deleted_sum = self.location_deleted_sum + location_deleted
        self.location_read_sum = self.location_read_sum + location_read
        self.location_write_sum = self.location_write_sum + location_write
        self.particle_created_sum = self.particle_created_sum + particle_created
        self.particle_deleted_sum = self.particle_deleted_sum + particle_deleted
        self.particle_read_sum = self.particle_read_sum + particle_read
        self.steps_sum = self.steps_sum + steps
        self.particle_write_sum = self.particle_write_sum + particle_write
        self.memory_write_sum = self.memory_write_sum + memory_write
        self.memory_read_sum = self.memory_read_sum + memory_read
        self.tile_created_sum = self.tile_created_sum + tile_created
        self.tile_deleted_sum = self.tile_deleted_sum + tile_deleted
        self.tiles_dropped_sum = self.tiles_dropped_sum + tiles_dropped
        self.tile_read_sum = self.tile_read_sum + tile_read
        self.tiles_taken_sum = self.tiles_taken_sum + tiles_taken
        self.tile_write_sum = self.tile_write_sum + tile_write
        self.particles_taken_sum = self.particles_taken_sum + particles_taken
        self.particles_dropped_sum = self.particles_dropped_sum + particles_dropped
        self.messages_sent += messages_sent
        self.messages_forwarded += messages_forwarded
        self.messages_delivered += messages_delivered
        self.messages_delivered_directly += messages_delivered_directly
        self.messages_received += messages_received
        self.message_ttl_expired += message_ttl_expired
        self.messages_delivered_unique += messages_delivered_unique
        self.messages_delivered_directly_unique += messages_delivered_directly_unique
        self.receiver_out_of_mem += receiver_out_of_mem

        if self.actual_round == self.sim.get_actual_round():
            self.steps = self.steps + steps
            self.particle_read = self.particle_read + particle_read
            self.tile_read = self.tile_read + tile_read
            self.location_read = self.location_read + location_read
            self.memory_read = self.memory_read + memory_read
            self.particle_write = self.particle_write + particle_write
            self.tile_write = self.tile_write + tile_write
            self.location_write = self.location_write + location_write
            self.memory_write = self.memory_write + memory_write
            self.particle_created = self.particle_created + particle_created
            self.tile_created = self.tile_created + tile_created
            self.location_created = self.location_created + location_created
            self.particle_deleted = self.particle_deleted + particle_deleted
            self.tile_deleted = self.tile_deleted + tile_deleted
            self.location_deleted = self.location_deleted + location_deleted
            self.tiles_dropped = self.tiles_dropped + tiles_dropped
            self.tiles_taken = self.tiles_taken + tiles_taken
            self.particles_taken = self.particles_taken + particles_taken
            self.particles_dropped = self.particles_dropped + particles_dropped
        elif self.actual_round != self.sim.get_actual_round():
            self.actual_round = self.sim.get_actual_round()
            self.steps = steps
            self.particle_read = particle_read
            self.tile_read = tile_read
            self.location_read = location_read
            self.memory_read = memory_read
            self.particle_write = particle_write
            self.tile_write = tile_write
            self.location_write = location_write
            self.memory_write = memory_write
            self.particle_created = particle_created
            self.tile_created = tile_created
            self.location_created = location_created
            self.particle_deleted = particle_deleted
            self.tile_deleted = tile_deleted
            self.location_deleted = location_deleted
            self.tiles_dropped = tiles_dropped
            self.tiles_taken = tiles_taken
            self.particles_taken = particles_taken
            self.particles_dropped = particles_dropped
        logging.debug("CSV: Ending writing_rounds")

    def next_line(self, round):
        csv_iterator = ['', round, self.seed, self.solution,
                        self.locations_num, self.location_created, self.location_created_sum,
                        self.location_deleted, self.location_deleted_sum,
                        self.location_read, self.location_read_sum,
                        self.location_write, self.location_write_sum,
                        self.memory_read, self.memory_read_sum, self.memory_write, self.memory_write_sum,
                        self.particle_num, self.particle_created, self.particle_created_sum,
                        self.particle_deleted, self.particle_deleted_sum,
                        self.particles_dropped, self.particles_dropped_sum,
                        self.particle_read, self.particle_read_sum,
                        self.steps, self.steps_sum,
                        self.particles_taken, self.particles_taken_sum,
                        self.particle_write, self.particle_write_sum,
                        self.success_counter, self.success_round,
                        self.tile_num, self.tile_created, self.tile_created_sum,
                        self.tile_deleted, self.tile_deleted_sum, self.tiles_dropped, self.tiles_dropped_sum,
                        self.tile_read, self.tile_read_sum, self.tiles_taken, self.tiles_taken_sum,
                        self.tile_write, self.tile_write_sum,
                        self.messages_sent, self.messages_forwarded, self.messages_delivered,
                        self.messages_delivered_directly, self.messages_received,
                        self.message_ttl_expired, self.messages_delivered_unique,
                        self.messages_delivered_directly_unique, self.receiver_out_of_mem]
        self.writer_round.writerow(csv_iterator)
        self.actual_round = round
        self.steps = 0
        self.particle_read = 0
        self.tile_read = 0
        self.location_read = 0
        self.memory_read = 0
        self.particle_write = 0
        self.tile_write = 0
        self.location_write = 0
        self.memory_write = 0
        self.particle_created = 0
        self.tile_created = 0
        self.location_created = 0
        self.particle_deleted = 0
        self.tile_deleted = 0
        self.location_deleted = 0
        self.tiles_dropped = 0
        self.tiles_taken = 0
        self.success_round = None
        self.success_counter = 0
        self.particles_taken = 0
        self.particles_dropped = 0
        self.messages_sent = 0
        self.messages_forwarded = 0
        self.messages_delivered = 0
        self.messages_delivered_directly = 0
        self.messages_received = 0
        self.message_ttl_expired = 0
        self.messages_delivered_unique = 0
        self.messages_delivered_directly_unique = 0
        self.receiver_out_of_mem = 0

    def aggregate_metrics(self):
        self.csv_file.close()
        data = pd.read_csv(self.file_name)
        file_name = self.directory + "/aggregate_rounds.csv"
        csv_file = open(file_name, 'w', newline='')
        writer_round = csv.writer(csv_file)
        """Average Min Max for all other metrics"""
        writer_round.writerow(['Seed', 'Rounds Total',
                               'Solution', 'Particle Counter', 'Foods Sources Counter', 'Pheromones Counter',
                               'Success Rate Sum', 'Success Ratio',
                               'Location Counter',
                               'Location Created Sum', 'Location Created Avg',
                               'Location Created Min', 'Location Created Max',
                               'Location Deleted Sum', 'Location Deleted Avg',
                               'Location Deleted Min', 'Location Deleted Max',
                               'Location Read Sum', 'Location Read Avg', 'Location Read Min', 'Location Read Max',
                               'Location Write Sum', 'Location Write Avg', 'Location Write Min', 'Location Write Max',
                               'Particle Counter',
                               'Particles Created Sum', 'Particles Created Avg',
                               'Particles Created Min', 'Particles Created Max',
                               'Particles Deleted Sum', 'Particles Deleted Avg',
                               'Particles Deleted Min', 'Particles Deleted Max',
                               'Particles Dropped Sum', 'Particles Dropped Avg',
                               'Particles Dropped Min', 'Particles Dropped Max',
                               'Particle Read Sum', 'Particle Read Avg', 'Particle Read Min', 'Particle Read Max',
                               'Partilcle Steps Total', 'Particle Steps Avg',
                               'Particle Steps Min', 'Particle Steps Max',
                               'Particles Taken Sum', 'Particles Taken Avg',
                               'Particles Taken Min', 'Particles Taken Max',
                               'Particle Write Sum', 'Particle Write Avg', 'Particle Write Min', 'Particle Write Max',
                               'Memory Read Sum', 'Memory Read Avg', 'Memory Read Min', 'Memory Read Max',
                               'Memory Write Sum', 'Memory Write Avg', 'Memory Write Min', 'Memory Write Max',
                               'Success Rate Sum', 'Success Rate Avg', 'Success Rate Min', 'Success Rate Max',
                               'Success Round Min', 'Success Round Max',
                               'Tile Counter',
                               'Tiles Created Sum', 'Tiles Created Avg', 'Tiles Created Min', 'Tiles Created Max',
                               'Tiles Deleted Sum', 'Tiles Deleted Avg', 'Tiles Deleted Min', 'Tiles Deleted Max',
                               'Tiles Dropped Sum', 'Tiles Dropped Avg', 'Tiles Dropped Min', 'Tiles Dropped Max',
                               'Tile Read Sum', 'Tile Read Avg', 'Tile Read Min', 'Tile Read Max',
                               'Tiles Taken Sum', 'Tiles Taken Avg', 'Tiles Taken Min', 'Tiles Taken Max',
                               'Tile Write Sum', 'Tile Write Avg', 'Tile Write Min', 'Tile Write Max',
                               'Messages Sent Sum', 'Messages Forwarded Sum',
                               'Messages Delivered Sum', 'Messages Delivered Directly Sum',
                               'Messages Received Sum', 'Messages TTL Expired',
                               'Messages Delivered Unique Sum', 'Messages Delivered Directly Unique Sum',
                               'Receiver Out Of Mem Sum'
                               ])

        csv_interator = [self.seed, data['Round Number'].count(),

                         self.solution, self.particle_num, self.tile_num, self.locations_num,
                         data['Success Counter'].sum(),
                         data['Success Counter'].sum() / data['Round Number'].sum(),

                         self.locations_num,
                         data['Location Created'].sum(), data['Location Created'].mean(),
                         data['Location Created'].min(), data['Location Created'].max(),

                         data['Location Deleted'].sum(), data['Location Deleted'].mean(),
                         data['Location Deleted'].min(), data['Location Deleted'].max(),

                         data['Location Read'].sum(), data['Location Read'].mean(), data['Location Read'].min(),
                         data['Location Read'].max(),

                         data['Location Write'].sum(), data['Location Write'].mean(), data['Location Write'].min(),
                         data['Location Write'].max(),

                         self.particle_num,
                         data['Particles Created'].sum(), data['Particles Created'].mean(),
                         data['Particles Created'].min(), data['Particles Created'].max(),

                         data['Particles Deleted'].sum(), data['Particles Deleted'].mean(),
                         data['Particles Deleted'].min(), data['Particles Deleted'].max(),

                         data['Particles Dropped'].sum(), data['Particles Dropped'].mean(),
                         data['Particles Dropped'].min(), data['Particles Dropped'].max(),

                         data['Particle Read'].sum(), data['Particle Read'].mean(), data['Particle Read'].min(),
                         data['Particle Read'].max(),

                         data['Particle Steps'].sum(), data['Particle Steps'].mean(),
                         data['Particle Steps'].min(), data['Particle Steps'].max(),

                         data['Particles Taken'].sum(), data['Particles Taken'].mean(), data['Particles Taken'].min(),
                         data['Particles Taken'].max(),

                         data['Particle Write'].sum(), data['Particle Write'].mean(), data['Particle Write'].min(),
                         data['Particle Write'].max(),

                         data['Memory Read'].sum(), data['Memory Read'].mean(), data['Memory Read'].min(),
                         data['Memory Read'].max(),

                         data['Memory Write'].sum(), data['Memory Write'].mean(), data['Memory Write'].min(),
                         data['Memory Write'].max(),

                         data['Success Counter'].sum(), data['Success Counter'].mean(), data['Success Counter'].min(),
                         data['Success Counter'].max(),

                         data['Success Round'].min(),
                         data['Success Round'].max(),

                         self.tile_num,
                         data['Tiles Created'].sum(), data['Tiles Created'].mean(), data['Tiles Created'].min(),
                         data['Tiles Created'].max(),

                         data['Tiles Deleted'].sum(), data['Tiles Deleted'].mean(), data['Tiles Deleted'].min(),
                         data['Tiles Deleted'].max(),

                         data['Tiles Dropped'].sum(), data['Tiles Dropped'].mean(), data['Tiles Dropped'].min(),
                         data['Tiles Dropped'].max(),

                         data['Tile Read'].sum(), data['Tile Read'].mean(), data['Tile Read'].min(),
                         data['Tile Read'].max(),

                         data['Tiles Taken'].sum(), data['Tiles Taken'].mean(), data['Tiles Taken'].min(),
                         data['Tiles Taken'].max(),

                         data['Tile Write'].sum(), data['Tile Write'].mean(), data['Tile Write'].min(),
                         data['Tile Write'].max(),

                         data['Messages Sent'].sum(), data['Messages Forwarded'].sum(),
                         data['Messages Delivered'].sum(), data['Messages Delivered Directly'].sum(),
                         data['Messages Received'].sum(),


                         data['Messages TTL Expired'].sum(),

                         data['Messages Delivered Unique'].sum(), data['Messages Delivered Directly Unique'].sum(),


                         data['Receiver Out Of Mem'].sum()
                         ]

        writer_round.writerow(csv_interator)
        csv_file.close()


class CsvMessageData:
    """
    Collects sending, forwarding and delivery information for a dictionary of message objects in a csv.
    Contains :class:`~csv_generatore.MessageData` objects.
    """

    def __init__(self, directory="outputs/"):
        """
        :param directory: The directory for the csv to be put in.
        :type directory: str
        """
        self.messages = {}
        self.directory = directory
        self.file_name = directory + '/messages.csv'
        self.csv_file = open(self.file_name, 'w', newline='')
        self.writer = csv.writer(self.csv_file)

        self.writer.writerow(['Key', 'Number',
                              'Original Sender Number', 'Receiver Number',
                              'Sent Count',
                              'Forwarding Count', 'Delivery Count',
                              'Direct Delivery Count',
                              'Initial Sent Round', 'First Delivery Round',
                              'First Delivery Hops', 'Minimum Hops'
                              ])

    def __del__(self):
        # write message data rows
        self.write_rows()

    def write_rows(self):
        """
        Writes rows for all messages.
        """
        for key, m_data in self.messages.items():
            self.writer.writerow([key, m_data.seq_number,
                                  m_data.sender, m_data.receiver,
                                  m_data.sent, m_data.forwarded,
                                  m_data.delivered, m_data.delivered_direct,
                                  m_data.sent_round, m_data.delivery_round,
                                  m_data.first_hops, m_data.min_hops
                                  ])
        self.csv_file.close()

    def add_messages(self, messages):
        """
        Adds messages to the messages dictionary.
        :param messages: iterable type of messages
        :type messages: Iterable
        """
        if hasattr(messages, '__iter__'):
            for m in messages:
                self.add_message(m)

    def add_message(self, message: Message):
        """
        Adds a new message to track.
        :param message: The message to track.
        :type message: :class:`~comms.Message`
        """
        if message.key not in self.messages.keys():
            self.messages[message.key] = MessageData(message)

    def update_metrics(self, message: Message, sent=0, forwarded=0,
                       delivered=0, delivered_direct=0, delivery_round=None,
                       ):
        """
        Updates the corresponding parameter values for a :param message: in the messages dictionary.
        :param message: The tracked message which statistics are updated.
        :type message: :class:`~message.Message`
        :param sent: The amount it was sent.
        :type sent: int
        :param forwarded: The amount it was forwarded.
        :type forwarded: int
        :param delivered: The amount it was delivered.
        :type delivered: int
        :param delivered_direct: The amount it was delivered directly from sender to receiver.
        :type delivered_direct: int
        :param delivery_round: The round the message was delivered in.
        :type delivery_round: int
        """
        self.add_message(message)
        m_data = self.messages[message.key]
        if not delivery_round:
            hops = None
        else:
            hops = message.hops
        m_data.update_metric(sent, forwarded, delivered, delivered_direct, delivery_round, hops)
        self.messages[message.key] = m_data


class MessageData:
    """
    The tracking data for a message.
    """
    def __init__(self, message: Message):
        """
        :param message:
        :type message: :class:`~comms.Message`
        """
        self.key = message.key
        self.seq_number = message.seq_number
        self.sender = message.original_sender.number
        self.receiver = message.actual_receiver.number
        self.sent = 0
        self.sent_round = message.start_round
        self.forwarded = 0
        self.delivered = 0
        self.delivered_direct = 0
        self.delivery_round = None
        self.first_hops = None
        self.min_hops = None

    def update_metric(self, sent=0, forwarded=0, delivered=0, delivered_direct=0, delivery_round=None, hops=None):
        """
        Updates the statistics.
        :param sent: The amount it was sent.
        :type sent: int
        :param forwarded: The amount it was forwarded.
        :type forwarded: int
        :param delivered: The amount it was delivered.
        :type delivered: int
        :param delivered_direct: The amount it was delivered directly from sender to receiver.
        :type delivered_direct: int
        :param delivery_round: The round the message was delivered in.
        :type delivery_round: int
        :param hops: The hops of the message object.
        :type hops: int
        """
        self.sent += sent
        self.forwarded += forwarded
        self.delivered += delivered
        self.delivered_direct += delivered_direct
        if delivery_round and not self.delivery_round:
            self.delivery_round = delivery_round
        if hops:
            if not self.first_hops:
                self.first_hops = hops
                self.min_hops = hops
            elif hops < self.min_hops:
                self.min_hops = hops
