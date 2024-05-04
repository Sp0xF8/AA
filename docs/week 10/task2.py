import multiprocessing as mp
import os

def serialSearch(pattern, text, index):
    found = False        
    for lineno in range(len(text)):
        #str.find(pattern) returns the position of the pattern in the string
        #and returns -1 if no match
        if text[lineno].find(pattern) != -1:
            print("Found the keyword in line "+str(index + lineno+1))
            found = True
            break
    
    if found is False:
        print("The text didn't contain this keyword!")  
    
def parallelisedSearch(pattern, text):
    # we'll create four processes to search the pattern at the same time
    # you do need to check whether your CPU supports the number of processes
    
    # in fact, we use serialSearch() again, but just four times with different sections of the text
    
    # we divide text into four portions, the first three are equal and the last one
    # clear up the mass
    
    n = 4 # number of processes
    
    steps = len(text)//n
    
    # first three processes get the equal portion of the text
    processes = [mp.Process(target=serialSearch, args=(pattern,text[i*steps:(i+1)*steps:],i*steps)) for i in range(n-1)]
    # add the last one which might have a different size of text
    processes.append(mp.Process(target=serialSearch, args=(pattern,text[(n-1)*steps::],(n-1)*steps)))
    
    for p in processes:
        p.start()
        
    for p in processes:
        p.join()
        
    
    

def main():
    
    pattern = 'KunWei'
    
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(absolute_path, "The Deathly Hallows.txt"), encoding='utf8') as file:
        # read in the text line by line as a string and text is
        # the list of storing all strings
        text = file.readlines()
    
    serialSearch(pattern, text, 0)
    
    # please uncomment the following command to try the parallised version
    #parallelisedSearch(pattern, text)
    file.close() 
    
if __name__ == '__main__': 
    main() 
    