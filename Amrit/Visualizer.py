import networkx as nx
import matplotlib.pyplot as plt
import TimeManager as TM
import pylab as pl

class VItem(object):
    item = None
    time = 0.0
    
    def __init__(self, item, time):
        self.item = item
        self.time = time

class Visualizer(object):
    sharedVisualizer = None
    
    mainGraph = nx.Graph()
    
    graphs = []
    nodes = []
    edges = {}
    
    @staticmethod
    def createVisualizer():
        Visualizer.sharedVisualizer = Visualizer()
    
    def addNode(self, node):
        item = VItem(node, TM.TimeManager.sharedManager.time)
        self.nodes.append(item)
        
        if len(self.graphs) == TM.TimeManager.sharedManager.time:
            self.graphs.append(nx.Graph())
        else:
            self.graphs[-1].add_node(node)
        
        #self.updateMainGraph(node=node)
        
    def addNodesAndEdges(self, nodes, edges):
        graph = nx.Graph()
        widths = []
        
        for node in nodes:
            graph.add_node(node)
            
        for edge in edges:
            graph.add_edge(edge.keys()[0][0], edge.keys()[0][1], weight=edge[edge.keys()[0]])
            
            widths.append(edge[edge.keys()[0]])
            
        self.updateGraph(graph, widths)
        
    def connect(self, fromNode, toNode, weight):
        if (toNode, fromNode) in self.edges.keys():
            self.edges[(toNode, fromNode)] = weight
            
            self.mainGraph.remove_edge(toNode, fromNode)
            self.mainGraph.add_edge(toNode, fromNode, weight=weight)
            
            #self.updateMainGraph(edge={(toNode, fromNode): weight})
            
        elif (fromNode, toNode) in self.edges.keys():
            self.edges[(fromNode, toNode)] = weight
            
            self.mainGraph.remove_edge(fromNode, toNode)
            self.mainGraph.add_edge(fromNode, toNode, weight=weight)
            
            #self.updateMainGraph(edge={(fromNode, toNode): weight})
            
        else:
            self.edges[(fromNode, toNode)] = weight
            self.mainGraph.add_edge(fromNode, toNode, weight=weight)
            
            #self.updateMainGraph(edge={(fromNode, toNode): weight})
    
    def updateGraph(self, graph, widths):
        plt.clf()
        
        nodes = graph.nodes()
        
        positions = {}
        for node in nodes:
            positions[node] = (node.position.x, node.position.y)
        
        if len(widths) != 0:
            nx.draw(graph, pos=positions, width=widths)
        
            plt.show()
            plt.pause(0.5)
    
    def updateMainGraph(self, node=None, edge=None):
        if node != None:
            nx.draw_networkx_nodes(self.mainGraph, {node: node.position.toTouple()}, nodelist=[node])
        
        elif edge != None:
            firstKey = edge.keys()[0]
            
            node1 = firstKey[0]
            node2 = firstKey[1]
                        
            nx.draw_networkx_edges(self.mainGraph, \
                                  {node1: node1.position.toTouple(), node2: node2.position.toTouple()}, \
                                  width=edge[firstKey], \
                                  edgelist=[firstKey])
                                                    
        plt.show()