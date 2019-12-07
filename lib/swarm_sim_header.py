def get_coordinates_in_direction(coordinates, direction):
    """
    Returns the coordination data of the pointed directions

    :param coordinates: particles actual staying coordination
    :param direction: The direction. Options:  E, SE, SW, W, NW, or NE
    :return: The coordinaiton of the pointed directions
    """
    return coordinates[0] + direction[0], coordinates[1] + direction[1], coordinates[2] + direction[2]


def scan_in(matter_map: dict, center, hop, grid):
    result = []
    n_sphere_border = grid.get_n_sphere_border(center, hop)
    for l in n_sphere_border:
        if l in matter_map:
            result.append(matter_map[l])
    return result


def scan_within(matter_map, center, hop, grid):
    result = []
    n_sphere_border = grid.get_n_sphere(center, hop)
    for l in n_sphere_border:
        if l in matter_map:
            result.append(matter_map[l])
    return result

