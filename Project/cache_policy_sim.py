import random

OFFSET_MASK = 0
INDEX_MASK = 0
TAG_MASK = 0

OFFSET_BITS = 0
INDEX_BITS = 0
TAG_BITS = 0

SETS = 0
WAYS = 0

def set_cfg(OB,IB,TB,OM,IM,TM,A,SS):
    global OFFSET_BITS, INDEX_BITS, TAG_BITS
    global OFFSET_MASK, INDEX_MASK, TAG_MASK
    global WAYS,SETS
    
    OFFSET_BITS = OB
    INDEX_BITS = IB
    TAG_BITS = TB
    
    OFFSET_MASK = OM
    INDEX_MASK = IM
    TAG_MASK = TM
    
    WAYS = A
    SETS = SS
    
    #print "(Tag,Index,Offset) : (", TAG_BITS,",",INDEX_BITS,",",OFFSET_BITS,")"
    #print "Sets, Ways : ", SETS,WAYS

def extract(val,flag):
    global OFFSET_BITS, INDEX_BITS, TAG_BITS
    global OFFSET_MASK, INDEX_MASK, TAG_MASK
    
    if flag == "OFFSET":
        return (val & OFFSET_MASK) >> 0
    elif flag == "INDEX":
        return (val & INDEX_MASK) >> OFFSET_BITS
    elif flag == "TAG":
        return (val & TAG_MASK) >> (OFFSET_BITS + INDEX_BITS)

def init_cache(SETS):
    cache = dict()
    for i in range(SETS):
        cache[i] = dict()
        
    return cache

def sadd(v):
    global WAYS
    return v if v == (WAYS - 1) else v + 1 

def update_and_find(set):
    max = 0
    LRUtag = 0
    for tag in set:
        if(set[tag] >= max):
            max = set[tag]
            LRUtag = tag
        set[tag] = sadd(set[tag])
        
    return LRUtag
        
def policy_LRU(trace):
    global OFFSET_BITS, INDEX_BITS, TAG_BITS
    global OFFSET_MASK, INDEX_MASK, TAG_MASK
    global SETS
    
    cache = init_cache(SETS)
    miss = 0
    memreq = len(trace)
    iter = 0

    print "Simulating Least Recently Used replacement policy..."
    for addr in trace:
        offset = extract(addr,"OFFSET")
        index = extract(addr,"INDEX")
        tag = extract(addr,"TAG")
        
        print "a:",hex(addr),"t:",hex(tag),"i:",hex(index),"o:",hex(offset)
        #print "t:",hex(tag),"i:",hex(index),"o:",hex(offset)
        #print "t:",tag,"i:",index,"o:",offset,
        
        set = cache[index]
        if tag not in set:
            miss = miss + 1
            if len(set) < WAYS:
                update_and_find(set)
                set[tag] = 0
            else:
                LRUtag = update_and_find(set)
                set.pop(LRUtag)
                set[tag] = 0
        else:
            update_and_find(set)
            set[tag] = 0
            
        iter = iter + 1
        if iter > 2:
            break

    print "Gathering statistics..."
    print "Misses: ", miss
    print "Memory Requests: ",memreq
    print "Miss Percentage: ",(float(miss)/memreq)*100,"%"

def update(set):
    for tag in set:
        set[tag] = sadd(set[tag])
  
def policy_RANDOM(trace):
    global OFFSET_BITS, INDEX_BITS, TAG_BITS
    global OFFSET_MASK, INDEX_MASK, TAG_MASK
    global SETS
    
    cache = init_cache(SETS)
    miss = 0
    memreq = len(trace)
    iter = 0
    
    print "Simulating random replacement policy..."
    for addr in trace:
        offset = extract(addr,"OFFSET")
        index = extract(addr,"INDEX")
        tag = extract(addr,"TAG")
        
        #print "a:",hex(addr),"t:",hex(tag),"i:",hex(index),"o:",hex(offset)
        #print "t:",hex(tag),"i:",hex(index),"o:",hex(offset)
        #print "t:",tag,"i:",index,"o:",offset,
        
        set = cache[index]
        if tag not in set:
            miss = miss + 1
            if len(set) < WAYS:
                set[tag] = 0
            else:
                #print len(set),set,set.keys
                LRUtag = random.sample(set,2)[0]
                #print LRUtag
                set.pop(LRUtag)
                set[tag] = 0
        else:
            set[tag] = 0
    
    print "Gathering statistics..."
    print "Misses: ", miss
    print "Memory Requests: ",memreq
    print "Miss Percentage: ",(float(miss)/memreq)*100,"%"
    