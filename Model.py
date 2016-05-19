"""
Overall simulation manager that carries variables and settings that will change the model
"""

import Logger as L
import unittest
import DCL_Person as Person
import math

class Model(object):
    def __init__(self, num_agents = 100):
        self.logger = L.Logger(self)
        self.agents = []
        self.num_agents = num_agents

        self.spawn_agents(num_agents)

    def run_simulation(self):

        for x in range (self.sim_length * self.steps_day):
            for agent in self.env.agents:
                agent.take_turn()
            #self.analytics.round_analyze()

        # Report any interesting statistiscs, etc
        self.analytics.finish_analyze()

    def spawn_agents(self, num_agents):
        for x in range(num_agents):
            self.agents.append(Person.Person())

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
