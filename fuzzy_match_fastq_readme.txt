Frequently we want to assess whether any sequencing reads match a given reference sequence with or without a number of mismatches or indels. The multiple short-read mappers available efficiently perform this task. Occasionally, a simpler and more direct method is desired, where you want to specify the maximum number of mismatchs, indels, and/or total errors allowed. This scenario is sometimes found when working with sequence data from amplicon panels. To address this, I have put together a short python script utilizing the capabilities of the ‘regex’ package. The script can be called from the command line as follows:

python fuzzy_match_fastq.py –i target_seqs.fa -l all_reads.fq -indels max_indels -sub max_substitutions -tot max_total_differences -t max_num_threads_to_use

where: 
-i specifies a fasta file with the sequences you want to compare the reads to
-l specifies a fastq file with the reads you want to assess
-indels specifies the maximum number of indel bases that you want to allow (default: 5)
-sub specifies the maximum number of substitutions you want to allow (default: 5)
-tot specifies is the maximum number of total differences (indels + substitutions) you want to allow (default: 10)
-t specifies the maximum number of threads you want to use (default: 1)

Although it does support using multiple threads (if you have more than one sequence in your fasta file to compare reads against) it is quite slow compared to short read aligners. So the only efficient use I find for it is if you have a small fastq file, perhaps with reads you have pre-filtered through some other means.
The output is a file with the name of the target fasta sequence containing the sequences for all the reads that matched successfully given your input parameters.
