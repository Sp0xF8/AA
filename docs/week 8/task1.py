import time
import os

def naiveSearching(pattern, text):
    lp = len(pattern)
    lt = len(text)
    count = 0
    i = 0
    j = 0
    
    
    for i in range(lt-lp+1):
        found = True
        for j in range(lp):
            if text[i+j] != pattern[j]:
                found = False
                break
        if found:
            print ("Found pattern at index " + str(i))
            count+=1
                  
    return count         

def main():
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    f = open(os.path.join(absolute_path, "binary.txt"), "r")
    
    text = f.read()
    pattern = '10110101'

    #text = "ABABDABACDABABCABAB"
    #pattern = "ABA"

    start = time.time()
    print(naiveSearching(pattern, text))
    end = time.time()
    print("The elapsed time is " + str(end-start))
    
if __name__ == '__main__':
    main()

