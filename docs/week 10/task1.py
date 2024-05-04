import multiprocessing as mp

def myfunc(message):
    print(message)

if __name__ == '__main__':  
    print("Number of cpu : ", mp.cpu_count())    
    messages=["Hello", "World", "Python", "Parallel"]
    processes = [mp.Process(target=myfunc, args=(messages[x],)) for x in range(4)]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
