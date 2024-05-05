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
    def peek(self):
        return self.items[len(self.items)-1]

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



    def isAdjacent(self, start, end):
        if end in [v for v,w in self.gdict[start]]:
            return True
        else:
            return False       
    
    
    def findPath(self, start, goal):
        visited = self.depthFirstSearch(start, goal)
        toDelete = []
        size = len(visited)
        if visited[size-1] == goal:
            #found the goal
            cur = size-1
            pre = cur-1
            while cur != 0:                
                if self.isAdjacent(visited[pre], visited[cur]):
                    cur = pre
                    pre -= 1
                else:
                    toDelete.append(visited[pre])
                    pre -= 1
            #delete the vertices from the path
            for i in toDelete:
                visited.remove(i)       
                 
        else:
            print("No path for the ending vertex!") 
        
        return visited
    
    
    def dijkstraSP(self, start, end):
        
        #check wheter start and end are valid nodes
        allnodes = list(self.gdict.keys())
                      
        if start not in allnodes or end not in allnodes:
            return None 
             
        
        
        infinite = 100000
        # build a table to record the total weight and its predecessor to get the weight
        # also, this table records all unvisited nodes, visited nodes are removed from this table 
        table = {}
        for node in allnodes:
            table[node] = (node, infinite)
        
        #record the sequence of visited nodes 
        edges = []
        table[start] = (start, 0) 
                   
        current = start
        while current != end: #find the goal
            
            # update total weight for all adjacent nodes of current
            for v, w in self.gdict[current]:
                if v in table: # not visited yet
                    # calculate node's total weight
                    totalweight = table[current][1] + w
                    
                    if totalweight < table[v][1]:
                        #update weight and previous node
                        table[v] = (current, totalweight)
                        
            #add the visited edge into the sequence
            #edges.append((table[current][0], current))
            # delete current node from table to denote it's been visited
            table.pop(current)
            
            # get the unvisited nodes from the table 
            unvisited = list(table.items())
            # terminate if all visited already
            if len(unvisited) == 0:
                return None 
            #sort the unvisited by its total weight
            unvisited.sort(key = lambda x:x[1][1])
            # pick up the first one or smalles one
            current = unvisited[0][0]
            # add the visited edge
            edges.append((table[current][0], current, table[current][1]))
        
        return edges    
        
                         
                 
g = GraphWeight([1,2,3,4,5,6,7,8,9],
                [(1,2,4), (1,4,1), (1,5,8),
                 (2,3,1), (2,4,2), (2,5,6), (2,6,1),
                 (3,5,2), (3,6,5),
                 (4,5,11),(4,7,9), (4,8,8),
                 (5,4,2), (5,6,3), (5,7,1), (5,8,1), (5,9,8),
                 (6,8,7), (6,9,8),
                 (7,5,4), (7,8,2),
                 (8,9,3)])

#print(g.getVertices())
#print(g.getEdgesAndWeights())
#print(g.findPath(1,9))
#print(g.breadthFirstSearch(1,9))
#print(g.depthFirstSearch(1,9))
print(g.dijkstraSP(1,9))
#print(g.gdict)


