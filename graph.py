
class Node : 
    
    def __init__(self, idx) : # Constructor
        self.id = idx
        self.connectedTo = dict()

    def addNeighbour(self, neighbour , weight = 0) :

        if neighbour.id not in self.connectedTo.keys() :  
            self.connectedTo[neighbour.id] = weight





    def getConnections(self) : 
        return self.connectedTo.keys()

    def getID(self) : 
        return self.id




class Graph : 

    totalV = 0 # total vertices in the graph
    
    def __init__(self,n) :
        self.n=n
        self.allNodes = dict()

    def addNode(self, idx) :
        if idx in self.allNodes : 
            return None
        
        Graph.totalV += 1
        node = Node(idx=idx)
        self.allNodes[idx] = node
        return node


    def addEdge(self, src, dst, wt = 0) :
        self.allNodes[src].addNeighbour(self.allNodes[dst], wt)
        self.allNodes[dst].addNeighbour(self.allNodes[src], wt)
    
    def isNeighbour(self, u, v) : 

        if u >=1 and u <= self.n**2 and v >=1 and v<= self.n**2 and u !=v :
            if v in self.allNodes[u].getConnections() : 
                return True
        return False




    # getter
    def getNode(self, idx) : 
        if idx in self.allNodes : 
            return self.allNodes[idx]
        return None

    def getAllNodesIds(self) : 
        return self.allNodes.keys()

