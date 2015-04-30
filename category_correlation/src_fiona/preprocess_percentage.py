#!/usr/bin/env python
# Realtime and Big Data Analytics

import sys


f1 = open('OpenPrice_360days_complete.txt', 'r')
f2 = open('ClosePrice_360days_complete.txt', 'r')
output = open('PriceDiff_percentage_360days.txt', 'w')

count1 = 0
count2 = 0

matrix1 = [[0 for x in range(365)] for x in range(4658)]
matrix2 = [[0 for x in range(365)] for x in range(4658)]
output_matrix = [[0 for x in range(364)] for x in range(4658)]

for line in f1:
	fields1 = line.strip().split('\t')	
	matrix1[count1] = fields1
	count1 += 1

for line in f2:
	fields2 = line.strip().split('\t')
	matrix2[count2] = fields2
	count2 += 1

output_matrix[0][0] = matrix1[0][3]
output_matrix[0][1] = matrix1[0][0]
output_matrix[0][2] = matrix1[0][2]

for j in range(3, 364):
		output_matrix[0][j] = matrix2[0][j + 1]

for i in range(1, 4658):
	output_matrix[i][0] = matrix1[i][3]
	output_matrix[i][1] = matrix1[i][0]
	output_matrix[i][2] = matrix1[i][2]

	for j in range(3, 364):
            try:
                output_matrix[i][j] = (float(matrix2[i][j + 1]) - float(matrix1[i][j + 1]))/float(matrix1[i][j+1])
            except:
                output_matrix[i][j] = 'NA'


for line in output_matrix:
	for item in line:
  		output.write("%s\t" % item)
  	output.write("\n")

print "finished"
