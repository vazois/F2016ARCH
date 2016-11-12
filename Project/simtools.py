def sadd(v):
    global WAYS
    return v if v == (WAYS - 1) else v + 1 
    #return v+1
    
def updateCounters(set):
    for block in set:
        set[block] = sadd(set[block])
        
def findLRU(set):
    LRUtag=0
    maxCount = 0
    for tag in set:
        if maxCount <= set[tag]:
            LRUtag = tag
    
    return LRUtag