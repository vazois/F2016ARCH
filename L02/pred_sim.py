import sys

argc = len(sys.argv)

if argc < 4:
	print "Please provide filename and (M,N) predictor parameters: e.g. ./pred_sim.py trace.txt 0 1"
	exit(1)



filename = sys.argv[1]
M = int(sys.argv[2])
N = int(sys.argv[3])

print "Simulating stack trace from <",filename,"> using a (",M,",",N,") predictor"


