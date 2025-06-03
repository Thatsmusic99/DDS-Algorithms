from typing import Callable

from graphs import Graph, Vertice


class Network:

    def __init__(self):
        pass


def token_network_bidirectional(size: int, vertice_generator: Callable[[], Vertice]) -> Network:

    nodes = []
    for i in range(0, size):
        nodes.append(vertice_generator())

    for i in range(0, size):
        src_node = nodes[i]
        dest_node = nodes[(i + 1) % size]

        

    graph = Graph(nodes, )
    pass
