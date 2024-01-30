def solution(world):
    particle_distance_list = []
    locations_distance_list = []
    for particle in world.particles:
        for direction in world.grid.get_directions_list():
            if not particle.matter_in(direction):
                particle.create_location_in(direction)
        particle_distance_list.append( get_closest_tile_distance(particle.coordinates, world))
    for location in world.locations:
        locations_distance_list.append( get_closest_tile_distance(location.coordinates, world))
    if particle_distance_list and locations_distance_list:
        if max(particle_distance_list) <= min(locations_distance_list):
            print ("Valid state")



def get_closest_tile_distance(source, world):
    min = None
    for tile in world.get_tiles_list():
        value = world.grid.get_distance(source, tile.coordinates)
        if min is None or (value < min):
            min = value
    return min


