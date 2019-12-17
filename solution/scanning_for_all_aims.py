"""
This solution just scans for particles that are within 5 hops range and prints them out.
"""


def solution(world):
    center = world.grid.get_center()
    if world.get_actual_round() == 1:
        all_matters_list = world.get_particle_map_coordinates()[center].scan_for_matters_within(hop=5)
        for matter in all_matters_list:
            if matter.type == 'particle':
                print("particle at", matter.coordinates)
            elif matter.type == 'tile':
                print("tile", matter.coordinates)
            elif matter.type == 'location':
                print("location", matter.coordinates)
    if world.get_actual_round() == 2:
        all_matters_list = world.get_particle_map_coordinates()[center].scan_for_particles_within(hop=5)
        for matter in all_matters_list:
            print("particle at", matter.coordinates)
        all_matters_list = world.get_particle_map_coordinates()[center].scan_for_tiles_within(hop=5)
        for matter in all_matters_list:
            print("tile", matter.coordinates)
        all_matters_list = world.get_particle_map_coordinates()[center].scan_for_locations_within(hop=5)
        for matter in all_matters_list:
            print("location", matter.coordinates)
