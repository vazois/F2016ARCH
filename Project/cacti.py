import sys
import math
import subprocess
import os.path

CACTI_FLD = "cacti53/"
CACTI = "./cacti53/cacti"

def getFLD():
    global CACTI_FLD
    return CACTI_FLD

def getExec():
    global CACTI
    return CACTI

def compile():
    if os.path.isfile(CACTI):
        return
    
    print "Compiling cacti..."
    make = subprocess.Popen(["make", "-C", CACTI_FLD], stdout=subprocess.PIPE)
    make.wait()
    
    if not os.path.isfile(CACTI):
        print "Compilation failed! Please check errors by manualy typing make in ",CACTI_FLD
        exit(1)

def clean():
    print "Cleaning cacti compilation..."
    make = subprocess.Popen(["make","clean", "-C", CACTI_FLD], stdout=subprocess.PIPE)
    make.wait()
    

