import sys
import os.path
import math


def mask(bits):
    return (1 << bits) - 1

CSIZE = 64*1024#64*1024 Bytes Data Size
BSIZE = 32# 32 Bytes Block Size
WAYS = 2 # Associativity
SETS = CSIZE/(WAYS*BSIZE)
TCSIZE = 0
filename = ""

#################################
#                                #
#     PARSE ARGUMENTS            #
#                                #
#################################

def sadd(v):
    global WAYS
    return v if v == (WAYS - 1) else v + 1 
    #return v+1
    
def extract(val,mask,shf):
    return (val & mask) >> shf
    
def info():
    global CSIZE, BSIZE, WAYS, SETS, filename
    global OFFSET_BITS, INDEX_BITS, TAG_BITS
    global OFFSET_MASK, INDEX_MASK, TAG_MASK
    print "Simulating ",WAYS,"- way associative cache with block size ", BSIZE, " bytes and data size ", CSIZE, " bytes on trace <", filename ,">"
    print "Additional space for tag in bytes: ",int(TCSIZE)
    print "# of Sets: ", SETS
    print "(TAG_BITS,INDEX_BITS,OFFSET_BITS): (", TAG_BITS,",",INDEX_BITS,",",OFFSET_BITS,")"
    print "(TAG_MASK,INDEX_MASK,OFFSET_MASK): (",hex(TAG_MASK),",",hex(INDEX_MASK),",",hex(OFFSET_MASK),")"
    
def initConfig():
    global CSIZE, BSIZE, WAYS, SETS,TCSIZE, filename
    global OFFSET_BITS, INDEX_BITS, TAG_BITS
    global OFFSET_MASK, INDEX_MASK, TAG_MASK
    
    SETS = CSIZE/(BSIZE*WAYS)
    OFFSET_BITS = int(math.log(BSIZE,2))
    OFFSET_MASK = mask(OFFSET_BITS)
    INDEX_BITS = int(math.log(SETS,2))
    INDEX_MASK = mask(INDEX_BITS) << OFFSET_BITS
    TAG_BITS = 32 - OFFSET_BITS - INDEX_BITS
    TAG_MASK = mask(TAG_BITS) << (OFFSET_BITS + INDEX_BITS)
    TCSIZE = math.ceil(float(SETS * WAYS * TAG_BITS)/8) 
     
    
def argParser(sys):
    global CSIZE, BSIZE, WAYS, filename
    argc = len(sys.argv)
    
    if argc < 2:
        print "Expecting at least 1 argument<>, 3 more are optional{}: <filename> {cache size} {block size} {ways}"
        exit(1)

    filename = sys.argv[1]
    if not os.path.isfile(filename):
        print "File <", filename, "> does not exist"
        exit(1)

    if argc == 2:
        print "Running on default configuration"
        initConfig()
        return

    if argc < 5:
        print "Expecting additional arguments: {cache size} {block size} {ways}"
        exit(1)
        
    
    arg = sys.argv[2]
    if arg.find('K') > 0:
        CSIZE = 1024 * int(arg.split('K')[0])
    elif arg.find('M') > 0:
        CSIZE = 1024 * 1024 * int(arg.split('M')[0])
    else:
        CSIZE = int(arg)
    
    BSIZE = int(sys.argv[3])
    if int(sys.argv[4]) == 0:
        WAYS = int(CSIZE/BSIZE)
    else:
        WAYS = int(sys.argv[4])
    initConfig()
    
def processTraceFile(file):
    global trace
    fp = open(file,'r')
    trace=list()
    
    print "Parsing File..."
    lines = fp.readlines()
    for line in lines:
        data = line.strip().split(' ')
        op = data[0]
        offset = int(data[1])
        addr = int(data[2],16) & 0xFFFFFFFF
        trace.append((op,offset,addr))
    fp.close()
    print "Parsing Finished..."
    
    return trace

def updateCounters(set):
    for block in set:
        set[block] = sadd(set[block])
        
def findLRU(set):
    LRUtag=0
    max = 0
    for tag in set:
        if set[tag] > max:
            LRUtag = tag
            max = set[tag]
    
    return LRUtag
    
    
def sim_LRU_cache(trace):
    global CSIZE, BSIZE, WAYS, SETS, filename
    global OFFSET_BITS, INDEX_BITS, TAG_BITS
    global OFFSET_MASK, INDEX_MASK, TAG_MASK
    
    print "Simulating cache access using LRU replacement policy...."
    
    #Init Virtual Cache
    cache = dict()
    LRU_item = dict()
    for i in range(SETS):
        cache[i] = dict()
        LRU_item[i] = dict()
        #for j in range(WAYS):
        #    cache[i][j] = (0,0,0)#(tag,valid,counter)
        #    cache[i][j] = (0,0)#(tag,counter)
        #    cache[i][j] = 0#(counter)
    
    
    #print cache
    #Simulate
    miss = 0
    memreq = len(trace)
    iter = 0
    for req in trace:
        addr = req[2]
        offset = extract(addr,OFFSET_MASK,0)
        index = extract(addr,INDEX_MASK,OFFSET_BITS)
        tag = extract(addr,TAG_MASK,INDEX_BITS+OFFSET_BITS)
        
        print "a:",hex(addr),"t:",tag,"i:",hex(index),"o:",hex(offset)
        #print "t:",hex(tag),"i:",hex(index),"o:",hex(offset)
        #print "t:",tag,"i:",index,"o:",offset,
        
        set = cache[index]
        if tag not in set: # MISS IF tag not in set
            miss = miss + 1
            if len(set) < WAYS:# IF THERE IS SPACE INSERT BLOCK
                #print "(miss)(insert)"
                updateCounters(set)
                set[tag] = 0
            else:#ELSE FIND BLOCK TO EVICT
                #print "(miss)(evict)",LRUtag
                LRUtag = max(set,key=set.get)
                #LRUtag = findLRU(set)
                set.pop(LRUtag)
                updateCounters(set)
                set[tag] = 0
        else:#IF TAG IN SET UPDATE COUNTERS
            updateCounters(set)
            set[tag] = 0
        
        #raw_input("Press Enter to continue...")
        #if iter % 100000 == 0:
        #    print iter
        iter = iter + 1
        #if iter > 10:
        break
        
    print "Simulation finished, gathering statistics..."
    
    print "Misses: ", miss
    print "Memory Requests: ",memreq
    print "Miss Percentage: ",(float(miss)/memreq)*100,"%"
    #print "Locality of Reference: ", max(pattern,key=pattern.get)
    #print pattern


argParser(sys)
info()
trace = processTraceFile(filename)
sim_LRU_cache(trace)

