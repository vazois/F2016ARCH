import sys

#################################
#								#
#			UTILITY 			#
#								#
#################################

ADDR_BITS = 6
ADDR_MASK = 0x3f

M = 0
N = 0
M_MASK=0
N_MASK=0

def decode(state):
	global N
	return (state>>(N-1))	

def mask(bits):
	return (1 << bits) - 1

def sadd(state):
	global N
	return state + 1 if state < mask(N) else state

def ssub(state):
	global N
	return state - 1 if state > 0 else state

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
	global M,N,ADDR_BITS, ADDR_MASK
	tables = 1 << M
	entries = 1 << ADDR_BITS
	
	print "Number of History Tables: ",tables
	print "Entries per Table: ",entries
	
	table=dict()
	for i in range(tables):
		table[i]=[0 for j in range(entries)]

	#print table
	
	
	ghr=0 #global history register
	mispred_count = 0
	iter = 0
	for branch in trace:
		real = branch[1]
		addr = addrIndex(branch[0])
		
		state = table[ghr][addr]
		pred = decode(state)#100 - > 1 , 011 -> 0, 10 -> 1
		
		mispred = (pred!=real)
		#print hex(branch[0]), branch[1], ghr,addr, pred,
		#print "Misprediction:",mispred
		

		if mispred:
			mispred_count = mispred_count + 1
			
		if(real == 0):
			table[ghr][addr] = ssub(state)
		else:
			table[ghr][addr] = sadd(state)
			
		
		#print table[ghr][addr]
		
		#{CHECK IF SHIFT IS CORRECT}
		ghr = ((ghr << 1) or (real << 1)) and M_MASK # shift the real outcome in and keep the M newest branch outcomes
		
		
		
		iter = iter + 1
		#if iter >100:
		#	break;
	print "iter:",iter
	print "mispred_count:",mispred_count
	print "percentage:",float(mispred_count)/iter

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

setMNBits(Marg,Narg)
setAddrBits(Barg);
print "Simulating branch predictor on stack trace <",filename,"> using a (",Marg,",",Narg,") predictor and {",ADDR_BITS,"} LSB of PC "
trace = processTraceFile(filename)


print "M bits:",M
print "M mask:",M_MASK
print "N bits:",N
print "N mask:",N_MASK

print "PC address mask:",ADDR_BITS
print "PC address mask:",hex(ADDR_MASK)


sim_trace(trace)


#for i in range(10):
#	pair = trace[i]
#	print hex(pair[0]),pair[1]


