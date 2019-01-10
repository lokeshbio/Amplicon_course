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
# Usage:  krona_qiime.py <taxonomy.tsv> <biom_table.tv>
#
##################################

# Remember that the sample names should match exactly!!!!!

import re
import sys
import math

Taxa_file = open(sys.argv[1], 'r')
Tab_file = open(sys.argv[2], 'r')


p2 = re.compile('\t')
p1 = re.compile(';')
taxa_dict = {}
samp_list = []
prop_dict = {}

count = 0
for line in Taxa_file:
	line = line.rstrip()
	#print(re.match('#',line))
	if count == 0:
		count += 1
	else:
		asv_list = re.split(p2,line)
		asv_key = asv_list[0]
		asv_taxa = re.sub('D_.__','',asv_list[1])
		taxa_list = re.split(p1,asv_list[1])
		taxa_dict[asv_key] = asv_taxa + ';NA' * (7 - len(taxa_list)) + ';' + asv_key


count = 0
for line in Tab_file:
	line = line.rstrip()
	if count == 0:
		count += 1
	elif count == 1:
		samp_list = re.split(p2,line)
		samp_list.pop(0)
		for samp_key in samp_list:
			prop_dict[samp_key]= {}	
		count += 1
			
	else:
		count += 1
		count_list = re.split(p2,line)
		taxa_key = count_list.pop(0)
		for i in range(len(count_list)):
			prop_dict[samp_list[i]][taxa_dict[taxa_key]]= count_list[i]
	
	

# Counting how many samples in each property for calculating avrage

for samp_key in samp_list:
	temp = samp_key+'.krona.txt'
	Out_file = open(temp, 'w')
	for taxa_key in prop_dict[samp_key]:
		annot = taxa_key.replace(';','\t')
		print(prop_dict[samp_key][taxa_key],'\t',annot,file = Out_file,sep='')
	Out_file.close()

Tab_file.close()



