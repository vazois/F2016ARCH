import sys
from cacti import cacti_call
from utils import CSIZE, BSIZE, WAYS, SETS, argParser, info




argParser(sys)
info()
cacti_call(CSIZE,BSIZE,WAYS)
