import math
from typing import List, Dict, Set, Tuple
from copy import deepcopy


class PMaxInfo:
    ids: Set[int]
    dist: float
    directions: List[int]
    lifetime: int

    def __init__(self):
        """
        A type for organizing information about the current p_max.
        ids: all agent ids that are believed to have the maximum distance
        dist: maximum agent distance known to this agent
        directions: all directions from where this agent received messages with the current PMax
        black_list: unused
        """
        self.ids = set()
        self.dist = -math.inf
        self.directions = []
        self.lifetime = 0

    def __str__(self) -> str:
        return "id: " + str(self.ids) + "|" + "dist: " + str(self.dist) + "|" + "direction: " + str(self.directions)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PMaxInfo):
            return False
        return self.dist == other.dist and any(self_id in other.ids for self_id in self.ids)

    def reset(self):
        self.ids = set()
        self.dist = -math.inf
        self.directions = []
        self.lifetime = 0


class OwnDistance:
    agent_distance: float
    agent_id: int

    def __init__(self, agent_distance: float, agent_id: int) -> None:
        """
        A message package, which contains information about the distance of the sender to the next item.
        :param agent_distance: distance of the sender to the next item
        :param agent_id: id of the sender agent
        """
        self.agent_distance = agent_distance
        self.agent_id = agent_id

    def __str__(self) -> str:
        return "id: " + str(self.agent_id) + " | dist: " + str(self.agent_distance)


class PMax(OwnDistance):
    p_max_ids: Set[int]
    p_max_dist: float
    p_max_dir: int
    p_max_lifetime: int

    def __init__(self, agent_distance: float, agent_id: int, p_max: PMaxInfo) -> None:
        """
        In addition to the information in OwnDistance this package contains information about the maximum agent distance
        known to this agent.
        :param agent_distance: distance of the sender to the next item
        :param agent_id: id of the sender agent
        :param p_max: maximum distance of a agent known to this agent
        :param p_max_table: currently unused
        """
        OwnDistance.__init__(self, agent_distance, agent_id)
        self.p_max_ids = deepcopy(p_max.ids)
        self.p_max_dist = p_max.dist
        self.p_max_dir = 0
        self.p_max_lifetime = p_max.lifetime

    def __str__(self) -> str:
        return OwnDistance.__str__(self) + " | max_id: " + str(self.p_max_ids) + " | max_dist: " + \
               str(self.p_max_dist) + " | max_dir: " + str(self.p_max_dir)


class Neighbor:
    type: str
    dist: float
    
    def __init__(self, type: str, dist: float) -> None:
        """
        A type storing the type and calculated distance for a neighbor of a agent
        :param type: type of the neighbor (fl, p, t)
        :param dist: calculated distance of the neighbor to the next item
        """
        self.type = type
        self.dist = dist

    def __str__(self) -> str:
        return str(self.type) + " | " + str(self.dist)

    def __repr__(self) -> str:
        return str(self)


class TargetitemInfo:
    target: Tuple[float]

    def __init__(self, target):
        self.target = target

    def __str__(self) -> str:
        return str(self.target)


NH_LIST_TYPE = List[Neighbor]
RCV_BUF_TYPE = Dict[int, OwnDistance]