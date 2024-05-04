# communication between Processes via pipe
from multiprocessing import Process, Pipe
def childFunc(conn):
    print(conn.recv())
    conn.send(["Hello, parent!"])
    conn.close()
    
def parentFunc(conn):
    conn.send(['Hello, child1!'])
    conn.send(['Hello, child2!'])
    print(conn.recv())
    print(conn.recv())
    conn.close()
    
if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    parent = Process(target=parentFunc, args=(parent_conn,))
    child1 =  Process(target=childFunc, args=(child_conn,))
    child2 =  Process(target=childFunc, args=(child_conn,))
       
    parent.start()
    child1.start()
    child2.start()
    parent.join()
    child1.join()
    child2.join()