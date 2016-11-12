import sys
import math
import subprocess
import os.path

BANKS=4
TECH = 0.32

CT = 0
POWER=0
AREA=0

def cacti_call(CSIZE,BSIZE,WAYS):
    CACTI = "./cacti41/cacti"
    if not os.path.isfile(CACTI):
        print "File ", CACTI, " does not exist. Please type make in cacti41 folder."
        exit(1)

    #call([CACTI, str(CSIZE), str(BSIZE), str(WAYS), str(TECH), str(BANKS)])
    proc = subprocess.Popen([CACTI, str(CSIZE), str(BSIZE), str(WAYS), str(TECH), str(BANKS)], stdout=subprocess.PIPE)
    for line in iter(proc.stdout.readline,''):
        print line.rstrip()

def modelCache():
    #Process cache features
    x=0