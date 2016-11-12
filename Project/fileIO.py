import os.path

def processTraceFile(file):
    global trace
    fp = open(file,'r')
    trace=list()
    
    print "Parsing File..."
    lines = fp.readlines()
    for line in lines:
        data = line.strip().split(' ')
        op = data[0]
        offset = int(data[1])
        addr = int(data[2],16) & 0xFFFFFFFF
        trace.append((op,offset,addr))
    fp.close()
    print "Parsing Finished..."
    
    return trace


def exists(filename):
    if not os.path.isfile(filename):
        print "File <", filename, "> does not exist"
        exit(1)