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

def concat(tag,index):
    global gmem
    return (tag << (gmem.OFFSET_BITS + gmem.INDEX_BITS)) | (index << gmem.OFFSET_BITS)

def find(lset,tag):
    for i in range(len(lset)):
        if lset[i] == tag:
            return i
    return -1

def fetch(memory,memorg,addr,hit):
    global gmem
    gmem = memorg        
    offset = extract(addr,"OFFSET")
    index = extract(addr,"INDEX")
    tag = extract(addr,"TAG")
    evictTag=-1
    #print "t:",hex(tag),"i:",hex(index),"o:",hex(offset)
    #print memory[0][index]
    if hit:
        if memorg.repl_policy == p.LRU:
            pos = find(memory[1][index],tag)# find tag position
            del memory[1][index][pos]#delete tag
            memory[1][index].insert(0,tag)#insert it at the beginning
            memory[0][index][tag]=0#insert it in the dictionary # not necessary
        elif memorg.repl_policy == p.PLRU:
            return -1
        elif memorg.repl_policy == p.RANDOM:
            memory[0][index][tag] = 0
    elif len(memory[0][index]) < gmem.A:
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
            evictTag = random.sample(memory[0][index],2)[0]
            #some_dict.pop( random.choice(some_dict.keys()) )                  
            memory[0][index].pop(evictTag)
            memory[0][index][tag] = 0
            
    return evictTag
        
def policy_LRU(trace,mem_org):
    global gmem
    gmem = mem_org[0]
    
    cache = dict()
    lru = dict()
    for i in range(gmem.SETS):
        cache[i] = dict()
        lru[i] = list()
    
    pair = [cache,lru]
    memreq = len(trace)
    iter = 0

    print "Simulating Least Recently Used replacement policy..."
    for addr in trace:
        offset = extract(addr,"OFFSET")
        index = extract(addr,"INDEX")
        tag = extract(addr,"TAG")
        
        set = cache[index]
        lset = lru[index]
        #fetch(pair,mem_org[0],addr,hit)
        
        if tag not in set:
            #mem_org[0].miss=mem_org[0].miss+1
            #fetch(pair,mem_org[0],addr,False)
            #continue
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
            #mem_org[0].hit = mem_org[0].hit + 1
            #fetch(pair,mem_org[0],addr,True)
            #continue
            pos = find(lset,tag)
            del lset[pos]
            lset.insert(0,tag)
            set[tag]=0
        
    print "Gathering statistics..."
    print "Misses: ", mem_org[0].miss
    print "Memory Requests: ",memreq
    print "Miss Percentage: ",(float(mem_org[0].miss)/memreq)*100,"%"
    
    return [mem_org[0].miss,memreq]
  
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
      
def policy_multi_level(trace,mem_org):
    global gmem
    
    print "Number of Memory Levels:",len(mem_org)
    memory = list()
    offset = mem_org[0].OFFSET_BITS
    print "Building Memory Hierarchy..."
    for i in range(len(mem_org) - 1):
        if offset != mem_org[i].OFFSET_BITS:
            print "Error: Block Size not equal across the cache hierarchy!!!(",mem_org[i].name,")"
            exit(1)
            
        if mem_org[i].repl_policy == p.LRU:
            print "Initializing",mem_org[i].name,"cache with LRU replacement policy..."
            memory.append([dict(),dict()])
            for j in range(mem_org[i].SETS):
                memory[i][0][j] = dict()#dictionary of tags for Set
                memory[i][1][j] = list()#list to organize LRU tags
        elif mem_org[i].repl_policy == p.PLRU:
            print "Initializing",mem_org[i].name,"cache with PLRU replacement policy..."
            memory.append([dict(),dict()])
            for j in range(mem_org[i].SETS):
                memory[i][0][j] = [0 for k in range(mem_org[i].A)]#list of tags
                memory[i][1][j] = 0#path for given set
        elif mem_org[i].repl_policy == p.RANDOM:
            print "Initializing",mem_org[i].name,"cache with RANDOM replacement policy..."
            memory.append([dict()])
            for j in range(mem_org[i].SETS):
                memory[i][0][j] = dict()# dictionary of tags
    
    
    miss = 0
    memreq = len(trace)
    iter = 0
    hit = False
    print "Simulating multi level hierarchy..."
    #gmem = mem_org[0]
    
    for addr in trace:
        hit = False
        hit_level = len(mem_org)-2
        for i in range(len(mem_org)-1):#Search for data across the memory hierarchy
            gmem = mem_org[i]        
            offset = extract(addr,"OFFSET")
            index = extract(addr,"INDEX")
            tag = extract(addr,"TAG")
            
            #set = memory[i][0][index]
            if tag in memory[i][0][index]:
                hit = True
                hit_level = i
                mem_org[i].hit = mem_org[i].hit + 1
                break
            else:
                mem_org[i].miss = mem_org[i].miss + 1
        
        if not hit:#Look in RAM if not find in caches
            mem_org[-1].hit = mem_org[-1].hit + 1
        
        #print "level:",hit_level
        #break
        if hit_level == 0 and hit:#Just read the data if it is at the highest level
            fetch(memory[0],mem_org[0],addr,True)
            continue
            
            
        for i in range(hit_level,-1,-1):
            #memorg = mem_org[i]
            #memory_level = system[i]
            evictTag=fetch(memory[i],mem_org[i],addr,hit)
            hit=False
            gmem = mem_org[i]
            offset = extract(addr,"OFFSET")
            index = extract(addr,"INDEX")
            tag = extract(addr,"TAG")
            #print "line:",i,memory[i][0][index],"a:",hex(addr),"t:", hex(tag),"h:", hex(index),"i:",iter
            j = i+1
            while evictTag != -1 and (j < len(mem_org)-2):
            #if evictTag != -1 and (i < len(mem_org)-2):
                evictAddr = concat(tag,index)
                evictTag = fetch(memory[j],mem_org[j],evictAddr,hit)
                j = j + 1
                
        iter = iter + 1
    for i in range(len(mem_org)):
        print mem_org[i].name,":",
        print "\t( hit:",mem_org[i].hit,", miss:",mem_org[i].miss,")"        
    return [22,11]
    
    
         
        
    