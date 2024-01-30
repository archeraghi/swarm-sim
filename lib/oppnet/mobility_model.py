import random
from enum import Enum

from ..std_lib import NE, E, SE, SW, W, NW


class Mode(Enum):
    Random_Walk = 0
    Back_And_Forth = 1
    Circle = 2
    Random = 3
    Static = 4
    Zonal = 5
    POI = 6
    Random_Mode = 7


class MobilityModel:

    @staticmethod
    def get(particle):
        return getattr(particle, "mobility_model")

    def __init__(self, start_x, start_y, mode: Mode, length=(5, 30), zone=(), starting_dir=None, poi=()):
        if mode == Mode.Random_Mode:
            mode = random.choice(list(Mode)[:-1])
        if mode == Mode.Zonal:
            self.min_x = zone[0]
            self.min_y = zone[1]
            self.max_x = zone[2]
            self.max_y = zone[3]
        else:
            self.min_x = start_x - length[1]
            self.min_y = start_y - length[1]
            self.max_x = start_x + length[1]
            self.max_y = start_y + length[1]
        self.mode = mode
        self.steps = 0
        self.min_length = length[0]
        self.max_length = length[1]
        if not starting_dir:
            self.starting_dir = self.random_direction()
        else:
            self.starting_dir = starting_dir
        self.route_length = random.randint(self.min_length, self.max_length)
        self.poi = poi
        self.return_dir = self.__return_direction()
        self.current_dir = self.starting_dir

    def set(self, particle):
        setattr(particle, "mobility_model", self)

    def __return_direction(self):
        return self.starting_dir - 3 if self.starting_dir > 2 else self.starting_dir + 3
    
    def next_direction(self, current_x_y=None):
        if self.mode == Mode.Back_And_Forth:
            return self.__back_and_forth__()
        elif self.mode == Mode.Random_Walk:
            return self.__random_walk__()
        elif self.mode == Mode.Circle:
            return self.__circle__()
        elif self.mode == Mode.Random:
            return self.__random__()
        elif self.mode == Mode.Static:
            return False
        elif self.mode == Mode.Zonal:
            return self.__zonal__(current_x_y)
        elif self.mode == Mode.POI:
            return self.__poi__(current_x_y)

    def __random__(self):
        self.current_dir = MobilityModel.random_direction()
        return self.current_dir

    def __circle__(self):
        if self.steps < self.route_length:
            self.steps += 1
        else:
            if self.current_dir == NE:
                self.current_dir = NW
            elif self.current_dir == NW:
                self.current_dir = W
            elif self.current_dir == W:
                self.current_dir = SW
            elif self.current_dir == SW:
                self.current_dir = SE
            elif self.current_dir == SE:
                self.current_dir = E
            elif self.current_dir == E:
                self.current_dir = NE
            self.steps = 1
            # new circle if we walked a full circle
            if self.current_dir == self.starting_dir:
                self.route_length = random.randint(1, self.max_length)
                self.starting_dir = MobilityModel.random_direction()
                self.current_dir = self.starting_dir
        return self.current_dir

    def __random_walk__(self):
        if self.steps < self.route_length:
            self.steps += 1
            return self.current_dir
        else:
            self.steps = 1
            self.route_length = random.randint(1, self.max_length)
            return self.__random__()

    def __back_and_forth__(self):
        if 0 <= self.steps < self.route_length:
            self.steps += 1
            return self.starting_dir
        elif self.steps == self.route_length:
            self.steps = -1
            return self.return_dir
        elif self.steps == -self.route_length:
            self.steps = 1
            return self.starting_dir
        else:
            self.steps -= 1
            return self.return_dir

    def __zonal__(self, current_x_y):
        (x, y) = current_x_y
        # check if at min_x then head anywhere but west

        directions = {W,
                      SW,
                      NW,
                      E,
                      SE,
                      NE}

        if self.min_x >= x:
            directions = directions.difference({W, SW, NW})
        if self.max_x <= x:
            directions = directions.difference({E, SE, NE})
        if self.min_y >= y:
            directions = directions.difference({SE, SW})
        if self.max_y <= y:
            directions = directions.difference({NE, NW})

        next_dir = MobilityModel.random_direction(list(directions))
        return next_dir

    def __poi__(self, current_x_y):
        if current_x_y == self.poi:
            print("mobility_model.py - poi():"
                  "Particle reached POI: {}".format(self.poi))
            return False

        # southern movement
        if current_x_y[1] > self.poi[1]:
            # western movement
            if current_x_y[0] > self.poi[0]:
                return SW
            # eastern movement
            elif current_x_y[0] < self.poi[0]:
                return SE
        # northern movement
        elif current_x_y[1] < self.poi[1]:
            # western movement
            if current_x_y[0] > self.poi[0]:
                return NW
            # eastern movement
            elif current_x_y[0] < self.poi[0]:
                return NE

        if current_x_y[0] < self.poi[0]:
            return E
        else:
            return W

    @staticmethod
    def random_direction(exceptions=None):
        if exceptions is None:
            exceptions = [W, SW, NW, E, SE, NE]
        return random.choice(exceptions)
