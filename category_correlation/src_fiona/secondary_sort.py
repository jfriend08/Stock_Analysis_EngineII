from mrjob.job import MRJob
from itertools import groupby
#from operator import itemgetter, attrgetter
import operator

MRJob.SORT_VALUES = True

class MRWordFrequencyCount(MRJob):
	
    def mapper(self, _, line):
        fields = line.strip().split('\t')
        stock = fields[0]
		
        info = eval(fields[1])
		
        for x in info:
            #industry_name = x[1]
            industry_name = x
			
            #print stock, (int(info[x]), industry_name)
            yield stock, (int(info[x]), industry_name)
	
	#yield words[0], (int(words[1]), "industry_name")
	
    def reducer(self, key, values):
        #values.sort(key=lambda x: x[1], reverse=True)
        values = sorted(values, key=lambda x: x[0], reverse = True)
        count = 0
		
        my_dict = {}
        sorted_dict = {}
		
        for d in values:
            if count < 10:
                count += 1
                my_dict[d[1]] = int(d[0])
		
        my_dict = sorted(my_dict.items(), key=operator.itemgetter(1), reverse=True)
		
        #print my_dict
		
        yield key, my_dict

if __name__ == '__main__':
    MRWordFrequencyCount.run()