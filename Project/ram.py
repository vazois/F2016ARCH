import os
import math
import subprocess
from cacti import getFLD, getExec

CACTI_FLD = getFLD()
CACTI = getExec()

def mask(bits):
    return (1 << bits) - 1

class RAM:
    names_ram=dict()
    values_ram=dict()

    names_ram["Capacity (bytes)"] = "C"
    names_ram["Banks"] = "BNKS"
    names_ram["Line size (bytes)"] ="B"
    names_ram["Associativity"] = "A"
    names_ram["Data width"] = "DW"
    names_ram["Access time (ns)"] = "AT"
    names_ram["Random cycle time (ns)"] = "RT"

    names_ram["Dynamic read power (mW)"] = "RPWR"
    names_ram["Stanby leakage per bank(mW)"] = "LPWR"

    names_ram["Area (mm2)"] = "AR"
    
    #########################
    C = 0
    B = 0
    A = 0
    #Access Time
    AT = 0
    RT = 0
    #Area Properties
    AR = 0
    RPWR = 0
    LPWR = 0
    
    cfg_file = ""
    name =""
    arg_list=list()
    miss = 0
    hit = 0
    type = "ram"
    size = ""
    repl_policy = ""
    policy_name = "-"
    
    timeAT = 0
    timeRT = 0
    
    #########################
    def __init__(self,filename,name):
        self.cfg_file = filename
        self.name = name
        self.arg_list = list()
        self.repl_policy = "-"
        self.policy_name = "-"
        self.miss = 0
        self.hit = 0
        self.RPWR = 0
        
        self.timeAT = 0
        self.timeRT = 0
        
        #########################
        self.C = 0
        self.B = 0
        self.A = 0
        #Access Time
        self.AT = 0
        self.RT = 0
        #Area Properties
        self.AR = 0
    
    def printFile(self):
        print self.cfg_file,self.cache_name
    
    def init(self):
        self.C = int(self.values_ram["C"])
        self.B = int(self.values_ram["B"])
        self.BNKS =int(self.values_ram["BNKS"])
        self.DW = int(self.values_ram["DW"])
    
        self.AT = float(self.values_ram["AT"])
        self.RT = float(self.values_ram["RT"])
        self.AR = float(self.values_ram["AR"])
        self.RPWR = float(self.values_ram["RPWR"])
        #self.LPWR = float(self.values_ram["LPWR"])
    
    def read_mdl(self,f,v):
        for i in range(len(f)):
            if f[i].strip() in self.names_ram:
                #print f[i],"=",v[i]
                self.values_ram[self.names_ram[f[i].strip()]] = float(v[i])
        
    def parse_cfg(self):
        if not os.path.isfile(self.cfg_file):
            print "ERROR: cache.cfg file is missing!!!"
            exit(1)
        
        fp = open(self.cfg_file,'r')
        lines = fp.readlines()
        for line in lines:
            data = line.strip().split("=")
        
            if data[0].strip() is "C":
                self.size = data[1].strip()
                if data[1].find('M') > 0:
                    data[1] = str(1024 * 1024 * int(data[1].split('M')[0]))
                elif data[1].find('G') > 0:
                    data[1] = str(1024 * 1024 * 1024 * int(data[1].split('G')[0]))
            
            #print data[0],data[1]
            #break
            self.arg_list.append(data[1].strip())
    
        fp.close()
    
    def access(self):
        self.timeAT += int(math.ceil(self.AT))
        self.timeRT += int(math.ceil(self.RT))
    
    def print_short_cfg(self,demands):
        miss_rate = (float(self.miss)/demands)*100
        hit_rate = (float(self.hit)/demands)*100
        self.timeAT = float(self.timeAT)/(10**6)
        print "{:>6} {:>6} {:>6} {:>9}".format(self.size, self.name,self.type,self.policy_name),
        print "{:>9} {:>9}".format(str(self.hit),str(self.miss)),
        print "{:8.2f} {:8.2f} {:10.2f} {:10.4f}".format(hit_rate,miss_rate, self.AT, self.timeAT),
        print "{:12.2f} {:12.2f}".format(self.AR,self.RPWR)
    
    def print_cfg(self):
        print "__________________________________"
        print "<<<<<    RAM   PROPERTIES    >>>>>"
        print "<",self.name," ram >"
        print "RAM Capacity :",self.C, "bytes"
        print "RAM Block size :", self.B, "bytes"
        print "RAM Data bus width :", self.DW, "bits"
        print "RAM Access time :",self.AT,"(ns)"
        print "RAM Random cycle time :",self.RT,"(ns)"
          
        
    def model(self):
        self.parse_cfg()
        print "Modeling",self.name,"RAM..."
    
        cfg = self.arg_list
        cfg.insert(0,CACTI)
        #print ' '.join(cfg)
        #try:
        ram = subprocess.Popen(cfg, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        err = False
        if ram.wait() < 0:
            print "Err: Cach cfg not correct!!!"
            exit(1)
        
        for line in iter(ram.stderr.readline,''):
            print "Err:",line.rstrip()
            err = True
        for line in iter(ram.stdout.readline,''):
            print "Err:",line.rstrip()
            err = True

        if err:
            exit(1)

        fp = open(cfg[-1],'r')
        lines = fp.readlines()
        f = lines[0].strip().split(",")
        v = lines[1].strip().split(",")
        fp.close()
        
        #for i in range(len(f)):
        #    print f[i],"=",v[i]
    
        self.read_mdl(f,v)
        self.init()
        
        
        
        
        