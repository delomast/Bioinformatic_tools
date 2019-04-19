#!/usr/bin/env python
# count cutsites in loci within a fasta file
#python3
#
#call in terminal as:  python count_cuts.py -fasta file.fa -seq AGAGTC -trim_front #
## sequence given can use regular expression syntax as recognized by python3 re library
## is case sensitive, to allow masking
## only finds non-overlapping matches

import re, sys

def Main():

	fasta = 'no_input'	#default values if no value is given
	sequence = 'no_input'
	trim_front = -9
		
	for flag in range(1, len(sys.argv), 1):	#start at 1 b/c 0 is name of script
		if sys.argv[flag] == '-fasta':
			fasta = sys.argv[flag + 1]
		if sys.argv[flag] == '-seq':
			sequence = sys.argv[flag + 1]
		if sys.argv[flag] == '-trim_front':
			trim_front = int(sys.argv[flag + 1])
	
	if not re.search('\.fa$|\.fasta$|\.fna$|\.ffn$|\.faa$|\.frn$', fasta):
		print('No fasta file input given. Exiting.')
		return
	if sequence == 'no_input':
		print('No sequence to search for given. Exiting.')
		return
	if trim_front < 0:
		print('Invalid value for the number of bases to trim off the front of each locus given. Exiting.')
		return
	
	#count cutsites
	count = 0
	search_exp = re.compile(sequence)
	
	with open(fasta, 'r') as fasta_input:
		line = fasta_input.readline()
		while line[0] != '>':		#STACKS puts a header in its fasta outputs, other programs mgiht as well. need to iterate until reaching the first sequence
			line = fasta_input.readline()
		genome_region = ''	#zero genome region to allow first case to be evaluated in while loop
		while line:
			if line[0] == '>':
				count += len(search_exp.findall(genome_region[trim_front:]))	#count cutsites and then move on to the next sequence
				genome_region = ''
			else:
				genome_region += line.rstrip()	#concatenate multiline sequences in the fasta for searching accross line breaks
			line = fasta_input.readline()
		count += len(search_exp.findall(genome_region[trim_front:]))	#count in last sequence
	
	#output result
	print('\n\nThere are ', str(count), ' matches in the fasta file to the sequence you gave.\n')
		
		
Main()
