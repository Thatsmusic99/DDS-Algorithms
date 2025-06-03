import random
from enum import Enum
from typing import Union

from graphs import Vertice, Graph, Edge


class GeneralState(Enum):
    LOYAL = 1
    TRAITOR = 2


class GeneralRank(Enum):
    LIEUTENANT = 1
    COMMANDER = 2


class Message(Enum):
    RETREAT = 1
    ATTACK = 2

    def opposite(self) -> "Message":
        return Message.RETREAT if self == Message.ATTACK else Message.ATTACK

class General(Vertice):

    def __init__(self):
        super().__init__("")
        self.state = GeneralState.LOYAL
        self.raml = GeneralRank.LIEUTENANT
        self.value = None

    def send(self, general: "General", message: Message | "SignedMessage"):
        if type(message) is SignedMessage:
            general.receive(message.message)
        else:
            general.receive(message)

    def receive(self, message: Message):
        self.value = message


class SignedMessage:

    def __init__(self, message: Message, general: General):
        self.message = message
        self.generals = [general]


def generate_generals(traitors: int, generals: int) -> tuple[General, Graph[General]]:

    # Create generals
    general_list = []
    for i in range(0, generals):
        general_list = General()

    # Make some generals traitors
    for i in range(0, traitors):
        while True:
            general = random.choice(general_list)
            if general.state == GeneralState.TRAITOR:
                continue
            general.state = GeneralState.TRAITOR
            break

    commander = random.choice(general_list)
    commander.rank = GeneralRank.COMMANDER

    # Set up all the edges
    edges = []
    for i in range(0, generals):
        for j in range(i + 1, generals):
            edge = Edge(general_list[i], general_list[j])
            edges.append(edge)

    return commander, Graph(general_list, edges)


def oral_messages(traitors: int, commander: General, order: Message, graph: Graph[General]):

    if traitors == 0:
        for general in graph.vertices:
            commander.send(general, order)

    else:
        for general in graph.vertices:
            if general == commander:
                continue

            commander.send(general, order)

            modified_graph = graph.clone()
            modified_graph.vertices.remove(commander)

            if general.state == GeneralState.TRAITOR:
                oral_messages(traitors - 1, general, order.opposite(), modified_graph)
            else:
                oral_messages(traitors - 1, general, order, modified_graph)

    responses = []

    for general in graph.vertices:



def run_oral_messages(traitors: int, generals: int):

    commander, graph = generate_generals(traitors, generals)
    commander_order = random.choice([Message.ATTACK, Message.RETREAT])

    if 3 * traitors >= generals:
        print("Too many traitors - oral messages cannot work.")
        return


def signed_messages(required_sigs: int, commander: General, order: Message, graph: Graph[General]):

    signed_order = SignedMessage(order, commander)

    for general in graph.vertices:
        if general == commander:
            continue

        # Store in the value set
        commander.send(general, signed_order)

        if general.state == GeneralState.TRAITOR:
            continue

        if len(signed_order.generals) < required_sigs and general not in signed_order.generals:
            signed_order.generals.append(general)







def run_signed_messages(traitors: int, generals: int):

    commander, graph = generate_generals(traitors, generals)
    commander_order = random.choice([Message.ATTACK, Message.RETREAT])





