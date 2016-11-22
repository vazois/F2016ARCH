from cacti import compile, clean
from simulate import simulate_trace, add_mem

import sys
from cache import Cache
from ram import RAM

argc = len(sys.argv)
if argc < 2:
    print "Expecting trace file for simulation!!!"
    exit(1)
    
trace_file = sys.argv[1]

compile()
L1 = Cache("L1.cfg","L1")
L1.model()
add_mem(L1)
#L1.print_cfg()

L2 = Cache("L2.cfg","L2")
L2.model()
add_mem(L2)
#L2.print_cfg()


DDR = RAM("ram.cfg","ddr3")
DDR.model()
#DDR.print_cfg()
add_mem(DDR)

simulate_trace(trace_file)


