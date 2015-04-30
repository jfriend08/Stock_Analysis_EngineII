#!/usr/bin/env python

import sys
import re


for line in sys.stdin:
	
    line = line.strip() # remove leading and trailing whitespace    
    fields=line.split('\t') # split by tab
    # pop out info, and only keep value in fields
    industry = fields.pop(0); symbol = fields.pop(0); weight = fields.pop(0);     
    # multiply every price difference by the weighting
    fields = [float(day) * float(weight) for day in fields]    
    
    count = 0
    for dayWeightedPrice in fields:
    	print industry + "\t" + str(count) + "_" + str(dayWeightedPrice)
    	count+=1