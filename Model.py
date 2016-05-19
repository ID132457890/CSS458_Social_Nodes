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
    def __init__(self, num_agents = 100, topics = 100, friend_thresh = 5, enemy_thresh = -5,
                 time_to_run = 3):
        self.logger = L.Logger(self, options = {'threshold': 1})
        self.agents = []
        self.num_agents = num_agents
        self.topics = topics
        self.friend_thresh = friend_thresh
        self.enemy_thresh = enemy_thresh
        self.time_to_run = time_to_run

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

        # seed some friends just by random for now
        for x in range(len(self.agents)):
            friend_to_add = None
            while friend_to_add is None or friend_to_add == x:
                friend_to_add = random.randint(0, len(self.agents) - 1)
            self.agents[x].friends.append(self.agents[friend_to_add])

def find_distance(agent1, agent2):
    """
    :param agent1: first agent
    :param agent2: second agent
    :return: distance (in miles) between agent1 and agent2

    Taken from http://andrew.hedges.name/experiments/haversine/
    Permission granted by terms specified on source page
    """
    dlon = agent1.location[0] - agent2.location[0]
    dlat = agent1.location[1] - agent2.location[1]
    a = (math.sin(dlat / 2)) ^ 2 + math.cos(agent1.location[1]) * \
         math.cos(agent2.location[1]) * (math.sin(dlon / 2)) ^ 2
    c = 2 * math.atan2(a ** .5, (1 - a) ** .5)
    return 3961 * c

class ModelTests(unittest.TestCase):
    def tests(self):
        m = Model()
        m.run_simulation()

if __name__ == "__main__":
    tests = ModelTests()
    tests.tests()
