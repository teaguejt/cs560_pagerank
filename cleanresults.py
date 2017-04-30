#!/usr/bin/env python

# Joe Teague and Clarence Jackson
# cleanresults.py -- clean up the pagerank results so it's easier to read.
# Basically, get rid of the adjacency lists so each line is just an article
# title and its rank.

import sys

if len(sys.argv) != 2:
	print 'usage: %s filename' % (sys.argv[0])

infile = sys.argv[1]
outfile = infile + '_clean'

inf = open(infile, 'r')
ouf = open(outfile, 'w')

for line in inf:
	words = line.split()
	outwords = words[0:2]
	for outword in outwords:
		ouf.write('%s\t' % (outword))
	ouf.write('\n')

inf.close()
ouf.close()
