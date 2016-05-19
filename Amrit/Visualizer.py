import networkx as nx
import matplotlib.pyplot as plt

class Visualizer(object):
    sharedVisualizer = None
    
    mainGraph = nx.Graph()
    
    nodes = []
    edges = {}
    
    @staticmethod
    def createVisualizer():
        Visualizer.sharedVisualizer = Visualizer()
    
    def addNode(self, node):
        self.nodes.append(node)
        self.mainGraph.add_node(node)
        
        self.updateMainGraph(node=node)
        
    def connect(self, fromNode, toNode, weight):
        if (toNode, fromNode) in self.edges:
            self.edges[(toNode, fromNode)] = weight
            
            self.mainGraph.remove_edge(toNode, fromNode)
            self.mainGraph.add_edge(toNode, fromNode, weight=weight)
            
            #self.updateMainGraph(edge={(toNode, fromNode): weight})
            
        elif (fromNode, toNode) in self.edges:
            self.edges[(fromNode, toNode)] = weight
            
            self.mainGraph.remove_edge(fromNode, toNode)
            self.mainGraph.add_edge(fromNode, toNode, weight=weight)
            
            #self.updateMainGraph(edge={(fromNode, toNode): weight})
            
        else:
            self.edges[(fromNode, toNode)] = weight
            self.mainGraph.add_edge(fromNode, toNode, weight=weight)
            
            self.updateMainGraph(edge={(fromNode, toNode): weight})
    
    def updateMainGraph(self, node=None, edge=None):
        if node != None:
            nx.draw_networkx_nodes(self.mainGraph, {node: node.position.toTouple()}, nodelist=[node])
        
        if edge != None:
            firstKey = edge.keys()[0]
            
            node1 = firstKey[0]
            node2 = firstKey[1]
                        
            nx.draw_networkx_edges(self.mainGraph, \
                                  {node1: node1.position.toTouple(), node2: node2.position.toTouple()}, \
                                  width=1, \
                                  edgelist=[firstKey])
                                                    
        plt.show()