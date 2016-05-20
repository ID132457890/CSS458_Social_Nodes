import numpy as N
import Visualizer as V
import PersonsManager as PM
import Person as PE

class Model(object):
    agents = []
    
    def __init__(self):
        PM.PersonsManager.createManager()
        V.Visualizer.createVisualizer()
    
    def spawnAgents(self, count=20):
        
        for num in range(0, count):
            position = PE.Position(N.random.uniform(-10, 10), N.random.uniform(-10, 10))
            
            PM.PersonsManager.sharedManager.addPerson(position)
            
    def startSimulating(self, maxTime=10):
        
        for time in range(maxTime + 1):
            if time == 0:
                PM.PersonsManager.sharedManager.startOnline()
            else:
                PM.PersonsManager.sharedManager.startSending()
        
model = Model()
model.spawnAgents()
model.startSimulating(1)