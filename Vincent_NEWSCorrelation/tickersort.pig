Q = LOAD './output/part-r-00000' AS (tag1, tag2, count:int);
Q = ORDER Q BY count DESC, tag1;
STORE Q INTO 'pig_ticker_output' USING PigStorage();
