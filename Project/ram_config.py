import os.path
import subprocess
from cacti import getFLD, getExec

RAM_CFG_FILE = "ram.cfg"
RAM_ARG_LIST = list()

CACTI_FLD = getFLD()
CACTI = getExec()

def model_ram(cfg):
    print "Modeling RAM..."
    
    cfg.insert(0,CACTI)
    #print ' '.join(cfg)
    #cache = subprocess.Popen(cfg, stdout=subprocess.PIPE)
    
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

def get_ram_cfg():
    global RAM_ARG_LIST
    return RAM_ARG_LIST
