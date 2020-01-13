import random


def solution(world):

    if world.get_actual_round() % 1 == 0:
        for particle in world.get_particle_list():
            print(world.get_actual_round()," Particle No.", particle.number)
            particle.move_to(random.choice(world.grid.get_directions_list()))
