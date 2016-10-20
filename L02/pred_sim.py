import sys

#################################
#								#
#			UTILITY 			#
#								#
#################################

ADDR_BITS = 6
ADDR_BLOCK = 0x3f
M = 0
N = 0

def setAddrBits(bits):
	global ADDR_BITS, ADDR_BLOCK
	ADDR_BITS = bits
	ADDR_BLOCK = (1 << bits) - 1
	

def addrIndex(x):
	return ADDR_BLOCK & x

def addrToInt(s):
	return int(s,16)

def processTraceFile(filename):
	fp = open(filename, "r")
	lines = fp.readlines()
	
	trace = list()
	for line in lines:
		data = line.strip().split(" ")
		addr = addrToInt(data[0])
		res = True if data[1] == "T" else False
		trace.append((addr,res))
	
	fp.close()
	return trace


#################################
#								#
#			SIMULATE			#
#								#
#################################
def sim_trace(trace):
	global M,N,ADDR_BITS, ADDR_BLOCKS
	tables = 1 << M
	entries = 1 << ADDR_BITS
	


#################################
#								#
#			MAIN FUNC			#
#								#
#################################

argc = len(sys.argv)

if argc < 5:
	print "Please provide filename, (M,N) predictor parameters and LSB to consider from PC: e.g. ./pred_sim.py trace.txt 0 1"
	exit(1)



filename = sys.argv[1]
M = int(sys.argv[2])
N = int(sys.argv[3])
bits = int(sys.argv[4])

print "Simulating branch predictor on stack trace <",filename,"> using a (",M,",",N,") predictor and {",bits,"} LSB of PC "
trace = processTraceFile(filename)
setAddrBits(bits);

print "addrBits:",ADDR_BITS
print "addrBlock:",hex(ADDR_BLOCK)


#for i in range(10):
#	pair = trace[i]
#	print hex(pair[0]),pair[1]


