from cacti import compile, clean

from cache_cfg_parse import model_cache, init_cache
from ram_cfg_parse import model_ram, init_ram

from simulate import setup_cache, print_cache_cfg
from simulate import print_ram_cfg
from simulate import set_policy, simulate_trace

import sys

argc = len(sys.argv)
if argc < 3:
    print "Expecting trace file and replacement policy for simulation!!!"
    exit(1)
    
trace_file = sys.argv[1]
policy = sys.argv[2]
set_policy(policy)

#compile cacti if necessary
compile()
#model and parse cache properties
model_cache()
init_cache()
setup_cache()
#model and parse ram properties
model_ram()
init_ram()

simulate_trace(trace_file)

print_cache_cfg()
print_ram_cfg()


import definitions as df
import math

def toggle(v,b):
    return v ^ (1 << b)

def insertAt(path):
    pos = 0
    step = df.A/2
    index = step - 1
    levels = int(math.log(df.A,2))
    #print levels
    
    #print "df.A:",df.A,"path:",path
    for i in range(levels):
        #print "step:",step,"pos:",pos,"bit:",bit,"index:",index
        bit = (path & (1<<index)) >> index
        path = path ^ (1 << index)#toggle(path,index)
        #print "step:",step,"pos:",pos,"bit:",bit,"index:",index
        
        pos = bit * step + pos
        step = step >> 1
        index = (index + step) if bit == 1 else (index - step)
        #index = index + bit*step - toggle(bit,0)*step
        #print path,pos,bit,npos,step
    #print "path:",path,"pos:",pos,#"pbin:",int("0",2)
    
    #6 5 4 3 2 1 0
    #0001011  11 0
    #0110011  51 4
    #0111101  61 2
    #1010101  85 1
    #1011110  94 5
    #1100110 102 3
    #1101000 104 7
    #0000000 0
    
path = int(sys.argv[3])
insertAt(path)
print path

