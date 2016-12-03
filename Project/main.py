from cacti import compile, clean
from simulate import simulate_trace, add_mem

import sys
from cache import Cache
from ram import RAM

argc = len(sys.argv)
if argc < 4:
    print "Expecting trace file for simulation, example number(i.e. 1,2,3 memory levels) and (s)hort or (f)ull specs!!!"
    exit(1)
    
trace_file = sys.argv[1]
example = int(sys.argv[2])
specs = sys.argv[3]
p = False if specs == "s" else True

    
    
compile()

L1 = None
L2 = None
L3 = None
DDR = None
if example >=1:
    L1 = Cache("L1.cfg","L1")
    L1.model()
    add_mem(L1)
    if p:
        L1.print_cfg()

if example >=2:
    L2 = Cache("L2.cfg","L2")
    L2.model()
    add_mem(L2)
    if p:
        L2.print_cfg()

if example >=3:
    L3 = Cache("L3.cfg","L3")
    L3.model()
    add_mem(L3)
    if p:
        L3.print_cfg()


DDR = RAM("ram.cfg","DDR3")
DDR.model()
#DDR.print_cfg()
add_mem(DDR)

print "----------------------------------"
simulate_trace(trace_file)


