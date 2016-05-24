import networkx as nx
import matplotlib.pyplot as plt
import TimeManager as TM
import pylab as pl

from enum import Enum

class VType(Enum):
    allGraphs = 0
    mainNodesGraph = 1
    postsSentGraph = 2
    avgFriendsGraph = 3
    avgEnemiesGraph = 4
    avgLikenessGraph = 5
    avgFriendsDistanceGraph = 6
    avgEnemiesDistanceGraph = 7
    onlinePeopleGraph = 8

class VItem(object):
    item = None
    time = 0.0
    
    def __init__(self, item, time):
        self.item = item
        self.time = time

class Visualizer(object):
    sharedVisualizer = None
    
    mainGraph = nx.Graph()
    
    mainGraphFig = None
    
    postsSentFig = None
    postsSent = []
    
    postsSharedFig = None
    postsShared = []
    
    avgFriendsFig = None
    avgFriends = []
    
    avgIgnoredFig = None
    avgIgnored = []
    
    avgLikenessFig = None
    avgLikeness = []
    
    avgFriendsDistanceFig = None
    avgFriendsDistance = []
    
    avgIgnoredDistanceFig = None
    avgIgnoredDistance = []
    
    avgMissedFig = None
    avgMissed = []
    
    onlinePeopleFig = None
    onlinePeople = []
    
    graphs = []
    nodes = []
    edges = {}
    
    acceptedTypes = []
    
    @staticmethod
    def createVisualizer(types=[]):
        Visualizer.sharedVisualizer = Visualizer(types=types)
        
    def __init__(self, types=[]):
        
        self.acceptedTypes = types
        
        if len(types) == 0 or VType.mainNodesGraph in types:
            self.mainGraphFig = plt.figure()
        
        if len(types) == 0 or VType.postsSentGraph in types:
            self.postsSentFig = plt.figure()
            self.postsSent = []
        
        #self.postsSharedFig = plt.figure()
        #self.postsShared = []
        
        if len(types) == 0 or VType.avgFriendsGraph in types:
            self.avgFriendsFig = plt.figure()
            self.avgFriends = []
        
        if len(types) == 0 or VType.avgEnemiesGraph in types:
            self.avgIgnoredFig = plt.figure()
            self.avgIgnored = []
        
        if len(types) == 0 or VType.avgLikenessGraph in types:
            self.avgLikenessFig = plt.figure()
            self.avgLikeness = []
        
        if len(types) == 0 or VType.avgFriendsDistanceGraph in types:
            self.avgFriendsDistanceFig = plt.figure()
            self.avgFriendsDistance = []
        
        if len(types) == 0 or VType.avgEnemiesDistanceGraph in types:
            self.avgIgnoredDistanceFig = plt.figure()
            self.avgIgnoredDistance = []
        
        #self.avgMissedFig = plt.figure()
        #self.avgMissed = []
        
        if len(types) == 0 or VType.onlinePeopleGraph in types:
            self.onlinePeopleFig = plt.figure()
            self.onlinePeople = []
    
    def addNode(self, node):
        item = VItem(node, TM.TimeManager.sharedManager.time)
        self.nodes.append(item)
        
        if len(self.graphs) == TM.TimeManager.sharedManager.time:
            self.graphs.append(nx.Graph())
        else:
            self.graphs[-1].add_node(node)
        
        #self.updateMainGraph(node=node)
        
    def addNodesAndEdges(self, nodes, edges):
        if len(self.acceptedTypes) == 0 or (VType.mainNodesGraph in self.acceptedTypes):
            graph = nx.Graph()
            widths = []
            colors = []
        
            for node in nodes:
                graph.add_node(node)
            
            for edge in edges:
                firstNode = edge.keys()[0][0]
                secondNode = edge.keys()[0][1]
                
                if (not ((firstNode, secondNode) in graph.edges())) and \
                    (not ((secondNode, firstNode) in graph.edges())):
                
                    weight = edge[edge.keys()[0]] / 54 * 6
                
                    if weight > 6.0:
                        weight = 6.0
                    elif weight < -6.0:
                        weight = 6.0
                    
                    if weight >= 4:
                        colors.append("g")
                    elif weight >= 0:
                        colors.append("#96ba07")
                    elif weight >= -4:
                        colors.append("#f59f0a")
                    elif weight >= -6:
                        colors.append("r")
                
                    graph.add_edge(firstNode, secondNode, weight=weight)
                
                    widths.append(weight)
            
            self.updateGraph(graph, widths, colors)
        
    def addPostsSent(self, postsSent):
        if len(self.acceptedTypes) == 0 or (VType.postsSentGraph in self.acceptedTypes):
            self.postsSent.append(postsSent)
        
            self.updatePostsSentTimeGraph()
        
    def addPostsShared(self, postsShared):
        self.postsShared.append(postsShared)
        
        self.updatePostsSharedTimeGraph()
        
    def addAvgFriends(self, friends):
        if len(self.acceptedTypes) == 0 or (VType.avgFriendsGraph in self.acceptedTypes):
            self.avgFriends.append(friends)
        
            self.updateAvgFriendsGraph()
        
    def addAvgIgnored(self, ignored):
        if len(self.acceptedTypes) == 0 or (VType.avgEnemiesGraph in self.acceptedTypes):
            self.avgIgnored.append(ignored)
        
            self.updateAvgIgnoredGraph()
        
    def addAvgLikeness(self, likeness):
        if len(self.acceptedTypes) == 0 or (VType.avgLikenessGraph in self.acceptedTypes):
            self.avgLikeness.append(likeness)
        
            self.updateAvgLikenessGraph()
        
    def addAvgFriendsDistance(self, distance):
        if len(self.acceptedTypes) == 0 or (VType.avgFriendsDistanceGraph in self.acceptedTypes):
            self.avgFriendsDistance.append(distance)
        
            self.updateAvgFriendsDistanceGraph()
        
    def addAvgIgnoredDistance(self, distance):
        if len(self.acceptedTypes) == 0 or (VType.avgEnemiesDistanceGraph in self.acceptedTypes):
            self.avgIgnoredDistance.append(distance)
        
            self.updateAvgIgnoredDistanceGraph()
        
    def addAvgMissed(self, missed):
        self.avgMissed.append(missed)
        
        self.updateAvgMissedGraph()
        
    def addOnlinePeople(self, people):
        if len(self.acceptedTypes) == 0 or (VType.inlinePeopleGraph in self.acceptedTypes):
            self.onlinePeople.append(people)
        
            self.updateOnlinePeopleGraph()
        
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
    
    def updateGraph(self, graph, widths, edgeColors):
        plt.figure(self.mainGraphFig.number)
        self.mainGraphFig.clear()
        
        nodes = graph.nodes()
        
        positions = {}
        for node in nodes:
            positions[node] = (node.location[0], node.location[1])
            
        colors = []
        for node in nodes:
            if node.online:
                colors.append("g")
            else:
                colors.append("r")
        
        if len(widths) != 0:
            nx.draw(graph, ax=self.mainGraphFig.add_subplot(111), pos=positions, width=widths, node_color=colors, \
            edge_color=edgeColors)
        
            self.mainGraphFig.show()
            
        plt.pause(0.01)
            
    def updatePostsSentTimeGraph(self):
        plt.figure(self.postsSentFig.number)
        
        self.postsSentFig.clear()
        sub = self.postsSentFig.add_subplot(111)
        sub.plot(range(len(self.postsSent)), self.postsSent)
        sub.set_title("Posts sent vs time")
        self.postsSentFig.show()
        
        plt.pause(0.01)
        
    def updatePostsSharedTimeGraph(self):
        plt.figure(self.postsSharedFig.number)
        
        self.postsSharedFig.clear()
        sub = self.postsSharedFig.add_subplot(111)
        sub.plot(range(len(self.postsShared)), self.postsShared)
        sub.set_title("Posts shared vs time")
        self.postsSharedFig.show()
        
        plt.pause(0.01)
        
    def updateAvgFriendsGraph(self):
        plt.figure(self.avgFriendsFig.number)
        
        self.avgFriendsFig.clear()
        sub = self.avgFriendsFig.add_subplot(111)
        sub.plot(range(len(self.avgFriends)), self.avgFriends)
        sub.set_title("Average # of friends vs time")
        self.avgFriendsFig.show()
        
        plt.pause(0.01)
        
    def updateAvgIgnoredGraph(self):
        plt.figure(self.avgIgnoredFig.number)
        
        self.avgIgnoredFig.clear()
        sub = self.avgIgnoredFig.add_subplot(111)
        sub.plot(range(len(self.avgIgnored)), self.avgIgnored)
        sub.set_title("Average # of ignored vs time")
        self.avgIgnoredFig.show()
        
        plt.pause(0.01)
        
    def updateAvgLikenessGraph(self):
        plt.figure(self.avgLikenessFig.number)
        
        self.avgLikenessFig.clear()
        sub = self.avgLikenessFig.add_subplot(111)
        sub.plot(range(len(self.avgLikeness)), self.avgLikeness)
        sub.set_title("Average likeness level vs time")
        self.avgLikenessFig.show()
        
        plt.pause(0.01)
        
    def updateAvgFriendsDistanceGraph(self):
        plt.figure(self.avgFriendsDistanceFig.number)
        
        self.avgFriendsDistanceFig.clear()
        sub = self.avgFriendsDistanceFig.add_subplot(111)
        sub.plot(range(len(self.avgFriendsDistance)), self.avgFriendsDistance)
        sub.set_title("Average friend distance vs time")
        self.avgFriendsDistanceFig.show()
        
        plt.pause(0.01)
    
    def updateAvgIgnoredDistanceGraph(self):
        plt.figure(self.avgIgnoredDistanceFig.number)
        
        self.avgIgnoredDistanceFig.clear()
        sub = self.avgIgnoredDistanceFig.add_subplot(111)
        sub.plot(range(len(self.avgIgnoredDistance)), self.avgIgnoredDistance)
        sub.set_title("Average ignored distance vs time")
        self.avgIgnoredDistanceFig.show()
        
        plt.pause(0.01)
        
    def updateAvgMissedGraph(self):
        plt.figure(self.avgMissedFig.number)
        
        self.avgMissedFig.clear()
        sub = self.avgMissedFig.add_subplot(111)
        sub.plot(range(len(self.avgMissed)), self.avgMissed)
        sub.set_title("Average missed opportunities vs time")
        self.avgMissedFig.show()
        
        plt.pause(0.01)
        
    def updateOnlinePeopleGraph(self):
        plt.figure(self.onlinePeopleFig.number)
        
        self.onlinePeopleFig.clear()
        sub = self.onlinePeopleFig.add_subplot(111)
        sub.plot(range(len(self.onlinePeople)), self.onlinePeople)
        sub.set_title("People becoming online vs time")
        self.onlinePeopleFig.show()
        
        plt.pause(0.01)
    
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
        
    def pause(self):
        plt.pause(0.5)