"""

TODO:
1- Order the names based on particles, markers, and tiles and transparencybetic
2- A new column called round_success
3- On demand extenstion of the metrics.


"""


import csv
import pandas as pd
import logging
import os


class CsvParticleFile:
    def __init__(self, directory ):
        self.file_name = directory + '/particle.csv'
        file_exists = os.path.isfile(self.file_name)
        if not file_exists:
            self.csv_file = open(self.file_name, 'w', newline='')
            self.writer = csv.writer(self.csv_file)
            self.writer.writerow(['Particle ID', 'Particle Number',
                                  'marker Created', 'marker Deleted',
                                  'marker Read', 'marker Write',
                                  'Memory Read', 'Memory Write',
                                  'Particles Created', 'Particles Deleted',
                                  'Particles Dropped',
                                  'Particle Read', 'Particle Steps',
                                  'Particles Taken', 'Particle Write',
                                  'Tiles Created', 'Tiles Deleted',
                                  'Tiles Dropped',
                                  'Tile Read', 'Tiles Taken',
                                  'Tile Write', 'Success'
                                  ])
    def write_particle(self, particle):
        csv_iterator = [particle.csv_particle_writer.id, particle.csv_particle_writer.number,
                        particle.csv_particle_writer.marker_created, particle.csv_particle_writer.marker_deleted,
                        particle.csv_particle_writer.marker_read, particle.csv_particle_writer.marker_write,
                        particle.csv_particle_writer.memory_read, particle.csv_particle_writer.memory_write,
                        particle.csv_particle_writer.particle_created,particle.csv_particle_writer.particles_dropped,
                        particle.csv_particle_writer.particle_deleted, particle.csv_particle_writer.particle_read,
                        particle.csv_particle_writer.steps, particle.csv_particle_writer.particles_taken,
                        particle.csv_particle_writer.particle_write,
                        particle.csv_particle_writer.tile_created, particle.csv_particle_writer.tile_deleted,
                        particle.csv_particle_writer.tiles_dropped,
                        particle.csv_particle_writer.tile_read, particle.csv_particle_writer.tiles_taken,
                        particle.csv_particle_writer.tile_write, particle.csv_particle_writer.success]
        self.writer.writerow(csv_iterator)


class CsvParticleData:
    def __init__(self,  particle_id, particle_number):
        self.id = particle_id
        self.number=particle_number
        self.steps = 0
        self.particle_created=0
        self.particle_deleted=0
        self.particles_dropped = 0
        self.particle_read = 0
        self.particles_taken = 0
        self.particle_write = 0
        self.tile_created = 0
        self.tile_deleted = 0
        self.tile_read = 0
        self.tile_write = 0
        self.marker_read = 0
        self.marker_write = 0
        self.marker_created = 0
        self.marker_deleted = 0
        self.memory_read = 0
        self.memory_write = 0
        self.tiles_taken = 0
        self.tiles_dropped = 0
        self.success=0


    def write_particle(self, steps= 0, particle_read=0, particle_created=0, particle_deleted=0, particles_dropped=0,
                       particles_taken=0,
                       particle_write=0, tile_created=0, tile_deleted=0, tile_read=0, tile_write=0, marker_read=0,
                       marker_write=0, marker_created=0, marker_deleted=0, memory_read=0, memory_write=0,
                        tiles_taken = 0, tiles_dropped = 0, success=0):
        self.steps = self.steps + steps
        self.particle_created=self.particle_created+particle_created
        self.particle_deleted=self.particle_deleted+particle_deleted
        self.particles_dropped = self.particles_dropped + particles_dropped
        self.particles_taken = self.particles_taken + particles_taken
        self.particle_read=self.particle_read+particle_read
        self.particle_write=self.particle_write+particle_write
        self.tile_created=self.tile_created+tile_created
        self.tile_deleted=self.tile_deleted+tile_deleted
        self.tile_read=self.tile_read+tile_read
        self.tile_write=self.tile_write+tile_write
        self.marker_read=self.marker_read+marker_read
        self.marker_write=self.marker_write+marker_write
        self.marker_created=self.marker_created+marker_created
        self.marker_deleted=self.marker_deleted+marker_deleted
        self.memory_read=self.memory_read+memory_read
        self.memory_write=self.memory_write+memory_write
        self.tiles_taken = self.tiles_taken + tiles_taken
        self.tiles_dropped = self.tiles_dropped + tiles_dropped
        self.success = self.success+success






