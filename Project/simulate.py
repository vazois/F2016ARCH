from cache_config import parse_cache_cfg, get_cache_args, model_cache, get_cache_cfg
from ram_config import parse_ram_cfg, get_ram_args, model_ram, get_ram_cfg
from cacti import compile, clean

from data_access_sim import set_cache_cfg, print_cache_cfg
from data_access_sim import set_ram_cfg, print_ram_cfg
from data_access_sim import set_policy, simulate_trace

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
parse_cache_cfg()
model_cache(get_cache_args())

#model and parse ram properties
parse_ram_cfg()
model_ram(get_ram_args())

set_cache_cfg(get_cache_cfg("C"),get_cache_cfg("B"),get_cache_cfg("A"),get_cache_cfg("AT"),get_cache_cfg("RT"))
set_ram_cfg(get_ram_cfg("C"),get_ram_cfg("B"),get_ram_cfg("BNKS"),get_ram_cfg("DW"),get_ram_cfg("AT"),get_ram_cfg("RT"))


simulate_trace(trace_file)

print_cache_cfg()
print_ram_cfg()



