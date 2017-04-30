#!/usr/bin/env python

import sys
import os
import time

if sys.argv != 2:
    print 'usage: %s processed_xml_file' % (sys.argv[0])
f = sys.argv[1]

call1 = 'cat %s | ./pr_mapper.py | sort | ./pr_reducer.py > iter' % (f)
call21 = 'cat inter | ./pr_reducer.py > iter'
call22 = 'cat iter | ./pr_mapper.py | sort > inter'
print call1
os.system(call1)

for i in range(0, 50):
	time.sleep(1)
	print call21
	os.system(call22)
	os.system('cp inter inter%d' % (i+1))
	os.system(call21)
	os.system('cp iter iter%d' % (i+1))
