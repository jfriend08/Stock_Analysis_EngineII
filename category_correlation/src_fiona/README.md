# Correlation computing

###Plan A:
The Hadoop Streaming Python can take multiple files as input, but they will be treated as an input flow. We need to compute the price difference within one day,which requires both the open price file and close price file to be manipulated at the same time. So I add one more step on preprocess to calcualte the daily price difference. 

###Plan B
However, the raw data of daily price contains both the open price and close price in one day, why don't we take advantage of that and try to use a mapper to do the preprocess.