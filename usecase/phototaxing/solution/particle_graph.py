from .utils import compare_coords
from .utils import determine_coords_from_direction

# This method constructs a graph out of the neighbors of a particle
# and makes connections whenever two particles are adjacent
# It returns a list of the graph nodes
def create_graph(neighbors):
    list_particle_nodes = []
    neighbors_nodes = []
    for nb in neighbors:
        new_node = ParticleNode()
        new_node.particle = nb
        neighbors_nodes.append(new_node)
        list_particle_nodes.append(new_node)
    for node in neighbors_nodes:
        particle = node.particle
        for nb_dir in range(0, 6):
            coords_a = determine_coords_from_direction(particle.coords, nb_dir)
            for node2 in neighbors_nodes:
                particle2 = node2.particle
                coords_b = particle2.coords
                if compare_coords(coords_a, coords_b):
                    node.make_connection(nb_dir, node2)
    return list_particle_nodes

# This method checks whether the graph stays locally connected if a particle moves from coords in direction dir
def check_connectivity_after_move(coords, neighbors, dir):
    list_particle_nodes = create_graph(neighbors)
    coords_empty_space = determine_coords_from_direction(coords, dir)
    dummy_node = ParticleNode()
    dummy_node.list_connections = []
    for dirval in range(0, 6):
        coords_nb = determine_coords_from_direction(coords_empty_space, dirval)
        for dummy_nb in list_particle_nodes:
            if compare_coords(coords_nb, dummy_nb.particle.coords):
                dummy_node.make_connection(-1, dummy_nb)
                dummy_nb.make_connection(-1, dummy_node)
    list_particle_nodes.append(dummy_node)
    run_search_from(dummy_node)
    checked = check_visited(list_particle_nodes)
    return [checked, len(dummy_node.list_connections)]

# This method simply runs a DFS on the neighborhood graph
def run_search_from(particle_node):
    if not particle_node.visited:
        particle_node.visited = True
        for conn in particle_node.list_connections:
            run_search_from(conn.particle_node)

# This runs the search algorithm, while excluding a specific coordinate/particle
def run_search_with_exclusion(particle_node, coords_to_exclude):
    particle = particle_node.particle
    if not particle_node.visited and particle is not None and not compare_coords(particle.coords, coords_to_exclude):
        particle_node.visited = True
        for conn in particle_node.list_connections:
            run_search_from(conn.particle_node)

# This checks if all nodes of a graph have been visited
def check_visited(list_particle_nodes):
    for node in list_particle_nodes:
        if not node.visited:
            return False
    return True

# This takes two neighborhood graphs and merges them at the points where the particles connect
# and then checks whether this merged graph is locally connected
def check_for_connectivity_in_merged_graphs(nb_graph1, nb_graph2):
    nodes_graph1 = create_graph(nb_graph1)
    nodes_graph2 = create_graph(nb_graph2)
    for node1 in nodes_graph1:
        for node2 in nodes_graph2:
            if node1.particle == node2.particle:
                node1.make_connection(-1, node2)
    run_search_from(nodes_graph1[0])
    return check_visited(nodes_graph1) and check_visited(nodes_graph2)

# The particle node contains the particle as well as the connections that it makes to its neighbors
class ParticleNode:
    particle = None
    list_connections = []
    visited = False
    marked = False
    avoid = False

    def __init__(self):
        self.particle = None
        self.list_connections = []
        self.visited = False
        self.marked = False
        self.avoid = False

    def make_connection(self, dir, node):
        conn = Connection()
        conn.dir = dir
        conn.particle_node = node
        self.list_connections.append(conn)


class Connection:
    dir = -1
    particle_node = None