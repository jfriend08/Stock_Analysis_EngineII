#! /usr/bin/env python

import sys, re
f = open('./constant/priceDiff_360days.txt', 'r')


tag_list=[]
for line in f:
	fields = line.strip().split('\t')
	tag_list.append(fields[1])

TAG = "#".join(tag_list)

for line in sys.stdin:
	line.strip()	
	print TAG + "\t" + line.replace("\n", "")