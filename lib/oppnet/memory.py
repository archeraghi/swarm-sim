import math
from enum import Enum
from lib.oppnet.communication import store_message
from lib.oppnet.meta import process_event, EventType


class MemoryMode(Enum):
    Schedule = 0
    Delta = 1


class Memory:
    def __init__(self, mode):
        self.memory = {}
        self.delta = {}
        self.mode = mode

    def add_scheduled_message_on(self, target_id, round_number, msg):
        if self.mode == MemoryMode.Schedule:
            if round_number in self.memory.keys():
                self.memory[round_number] = self.memory.get(target_id).append((target_id, msg))
            else:
                self.memory[round_number] = [(target_id, msg)]
        else:
            #TODO: throw error
            print("wrong mode")


    def try_deliver_scheduled_messages(self, sim):
        if sim.get_actual_round() in self.memory.keys():
            m_particles = sim.get_particle_map_id()
            tuples_particles = self.memory.pop(sim.get_actual_round())
            for e in tuples_particles:
                p_id = e[0]
                p_msg = e[1]
                if p_id in m_particles.keys():
                    p = m_particles.get(p_id)
                    p.write_memory(p_msg)

    def add_delta_message_on(self, target_id, msg, position, start_round, delta, expirerate):
        if self.mode == MemoryMode.Delta:
            process_event(EventType.MessageSent, msg.sender, msg.receiver, msg)  # TODO rethink section
            if target_id in self.memory.keys():
                self.memory.get(target_id).append((msg, position, start_round, delta, expirerate))
            else:
                self.memory[target_id] = [(msg, position, start_round, delta, expirerate)]

        else:
            #TODO: throw error
            print("wrong mode")

    def try_deliver_delta_messages(self, sim):
        actual_round = sim.get_actual_round()
        print(actual_round)
        new_memory = {}
        for target in self.memory.keys():
            new_msgs = []
            for m in self.memory[target]:
                msg = m[0]
                position = m[1]
                start_round = m[2]
                delta = m[3]
                expirerate = m[4]
                past_rounds = actual_round - start_round
                distance = delta * past_rounds
                x = abs(position.getx()-sim.get_particle_map_id()[target].coords[0])
                y = abs(position.gety()-sim.get_particle_map_id()[target].coords[1])
                distance_start_target = math.sqrt(x**2 + y**2)
                if distance < expirerate:
                    if distance >= distance_start_target:
                        store_message(msg, msg.get_sender(), msg.get_receiver())
                    else:
                        new_msgs.append(m)
            if len(new_msgs) > 0:
                new_memory[target] = new_msgs
        self.memory = new_memory

    def try_deliver_messages(self, sim):
            self.option[self.mode](self, sim)

    option = {MemoryMode.Schedule: try_deliver_scheduled_messages,
              MemoryMode.Delta: try_deliver_delta_messages}
