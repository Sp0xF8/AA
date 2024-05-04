# communication between Processes via Queue
from multiprocessing import Process, Queue
def childFunc(conn):
    print(conn.get())    
   
if __name__ == '__main__':
    
    q= Queue()
    #q.
    
    child1 =  Process(target=childFunc, args=(q,))
    child2 =  Process(target=childFunc, args=(q,))
       
    q.put("Hello, child1!")
    q.put("Hello, child2!")
  
    child1.start()
    child2.start() 
    child1.join()
    child2.join()