class CsvRoundData:
    def __init__(self, task=0, scenario=0, solution=0, seed=20, directory="outputs/"):

        self.task = task
        self.scenario = scenario
        self.solution = solution
        self.actual_round= 1
        self.seed = seed
        self.steps  = 0
        self.steps_sum = 0
        self.particle_created=0
        self.particle_deleted=0
        self.particle_num = 0
        self.particle_read = 0
        self.particle_write = 0
        self.tile_created = 0
        self.tile_deleted = 0
        self.tile_num = 0
        self.tile_read = 0
        self.tile_write = 0
        self.markers_num = 0
        self.marker_read = 0
        self.marker_write = 0
        self.marker_created = 0
        self.marker_deleted = 0
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
        self.marker_read_sum = 0
        self.marker_write_sum = 0
        self.marker_created_sum = 0
        self.marker_deleted_sum = 0
        self.memory_read_sum = 0
        self.memory_write_sum = 0
        self.success_round = 0
        self.success_counter = 0
        self.tiles_taken = 0
        self.tiles_dropped = 0
        self.tiles_taken_sum = 0
        self.tiles_dropped_sum = 0
        self.directory = directory
        self.file_name = directory + '/rounds.csv'
        self.csv_file = open(self.file_name, 'w', newline='')
        self.writer_round = csv.writer(self.csv_file)
        self.writer_round.writerow(['',
                                     'scenario', 'solution', 'Seed', 'Round Number',
                                    'Success Counter', 'Success Round',
                                    'Particle Counter',
                                    'Particles Created', 'Particles Created Sum',
                                    'Particles Deleted', 'Particles Deleted Sum',
                                    'Particles Dropped', 'Particles Dropped Sum',
                                    'Particle Read', 'Particle Read Sum',
                                    'Particle Steps', 'Particle Steps Sum',
                                    'Particles Taken', 'Particles Taken Sum',
                                    'Particle Write', 'Particle Write Sum',
                                    'Memory Read', 'Memory Read Sum',
                                    'Memory Write', 'Memory Write Sum',
                                    'marker Counter',
                                    'marker Created', 'marker Created Sum',
                                    'marker Deleted', 'marker Deleted Sum',
                                    'marker Read', 'marker Read Sum',
                                    'marker Write', 'marker Write Sum',
                                    'Tile Counter',
                                    'Tiles Created', 'Tiles Created Sum',
                                    'Tiles Deleted', 'Tiles Deleted Sum',
                                    'Tiles Dropped', 'Tiles Dropped Sum',
                                    'Tile Read', 'Tile Read Sum',
                                    'Tiles Taken', 'Tiles Taken Sum',
                                    'Tile Write', 'Tile Write Sum',
                                    ])

    def update_particle_num (self, particle):
        self.particle_num = particle

    def update_tiles_num (self, tile):
        self.tile_num = tile

    def update_markers_num(self, act_markers_num):
        self.markers_num = act_markers_num

    def success(self):
        self.success_counter=self.success_counter+1

    def update_metrics(self, steps = 0,
                        particle_read = 0, tile_read = 0, marker_read = 0, memory_read = 0,
                        particle_write = 0, tile_write = 0, marker_write = 0, memory_write = 0,
                        particle_created=0, tile_created=0, marker_created=0,
                        particle_deleted=0, tile_deleted=0, marker_deleted=0, tiles_taken=0, tiles_dropped=0,
                        particles_taken=0, particles_dropped=0):
        logging.debug("CSV: Starting writing_rounds")
        self.marker_created_sum = self.marker_created_sum + marker_created
        self.marker_deleted_sum = self.marker_deleted_sum + marker_deleted
        self.marker_read_sum = self.marker_read_sum + marker_read
        self.marker_write_sum = self.marker_write_sum + marker_write
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


        self.steps = self.steps + steps
        self.particle_read = self.particle_read + particle_read
        self.tile_read = self.tile_read + tile_read
        self.marker_read = self.marker_read + marker_read
        self.memory_read = self.memory_read + memory_read
        self.particle_write = self.particle_write + particle_write
        self.tile_write = self.tile_write + tile_write
        self.marker_write = self.marker_write + marker_write
        self.memory_write = self.memory_write + memory_write
        self.particle_created = self.particle_created + particle_created
        self.tile_created = self.tile_created + tile_created
        self.marker_created = self.marker_created + marker_created
        self.particle_deleted = self.particle_deleted + particle_deleted
        self.tile_deleted = self.tile_deleted + tile_deleted
        self.marker_deleted = self.marker_deleted + marker_deleted
        self.tiles_dropped = self.tiles_dropped + tiles_dropped
        self.tiles_taken = self.tiles_taken + tiles_taken
        self.particles_taken= self.particles_taken + particles_taken
        self.particles_dropped = self.particles_dropped + particles_dropped
        logging.debug("CSV: Ending writing_rounds")

    def next_line(self, sim_round):
        csv_iterator = ['', self.scenario, self.solution, self.seed, sim_round,
                        self.success_counter, self.success_round,
                        self.particle_num, self.particle_created, self.particle_created_sum,
                        self.particle_deleted, self.particle_deleted_sum,
                        self.particles_dropped, self.particles_dropped_sum,
                        self.particle_read, self.particle_read_sum,
                        self.steps, self.steps_sum,
                        self.particles_taken, self.particles_taken_sum,
                        self.particle_write, self.particle_write_sum,
                        self.memory_read, self.memory_read_sum, self.memory_write, self.memory_write_sum,
                        self.markers_num, self.marker_created, self.marker_created_sum,
                        self.marker_deleted, self.marker_deleted_sum,
                        self.marker_read, self.marker_read_sum,
                        self.marker_write, self.marker_write_sum,
                        self.tile_num, self.tile_created, self.tile_created_sum,
                        self.tile_deleted, self.tile_deleted_sum, self.tiles_dropped, self.tiles_dropped_sum,
                        self.tile_read, self.tile_read_sum, self.tiles_taken, self.tiles_taken_sum,
                        self.tile_write, self.tile_write_sum]
        self.writer_round.writerow(csv_iterator)
        self.actual_round = sim_round
        self.steps=0
        self.particle_read=0
        self.tile_read=0
        self.marker_read=0
        self.memory_read=0
        self.particle_write=0
        self.tile_write=0
        self.marker_write=0
        self.memory_write=0
        self.particle_created = 0
        self.tile_created = 0
        self.marker_created = 0
        self.particle_deleted = 0
        self.tile_deleted = 0
        self.marker_deleted = 0
        self.tiles_dropped = 0
        self.tiles_taken = 0
        self.success_round = 0
        self.success_counter = 0
        self.particles_taken = 0
        self.particles_dropped = 0

    def aggregate_metrics(self):
        self.csv_file.close()
        data = pd.read_csv(self.file_name)
        file_name = self.directory+"/aggregate_rounds.csv"
        csv_file = open(file_name, 'w', newline='')
        writer_round = csv.writer(csv_file)
        """Average Min Max for all other metrics"""
        writer_round.writerow(['Scenario','Solution', 'Seed', 'Rounds Total',
                                'Success Rate Sum', 'Success Ratio',
                                'Success Rate Avg', 'Success Rate Min', 'Success Rate Max',
                                'Success Round Min', 'Success Round Max',
                                'Particle Counter',
                                'Particles Created Sum', 'Particles Created Avg',
                                'Particles Created Min', 'Particles Created Max',
                                'Particles Deleted Sum', 'Particles Deleted Avg',
                                'Particles Deleted Min', 'Particles Deleted Max',
                                'Particles Dropped Sum', 'Particles Dropped Avg',
                                'Particles Dropped Min', 'Particles Dropped Max',
                                'Particle Read Sum', 'Particle Read Avg', 'Particle Read Min', 'Particle Read Max',
                                'Partilcle Steps Total',  'Particle Steps Avg',
                                'Particle Steps Min', 'Particle Steps Max',
                                'Particles Taken Sum', 'Particles Taken Avg',
                                'Particles Taken Min', 'Particles Taken Max',
                                'Particle Write Sum', 'Particle Write Avg', 'Particle Write Min', 'Particle Write Max',
                                'marker Counter',
                                'marker Created Sum', 'marker Created Avg',
                                'marker Created Min', 'marker Created Max',
                                'marker Deleted Sum', 'marker Deleted Avg',
                                'marker Deleted Min', 'marker Deleted Max',
                                'marker Read Sum', 'marker Read Avg', 'marker Read Min', 'marker Read Max',
                                'marker Write Sum', 'marker Write Avg', 'marker Write Min', 'marker Write Max',
                                'Memory Read Sum', 'Memory Read Avg', 'Memory Read Min', 'Memory Read Max',
                                'Memory Write Sum', 'Memory Write Avg', 'Memory Write Min', 'Memory Write Max',
                                'Tile Counter',
                                'Tiles Created Sum', 'Tiles Created Avg', 'Tiles Created Min', 'Tiles Created Max',
                                'Tiles Deleted Sum', 'Tiles Deleted Avg', 'Tiles Deleted Min', 'Tiles Deleted Max',
                                'Tiles Dropped Sum', 'Tiles Dropped Avg', 'Tiles Dropped Min', 'Tiles Dropped Max',
                                'Tile Read Sum', 'Tile Read Avg', 'Tile Read Min', 'Tile Read Max',
                                'Tiles Taken Sum', 'Tiles Taken Avg', 'Tiles Taken Min', 'Tiles Taken Max',
                                'Tile Write Sum', 'Tile Write Avg', 'Tile Write Min', 'Tile Write Max'])

        csv_interator = [self.scenario, self.solution, self.seed, data['Round Number'].count(),

                         data['Success Counter'].sum(),
                         data['Success Counter'].sum()/ data['Round Number'].sum(),

                         data['Success Counter'].mean(), data['Success Counter'].min(),
                         data['Success Counter'].max(),

                         data['Success Round'].min(),
                         data['Success Round'].max(),

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


                         self.markers_num,
                         data['marker Created'].sum(), data['marker Created'].mean(),
                         data['marker Created'].min(), data['marker Created'].max(),

                         data['marker Deleted'].sum(), data['marker Deleted'].mean(),
                         data['marker Deleted'].min(), data['marker Deleted'].max(),

                         data['marker Read'].sum(), data['marker Read'].mean(), data['marker Read'].min(),
                         data['marker Read'].max(),

                         data['marker Write'].sum(), data['marker Write'].mean(), data['marker Write'].min(),
                         data['marker Write'].max(),

                         data['Memory Read'].sum(), data['Memory Read'].mean(), data['Memory Read'].min(),
                         data['Memory Read'].max(),

                         data['Memory Write'].sum(), data['Memory Write'].mean(), data['Memory Write'].min(),
                         data['Memory Write'].max(),


                         self.tile_num,
                         data['Tiles Created'].sum(), data['Tiles Created'].mean(), data['Tiles Created'].min(),
                         data['Tiles Created'].max(),

                         data['Tiles Deleted'].sum(), data['Tiles Deleted'].mean(), data['Tiles Deleted'].min(),
                         data['Tiles Deleted'].max(),

                         data['Tiles Dropped'].sum(), data['Tiles Dropped'].mean(), data['Tiles Dropped'].min(),
                         data['Tiles Dropped'].max(),

                         data['Tile Read'].sum(), data['Tile Read'].mean(),  data['Tile Read'].min(),
                         data['Tile Read'].max(),

                         data['Tiles Taken'].sum(), data['Tiles Taken'].mean(), data['Tiles Taken'].min(),
                         data['Tiles Taken'].max(),

                         data['Tile Write'].sum(), data['Tile Write'].mean(), data['Tile Write'].min(),
                         data['Tile Write'].max()]



        writer_round.writerow(csv_interator)
        csv_file.close()


    def all_aggregate_metrics(self):
        self.csv_file.close()
        data = pd.read_csv(self.file_name)
        file_name = self.directory+"/aggregate_rounds.csv"
        csv_file = open(file_name, 'w', newline='')
        writer_round = csv.writer(csv_file)
        """Average Min Max for all other metrics"""
        writer_round.writerow(['Scenario','Solution', 'Seed', 'Rounds Total',
                                 'Particle Counter',
                                'Success Rate Sum', 'Success Ratio',
                                'Success Rate Avg', 'Success Rate Min', 'Success Rate Max',
                                'Success Round Min', 'Success Round Max',
                                'Particle Counter',
                                'Particles Created Sum', 'Particles Created Avg',
                                'Particles Created Min', 'Particles Created Max',
                                'Particles Deleted Sum', 'Particles Deleted Avg',
                                'Particles Deleted Min', 'Particles Deleted Max',
                                'Particles Dropped Sum', 'Particles Dropped Avg',
                                'Particles Dropped Min', 'Particles Dropped Max',
                                'Particle Read Sum', 'Particle Read Avg', 'Particle Read Min', 'Particle Read Max',
                                'Partilcle Steps Total',  'Particle Steps Avg',
                                'Particle Steps Min', 'Particle Steps Max',
                                'Particles Taken Sum', 'Particles Taken Avg',
                                'Particles Taken Min', 'Particles Taken Max',
                                'Particle Write Sum', 'Particle Write Avg', 'Particle Write Min', 'Particle Write Max',
                                'marker Counter',
                                'marker Created Sum', 'marker Created Avg',
                                'marker Created Min', 'marker Created Max',
                                'marker Deleted Sum', 'marker Deleted Avg',
                                'marker Deleted Min', 'marker Deleted Max',
                                'marker Read Sum', 'marker Read Avg', 'marker Read Min', 'marker Read Max',
                                'marker Write Sum', 'marker Write Avg', 'marker Write Min', 'marker Write Max',
                                'Memory Read Sum', 'Memory Read Avg', 'Memory Read Min', 'Memory Read Max',
                                'Memory Write Sum', 'Memory Write Avg', 'Memory Write Min', 'Memory Write Max',
                                'Tile Counter',
                                'Tiles Created Sum', 'Tiles Created Avg', 'Tiles Created Min', 'Tiles Created Max',
                                'Tiles Deleted Sum', 'Tiles Deleted Avg', 'Tiles Deleted Min', 'Tiles Deleted Max',
                                'Tiles Dropped Sum', 'Tiles Dropped Avg', 'Tiles Dropped Min', 'Tiles Dropped Max',
                                'Tile Read Sum', 'Tile Read Avg', 'Tile Read Min', 'Tile Read Max',
                                'Tiles Taken Sum', 'Tiles Taken Avg', 'Tiles Taken Min', 'Tiles Taken Max',
                                'Tile Write Sum', 'Tile Write Avg', 'Tile Write Min', 'Tile Write Max'])

        csv_interator = [self.scenario, self.solution, self.seed, data['Round Number'].count(),

                          self.particle_num,
                         data['Success Counter'].sum(),
                         data['Success Counter'].sum()/ data['Round Number'].sum(),

                         data['Success Counter'].mean(), data['Success Counter'].min(),
                         data['Success Counter'].max(),

                         data['Success Round'].min(),
                         data['Success Round'].max(),

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


                         self.markers_num,
                         data['marker Created'].sum(), data['marker Created'].mean(),
                         data['marker Created'].min(), data['marker Created'].max(),

                         data['marker Deleted'].sum(), data['marker Deleted'].mean(),
                         data['marker Deleted'].min(), data['marker Deleted'].max(),

                         data['marker Read'].sum(), data['marker Read'].mean(), data['marker Read'].min(),
                         data['marker Read'].max(),

                         data['marker Write'].sum(), data['marker Write'].mean(), data['marker Write'].min(),
                         data['marker Write'].max(),

                         data['Memory Read'].sum(), data['Memory Read'].mean(), data['Memory Read'].min(),
                         data['Memory Read'].max(),

                         data['Memory Write'].sum(), data['Memory Write'].mean(), data['Memory Write'].min(),
                         data['Memory Write'].max(),


                         self.tile_num,
                         data['Tiles Created'].sum(), data['Tiles Created'].mean(), data['Tiles Created'].min(),
                         data['Tiles Created'].max(),

                         data['Tiles Deleted'].sum(), data['Tiles Deleted'].mean(), data['Tiles Deleted'].min(),
                         data['Tiles Deleted'].max(),

                         data['Tiles Dropped'].sum(), data['Tiles Dropped'].mean(), data['Tiles Dropped'].min(),
                         data['Tiles Dropped'].max(),

                         data['Tile Read'].sum(), data['Tile Read'].mean(),  data['Tile Read'].min(),
                         data['Tile Read'].max(),

                         data['Tiles Taken'].sum(), data['Tiles Taken'].mean(), data['Tiles Taken'].min(),
                         data['Tiles Taken'].max(),

                         data['Tile Write'].sum(), data['Tile Write'].mean(), data['Tile Write'].min(),
                         data['Tile Write'].max()]



        writer_round.writerow(csv_interator)
        csv_file.close()