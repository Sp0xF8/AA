import multiprocessing as mp
import os

def serialSearch(pattern, text, conn):
    message = conn.get()
    start = int(message[0])
    end = int(message[1])
        
    found = False        
    for lineno in range(start, end):
        
        if text[lineno].find(pattern) != -1:
            print("Found the keyword in line "+str(lineno+1))
            found = True
            break
    
    if found is False:
        print("The text didn't contain this keyword!")  
    
def parallelisedSearch(pattern, text):
    n = 4 # number of processes
    steps = len(text)//n
    
    q = mp.Queue()
    # creat n processes
    processes = [mp.Process(target=serialSearch, args=(pattern,text, q)) for i in range(n)]
    # start all processes        
    for p in processes:
        p.start()
    
    #send the boundaries of the text to all processes
    for i in range(n-1):
        q.put([i*steps, (i+1)*steps])
    #send the last part of the text
    q.put([(n-1)*steps, len(text)])
        
    for p in processes:
        p.join()
        
    
    

def main():
    
    pattern = 'KunWei'
    
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(absolute_path, "The Deathly Hallows.txt"), encoding='utf8') as file:
    
        # read in the text line by line as a string and text is
        # the list of storing all strings
        text = file.readlines()
    
    #serialSearch(pattern, text, 0)
    parallelisedSearch(pattern, text)
    file.close() 
    
if __name__ == '__main__': 
    main() 