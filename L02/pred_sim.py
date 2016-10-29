import sys
import os.path


#################################
#								#
#			UTILITY 			#
#								#
#################################

def mask(bits):
	return (1 << bits) - 1

ADDR_BITS = 6
ADDR_MASK = mask(ADDR_BITS)

M = 4
N = 2
M_MASK=mask(M)
N_MASK=mask(N)

HR_BITS = 4
HR_MASK = mask(HR_BITS)

def decode(state):
	global N
	return (state>>(N-1))
	
def ffs(x):
	shf = (x&-x).bit_length()-1
	return shf if shf > 0 else 0 
	
def sadd(state):
	global N_MASK
	shf = ffs(~state)
	#print "ffs_add:",shf
	return   ((1 << shf) | state ) & N_MASK
	#global N
	#return state + 1 if state < mask(N) else state

def ssub(state):
	global N_MASK
	shf = ffs(state)
	#print "ffs_sub:",(~(1 << shf))
	return   ((~(1 << shf)) & state ) & N_MASK
	#global N
	#return state - 1 if state > 0 else state

def setMNBits(Marg,Narg):
	global M,N
	global  M_MASK, N_MASK
	M = Marg
	N = Narg
	M_MASK = mask(M)
	N_MASK = mask(N)

def setAddrBits(bits):
	global ADDR_BITS, ADDR_MASK
	ADDR_BITS = bits
	ADDR_MASK = mask(ADDR_BITS)
	

def addrIndex(x):
	return ADDR_MASK & x

def addrToInt(s):
	return int(s,16)

def processTraceFile(filename):
	fp = open(filename, "r")
	lines = fp.readlines()
	
	trace = list()
	for line in lines:
		data = line.strip().split(" ")
		addr = addrToInt(data[0])
		res = 1 if data[1] == "T" else 0
		trace.append((addr,res))
	
	fp.close()
	return trace

#################################
#								#
#			SIMULATE			#
#								#
#################################
def sim_trace(trace):
	global M,N,M_MASK,ADDR_BITS, ADDR_MASK
	tables = 1 << M
	entries = 1 << ADDR_BITS
	
	print "Number of History Tables: ",tables
	print "Entries per Table: ",entries
	print "Total predictor entries: ",(tables * entries)
	
	table=dict()
	for i in range(tables):
		table[i]=[0 for j in range(entries)]
	
	ghr=0 #global history register
	mispred_count = 0
	iter = 0
	util = dict()
	for branch in trace:
		real = branch[1]
		addr = addrIndex(branch[0])
		
		gaddr = ghr << (ADDR_BITS) | addr
		util[ gaddr ] = 1
		state = table[ghr][addr]
		pred = decode(state)#100 - > 1 , 011 -> 0, 10 -> 1
		
		mispred = (pred!=real)
		#print hex(branch[0]), branch[1], ghr,addr, pred,
		#print "Misprediction:",mispred
		#if addr==24 and ghr == 7:
		#	print "addr:",addr,"r:",real,"p:",pred,"g:",ghr,"i:",iter/3

		if mispred:
			mispred_count = mispred_count + 1
			
		if(real == 0):
			table[ghr][addr] = ssub(state)
		else:
			table[ghr][addr] = sadd(state)
		
		#table[ghr][addr] = ((state << 1) | real) & N_MASK	
			
		
		ghr = ((ghr << 1) | (real)) & M_MASK # shift the real outcome in and keep the M newest branch outcomes		
		
		iter = iter + 1
	print "Branch count: ",iter
	print "Misprediction count: ",mispred_count
	print "Misprediction percentage: ",(float(mispred_count)/iter)*100
	print "Predictor entries utilized: ", len(util)
	print "Entry percentage utilization: ",(float(len(util))/(tables * entries))*100

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
Marg = int(sys.argv[2])
Narg = int(sys.argv[3])
Barg = int(sys.argv[4])

if not os.path.isfile(filename):
	print "File ", filename, " does not exist"
	exit(1)

if (Marg < 0 or Marg >= 16):
	print "Number of bits in the BHR should >= 0 and < 16"
	exit(1)
	
if (Narg < 1):
	print "Number of bits for the counter in the entries of the BHT should be >= 1"
	exit(1)

if (Barg < 1 or Barg > 16):
	print "Number of bits used for indexing from the PC address should be >=1 and <= 16"
	exit(1)



setMNBits(Marg,Narg)
setAddrBits(Barg);
print "Simulating branch predictor on stack trace <",filename,"> using a (",Marg,",",Narg,") predictor and {",ADDR_BITS,"} LSB of PC "
trace = processTraceFile(filename)


print "M bit count and mask:",M,",",hex(M_MASK)
print "N bit count and mask:",N,",",hex(N_MASK)
print "PC address bit count and mask:",ADDR_BITS,",",hex(ADDR_MASK)

#exit(1)

sim_trace(trace)
