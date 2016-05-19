import numpy as N
import Visualizer as V
import PersonsManager as PM

class Model(object):
    agents = []
    
    def __init__(self):
        PM.PersonsManager.createManager()
        V.Visualizer.createVisualizer()
    
    def spawnAgents(self, count=100):
        
        for num in range(0, count):
            PM.PersonsManager.sharedManager.addPerson()
            
    def sendMessage(self):
        PM.PersonsManager.sharedManager.startSending()
        
model = Model()
model.spawnAgents()