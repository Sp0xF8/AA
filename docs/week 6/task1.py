class Graph:
    def __init__(self, V=None, E=None, directed=True):
        self.gdict = {}
        self.directed = directed
        # make sure that both E and V are given
        if V != None and E != None:
            #create a dictionary based on V and E
            for v in V:
                self.gdict[v] = []
                
            if directed is True: 
                for sv, ev in E:
                    if sv in self.gdict:
                        self.gdict[sv].append(ev)
            else: # undirected graphs
                for sv, ev in E:
                    if sv in self.gdict and ev in self.gdict:
                        self.gdict[sv].append(ev)
                        self.gdict[ev].append(sv)
    
    def getVertices(self):
        return list(self.gdict.keys())
               
    def getEdges(self):
        edges = []
        for key, value in self.gdict.items():
            for v in value:
                edges.append((key,v))    
        return edges
    
    def addVertices(self, vertices):
        for v in vertices:
            if v not in self.gdict:
                self.gdict[v] = []
    
    def addEdges(self, edges):
        if self.directed is True: 
                for sv, ev in edges:
                    if sv in self.gdict:
                        self.gdict[sv].append(ev)
        else: # undirected graphs
            for sv, ev in edges:
                if sv in self.gdict and ev in self.gdict:
                    self.gdict[sv].append(ev)
                    self.gdict[ev].append(sv)
                        
        

g = Graph(["a","b","c"], [("a", "b"), ("b", "c"), ("c", "a")])

print(g.getVertices())
print(g.getEdges())

g.addVertices(['d'])
g.addEdges([('d','a')])
print(g.getVertices())
print(g.getEdges())