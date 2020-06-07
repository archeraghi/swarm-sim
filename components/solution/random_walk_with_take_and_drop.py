import random


def solution(world):

    for p in world.particles:
        t = p.scan_for_matters_in(matter_type="tile")
        p.drop_tile_in(random.choice(world.grid.get_directions_list()))
        if len(t) > 0:
            p.take_tile_with(t[0].get_id())
        p.move_to(random.choice(world.grid.get_directions_list()))
