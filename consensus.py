from graphs import Vertice, Graph, Edge
from typing import TypeVar, Generic
from enum import Enum

T = TypeVar("T")


class Result(Enum):
    PASS = 0
    FAIL = 1
    ERROR = 2
    UNKNOWN = 3


class Process(Vertice, Generic[T]):

    def __init__(self, initial_value: T):
        super().__init__(str(initial_value))
        self.w = [initial_value]
        self.rounds = 0
        self.decision = None

    def decision_rule(self, prescribed_value: T):
        if len(self.w) == 1:
            self.decision = self.w[0]
        else:
            self.decision = prescribed_value


def generate_network(network_size: int) -> Graph[Process[Result]]:

    processes = []
    for i in range(0, network_size):
        processes.append(Process(Result.PASS))

    edges = []
    for i in range(0, network_size):
        for j in range(i + 1, network_size):
            edges.append(Edge(processes[i], processes[j]))

    return Graph(processes, edges)


def floodset(faulty_processes: int, network: Graph[Process[Result]]):


    pass


def run_floodset(faulty_processes: int, network_size: int):

