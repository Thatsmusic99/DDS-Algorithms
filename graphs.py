import enum
from typing import Optional, TypeVar, Generic
from enum import Enum




class State(Enum):
    UNKNOWN = 1
    LEADER = 2



class Vertice:

    def __init__(self, label: str):
        self.label = label
        self.crashed = False


T = TypeVar("T", bound=Vertice)


class Matrix:

    def __init__(self, rows: int, columns: int):
        self.contents = {}

    def __getitem__(self, item: tuple[Vertice, Vertice]):
        if item[1] in self.contents:
            return self.contents[item[1]][item[0]] or 0
        return 0

    def __setitem__(self, key: tuple[Vertice, Vertice], value):
        self.contents[key[1]][key[0]] = value


class Edge(Generic[T]):

    def __init__(self, start: T, end: T, weight: Optional[int] = None, directed: bool = False):
        self.start = start
        self.end = end
        self.directed = directed
        self.weight = weight

    def get_weight(self) -> int:
        return 1 if self.weight is None else self.weight


class Graph(Generic[T]):

    def __init__(self, vertices: list[T], edges: list[Edge[T]]):
        self.vertices = vertices
        self.edges = edges

    def get_order(self):
        return len(self.vertices)

    def get_size(self):
        return len(self.edges)

    def get_neighbours(self, vertice: T) -> list[T]:
        neighbours = []
        for edge in self.edges:
            if edge.start == vertice and edge.end != vertice:
                neighbours.append(edge.end)
            elif edge.end == vertice and edge.start != vertice and not edge.directed:
                neighbours.append(edge.start)

        return neighbours

    def get_edge(self, start_node: T, end_node: T) -> Edge[T] | None:
        for edge in self.edges:
            if edge.start == start_node and edge.end == end_node:
                return edge
            elif edge.end == start_node and edge.start == end_node and not edge.directed:
                return edge
        return None

    def adjacency_matrix(self) -> Matrix:
        blank_matrix = Matrix(len(self.vertices), len(self.vertices))

        for edge in self.edges:

            blank_matrix[(edge.start, edge.end)] = edge.get_weight()

            if not edge.directed:
                blank_matrix[(edge.end, edge.start)] = edge.get_weight()

        return blank_matrix

    def connected_components(self):

        # Have a collection of unvisited nodes
        unvisited = self.vertices.copy()

        components = 0
        while len(unvisited) > 0:
            next_node = unvisited.pop()

            neighbours = self.get_neighbours(next_node)
            to_explore = neighbours.copy()

            # Go through each neighbour to add its own neighbours
            while len(to_explore) > 0:
                next_node = to_explore.pop()
                unvisited.remove(next_node)

                for neighbour in self.get_neighbours(next_node):
                    if neighbour not in unvisited:
                        continue
                    to_explore.append(neighbour)

            components += 1

        return components

    def is_bridge(self, edge: Edge) -> bool:

        modified_edges = self.edges.copy()
        modified_edges.remove(edge)
        removed_edge_graph = Graph(self.vertices, modified_edges)

        return removed_edge_graph.connected_components() > self.connected_components()

    def clone(self) -> "Graph"[T]:
        return Graph(self.vertices.copy(), self.edges.copy())


