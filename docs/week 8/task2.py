import time
import os
def calculateLPSArray(pattern):
    lp = len(pattern)
    
    lps = [None]*lp
    i = 0
    j = 1
    lps[0] = 0
    while lps[lp-1] == None:
        if pattern[i] == pattern[j]:
            lps[j] = i+1 
            i += 1
            j += 1
        else:
            if i==0:
                lps[j] = 0
                j += 1
            else:
                i = lps[i-1]
    return lps           

def KMPSearch(pattern, text):
    lp = len(pattern)
    lt = len(text)
    count = 0
    
    lps = calculateLPSArray(pattern)
    i=0
    j=0   
    
    while i < lt:
        if pattern[j] == text[i]: 
            i += 1
            j += 1
            if j == lp:
                print ("Found pattern at index " + str(i-j))
                count += 1
                j = lps[j-1]
        else:
            if j == 0:
                i += 1
            else:
                
                j=lps[j-1]
    return count

def main():
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    f = open(os.path.join(absolute_path, "binary.txt"), "r")
    
    text = f.read()
    pattern = '10110101'
        
    start = time.time()
    print(KMPSearch(pattern, text))
    end = time.time()
    print("The elapsed time is " + str(end-start))
    
    
    
if __name__ == '__main__':
    main()


