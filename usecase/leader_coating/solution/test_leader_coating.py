import leader_coating as coating
from _pytest.debugging import pytestPDB

ENTRANCE = 100
PREVIOUS = 11
BESIDE_SUBJECT = 103
FREE_LOCATION = 1000
SUBJECT = 200
from hypothesis import given
from hypothesis.strategies import dictionaries, tuples, booleans, floats, lists




S6=6*SUBJECT



S5_P= 5*SUBJECT + PREVIOUS #DEAD_END


S4_BS_P= 4*SUBJECT + BESIDE_SUBJECT + PREVIOUS #Corner

FL_S3_BS_P= FREE_LOCATION + 3*SUBJECT + BESIDE_SUBJECT + PREVIOUS

FL2_S2_BS_P = 2*FREE_LOCATION + 2*SUBJECT + BESIDE_SUBJECT + PREVIOUS # OUTSIDE
FL3_S_BS_P= 3*FREE_LOCATION + SUBJECT + BESIDE_SUBJECT + PREVIOUS # OUTSIDE
FL5_P = 5*FREE_LOCATION + PREVIOUS #OUTSIDE


S3_BS_P_E= 3*SUBJECT + BESIDE_SUBJECT + ENTRANCE + PREVIOUS # SPECIAL CASE ALLREADY IN TUNNEL

S4_P_E= 4*SUBJECT + ENTRANCE +  PREVIOUS
S3_P_E2= 3*SUBJECT + 2*ENTRANCE + PREVIOUS
FL_S2_BS_P_E= FREE_LOCATION+ 2*SUBJECT + BESIDE_SUBJECT + PREVIOUS + ENTRANCE


S2_BS3_P= 2*SUBJECT + 3*BESIDE_SUBJECT + PREVIOUS
S3_BS2_P= 3*SUBJECT + 2*BESIDE_SUBJECT + PREVIOUS
FL_S2_BS2_P= FREE_LOCATION+ 2*SUBJECT + 2*BESIDE_SUBJECT + PREVIOUS


def get_directions_list():
    """
    returns a list of the direction vectors
    :return: list of 3d tuples - '(float, float, float)'
    """

    directions= [(0.5, 1, 0),
            (1, 0, 0),
             (0.5, -1, 0),
             (-0.5, -1, 0),
             (-1, 0, 0),
             (-0.5, 1, 0)]
    return directions


def s6(direction):
    matter_dict = {(0.5, 1, 0): True, (1, 0, 0): True, (0.5, -1, 0): True, (-0.5, -1, 0): True, (-1, 0, 0): True,
                   (-0.5, 1, 0): True}
    return matter_dict[direction]

def test_get_neighbors_s6( ):
    assert coating.get_neighbors(get_directions_list(), s6, (0.5, 1, 0))[0] == S6


def test_get_neighbors_S5__P():
     assert coating.get_neighbors(get_directions_list(), s5_e, (0.5, 1, 0))[0] == S5_P


def test_get_neighbors_S4_BS_P():
    assert coating.get_neighbors(get_directions_list(), s4_bs2, (0.5, 1, 0))[0] == S4_BS_P


def test_get_neighbors_FL_S3_BS_P():
    assert coating.get_neighbors(get_directions_list(), fl_s3_bs2, (0.5, 1, 0))[0] ==FL_S3_BS_P


def test_next_direction_S4_BS_P():
    sum, neighbors = coating.get_neighbors(get_directions_list(), s4_bs2, (0.5, -1, 0))
    assert coating.next_direction((0,0,0), sum, neighbors, [(0.5, -1, 0)]) ==  (0.5, 1, 0)


def test_next_direction_FL_S3_BS_P():
    sum, neighbors = coating.get_neighbors(get_directions_list(), fl_s3_bs2,  (-0.5, -1, 0))
    assert coating.next_direction((0,0,0), sum, neighbors,  [(-0.5, -1, 0)] ) ==  (0.5, 1, 0)


def test_next_direction_FL3_S_BS_P():
    sum, neighbors = coating.get_neighbors(get_directions_list(), fl3_s_bs2,  (-1, 0, 0))
    assert coating.next_direction((0,0,0), sum, neighbors,  [(-1, 0, 0)] ) ==  (0.5, 1, 0)


def test_next_direction_FL2_S2_BS_P():
    sum, neighbors = coating.get_neighbors(get_directions_list(), fl2_s2_bs2, (-1, 0, 0))
    assert coating.next_direction((0,0,0), sum, neighbors,  [(-1, 0, 0)]) ==  (0.5, 1, 0)




