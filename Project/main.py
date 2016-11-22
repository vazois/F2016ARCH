from cacti import compile, clean
from simulate import set_policy, simulate_trace, add_mem

import sys
from cache import Cache
from ram import RAM

argc = len(sys.argv)
if argc < 3:
    print "Expecting trace file and replacement policy for simulation!!!"
    exit(1)
    
trace_file = sys.argv[1]
policy = sys.argv[2]

L1 = Cache("cache.cfg","L1")
L1.model()
#L1.print_cfg()
add_mem(L1)

DDR = RAM("ram.cfg","ddr3")
DDR.model()
#DDR.print_cfg()
add_mem(DDR)

simulate_trace(trace_file)


