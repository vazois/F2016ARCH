import math
from fileIO import exists

CSIZE = 64*1024#64*1024 Bytes Data Size
BSIZE = 16# 32 Bytes Block Size
WAYS = 8 # Associativity
SETS = CSIZE/(WAYS*BSIZE)
TCSIZE = 0
filename = ""

def mask(bits):
    return (1 << bits) - 1

def extract(val,mask,shf):
    return (val & mask) >> shf

#################################
#                                #
#     PARSE ARGUMENTS            #
#                                #
#################################

def info():
    global CSIZE, BSIZE, WAYS, SETS, filename
    global OFFSET_BITS, INDEX_BITS, TAG_BITS
    global OFFSET_MASK, INDEX_MASK, TAG_MASK
    print "Simulating ",WAYS,"- way associative cache with block size ", BSIZE, " bytes and data size ", CSIZE, " bytes on trace <", filename ,">"
    print "TAG, INDEX, OFFSET: (", TAG_BITS,",", INDEX_BITS,",", OFFSET_BITS,")"
    print "TAG_MASK, INDEX_MASK, OFFSET_MASK: (", hex(TAG_MASK),",",hex(INDEX_MASK),",", hex(OFFSET_MASK),")"
    print "Sets: ", SETS
    print "Tag Space: ",int(TCSIZE),"bytes"
    
    
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
    exists(filename)

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
    if sys.argv[4] == 'N':
        WAYS = int(CSIZE/BSIZE)
    else:
        WAYS = int(sys.argv[4])
    initConfig()