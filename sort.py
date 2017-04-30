#!/usr/bin/env python

# Joe Teague and Clarence Jackson
# sort.py -- since MapReduce outputs pages alphabetically, this will read the 
# final clean version of iterations from a run of 25 experiments and sort the
# pages by pagerank. In other words, just give it the directory name and this
# script will do all the heavy lifting.

import sys
import os
import operator

iters = 25

if len(sys.argv) != 2 and len(sys.argv) != 3:
	print 'usage: %s dir_name (iters)' % (sys.argv[0])
	sys.exit(1)

dirname = sys.argv[1]
if not os.path.exists(dirname):
	print 'directory %s does not exist.' % (dirname)
	sys.exit(1)

if len(sys.argv) == 3:
	iters = int(sys.argv[2])

print 'Will sort %d iters in directory %s' % (iters, dirname)

flist = ['initial', 'final']
for i in range(0, iters):
	flist.append('iter%d' % (i + 1))

for f in flist:
	ifname = '%s/%s_clean' % (dirname, f)
	ofname = '%s/%s_sorted' % (dirname, f)
	infile = open(ifname, 'r')

	ranklist = []
	for line in infile:
		words = line.split()
		tup = (words[0], float(words[1]))
		ranklist.append(tup)
	
	infile.close();
	sortlist = sorted(ranklist, key = lambda x: x[1], reverse = True)
	
	outfile = open(ofname, 'w')
	for tup in sortlist:
		outfile.write('%s     %f\n' % (tup[0], tup[1]))
	outfile.close()
