import math
import os.path

from cache_policy_sim import policy_LRU, policy_RANDOM
import definitions as df

def mask(bits):
    return (1 << bits) - 1

def setup_cache():
    df.OFFSET_BITS = int(math.log(df.B,2))
    df.SETS = int(df.C/(df.B * df.A))
    df.INDEX_BITS = int(math.log(df.SETS,2))
    df.TAG_BITS = df.ADDR_WIDTH - df.INDEX_BITS - df.OFFSET_BITS
    
    df.OFFSET_MASK = mask(df.OFFSET_BITS)
    df.INDEX_MASK = mask(df.INDEX_BITS) << df.OFFSET_BITS
    df.TAG_MASK = mask(df.TAG_BITS) << (df.OFFSET_BITS + df.INDEX_BITS)

def set_ram_cfg():    
    df.C_RAM = int(CSIZE)
    df.B_RAM = int(BSIZE)
    df.BNKS_RAM =int(BANKS)
    df.DW_RAM = int(DWIDTH)
    
    df.AT_RAM = ATIME
    df.RT_RAM = RTIME
    
    
def print_ram_cfg():
    global C_RAM,B_RAM,BNKS_RAM, DW_RAM
    global AT_RAM,RT_RAM
    
    print "__________________________________"
    print "<<<<<    RAM   PROPERTIES    >>>>>"
    print "RAM Capacity :",df.C_RAM, "bytes"
    print "RAM Block size :", df.B_RAM, "bytes"
    print "RAM Data bus width :", df.DW_RAM, "bits"
    print "RAM Access time :",df.AT_RAM,"(ns)"
    print "RAM Random cycle time :",df.RT_RAM,"(ns)"
    
def print_cache_cfg():    
    print "__________________________________"
    print "<<<<<    CACHE PROPERTIES    >>>>>"
    print "Cache properties : ",df.C," byte ", df.A ,"- way associative cache with ", df.B, " byte line"
    print "(Tag,Index,Offset) : (", df.TAG_BITS,",",df.INDEX_BITS,",",df.OFFSET_BITS,")"
    print "(Tag Mask,Index Mask,Offset Mask) : (",hex(df.TAG_MASK),",",hex(df.INDEX_MASK),",",hex(df.OFFSET_MASK),")"
    print "Sets :",df.SETS
    print "Cache Access time :",df.AT_CACHE,"(ns)"
    print "Cache Random cycle time :",df.RT_CACHE,"(ns)"
    #print "__________________________________"
    #print "<<<<<<<<<<<<<<<<->>>>>>>>>>>>>>>>>"  

def set_policy(policy):
    global LRU,RANDOM
    global ACTIVE_POLICY
    
    if policy == df.LRU:
        df.ACTIVE_POLICY = policy
    elif policy == df.RANDOM:
        df.ACTIVE_POLICY = policy
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
    
    df.ADDR_MASK = mask(df.ADDR_WIDTH)
    for line in lines:
        data = line.strip().split(" ")
        addr = int(data[2],16) & df.ADDR_MASK
        trace.append(addr)
        #print hex(addr)
        #break
    fp.close()
    return trace

from cache_policy_sim import test_cache

def simulate_trace(filename):
    global LRU,RANDOM
    global ACTIVE_POLICY
    
    global OFFSET_BITS, INDEX_BITS, TAG_BITS
    global OFFSET_MASK, INDEX_MASK, TAG_MASK
    global A,SETS
    
    
    trace = parse_trace(filename)
    #set_cfg(OFFSET_BITS, INDEX_BITS, TAG_BITS, OFFSET_MASK, INDEX_MASK, TAG_MASK, A, SETS)
    
    test_cache()
    #return
    
    if df.ACTIVE_POLICY == df.LRU:
        policy_LRU(trace)
    elif df.ACTIVE_POLICY == df.RANDOM:
        policy_RANDOM(trace)
        




    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    