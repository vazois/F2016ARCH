import definitions as df
import random

def test_cache():
    print "Test Cache>>>>>>>>>>>>>>>>>>>>>"
    print "Cache properties : ",df.C," byte ", df.A ,"- way associative cache with ", df.B, " byte line"
    print "(Tag,Index,Offset) : (", df.TAG_BITS,",",df.INDEX_BITS,",",df.OFFSET_BITS,")"
    print "(Tag Mask,Index Mask,Offset Mask) : (",hex(df.TAG_MASK),",",hex(df.INDEX_MASK),",",hex(df.OFFSET_MASK),")"
    print "Sets :",df.SETS

def extract(val,flag):
    global OFFSET_BITS, INDEX_BITS, TAG_BITS
    global OFFSET_MASK, INDEX_MASK, TAG_MASK
    
    if flag == "OFFSET":
        return (val & df.OFFSET_MASK) >> 0
    elif flag == "INDEX":
        return (val & df.INDEX_MASK) >> df.OFFSET_BITS
    elif flag == "TAG":
        return (val & df.TAG_MASK) >> (df.OFFSET_BITS + df.INDEX_BITS)

def sadd(v):
    return v if v == (df.A - 1) else v + 1

def find(lset,tag):
    for i in range(len(lset)):
        if lset[i] == tag:
            return i
    return -1
        
def policy_LRU(trace):
    cache = dict()
    lru = dict()
    for i in range(df.SETS):
        cache[i] = dict()
        lru[i] = list()
    
    
    miss = 0
    memreq = len(trace)
    iter = 0

    print "Simulating Least Recently Used replacement policy..."
    for addr in trace:
        offset = extract(addr,"OFFSET")
        index = extract(addr,"INDEX")
        tag = extract(addr,"TAG")
        
        #print "a:",hex(addr),"t:",hex(tag),"i:",hex(index),"o:",hex(offset)
        #print "t:",hex(tag),"i:",hex(index),"o:",hex(offset)
        #print "t:",tag,"i:",index,"o:",offset,
        
        set = cache[index]
        lset = lru[index]
        
        if tag not in set:
            miss=miss+1
            if len(set) < df.A:
                set[tag]=0
                lset.insert(0,tag)
            else:
                LRUtag = lset[-1]
                del lset[-1]
                set.pop(LRUtag)
                lset.insert(0,tag)
                set[tag]=0
            
        else:
            pos = find(lset,tag)
            del lset[pos]
            lset.insert(0,tag)
            set[tag]=0

    print "Gathering statistics..."
    print "Misses: ", miss
    print "Memory Requests: ",memreq
    print "Miss Percentage: ",(float(miss)/memreq)*100,"%"

def update(set):
    for tag in set:
        set[tag] = sadd(set[tag])
  
def policy_RANDOM(trace):
    
    cache = dict()
    for i in range(df.SETS):
        cache[i] = dict()
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
            if len(set) < df.A:
                set[tag] = 0
            else:                
                LRUtag = random.sample(set,2)[0]                
                set.pop(LRUtag)
                set[tag] = 0
        else:
            set[tag] = 0
    
    print "Gathering statistics..."
    print "Misses: ", miss
    print "Memory Requests: ",memreq
    print "Miss Percentage: ",(float(miss)/memreq)*100,"%"
   
def insertAt(path):
    pos = 0
    step = df.A/2
    index = step - 1
    levels = int(math.log(df.A,2))

    for i in range(levels):
        bit = (path & (1<<index)) >> index
        path = path ^ (1 << index)
        
        pos = bit * step + pos
        step = step >> 1
        index = (index + step) if bit == 1 else (index - step)
        
    return pos

def policy_PLRU(trace):
    cache = dict()
    lru = list()
    
    for i in range(df.SETS):
        cache[i] = [0 for i in range(df.A)]
        lru[i] = 0
    
    miss = 0
    memreq = len(trace)
    iter = 0
    
    print "Simulating pseudo LRU replacement policy..."
    for addr in trace:
        offset = extract(addr,"OFFSET")
        index = extract(addr,"INDEX")
        tag = extract(addr,"TAG")
        
        set = cache[index]
        path = plru[index]
        
        if tag not in set:
            miss = miss + 1
            pos = insertAt(path)
            set[pos] = tag
    
    print "Gathering statistics..."
    print "Misses: ", miss
    print "Memory Requests: ",memreq
    print "Miss Percentage: ",(float(miss)/memreq)*100,"%"        
        
            
        
    