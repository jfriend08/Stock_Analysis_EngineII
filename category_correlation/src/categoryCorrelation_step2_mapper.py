#!/usr/bin/env python
import sys
import re


for line in sys.stdin:
	line = line.strip().replace("\n", "")		
	fields = line.split("\t")

	M = re.search("#", fields[0])
	
	if M: # so this is the info coming from industry
		print "Has TAG"
		AllTAGs = fields.pop(0).split("#")
		for eachTag in AllTAGs:
			print eachTag + "\t" + "\t".join(map(str,fields))		
	
	else: # so this is the info coming from every stock
		industry = fields.pop(0); symbol = fields.pop(0); weight = fields.pop(0);
		print symbol + "\t" + "\t".join(map(str,fields))