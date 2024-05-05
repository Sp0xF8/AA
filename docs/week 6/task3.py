class Queue:
    def __init__(self):
        self.items = []
    def isEmpty(self):
        return self.items == []
    def enqueue(self, item):
        self.items.insert(0,item)
    def dequeue(self):
        return self.items.pop()
    def size(self):
        return len(self.items)
    def printAll(self):
        print(self.items[::-1])

class Stack:
    def __init__(self):
        self.items = []
    def push(self, item):
        self.items.append(item)
    def pop(self):
        size = len(self.items)
        if size<=0:
            print("The stack is empty and no element can be popped!")
            return None
        else:
            return self.items.pop(size-1)
    def peek(self):
        size = len(self.items)
        if size<=0:
            print("The stack is empty and no element can be peeked!")
            return None
        else:
            return self.items[size-1]
    def isEmpty(self):
        if len(self.items) == 0:
            return True
        return False
    
    def size(self):
        return len(self.items)

    def print(self):
        print(self.items)

class GraphWeight:
    def __init__(self, V=None, E=None, directed=True):
        self.gdict = {}
        self.directed = directed
        # make sure that both E and V are given
        if V != None and E != None:
            #create a dictionary based on V and E
            for v in V:
                self.gdict[v] = []
                
            if directed is True: 
                for sv, ev, weight in E:
                    if sv in self.gdict:
                        self.gdict[sv].append((ev, weight))
                
            else: # undirected graphs
                for sv, ev, weight in E:
                    if sv in self.gdict and ev in self.gdict:
                        self.gdict[sv].append((ev, weight))
                        self.gdict[ev].append((sv, weight))
    
    def getVertices(self):
        return list(self.gdict.keys())
               
    def getEdges(self):
        edges = []
        for key, value in self.gdict.items():
            for v in value:
                edges.append((key,v[0]))  
                 
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
      
    def getEdgesAndWeights(self):
        edges = []
        for key, value in self.gdict.items():
            for v in value:
                edges.append((key,v[0], v[1]))    
        return edges
    
        
    def addEdges(self, edges):
        if self.directed is True: 
                for sv, ev, weight in edges:
                    if sv in self.gdict:
                        self.gdict[sv].append((ev, weight))
        else: # undirected graphs
            for sv, ev, weight in edges:
                if sv in self.gdict and ev in self.gdict:
                    self.gdict[sv].append((ev, weight))
                    self.gdict[ev].append((sv, weight))
    
    
    def breadthFirstSearch(self, start, goal):
        current = start        
        visited = []
        toVisit = Queue()
        toVisit.enqueue(current)
        
        while not toVisit.isEmpty():
            current = toVisit.dequeue()
            if current == goal:
                visited.append(current)
                break
            else:
                for v in [v for v, weight in self.gdict[current]]:
                    # unvisited node can be pushed into the stack
                    if v not in visited:
                        toVisit.enqueue(v)
                if current not in visited:
                    visited.append(current)
        
        return visited 
    
        
    def depthFirstSearch(self, start, goal):
        current = start        
        visited = []
        toVisit = Stack()
        toVisit.push(current)
        
        while not toVisit.isEmpty():
            current = toVisit.pop()
            if current == goal:
                visited.append(current)
                break
            else:
                for v in [v for v, weight in self.gdict[current]]:
                    # unvisited node can be pushed into the stack
                    if v not in visited:
                        toVisit.push(v)
                if current not in visited:
                    visited.append(current)
        
        return visited 
    
g = GraphWeight(['s','a','b','c','d','e','f','g'], 
                [('s','a', 0), ('s','b', 0),('s','c', 0),
                 ('a','d', 0),('b','e', 0),('c','f', 0),
                 ('d','g', 0),('e','g', 0),('f','g', 0)], 
                False)

print(g.depthFirstSearch('s', 'a'))
print(g.breadthFirstSearch('s', 'g'))