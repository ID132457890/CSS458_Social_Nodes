"""
Overall simulation manager that carries variables and settings that will change the model
"""

import Logger as L
import unittest
import DCL_Person as Person
import DCL_Personality as Personality
import math
import random

class Model(object):
    def __init__(self, num_agents = 10000, topics = 100, friend_thresh = 5, enemy_thresh = -5,
                 time_to_run = 3, probability_initially_online = 0.005, probability_become_online = 0.0005):
        self.logger = L.Logger(self, options = {'threshold': 1})
        self.agents = []
        self.online_agents = []
        self.num_agents = num_agents
        self.topics = topics
        self.friend_thresh = friend_thresh
        self.enemy_thresh = enemy_thresh
        self.time_to_run = time_to_run
        self.probability_initially_online = probability_initially_online
        self.probability_become_online = probability_become_online

        self.spawn_agents(num_agents)

    def run_simulation(self):

        for x in range (self.time_to_run):
            for agent in self.agents:
                agent.take_turn()
            #self.analytics.round_analyze()

        # Report any interesting statistiscs, etc
        # self.analytics.finish_analyze()

    def spawn_agents(self, num_agents):
        for x in range(num_agents):
            self.agents.append(Person.Person(self, personality = Personality.Personality))
            if random.random() < self.probability_initially_online:
                self.agents[x].online = True
                self.online_agents.append(self.agents[x])

        # connect some users to internet and seed some friends just by random for now
        for agent in self.online_agents:
            self.initial_connect_friend(agent)

    def initial_connect_friend(self, agent):
        # just random for now, will make more complex later
        friend_to_add = None
        while friend_to_add is None or friend_to_add == agent:
            friend_to_add = self.online_agents[random.randint(0, len(self.online_agents) - 1)]
        agent.friends.append(friend_to_add)

def find_distance(agent1, agent2):
    """
    :param agent1: first agent
    :param agent2: second agent
    :return: distance (in miles) between agent1 and agent2

    Taken from http://andrew.hedges.name/experiments/haversine/
    Permission granted by terms specified on source page
    """
    dlon = math.radians(agent1.location[0]) - math.radians(agent2.location[0])
    dlat = math.radians(agent1.location[1]) - math.radians(agent2.location[1])
    a = (math.sin(dlat / 2)) ** 2 + math.cos(math.radians(agent1.location[1])) * \
         math.cos(math.radians(agent2.location[1])) * (math.sin(dlon / 2)) ** 2
    c = 2 * math.atan2(a ** .5, (1 - a) ** .5)
    return 3961 * c

class ModelTests(unittest.TestCase):
    def tests(self):
        m = Model()
        seattleperson = Person.Person(m, location=(-122, -48))
        newyorkperson = Person.Person(m, location=(-74, -40))
        jakartaperson = Person.Person(m, location=(107, 6))
        self.assertEquals(int(find_distance(seattleperson, newyorkperson)), 2409)
        self.assertEquals(int(find_distance(newyorkperson, jakartaperson)), 10092)
        self.assertEquals(int(find_distance(jakartaperson, seattleperson)), 8361)
        m.run_simulation()

if __name__ == "__main__":
    tests = ModelTests()
    tests.tests()
