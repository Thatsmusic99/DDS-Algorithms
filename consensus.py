from graphs import Vertice, Graph, Edge
from typing import TypeVar, Generic
from enum import Enum
import random

T = TypeVar("T")


class ProcessStatus(Enum):
    CORRECT = 0
    DEAD = 1


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
        self.status = ProcessStatus.CORRECT

    def send_w(self, process: "Process"):
        process.receive(self.w)

    def receive(self, w: list[T]):
        if self.status != ProcessStatus.DEAD:
            self.w = set(self.w + w)

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

    failed_processes = 0
    
    for round in range(0, faulty_processes + 1):

        # Have every process send each other its values
        for process_i in range(0, len(network.vertices)):

            process_i_actual = network.vertices[process_i]
            if process_i_actual.status == ProcessStatus.DEAD:
                continue

            for process_j in range(process_i + 1, len(network.vertices)):

                # Whilst sending, make it possible for process i to crash
                if failed_processes < faulty_processes:
                    if random.randint(0, 20) == 0:
                        failed_processes += 1
                        process_i_actual.status = ProcessStatus.DEAD
                        break
                
                # Send w to process j
                process_i_actual.send_w(network.vertices[process_j])

    # Now, apply the decision rule
    # I can't be asked to do this right now
    # But basically check each non-faulty process' W set


def run_floodset(faulty_processes: int, network_size: int, prescribed_value: T):

    graph = generate_network(network_size)
    floodset(faulty_processes, graph)
