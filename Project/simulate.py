import math
import os.path

from cache_policy_sim import policy_LRU, policy_RANDOM, policy_PLRU
import definitions as df

mem_org = list()
mem_str = list()

def add_mem_str(strategy):
    global mem_str
    mem_str.append(strategy)
    
def add_mem(mem):
    global mem_org
    mem_org.append(mem)

def set_policy(policy):
    global LRU,RANDOM
    global ACTIVE_POLICY
    
    if policy == df.LRU:
        df.ACTIVE_POLICY = policy
    elif policy == df.RANDOM:
        df.ACTIVE_POLICY = policy
    elif policy == df.PLRU:
        df.ACTIVE_POLICY = policy
    else:
        print "Chosen policy (",policy,") not supported!!!"
        print "Supported Replacement Policies..."
        print "LRU = Least Recently Used"
        print "RR = Random Replacement"
        print "PLRU = Pseudo LRU"
        exit(1)

def mask(bits):
    return (1 << bits) - 1

def parse_trace(filename):
    global ADDR_WIDTH
    if not os.path.isfile(filename):
        print "ERROR: trace file (",filename,") does not exist!!!"
        exit(1)
    
    print "Parsing trace file..."
    fp = open(filename,'r')
    trace=list()
    lines = fp.readlines()
    for line in lines:
        data = line.strip().split(" ")
        addr = int(data[1],16) & 0xFFFFFFFF
        trace.append(addr)
        #print hex(addr)
        #break
    fp.close()
    return trace

def simulate_trace(filename):
    global mem_org    
    trace = parse_trace(filename)

    if df.ACTIVE_POLICY == df.LRU:
        sim = policy_LRU(trace,mem_org)
    elif df.ACTIVE_POLICY == df.RANDOM:
        sim = policy_RANDOM(trace,mem_org)
    elif df.ACTIVE_POLICY == df.PLRU:
        sim = policy_PLRU(trace,mem_org)
        

    print "Simulation:",sim[0],sim[1]


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    