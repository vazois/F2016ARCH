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



