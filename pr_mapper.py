#!/usr/bin/env python

# Joe Teague and Clarence Jackson
# pr_mapper.py -- takes input in the form url, rank, [outbound links]
# outputs each outbound link with its calculated pagerank, then (so everything
# can be pieced back together), the initial url and its complete list of 
# outbound links

import sys

for line in sys.stdin:
	words = line.split()
	url  = words[0]			# Current page
	rank = float(words[1])
	outs = words[2:]
	
	for out in outs:
		print '%s %s' % (out, rank / len(outs))

	print '%s LIST' % (url),
	for out in outs:
		print ' %s' % (out),
	print ''
	print '%s 0' % (url)
