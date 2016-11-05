import sys
import os.path


CSIZE = 1024#1024 Bytes Data Size
BSIZE = 32# 32 Bytes Block Size
WAYS = 4 # Associativity
filename = ""

trace = list()

#################################
#                                #
#     PARSE ARGUMENTS            #
#                                #
#################################

def config(file,csize,bsize,ways):
    print "Simulating ",ways,"- way associative cache with block size ", bsize, " bytes and total size ", csize, " bytes on trace <", file ,">"
    
def argParser(sys):
    global CSIZE, BSIZE, WAYS, filename
    argc = len(sys.argv)
    
    if argc < 2:
        print "Expecting at least 1 argument<>, 3 more are optional{}: <filename> {cache size} {block size} {ways}"
        exit(1)

    filename = sys.argv[1]
    if not os.path.isfile(filename):
        print "File <", filename, "> does not exist"
        exit(1)

    if argc == 2:
        print "Running on default configuration"
        config(filename,CSIZE,BSIZE,WAYS)
        return

    if argc < 5:
        print "Expecting additional arguments: {cache size} {block size} {ways}"
        exit(1)
        
    
    arg = sys.argv[2]
    if arg.find('K') > 0:
        CSIZE = 1024 * int(arg.split('K')[0])
    elif arg.find('M') > 0:
        CSIZE = 1024 * 1024 * int(arg.split('M')[0])
    else:
        CSIZE = int(arg)
    
    BSIZE = int(sys.argv[3])
    WAYS = int(sys.argv[4])
    config(filename,CSIZE,BSIZE,WAYS)
    
def processTraceFile(file):
    fp = open(file,'r')
    
    lines = fp.readlines()
    
    for line in lines:
        data = line.strip().split(' ')
        op = data[0]
        offset = int(data[1])
        addr = int(data[2]) & 0xFFFFFFFF
    fp.close()
     


argParser(sys)

