import os.path
import subprocess
from cacti import getFLD, getExec

CACHE_CFG_FILE = "cache.cfg"
CACHE_ARG_LIST = list()

CACTI_FLD = getFLD()
CACTI = getExec()

names_cache=dict()
values_cache=dict()

names_cache["Capacity (bytes)"] = "C"
names_cache["Banks"] = "BNKS"
names_cache["Line size (bytes)"] ="B"
names_cache["Associativity"] = "A"
names_cache["Data width"] = "DW"
names_cache["Access time (ns)"] = "AT"
names_cache["Random cycle time (ns)"] = "RT"

names_cache["Dynamic read power (mW)"] = "RPWR"
names_cache["Stanby leakage per bank(mW)"] = "LBPWR"

names_cache["Area (mm2)"] = "AR"


def get_cache_cfg(name):
    global values_cache
    return values_cache[name]

def read_cache_mdl(f,v):
    global names_cache, values_cache
    for i in range(len(f)):
        if f[i].strip() in names_cache:
            #print f[i],"=",v[i]
            values_cache[names_cache[f[i].strip()]] = float(v[i])
    
    #print values

def model_cache(cfg):
    print "Modeling Cache..."
    
    cfg.insert(0,CACTI)
    #print ' '.join(cfg)
    #try:
    cache = subprocess.Popen(cfg, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    err = False
    if cache.wait() < 0:
        print "Err: Cach cfg not correct!!!"
        exit(1)
        
    for line in iter(cache.stderr.readline,''):
        print "Err:",line.rstrip()
        err = True
    for line in iter(cache.stdout.readline,''):
        print "Err:",line.rstrip()
        err = True

    if err:
        exit(1)

    fp = open(cfg[-1],'r')
    lines = fp.readlines()
    f = lines[0].strip().split(",")
    v = lines[1].strip().split(",")
    
    #for i in range(len(f)):
    #    print f[i],"=",v[i]
    
    read_cache_mdl(f,v)
    
    fp.close()

def parse_cache_cfg():
    global CACHE_ARG_LIST
    
    if not os.path.isfile(CACHE_CFG_FILE):
        print "ERROR: cache.cfg file is missing!!!"
        exit(1)
        
    fp = open(CACHE_CFG_FILE,'r')
    lines = fp.readlines()
    for line in lines:
        data = line.strip().split("=")
        
        if data[0].strip() is "C":
            if data[1].find('K') > 0:
                data[1] = str(1024 * int(data[1].split('K')[0]))
            elif data[1].find('M') > 0:
                data[1] = str(1024 * 1024 * int(data[1].split('M')[0]))
            
        #print data[0],data[1]
        #break
        CACHE_ARG_LIST.append(data[1].strip())
    
    fp.close()

def get_cache_args():
    global CACHE_ARG_LIST
    return CACHE_ARG_LIST
    