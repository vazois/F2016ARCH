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
    names_ram["Stanby leakage per bank(mW)"] = "LBPWR"

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
    
    cfg_file = ""
    ram_name =""
    arg_list=list()
    #########################
    def __init__(self,filename,name):
        self.cfg_file = filename
        self.ram_name = name
    
    def printFile(self):
        print self.cfg_file,self.cache_name
    
    def init(self):
        self.C = int(self.values_ram["C"])
        self.B = int(self.values_ram["B"])
        self.BNKS =int(self.values_ram["BNKS"])
        self.DW = int(self.values_ram["DW"])
    
        self.AT = float(self.values_ram["AT"])
        self.RT = float(self.values_ram["RT"])
    
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
                if data[1].find('M') > 0:
                    data[1] = str(1024 * 1024 * int(data[1].split('M')[0]))
                elif data[1].find('G') > 0:
                    data[1] = str(1024 * 1024 * 1024 * int(data[1].split('G')[0]))
            
            #print data[0],data[1]
            #break
            self.arg_list.append(data[1].strip())
    
        fp.close()
    
    def print_cfg(self):
        print "__________________________________"
        print "<<<<<    RAM   PROPERTIES    >>>>>"
        print "RAM Capacity :",self.C, "bytes"
        print "RAM Block size :", self.B, "bytes"
        print "RAM Data bus width :", self.DW, "bits"
        print "RAM Access time :",self.AT,"(ns)"
        print "RAM Random cycle time :",self.RT,"(ns)"
          
        
    def model(self):
        self.parse_cfg()
        print "Modeling RAM..."
    
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
        
        
        
        
        