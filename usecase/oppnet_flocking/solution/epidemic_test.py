import lib.oppnet.routing
from lib.oppnet.communication import generate_random_messages


def solution(world):
    particles = world.get_particle_list()

    if world.get_actual_round() == 1:
        # initially generate 5 message per particle
        generate_random_messages(particles, amount=2, world=world)
    else:
        # generate 2 messages per particle, every 20 rounds
        if world.get_actual_round() % 20 == 0:
            generate_random_messages(particles, amount=2, world=world)
        # move in every round starting from the second one
        for particle in particles:
            next_direction = particle.mobility_model.next_direction(current_x_y_z=particle.coordinates)
            if next_direction:
                particle.move_to(next_direction)

        lib.oppnet.routing.next_step(particles)
