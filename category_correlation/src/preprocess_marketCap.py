#! /usr/bin/env python

import sys, re


def marketCap2Float(marketCap):
	# print marketCap
	multiply = 0
	value = 0
	if (marketCap == 'n/a'):
		return 0
	elif (marketCap[-1] == 'B'):
		multiply = 1000000000
		value = float(marketCap[:-1])
	elif (marketCap[-1] == 'M'):
		multiply = 1000000
		value = float(marketCap[:-1])
	else:
		#so it is real number
		multiply = 1
		value = float(marketCap[:])

	return value * multiply



#First pass, to calculate the total marketCap for each industry
f = open('/Volumes/HHD/Users/yun-shaosung/HDD_Doc/NYU/RealTimeBigData/project/Data2/companylist02.txt', 'r')
dict_market={}
dict_symbol2market={}
for line in f:
	fields = line.strip().split('\t')
	symbol = fields[0].replace(" ", "") #some symbol have many space after it, this will cause dict not match
	industry = fields[6]
	marketCap = fields[3].replace(",", "").replace("$","")
	marketCap_num = marketCap2Float(marketCap)

	try:
		dict_market[industry] = dict_market[industry] + marketCap_num
	except:
		dict_market[industry] = marketCap_num


#Second pass, to get the precentage of that stock in that industry
f = open('/Volumes/HHD/Users/yun-shaosung/HDD_Doc/NYU/RealTimeBigData/project/Data2/companylist02.txt', 'r')
for line in f:
	fields = line.strip().split('\t')
	symbol = fields[0].replace(" ", "") #some symbol have many space after it, this will cause dict not match
	industry = fields[6]
	marketCap = fields[3].replace(",", "").replace("$","")	
	dict_symbol2market[symbol] = [industry, marketCap, marketCap2Float(marketCap)/dict_market[industry]]



#Finally, passing the standard input and append information accordingly
count = 0
for line in sys.stdin:	
    words = line.strip().split("\t")
    StockSymbol = words[0].replace('\"',"")
    if count == 0:
    	print StockSymbol + "\t" + words[1].replace('\"',"") + "\t" + "MarketCapPercentage" + "\t" + '\t'.join(map(str, words[2:])).replace('\"',"")
    	count+=1
    else:	
    	print StockSymbol + "\t" + words[1].replace('\"',"") + "\t" + str(dict_symbol2market[StockSymbol][2]) + "\t" + '\t'.join(map(str, words[2:])).replace('\"',"")

    
