# def test_next_direction_PL2():
#     sum, neighbors = coating.get_neighbors(get_directions_list(), fl2_s2_bs2)
#     assert coating.next_direction((0,0,0), sum, neighbors,  (-0.5, 1, 0)) ==  None

def test_get_neighbors_FL2_S2_BS_P():
    assert coating.get_neighbors(get_directions_list(), fl2_s2_bs2, (0.5, 1, 0))[0] == FL2_S2_BS_P


def test_get_neighbors_FL3_S_BS_P():
    assert coating.get_neighbors(get_directions_list(), fl3_s_bs2, (0.5, 1, 0))[0] ==FL3_S_BS_P


def test_get_neighbors_FL5_P():
    assert coating.get_neighbors(get_directions_list(), fl6, (0.5, 1, 0))[0] ==FL5_P


def test_get_neighbors_S3_BS_P_E():
    assert coating.get_neighbors(get_directions_list(), s3_bs2_e, (0.5, 1, 0))[0] ==S3_BS_P_E


def test_get_neighbors_S4_P_E():
    assert coating.get_neighbors(get_directions_list(), s4_e2, (0.5, 1, 0))[0] ==S4_P_E



def test_get_neighbors_S3_P_E2():
    assert coating.get_neighbors(get_directions_list(), s3_e3, (0.5, -1, 0))[0] ==S3_P_E2


def test_get_neighbors_FL_S2_BS_P_E():
    assert coating.get_neighbors(get_directions_list(), fl_s2_bs2_e, (-1, 0, 0))[0] ==FL_S2_BS_P_E


def test_get_neighbors_FL_S2_BS2_P():
    assert coating.get_neighbors(get_directions_list(), fl_s2_bs2_e, (0.5, 1, 0))[0] ==FL_S2_BS2_P

def test_get_neighbors_S2_BS3_P():
    assert coating.get_neighbors(get_directions_list(), s2_bs4, (0.5, 1, 0))[0] ==S2_BS3_P


def test_get_neighbors_S3_BS2_P():
    assert coating.get_neighbors(get_directions_list(), s3_bs2_e, (-1, 0, 0))[0] ==S3_BS2_P

S5_E= 5*SUBJECT + ENTRANCE
def s5_e(direction):
    matter_dict = {(0.5, 1, 0): False, (1, 0, 0): True, (0.5, -1, 0): True, (-0.5, -1, 0): True, (-1, 0, 0): True,
                   (-0.5, 1, 0): True}
    return matter_dict[direction]


S4_BS2= 4*SUBJECT + 2*BESIDE_SUBJECT
def s4_bs2(direction):
    matter_dict = {(0.5, 1, 0): False, (1, 0, 0): False, (0.5, -1, 0): True, (-0.5, -1, 0): True, (-1, 0, 0): True,
                   (-0.5, 1, 0): True}
    return matter_dict[direction]


FL_S3_BS2= FREE_LOCATION + 3*SUBJECT + 2*BESIDE_SUBJECT
def fl_s3_bs2(direction):
    matter_dict = {(0.5, 1, 0): False, (1, 0, 0): False, (0.5, -1, 0): False, (-0.5, -1, 0): True, (-1, 0, 0): True,
                   (-0.5, 1, 0): True}
    return matter_dict[direction]


FL2_S2_BS2= 2*FREE_LOCATION + 2*SUBJECT + 2*BESIDE_SUBJECT
def fl2_s2_bs2(direction):
    matter_dict = {(0.5, 1, 0): False, (1, 0, 0): False, (0.5, -1, 0): False, (-0.5, -1, 0): False, (-1, 0, 0): True,
                   (-0.5, 1, 0): True}
    return matter_dict[direction]


FL3_S_BS2= 3*FREE_LOCATION + SUBJECT + 2*BESIDE_SUBJECT
def fl3_s_bs2(direction):
    matter_dict = {(0.5, 1, 0): False, (1, 0, 0): False, (0.5, -1, 0): False, (-0.5, -1, 0): False, (-1, 0, 0): False,
                   (-0.5, 1, 0): True}
    return matter_dict[direction]


FL6 = 6*FREE_LOCATION
def fl6(direction):
    matter_dict = {(0.5, 1, 0): False, (1, 0, 0): False, (0.5, -1, 0): False, (-0.5, -1, 0): False, (-1, 0, 0): False,
                   (-0.5, 1, 0): False}
    return matter_dict[direction]


