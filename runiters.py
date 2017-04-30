#!/usr/bin/env python

# Joe Teague and Clarence Jackson
# runiters.py -- take an unprocessed Wikiemedia XML file, process it, then run
# 25 pagerank iterations to check convergence of pagerank values.
# The results of each experiment are stored in the results_expname directory.
# The initial processed file, the results of each iteration, and the final 
# results are contained within as:
#     -- initial: the initial preprocessed file
#     -- iterx:   the results of iteration x
#     -- final:   the results of the last iteration (idential to itermax)

# usage example: ./runiters.py experiment (iters)
# experiment.xml must exist. results_experiment directory will be created and
# filled.

# NOTE: This already assumes that your environment and HDFS are set up and
# working. A directory in HDFS called '/pagerank' MUST exist for this to work.

import sys
import os
import time

preprocessor = './preprocess.py'
iters = 25
itertimes = []
hadptimes = []

if len(sys.argv) != 2 and len(sys.argv) != 3:
	print 'usage: %s experiment (iters)' % (sys.argv[0])
	sys.exit(1)
elif len(sys.argv) == 3:
	iters = int(sys.argv[2])

exp      = sys.argv[1]
expshort = exp.replace('.xml', '')
basefile = exp
prfile   = 'pr_' + expshort
ifile    = 'initial'
ffile    = 'final'
dirname  = 'results_' + expshort
hadoopf  = '/pagerank/%s' % (prfile)

print 'Experiment details:'
print '\tname:           %s' % (exp)
print '\tbase xml file:  %s' % (basefile)
print '\tprocessed file: %s' % (prfile)
print '\tdirectory:      %s' % (dirname)
print '\titerations:     %d' % (iters)

# Create the results directory if it doesn't already exist
# Otherwise, clean it out in preparation for the experiment.
if not os.path.exists(dirname):
	os.makedirs(dirname)
else:
	os.system('rm %s/*' % (dirname))

# Preprocess the file and copy the initial list to HDFS and the results dir.
cmd = './preprocess.py %s' % (basefile)
print 'Running preprocessor:'
os.system(cmd)

os.system('cp %s initial' % (prfile))
os.system('cp initial %s/initial' % (dirname))
os.system('./cleanresults.py initial')
os.system('cp initial_clean %s/initial_clean' % (dirname))
os.system('rm initial_clean initial')

# ITERATIONS
for i in range(0, iters):
	start_time = time.time()

	# prep the remote directory
	print('iter %d: preparing' % (i + 1))
	os.system('hadoop fs -rm -r -f /pagerank/output')
	os.system('hadoop fs -rm /pagerank/*')
	os.system('hadoop fs -put %s %s' % (prfile, hadoopf))

	# Execute!
	hadoop_cmd = "hadoop jar /usr/local/hadoop-2.7.1/share/hadoop/tools/lib/hadoop-streaming-2.7.1.jar "
	hadoop_files= "-files pr_mapper.py,pr_reducer.py "
	hadoop_mr = "-mapper pr_mapper.py -reducer pr_reducer.py "
	hadoop_in = "-input %s " % (hadoopf)
	hadoop_out = '-output /pagerank/output'
	hadoop_full = hadoop_cmd + hadoop_files + hadoop_mr + hadoop_in + hadoop_out
	print('iter %d: executing %s' % (i + 1, hadoop_full))
	hadoop_start_time = time.time()
	os.system(hadoop_full)
	hadptimes.append(time.time() - hadoop_start_time)

	# Pull the file back to local fs, name it, clean it up, and copy it
	# to the results directory
	print('iter %d: creating local output/clean files' % (i + 1))
	os.system('hadoop fs -get /pagerank/output/part-00000 iter%d' % (i + 1))
	os.system('./cleanresults.py iter%d' % (i + 1))
	os.system('cp iter%d* %s/' % (i + 1, dirname))
	os.system('mv iter%d %s' % (i + 1, prfile))
	os.system('rm iter%d*' % (i + 1))
	itertimes.append(time.time() - start_time)

# Create the final run results and clean up
os.system('rm %s' % (prfile))
os.system('cp %s/iter%d %s/final' % (dirname, i + 1, dirname))
os.system('cp %s/iter%d_clean %s/final_clean' % (dirname, i + 1, dirname))

# Print timing information
itersum = 0
hadpsum = 0
print('Times:')
print('Iter     Total iter time     Hadoop run time')
if len(itertimes) != len(hadptimes):
	print('timing error: list size mismatch')
else:
	for i in range(0, len(itertimes)):
		print '%4d     %15f     %15f' % (i + 1, itertimes[i], hadptimes[i])
		itersum += itertimes[i]
		hadpsum += hadptimes[i]
	print 'tot:     %15f     %15f' % (itersum, hadpsum)
