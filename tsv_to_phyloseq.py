#!/usr/bin/env python3
##### Program description #######
#
# Title: Combine samples with same property
#
# Author(s): Lokeshwaran Manoharan
#
#
#
# Description: the abundance values are averaged for each property from all the samples  
#  
# List of subroutines: 
#
#
#
# Overall procedure: using hashes/dictionaries in python
#
# Usage:  tsv_to_phyloseq.py <taxonomy.tsv> <phyloseq.tsv>
#
##################################

# Remember that the sample names should match exactly!!!!!

import re
import sys
import math

Taxa_file = open(sys.argv[1], 'r')
Tab_file = open(sys.argv[2], 'w')


p2 = re.compile('\t')
p1 = re.compile(';')
taxa_dict = {}


print('ASV','kingdom','phylum','class','order','family','genus','species',file = Tab_file,sep='\t')

count = 0
for line in Taxa_file:
	line = line.rstrip('\n')
	#print(re.match('#',line))
	if count == 0:
		count += 1
	else:
		asv_list = re.split(p2,line)
		asv_key = asv_list[0]
		asv_taxa = re.sub('.__','',asv_list[1])
		taxa_list = re.split(p1,asv_taxa)
		taxa_dict[asv_key] = '\t'.join(taxa_list) + '\tNA' * (7 - len(taxa_list)) 
		print(asv_key,taxa_dict[asv_key] ,file = Tab_file,sep='\t')



Taxa_file.close()
Tab_file.close()



