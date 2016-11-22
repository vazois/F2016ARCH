import math
import os.path

from cache_policy_sim import policy_LRU, policy_RANDOM, policy_PLRU, policy_multi_level
import policies as p

mem_org = list()
def add_mem(mem):
    global mem_org
    mem_org.append(mem)

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
    
    sim = policy_multi_level(trace,mem_org)
    #if len(mem_org) == 2:
    #    if mem_org[0].repl_policy == p.LRU:
    #        sim = policy_LRU(trace,mem_org)
    #    elif mem_org[0].repl_policy == p.RANDOM:
    #        sim = policy_RANDOM(trace,mem_org)
    #    elif mem_org[0].repl_policy == p.PLRU:
    #        sim = policy_PLRU(trace,mem_org)
    #else:
    #    sim = policy_multi_level(trace,mem_org)
        
        
    #print "Simulation:",sim[0],sim[1]


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    