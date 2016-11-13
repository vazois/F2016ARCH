import os.path
import subprocess
from cacti import getFLD, getExec

RAM_CFG_FILE = "ram.cfg"
RAM_ARG_LIST = list()

CACTI_FLD = getFLD()
CACTI = getExec()

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

def get_ram_cfg(name):
    global values_ram
    return values_ram[name]

def read_ram_mdl(f,v):
    global names_ram, values_ram
    for i in range(len(f)):
        if f[i].strip() in names_ram:
            #print f[i],"=",v[i]
            values_ram[names_ram[f[i].strip()]] = float(v[i])

def model_ram(cfg):
    print "Modeling RAM..."
    
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
    
    #for i in range(len(f)):
    #    print f[i],"=",v[i]
    
    read_ram_mdl(f,v)
    fp.close()
    
def parse_ram_cfg():
    global RAM_ARG_LIST
    if not os.path.isfile(RAM_CFG_FILE):
        print "ERROR: ram.cfg file is missing!!!"
        exit(1)
        
    fp = open(RAM_CFG_FILE,'r')
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
        RAM_ARG_LIST.append(data[1].strip())
    
    fp.close()

def get_ram_args():
    global RAM_ARG_LIST
    return RAM_ARG_LIST
