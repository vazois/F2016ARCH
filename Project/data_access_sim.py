import math
import os.path

from cache_policy_sim import set_cfg, policy_LRU, policy_RANDOM

C = 0
B = 0
A = 0
SETS = 0

ADDR_WIDTH = 32

OFFSET_MASK = 0
INDEX_MASK = 0
TAG_MASK = 0

OFFSET_BITS = 0
INDEX_BITS = 0
TAG_BITS = 0

OFFSET = "OFFSET"
INDEX = "INDEX"
TAG = "TAG"

AT = 0
RT = 0

def mask(bits):
    return (1 << bits) - 1

def sadd(v):
    global A
    return v if v == (A - 1) else v + 1 


def set_cache_cfg_no_time(CSIZE,BSIZE,ASSOC):
    set_cache_cfg(CSIZE,BSIZE,ASSOC,1,1)

def set_cache_cfg(CSIZE,BSIZE,ASSOC,ATIME,RTIME):
    global C,B,A
    global OFFSET_BITS, INDEX_BITS, TAG_BITS
    global OFFSET_MASK, INDEX_MASK, TAG_MASK
    global SETS
    global AT,RT
    
    AT = ATIME
    RT = RTIME
    
    C=int(CSIZE)
    B=int(BSIZE)
    A=int(ASSOC)
    
    OFFSET_BITS = int(math.log(B,2))
    SETS = int(CSIZE/(BSIZE * A))
    INDEX_BITS = int(math.log(SETS,2))
    TAG_BITS = ADDR_WIDTH - INDEX_BITS - OFFSET_BITS
    
    OFFSET_MASK = mask(OFFSET_BITS)
    INDEX_MASK = mask(INDEX_BITS) << OFFSET_BITS
    TAG_MASK = mask(TAG_BITS) << (OFFSET_BITS + INDEX_BITS)
    
C_RAM = 0
B_RAM = 0
BNKS_RAM = 0
DW_RAM = 0
AT_RAM = 0
RT_RAM = 0

def set_ram_cfg(CSIZE,BSIZE,BANKS,DWIDTH,ATIME,RTIME):
    global C_RAM,B_RAM,BNKS_RAM, DW_RAM
    global AT_RAM,RT_RAM
    
    C_RAM = int(CSIZE)
    B_RAM = int(BSIZE)
    BNKS_RAM =int(BANKS)
    DW_RAM = int(DWIDTH)
    
    AT_RAM = ATIME
    RT_RAM = RTIME
    
    
def print_ram_cfg():
    global C_RAM,B_RAM,BNKS_RAM, DW_RAM
    global AT_RAM,RT_RAM
    
    print "__________________________________"
    print "<<<<<    RAM   PROPERTIES    >>>>>"
    print "RAM Capacity :",C_RAM, "bytes"
    print "RAM Block size :", B_RAM, "bytes"
    print "RAM Data bus width :", DW_RAM, "bits"
    print "RAM Access time :",AT_RAM,"(ns)"
    print "RAM Random cycle time :",RT_RAM,"(ns)"
    
def print_cache_cfg():
    global C,B,A
    global OFFSET_BITS, INDEX_BITS, TAG_BITS
    global OFFSET_MASK, INDEX_MASK, TAG_MASK
    global SETS
    global AT,RT
    
    print "__________________________________"
    print "<<<<<    CACHE PROPERTIES    >>>>>"
    print "Cache properties : ",C," byte ", A ,"- way associative cache with ", B, " byte line"
    print "(Tag,Index,Offset) : (", TAG_BITS,",",INDEX_BITS,",",OFFSET_BITS,")"
    print "(Tag Mask,Index Mask,Offset Mask) : (",hex(TAG_MASK),",",hex(INDEX_MASK),",",hex(OFFSET_MASK),")"
    print "Sets :",SETS
    print "Cache Access time :",AT,"(ns)"
    print "Cache Random cycle time :",RT,"(ns)"
    #print "__________________________________"
    #print "<<<<<<<<<<<<<<<<->>>>>>>>>>>>>>>>>"

ACTIVE_POLICY = "LRU"
LRU = "LRU"
RANDOM = "RR"    

def set_policy(policy):
    global LRU,RANDOM
    global ACTIVE_POLICY
    
    if policy == LRU:
        ACTIVE_POLICY = policy
    elif policy == RANDOM:
        ACTIVE_POLICY = policy
    else:
        print "Chosen policy (",policy,") not supported!!!"
        print "Type LRU = Least Recently Used, RR = Random Replacement"
        exit(1)


def parse_trace(filename):
    global ADDR_WIDTH
    if not os.path.isfile(filename):
        print "ERROR: trace file (",filename,") does not exist!!!"
        exit(1)
    
    fp = open(filename,'r')
    trace=list()
    
    lines = fp.readlines()
    
    ADDR_MASK = mask(ADDR_WIDTH)
    for line in lines:
        data = line.strip().split(" ")
        addr = int(data[2],16) & ADDR_MASK
        trace.append(addr)
        #print hex(addr)
        #break
    fp.close()
    return trace
        
def simulate_trace(filename):
    global LRU,RANDOM
    global ACTIVE_POLICY
    
    global OFFSET_BITS, INDEX_BITS, TAG_BITS
    global OFFSET_MASK, INDEX_MASK, TAG_MASK
    global A,SETS
    
    
    trace = parse_trace(filename)
    set_cfg(OFFSET_BITS, INDEX_BITS, TAG_BITS, OFFSET_MASK, INDEX_MASK, TAG_MASK, A, SETS)
    
    if ACTIVE_POLICY == LRU:
        policy_LRU(trace)
    elif ACTIVE_POLICY == RANDOM:
        policy_RANDOM(trace)
        




    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    