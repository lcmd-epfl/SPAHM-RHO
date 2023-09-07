#!/usr/bin/env python3

import argparse
import numpy as np

parser = argparse.ArgumentParser(description='Split representation by elements')
parser.add_argument('--q', type=str,  dest='qfile',  required=True, help='list of all atoms')
parser.add_argument('--s', type=str,  dest='suf',    required=True, help='file suffix')
args = parser.parse_args()

#data = np.load(args.dfile)
qs   = np.loadtxt(args.qfile, dtype=str)
suf  = args.suf


mydict = {}
for q in set(qs):
  mydict[q] = list(np.loadtxt(str(q)+'_'+suf+'.dat', ndmin=1))

data = []
for q in qs:
  data.append(mydict[q].pop(0))

np.savetxt(suf+'.dat', np.array(data))
