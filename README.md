#Stock_Analysis_Engine
Using Hadoop to analyze stock market

#Data source
[google drive](https://drive.google.com/folderview?id=0BzG5zLRRrgKwfkthYmJhdW94aUE1QVpDeTN4bnhsVDJuNmJSZ1d2aElaSExJaUVpWWs5ZDg&usp=sharing)

#Description
The project provides the US stock investors an intelligent stock analytical tool to help them make wise investment decisions. The basic idea underneath is to effectively apply advanced analytical technologies (including statistical analysis, machine learning, data mining and natural language processing, etc.) under the framework of ''Big Data Technolog''. 

#Analytic works
- price_correlation
- category_correlation
- NEWSCorrelation
- NEWSSentimental
- RevenuePredictModel
- Classification

#Start HTTP Server:
```python
python start.py

#It will return the port it is listening:
#Front end will listen to: http://linserv2.cims.nyu.edu:37184
```

API:
http://linserv2.cims.nyu.edu:37184/search?q=STOCKNAME