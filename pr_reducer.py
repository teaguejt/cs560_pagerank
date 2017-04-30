#!/usr/bin/env python

# Joe Teague and Clarence Jackson
# pr_mapper.py -- finalizes the pagerank calculation performed by the mapper
# and outputs new values in a form that can be easily read again by the mapper
# for subsequent iterations. Since there is the potential for empty pages to
# now be present (since EVERY link encountered is given an entry), we have to
# account for that as well.

d = 0.85
s = 1 - d
oldkey = ''

import sys

outs = []
rank = 0

for line in sys.stdin:
	words = line.split()
	key = words[0]

	if oldkey == '':
		oldkey = key

	if key != oldkey:
		rank = s + (d * rank)
		print('%s %s' % (oldkey, rank)),
		for out in outs:
			print ' %s' % (out),
		print ''
		outs = []
		rank = 0
		oldkey = key
		
	if words[1] != 'LIST':
		rank += float(words[1])
	else:
		outs = words[2:]

rank = s + (d * rank)
print('%s %s' % (oldkey, rank)),
for out in outs:
	print ' %s' % (out),
print ''