S2_BS4= 2*SUBJECT + 4*BESIDE_SUBJECT
def s2_bs4(direction):
    matter_dict = {(0.5, 1, 0): False, (1, 0, 0): False, (0.5, -1, 0): True, (-0.5, -1, 0): False, (-1, 0, 0): False,
                   (-0.5, 1, 0): True}
    return matter_dict[direction]


S3_BS2_E= 3*SUBJECT + 2*BESIDE_SUBJECT + ENTRANCE
def s3_bs2_e(direction):
    matter_dict = {(0.5, 1, 0): False, (1, 0, 0): False, (0.5, -1, 0): True, (-0.5, -1, 0): True, (-1, 0, 0): False,
                   (-0.5, 1, 0): True}
    return matter_dict[direction]




S4_E2= 4*SUBJECT + 2*ENTRANCE
def s4_e2(direction):
    matter_dict = {(0.5, 1, 0): False, (1, 0, 0): True, (0.5, -1, 0): True, (-0.5, -1, 0): False, (-1, 0, 0): True,
                   (-0.5, 1, 0): True}
    return matter_dict[direction]


S3_E3= 3*SUBJECT + 3*ENTRANCE
def s3_e3(direction):
    matter_dict = {(0.5, 1, 0): False, (1, 0, 0): True, (0.5, -1, 0): False, (-0.5, -1, 0): True, (-1, 0, 0): False,
                   (-0.5, 1, 0): True}
    return matter_dict[direction]



FL_S2_BS2_E= FREE_LOCATION+ 2*SUBJECT + 2*BESIDE_SUBJECT + ENTRANCE
def fl_s2_bs2_e(direction):
    matter_dict = {(0.5, 1, 0): False, (1, 0, 0): True, (0.5, -1, 0): False, (-0.5, -1, 0): False, (-1, 0, 0): False,
                   (-0.5, 1, 0): True}
    return matter_dict[direction]


# import itertools
# def neighbor_generator():
#     for i in itertools.product([0, 1], repeat=6):
#         matter_dict = {(0.5, 1, 0): i[0], (1, 0, 0): i[1], (0.5, -1, 0): i[2], (-0.5, -1, 0): i[3],
#                        (-1, 0, 0): i[4],
#                        (-0.5, 1, 0): i[5]}



def get_coordinates_in_direction(position, direction):
    """
    calculates a new position from current position and direction
    :param position: coordinates, (float, float, float) tuple, current position
    :param direction: coordinates, (float, float, float) tuple, direction
    :return: coordinates, (float, float, float) tuple, new position
    """
    new_pos = []
    for i in range(len(position)):
        new_pos.append(position[i]+direction[i])
    return tuple(new_pos)


def get_distance(start,end):
    if start[1] == end[1] and start[0] != end[0]:
        return abs(end[0] - start[0])
    elif abs(end[0] - start[0]) - (abs(end[1] - start[1]) * 0.5) > 0:
        return abs(end[1] - start[1]) + abs(end[0] - start[0]) - ( abs(end[1] - start[1]) * 0.5 )
    return abs(end[1] - start[1])


def test_label_neighbor_subject():
    facing_direction = (0.5, 1, 0)
    direction_right = (1, 0, 0)
    direction_left = (-0.5, 1, 0)
    assert coating.label_neighbor(facing_direction, direction_left, direction_right, s6, (1, 0, 0)) == SUBJECT


def test_label_neighbor_beside_subject():
    facing_direction = (0.5, 1, 0)
    direction_right = (1, 0, 0)
    direction_left = (-0.5, 1, 0)
    assert coating.label_neighbor(facing_direction, direction_left, direction_right, s4_bs2, (1, 0, 0)) == BESIDE_SUBJECT


def test_label_neighbor_free_location():
    facing_direction = (0.5, 1, 0)
    direction_right = (1, 0, 0)
    direction_left = (-0.5, 1, 0)
    assert coating.label_neighbor(facing_direction, direction_left, direction_right, fl6, (1, 0, 0)) == FREE_LOCATION


def test_label_neighbor_entrance():
    facing_direction = (0.5, 1, 0)
    direction_right = (1, 0, 0)
    direction_left = (-0.5, 1, 0)
    assert coating.label_neighbor(facing_direction, direction_left, direction_right, s5_e, (1, 0, 0)) == ENTRANCE


def test_label_neighbor_previous():
    facing_direction = (1, 0, 0)
    direction_right = (0.5, 1, 0)
    direction_left = (-0.5, 1, 0)
    assert coating.label_neighbor(facing_direction, direction_left, direction_right) == PREVIOUS



