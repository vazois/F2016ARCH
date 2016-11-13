from cache_config import parse_cache_cfg, get_cache_cfg, model_cache
from ram_config import parse_ram_cfg, get_ram_cfg, model_ram
from cacti import compile, clean


compile()
parse_cache_cfg()
model_cache(get_cache_cfg())

parse_ram_cfg()
model_ram(get_ram_cfg())
