from graph import Graph
from math import sqrt
class SudokuConnections : 
    def __init__(self,n) :  # constructor

        self.graph = Graph(n) # Graph Object
        self.n=n
        self.rows = n
        self.cols = n
        self.total_blocks = self.rows*self.cols #81

        self.__generateGraph() # Generates all the nodes
        self.connectEdges() # connects all the nodes acc to sudoku constraints

        self.allIds = self.graph.getAllNodesIds() # storing all the ids in a list

        

    def __generateGraph(self) :
        for idx in range(1, self.total_blocks+1) : 
            _ = self.graph.addNode(idx)

    def connectEdges(self) :
        matrix = self.__getGridMatrix()

        head_connections = dict() # head : connections

        for row in range(self.n) :
            for col in range(self.n) :

                head = matrix[row][col] #id of the node
                connections = self.__whatToConnect(matrix, row, col)

                head_connections[head] = connections
        # connect all the edges

        self.__connectThose(head_connections=head_connections)

    def __connectThose(self, head_connections) :
        for head in head_connections.keys() : #head is the start idx
            connections = head_connections[head]
            for key in connections :  #get list of all the connections
                for v in connections[key] :
                    self.graph.addEdge(src=head, dst=v)


    def __whatToConnect(self, matrix, rows, cols) :
        connections = dict()

        row = []
        col = []
        block = []

        # ROWS
        for c in range(cols + 1, self.n):
            if rows < self.n and c < self.n:
                row.append(matrix[rows][c])

        connections["rows"] = row

        # COLS
        for r in range(rows + 1, self.n):
            if r < self.n and cols < self.n:
                col.append(matrix[r][cols])

        connections["cols"] = col
        # BLOCKS
        block_start_row = (rows // int(sqrt(self.n))) * int(sqrt(self.n))
        block_start_col = (cols // int(sqrt(self.n))) * int(sqrt(self.n))
        for i in range(block_start_row, block_start_row + int(sqrt(self.n))):
            for j in range(block_start_col, block_start_col + int(sqrt(self.n))):
                if i != rows and j != cols and i < self.n and j < self.n:
                    block.append(matrix[i][j])

        connections["blocks"] = block
        return connections


    def __getGridMatrix(self) :
        matrix = [[0 for cols in range(self.cols)]
        for rows in range(self.rows)]

        count = 1
        for rows in range(self.n) :
            for cols in range(self.n):
                matrix[rows][cols] = count
                count+=1
        return matrix
