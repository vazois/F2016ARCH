import os
import math
import subprocess
import policies as p
from cacti import getFLD, getExec

CACTI_FLD = getFLD()
CACTI = getExec()

def mask(bits):
    return (1 << bits) - 1

class Cache:
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
    
    LRU = "LRU"
    RANDOM = "RR" 
    PLRU="PLRU"
    
    C = 0
    B = 0
    A = 0
    SETS = 0

    #Addressing
    OFFSET_MASK = 0
    INDEX_MASK = 0
    TAG_MASK = 0

    OFFSET_BITS = 0
    INDEX_BITS = 0
    TAG_BITS = 0

    #Access Time
    AT = 0
    RT = 0

    #Area Properties
    AR = 0
    
    ADDR_WIDTH = 32
    
    cfg_file = ""
    cache_name =""
    arg_list=list()
    repl_policy = ""
    
    def __init__(self,filename,name):
        self.cfg_file = filename
        self.cache_name = name
        self.arg_list = list()
        
        self.C = 0
        self.B = 0
        self.A = 0
        self.SETS = 0
        #Addressing
        self.OFFSET_MASK = 0
        self.INDEX_MASK = 0
        self.TAG_MASK = 0
        self.OFFSET_BITS = 0
        self.INDEX_BITS = 0
        self.TAG_BITS = 0
        #Access Time
        self.AT = 0
        self.RT = 0
        #Area Properties
        self.AR = 0
        
        self.repl_policy = ""
    
    def printFile(self):
        print self.cfg_file,self.cache_name
    
    def init(self):
        self.C=int(self.values_cache["C"])
        self.B=int(self.values_cache["B"])
        self.A=int(self.values_cache["A"])
        self.AT=float(self.values_cache["AT"])
        self.RT=float(self.values_cache["RT"])
        self.AR = float(self.values_cache["AR"])
        self.setup()
    
    def set_ram_addr(self,bits):
        self.ADDR_WIDTH = bits
        
    def read_mdl(self,f,v):
        for i in range(len(f)):
            if f[i].strip() in self.names_cache:
                #print f[i],"=",v[i]
                self.values_cache[self.names_cache[f[i].strip()]] = float(v[i])
    
    def set_policy(self,policy):
        if policy == p.LRU:
            self.repl_policy = policy
        elif policy == p.RANDOM:
            self.repl_policy = policy
        elif policy == p.PLRU:
            self.repl_policy = policy
        else:
            print "Chosen policy (",policy,") not supported!!!"
            print "Supported Replacement Policies..."
            print "LRU = Least Recently Used"
            print "RR = Random Replacement"
            print "PLRU = Pseudo LRU"
            exit(1)
            
    def parse_cfg(self):
        if not os.path.isfile(self.cfg_file):
            print "ERROR: cache.cfg file is missing!!!"
            exit(1)
        
        fp = open(self.cfg_file,'r')
        lines = fp.readlines()
        for line in lines:
            data = line.strip().split("=")
        
            if data[0].strip() is "C":
                if data[1].find('K') > 0:
                    data[1] = str(1024 * int(data[1].split('K')[0]))
                elif data[1].find('M') > 0:
                    data[1] = str(1024 * 1024 * int(data[1].split('M')[0]))
            
            if data[0].strip() == "REPL":
                #self.repl_policy = data[1].strip()
                self.set_policy(data[1].strip())
            else:
                #print data[0],data[1]
                #break
                self.arg_list.append(data[1].strip())
        
        fp.close()
    
    def setup(self):
        self.OFFSET_BITS = int(math.log(self.B,2))
        self.SETS = int(self.C/(self.B * self.A))
        self.INDEX_BITS = int(math.log(self.SETS,2))
        self.TAG_BITS = self.ADDR_WIDTH - self.INDEX_BITS - self.OFFSET_BITS
    
        self.OFFSET_MASK = mask(self.OFFSET_BITS)
        self.INDEX_MASK = mask(self.INDEX_BITS) << self.OFFSET_BITS
        self.TAG_MASK = mask(self.TAG_BITS) << (self.OFFSET_BITS + self.INDEX_BITS)
    
    def print_cfg(self):    
        print "__________________________________"
        print "<<<<<    CACHE PROPERTIES    >>>>>"
        print "<",self.cache_name," cache >"
        print "Cache properties : ",self.C," byte ", self.A ,"- way associative cache with ", self.B, " byte line"
        print "(Tag,Index,Offset) : (", self.TAG_BITS,",",self.INDEX_BITS,",",self.OFFSET_BITS,")"
        print "(Tag Mask,Index Mask,Offset Mask) : (",hex(self.TAG_MASK),",",hex(self.INDEX_MASK),",",hex(self.OFFSET_MASK),")"
        print "Sets :",self.SETS
        print "Cache Access time :",self.AT,"(ns)"
        print "Cache Random cycle time :",self.RT,"(ns)"
        print "Cache Area (mm^2):",self.AR
        #print "__________________________________"
        #print "<<<<<<<<<<<<<<<<->>>>>>>>>>>>>>>>>"  
        
    def model(self):
        self.parse_cfg()
        print "Modeling",self.cache_name,"Cache..."
    
        #cfg = self.arg_list
        self.arg_list.insert(0,CACTI)
        #print len(cfg)
        #try:
        cache = subprocess.Popen(self.arg_list, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
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

        fp = open(self.arg_list[-1],'r')
        lines = fp.readlines()
        f = lines[0].strip().split(",")
        v = lines[1].strip().split(",")
        fp.close()
        
        #for i in range(len(f)):
        #    print f[i],"=",v[i]
    
        self.read_mdl(f,v)
        self.init()
        
        
        
        
        