#!/usr/bin/env python

# preprocess.py
# Joe Teague and Clarence Jackson

# Preprocess the xml by checking page text and stripping out meaningless 
# pages. In this case, we define meaningless pages as pages where the length
# of the text is less than 250 characters.

# Please note this is intended to work with a Wikipedia dump and will probably
# have to be modified if you use it to process anything else.

# Please also note that this requires Beautiful Soup 4 for parsing. If you
# don't have this, you can install it with 'pip install bs4'

import sys
import xml.etree.ElementTree as ET
import re
import threading
from StringIO import StringIO

records = 0
outf = open('pr_%s' % (sys.argv[1].replace('.xml', '')), 'w')
titles = 0
title = ""
finished = False

def stthread():
	if not finished:
		threading.Timer(10.0, stthread).start()
		print '%s: processing %s' % (sys.argv[0], title)

def cleantag(el):
	return el.split('}')[1]

def pr_link(ln):
	return ln.lower().replace(' ', '_').replace('|', '_').replace('\n', '_')

if len(sys.argv) != 2:
	print 'usage: %s input_file' % (sys.argv[0])
	sys.exit(1)

stthread()

for event, elem in ET.iterparse(sys.argv[1], events=('start', 'end', 'start-ns', 'end-ns')):
	#print elem
	#if hasattr(elem, 'tag'):
	#	print cleantag(elem.tag)

	if event == 'end' and cleantag(elem.tag) == 'page':
		llist = []
		for child in elem:
			if cleantag(child.tag) == 'title':
				title = child.text.lower().replace(' ', '_')
			elif cleantag(child.tag) == 'revision':
				for subchild in child:
					if cleantag(subchild.tag) == 'text':
						ttext = subchild.text
						if ttext == None:
							continue
						for i in range(0, len(ttext)):
							if ttext[i:i+2] == '[[':
								j = i
								while ttext[j:j+2] != ']]' and j < len(ttext):
									if j >= len(ttext):
										continue
									j += 1
								link = pr_link(ttext[i + 2:j])
								if 'file:' not in link and 'category:' not in link and \
										'wikipedia:' not in link and \
										link not in llist and link != title:
									llist.append(link)
									#print i, j, link, len(ttext)
		#print llist
		if len(llist) == 0 or 'category:' in title:
			continue
		outf.write('%s\t10.0' % (title.encode('UTF-8')))
		for link in llist:
			if link is None or link == '':
				continue
			outf.write(' %s' % (link.encode('UTF-8')))
		outf.write('\n')
		elem.clear()
		records += 1
		if records % 10000 == 0:
			re.purge()
			print '%s: processed %d records' % (sys.argv[0], records)
#print('%s %s' % (elem.tag, elem.attrib))
finished = True
print('done')
outf.close()
