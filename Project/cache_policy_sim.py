import random
import math
import policies as p

gmem = 0

def extract(val,flag):
    global gmem
    if flag == "OFFSET":
        return (val & gmem.OFFSET_MASK) >> 0
    elif flag == "INDEX":
        return (val & gmem.INDEX_MASK) >> gmem.OFFSET_BITS
    elif flag == "TAG":
        return (val & gmem.TAG_MASK) >> (gmem.OFFSET_BITS + gmem.INDEX_BITS)

def sadd(v):
    return v if v == (df.A - 1) else v + 1

def find(lset,tag):
    for i in range(len(lset)):
        if lset[i] == tag:
            return i
    return -1
        
def policy_LRU(trace,mem_org):
    global gmem
    gmem = mem_org[0]
    
    cache = dict()
    lru = dict()
    for i in range(gmem.SETS):
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
        
        set = cache[index]
        lset = lru[index]
        if tag not in set:
            miss=miss+1
            if len(set) < gmem.A:
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
    
    return [miss,memreq]

def update(set):
    for tag in set:
        set[tag] = sadd(set[tag])
  
def policy_RANDOM(trace,mem_org):
    global gmem
    gmem = mem_org[0]
    
    cache = dict()
    for i in range(gmem.SETS):
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
            if len(set) < gmem.A:
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
    return [miss,memreq]
    
   
def insertAt(path):
    pos = 0
    step = gmem.A/2
    index = step - 1
    levels = int(math.log(gmem.A,2))

    for i in range(levels):
        bit = (path & (1<<index)) >> index
        path = path ^ (1 << index)
        
        pos = bit * step + pos
        step = step >> 1
        index = (index + step) if bit == 1 else (index - step)
        
    return [pos,path]

def policy_PLRU(trace,mem_org):
    global gmem
    gmem = mem_org[0]
    
    cache = dict()
    #test = dict()
    lru=dict()
    for i in range(gmem.SETS):
        cache[i] = [0 for j in range(gmem.A)]
        #test[i] = dict()
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
        path = lru[index]
        
        if tag not in set:
            #if tag in test[index]:
            #    print set,tag,index
            miss = miss + 1
            ret = insertAt(path)
            set[ret[0]] = tag
            lru[index] = ret[1]
            #if tag in test[index]:
            #    print set,tag,index,ret[0]
            #    raw_input("Press to continue...")
                
        #test[index][tag]=0
    
    print "Gathering statistics..."
    print "Misses: ", miss
    print "Memory Requests: ",memreq
    print "Miss Percentage: ",(float(miss)/memreq)*100,"%"        
    
    return [miss,memreq]    


def fetch(memory,memorg,addr):
    gmem = memorg        
    offset = extract(addr,"OFFSET")
    index = extract(addr,"INDEX")
    tag = extract(addr,"TAG")
    
    if len(set) < gmem.A:
        #if len(set) < gmem
        if memorg.repl_policy == p.LRU:
            memory[0][index][tag] = 0
            memory[1][index].insert(0,tag)
        elif memorg.repl_policy == p.PLRU:
            path = memory[1][index]
            ret = insertAt(path)
            memory[0][index][ret[0]] = tag
            memory[1][index] = ret[1]
        elif memorg.repl_policy == p.RANDOM:
            memory[0][index][tag] = 0
    else:
        evictTag=0
        if memorg.repl_policy == p.LRU:                    
            evictTag = memory[1][index][-1]
            del memory[1][index][-1]
            memory[1][index].insert(0,tag)
            memory[0][index].pop(evictTag)
            memory[0][index][tag]=0
        elif memorg.repl_policy == p.PLRU:                    
            ret = insertAt(memory[1][index])
            evictTag = memory[0][index][ret[0]]
            memory[0][index][ret[0]] = tag
            memory[1][index] = ret[1]
        elif memorg.repl_policy == p.RANDOM:
            evictTag = random.sample(set,2)[0]                
            memory[0][index].pop(evictTag)
            memory[0][index][tag] = 0
            

def policy_multi_level(trace,mem_org):
    global gmem
    
    memory = list()
    print "Building Memory Hierarchy..."
    for i in range(len(mem_org) - 1):
        if mem_org[i].repl_policy == p.LRU:
            print "Initializing",mem_org[i].cache_name,"cache with LRU replacement policy..."
            memory.append([dict(),dict()])
            for j in range(mem_org[i].SETS):
                memory[i][0][j] = dict()
                memory[i][1][j] = list()
        elif mem_org[i].repl_policy == p.PLRU:
            print "Initializing",mem_org[i].cache_name,"cache with PLRU replacement policy..."
            memory.append([dict(),dict()])
            for j in range(mem_org[i].SETS):
                memory[i][0][j] = [0 for k in range(mem_org[i].A)]
                memory[i][1][j] = 0
        elif mem_org[i].repl_policy == p.RANDOM:
            print "Initializing",mem_org[i].cache_name,"cache with RANDOM replacement policy..."
            memory.append([dict()])
            for j in range(mem_org[i].SETS):
                memory[i][0][j] = dict()
    
    
    miss = 0
    memreq = len(trace)
    iter = 0
    hit = False
    print "Simulating multi level hierarchy..."
    #gmem = mem_org[0]
    
    for addr in trace:
        hit = False
        hit_level = len(mem_org)-2
        set = 0
        for i in range(len(mem_org)-1):
            gmem = mem_org[i]        
            offset = extract(addr,"OFFSET")
            index = extract(addr,"INDEX")
            tag = extract(addr,"TAG")
            
            set = memory[i][0][index]
            if tag in set:
                hit = True
                hit_level = i
                break
            
        
        for i in range(hit_level,-1,-1):
            gmem = mem_org[i]        
            offset = extract(addr,"OFFSET")
            index = extract(addr,"INDEX")
            tag = extract(addr,"TAG")
            
            if len(set) < gmem.A:
                #if len(set) < gmem
                if mem_org[i].repl_policy == p.LRU:
                    memory[i][0][index][tag] = 0
                    memory[i][1][index].insert(0,tag)
                elif mem_org[i].repl_policy == p.PLRU:
                    path = memory[i][1][index]
                    ret = insertAt(path)
                    memory[i][0][index][ret[0]] = tag
                    memory[i][1][index] = ret[1]
                elif mem_org[i].repl_policy == p.RANDOM:
                    memory[i][0][index][tag] = 0
            else:
                evictTag=0
                if mem_org[i].repl_policy == p.LRU:                    
                    evictTag = memory[i][1][index][-1]
                    del memory[i][1][index][-1]
                    memory[i][1][index].insert(0,tag)
                    memory[i][0][index].pop(evictTag)
                    memory[i][0][index][tag]=0
                elif mem_org[i].repl_policy == p.PLRU:                    
                    ret = insertAt(memory[i][1][index])
                    evictTag = memory[i][0][index][ret[0]]
                    memory[i][0][index][ret[0]] = tag
                    memory[i][1][index] = ret[1]
                elif mem_org[i].repl_policy == p.RANDOM:
                    evictTag = random.sample(set,2)[0]                
                    memory[i][0][index].pop(evictTag)
                    memory[i][0][index][tag] = 0
                
                #if i < len(mem_org)-2:
                    #evictAddr = (evictTag) &
                #    return [22,11]
                    
                #print "t:",hex(tag),"i:",hex(index),"o:",hex(offset)
                #print "t:",hex(evictTag),"i:",hex(index)
                
                #return [22,11]
                
    return [22,11]
    
    
         
        
    