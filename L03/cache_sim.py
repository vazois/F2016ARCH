import sys
import os.path
import math


def mask(bits):
    return (1 << bits) - 1

CSIZE = 64*1024#1024 Bytes Data Size
BSIZE = 16# 32 Bytes Block Size
WAYS = 2 # Associativity
SETS = CSIZE/(WAYS*BSIZE)
filename = ""

#################################
#                                #
#     PARSE ARGUMENTS            #
#                                #
#################################
def extract(val,mask,shf):
    return (val & mask) >> shf
    
def info():
    global CSIZE, BSIZE, WAYS, SETS, filename
    global OFFSET_BITS, INDEX_BITS, TAG_BITS
    global OFFSET_MASK, INDEX_MASK, TAG_MASK
    print "Simulating ",WAYS,"- way associative cache with block size ", BSIZE, " bytes and total size ", CSIZE, " bytes on trace <", filename ,">"
    print "# of Sets: ", SETS
    print "OFFSET_BITS: ", OFFSET_BITS
    print "INDEX_BITS: ", INDEX_BITS
    print "TAG_BITS: ", TAG_BITS
    print "OFFSET_MASK: ", hex(OFFSET_MASK)
    print "INDEX_MASK: ", hex(INDEX_MASK)
    print "TAG_MASK: ", hex(TAG_MASK)
    
def initConfig():
    global CSIZE, BSIZE, WAYS, SETS, filename
    global OFFSET_BITS, INDEX_BITS, TAG_BITS
    global OFFSET_MASK, INDEX_MASK, TAG_MASK
    
    SETS = CSIZE/(WAYS*BSIZE)
    OFFSET_BITS = int(math.log(BSIZE,2))
    OFFSET_MASK = mask(OFFSET_BITS)
    INDEX_BITS = int(math.log(SETS,2))
    INDEX_MASK = mask(INDEX_BITS) << OFFSET_BITS
    TAG_BITS = 32 - OFFSET_BITS - INDEX_BITS
    TAG_MASK = mask(TAG_BITS) << (OFFSET_BITS + INDEX_BITS)
     
    
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
    

def sim_LRU_cache(trace):
    global CSIZE, BSIZE, WAYS, SETS, filename
    global OFFSET_BITS, INDEX_BITS, TAG_BITS
    global OFFSET_MASK, INDEX_MASK, TAG_MASK
    
    #Init Virtual Cache
    cache = dict()
    for i in range(SETS):
        cache[i] = dict()
        for j in range(WAYS):
            cache[i][j] = (0,0,0)#(tag,valid,counter)
    
    
    #print cache
    #Simulate
    for req in trace:
        print req
        addr = req[2]
        
        offset = extract(addr,OFFSET_MASK,0)
        index = extract(addr,INDEX_MASK,OFFSET_BITS)
        tag = extract(addr,TAG_MASK,INDEX_BITS+OFFSET_BITS)
        
        print hex(addr),hex(tag),hex(index),hex(offset)
        
        break
    
     


argParser(sys)
info()
trace = processTraceFile(filename)
sim_LRU_cache(trace)

