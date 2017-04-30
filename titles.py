#!/usr/bin/env python

# Joe Teague and Clarence Jackson
# titles.py: take the XML file, and create a file containing all the page
# titles found within. For good measure, ignore any page title of length below
# 5 characters, as it probably has no useful information.

# usage: ./titles.py FILE

# Please note this is for Wikipedia dumps and may not work correctly for other
# data sources without modification.

import sys

outfilename = "titles.txt"
tl = []

if len(sys.argv) != 2:
	print "usage: %s input_file" % (sys.argv[0])
	sys.exit(1)

try:
	with open(sys.argv[1], 'r') as f:
		print("input file opened")

		for line in f:
			if '<title>' in line and '</title>' in line:
				pl1 = line.replace('<title>', '')
				pl2 = pl1.replace('</title>', '')
				title = pl2.replace('\n', '')
				tl.append(title)
		
		f.close()

except IOError:
	print("input file could not be opened")


try:
	with open(outfilename, 'w') as f:
		for title in tl:
			f.write('%s\n' % (title))

		f.close()

except IOError:
	print('output file could not be opened')

print('done!')
