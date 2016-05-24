import Person
import Model
import Logger
import Personality
import Post

import unittest

class TestModelMethods(unittest.TestCase):

    def TestModelInstantiation(self):
        m = None
        m = Model.model()
        self.assertNotEquals(m, None, "Model instantiation not working.")

    def TestDistanceCalculator(self):
        m = Model.model()

        seattleperson = Person.Person(m, location=(-122, -48))
        newyorkperson = Person.Person(m, location=(-74, -40))
        jakartaperson = Person.Person(m, location=(107, 6))
        self.assertEquals(int(Model.find_distance(seattleperson, newyorkperson)), 2409, "SEA->NYC != 2409")
        self.assertEquals(int(Model.find_distance(newyorkperson, jakartaperson)), 10092, "NYC->JKT != 10092")
        self.assertEquals(int(Model.find_distance(jakartaperson, seattleperson)), 8361, "JKT->SEA != 8361")