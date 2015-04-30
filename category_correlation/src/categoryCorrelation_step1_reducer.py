#!/usr/bin/env python
##The idea for reducer is to let it hold a list of 365 elements, 
##which each element hold the accumulate value for specific day.
##Re-init the list when the nex key pass in


from operator import itemgetter
import sys, re

cur_industry = None
for line in sys.stdin:    
    line = line.strip() # remove leading and trailing whitespace
    
    # parse the input and do proper process
    (industry, day_price) = line.split('\t')
    (day, price) = day_price.split('_')
    price = float(price)

    # case of same industry
    if cur_industry == industry:    	
        everydayPrice[int(day)] = everydayPrice[int(day)] + price
    	
    # case of new different industry
    else:
        # if exist, print it
        if cur_industry:        	
            print cur_industry + "\t" + '\t'.join(map(str,everydayPrice))
        
        # then initialize a new one
        cur_industry = industry
        everydayPrice = [0 for _ in range(365)]        

if cur_industry:        	
	print cur_industry + "\t" + '\t'.join(map(str,everydayPrice))
        
