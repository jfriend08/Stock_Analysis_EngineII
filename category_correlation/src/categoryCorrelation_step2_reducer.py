#!/usr/bin/env python
from operator import itemgetter
import sys, re

def counting(stock_prices, industry_dict):
	industryCount_dict = {}
	for industry in industry_dict.keys():		
		industryCount_dict[industry] = 0
		industry_price = industry_dict[industry]
		
		for i in range(len(stock_prices)):			
			if float(stock_prices[i])*float(industry_price[i]) >0:
				industryCount_dict[industry] += 1
	return industryCount_dict
		
cur_Stock = None
for line in sys.stdin:    
    
    line = line.strip() # remove leading and trailing whitespace
    try:
    	fields = line.split("\t")
    	stock = fields.pop(0)	        
    	if cur_Stock == stock:	    	    	    	
    		M = re.match(r"[A-Za-z]", fields[0])
    		if M: #info from category    		    		
    			industry = fields.pop(0)
    			industry_dict[industry] = fields    			
    	else:	
			if cur_Stock:        	
				# now is the next stock, do something (e.g. print result for previous stock)			
				industryCount_dict = counting(stock_prices, industry_dict)
				print cur_Stock + "\t" + str(industryCount_dict)
				# for industry in industryCount_dict.keys():
				# 	print "industry: " + industry + " count: " + str(industryCount_dict[industry])

			cur_Stock = stock
			stock_prices = fields #assign the new stock price
			industry_dict = {} # init new dictory to save all industry prices

    except:
		pass
	    