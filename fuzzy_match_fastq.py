#!/usr/bin/python3
#Tom Delomas December 2018
######note: this is very slow, it will only be useful for combing through small fastq files with few target sequences
######for most cases, uses bowtie2 | samtools | bcftools mpileup | bcftools call
#comb through a fastq file and pull out reads that contain input sequences in a fasta file with a given number of matching errors
#will multi-thread if more than one seq is given and -t is > 1
#in terminal type fuzzy_match_fastq.py -i target_seqs.fa -l all_reads.fq -indels #max_indels -sub #max_substitutions -tot #max_total_differences -t max_num_threads_to_use
# -indels defaults is 5
# -sub default is 5
# -tot default is 10
# -t defauls is 1

import regex, sys
from Bio import SeqIO
from multiprocessing import Process

def search(target_seq, file_to_search, output_name, max_sub, max_tot, max_indels):
	#open output file
	output_file = open(output_name, 'w')
	#complie regex
	compiled_regex = regex.compile('('+target_seq+'){s<='+str(max_sub)+',1i+1d<='+str(max_indels)+',e<='+str(max_tot)+'}')
	#comb through reads
	for read in SeqIO.parse(file_to_search, 'fastq'):
		if compiled_regex.search(str(read.seq)):
		#if len(regex.search('('+target_seq+'){s<='+str(max_sub)+',1i+1d<='+str(max_indels)+',e<='+str(max_tot)+'}', str(read.seq))) > 0:
			output_file.write(str(read.seq) + '\n')

def get_valid_filename(s):	#from Django
    # Return the given string converted to a string that can be used for a clean
    # filename. Remove leading and trailing spaces; convert other spaces to
    # underscores; and remove anything that is not an alphanumeric, dash,
    # underscore, or dot.
    # >>> get_valid_filename("john's portrait in 2004.jpg")
    # 'johns_portrait_in_2004.jpg'
    s = str(s).strip().replace(' ', '_')
    return regex.sub(r'(?u)[^-\w.]', '', s)

def Main():
	#define defaults then get input values
	target_file = ''
	library_file = ''
	max_indels = 5
	max_sub = 5
	max_tot = 10
	threads = 1
	
	for flag in range(1, len(sys.argv), 1):	#start at 1 b/c 0 is name of script
		if sys.argv[flag] == '-i':
			target_file = sys.argv[flag + 1]
		if sys.argv[flag] == '-l':
			library_file = sys.argv[flag + 1]
		if sys.argv[flag] == '-indels':
			max_indels = int(sys.argv[flag + 1])
		if sys.argv[flag] == '-sub':
			max_sub = int(sys.argv[flag + 1])
		if sys.argv[flag] == '-tot':
			max_tot = int(sys.argv[flag + 1])
		if sys.argv[flag] == '-t':
			threads = int(sys.argv[flag + 1])
			
	print('Searching for matches with a maximum of ', str(max_indels), ' indels, ', str(max_sub), ' substitutions, and ', str(max_tot), ' total differences')

	#to avoid loading entire input fasta into memeorey in case of large file, iterate through and search as you go
	used_thread = 0	#this will count how many threads are used
	processes = {} #dictionary of processes
	#read in seq to search
	for target in SeqIO.parse(target_file, 'fasta'):
		seq = str(target.seq)
		out_name = get_valid_filename(str(target.id)) + '.txt'	#turn name of fasta into a valid filename
		#start processes of sorting
		processes[used_thread] = Process(target=search, args=(seq, library_file, out_name, max_sub, max_tot, max_indels))
		processes[used_thread].start()
		used_thread += 1
		
		if used_thread == threads:	#this pauses script once the maximum number of threads is reached and the continues when all processes are finished
			#join processes
			for i in processes:
				processes[i].join()
			used_thread = 0
			processes = {}
	
	for i in processes:		#join remaining processes if threads is not an exact multiple of the number of sequences
		processes[i].join()

Main()