import tornado.httpserver
import tornado.ioloop
import tornado.web
import hashlib
import socket
import getpass
import os, re, math
import json, operator
import pickle
import urllib
from nltk.tokenize import RegexpTokenizer

from tornado.httpclient import AsyncHTTPClient
from tornado import gen
from tornado.options import define, options

from operator import mul

IndustryCorrelation = {}
tokenizer = None
price_correlation ={}
NEWSCorrelation = {}
P_2015revenue = {}
classification = {}


from constants import color
bcolors = color.bcolors()

def top10String(sorted_List, title, addlink):        
    outputStr = "<h1>%s</h1>" % title
    for (industry, count) in sorted_List[:10]:
        if addlink:
            url = "http://finance.yahoo.com/q?s=%s&fr=uh3_finance_web&uhb=uhb2" % industry
            outputStr += '<a href=%s>%s</a>: %s<br>' % (url, industry, str(count))
        else:
            outputStr+= industry + ":\t" + str(count) + "<br>"
    

    return outputStr

def Tosnippet(text, keywords, extend):
    returnText= '...'    
        
    for keyword in keywords:        
        loc= 0
        tmp= 0
        loc = text.lower().find(keyword.lower(), loc)
        toReplace = text[int(loc):int(loc)+int(len(keyword))]            
        text= text.replace(toReplace, '<strong>{}</strong>'.format(toReplace)) + "..."
        loc= 0
        tmp= 0
        while (loc<len(text) and loc!=-1):
            tmp = loc        
            loc = text.lower().find(keyword.lower(), loc)            
            if loc==-1 or loc==tmp:
                break            
            if(loc<len(text) or loc-extend>tmp):
                returnText = returnText + text[loc-extend:loc+extend] + "..."
            elif loc==-1 or loc==tmp:
                break    

    return returnText

def vectorSpaceCalculation(vectorSpace):
    # vectorSpace stored each token as the key, and its corresponding (docID, TF, idf)s
    
    # multiply all TFidfs if they all have the same docid, and then saved in TFidf_dic
    # so each TFidf_dic[docID] is one 
    TFidf_dic = {}
    TFidf_dic_vectorSpace = {}
    q_space = {}
    for token in vectorSpace.keys():
        for (docid, TF, idf) in vectorSpace[token]:
            value = TF*idf
            try:
                if (value==0):
                    TFidf_dic[docid] = TFidf_dic[docid]
                else:
                    TFidf_dic[docid] = TFidf_dic[docid] * value

                TFidf_dic_vectorSpace[docid].append(value)
            except KeyError:
                TFidf_dic[docid] = value                    
                TFidf_dic_vectorSpace[docid] = [value]

            try:
                q_space[token] = idf
            except KeyError:
                q_space[token] = idf

    # Length of q 
    print TFidf_dic_vectorSpace
    squ_sum=0
    for k in q_space.keys():        
        squ_sum= squ_sum + q_space[k]*q_space[k]
    q_space_length=math.sqrt(squ_sum)

    resultList = []
    for eachDocID in TFidf_dic.keys():        
        
        # Length of current document
        squ_sum=0        
        for value in TFidf_dic_vectorSpace[eachDocID]:
            squ_sum = squ_sum + value * value
        curDoc_length = math.sqrt(squ_sum)

        # similarity values
        cosSim = TFidf_dic[eachDocID]/(q_space_length*curDoc_length)
        resultList.append((eachDocID,cosSim))

    return resultList
    


class Application(tornado.web.Application):
    def __init__(self, server):
        if(server == 'indexServer'):            
            handlers = [
                (r"/", HomeHandler),            
                (r"/index", idxSearchHandler)
            ]        
        elif (server == 'docServer'):            
            handlers = [
                (r"/", HomeHandler),            
                (r"/doc", docSearchHandler)
            ]
        else:
            raise NameError('wrong server name')
        
        tornado.web.Application.__init__(self, handlers)

class idxSearchHandler(tornado.web.RequestHandler):
    @gen.coroutine            
    def get(self):
        global IndustryCorrelation, tokenizer, price_correlation, NEWSCorrelation, P_2015revenue, classification
        myquery = self.request.uri
        myquery = urllib.unquote(myquery.split('?q=')[-1])                
        mydict= {}
        OutputStr = []
        
        #IndustryCorrelation            
        try:
            mydict = eval(IndustryCorrelation[myquery.upper()])
            sorted_List = sorted(mydict.items(), key=operator.itemgetter(1), reverse=True)        
            OutputStr.append(top10String(sorted_List, "Top10 related industry to your stock", False))
        except:
            print "first"
            OutputStr.append("Stock not found in system"  )
            
        #price_correlation            
        try:
            mydict = price_correlation[myquery.upper()]
            OutputStr.append(top10String(mydict['top20'], "Top10 related stocks to your stock", True))
            OutputStr.append(top10String(mydict['worst20'], "Worst10 related stocks to your stock", True))            
        except:
            print "second"
            OutputStr.append("Stock not found in system"  )

        #NEWSCorrelation
        try:
            match = NEWSCorrelation[myquery.upper()]
            sorted_List = sorted(match, key=lambda tup: tup[1], reverse=True)
            OutputStr.append(top10String(sorted_List, "Top10 related NEWScorrelation to your stock",True))            
        except:
            print "third"
            OutputStr.append("Stock not found in system"  )

        #P_2015revenue        
        out = "<h1>Chance of increasing revenue in 2015</h1>"
        try:
            match = P_2015revenue[myquery.upper()]            
            out+= myquery.upper() + ":\t" + str(match) + "<br>"
            OutputStr.append(out)            
        except:
            print "third"
            OutputStr.append(out + "Stock not found in system")

        
        # print classification
        out = "<h1>Classification</h1>"        
        try:
            matchList = [float(x) for x in classification[myquery.upper()]]            
            firstsum = sum(matchList[:3])
            secondsum =  sum(matchList[3:])
            matchList[0] = matchList[0]/firstsum
            matchList[1] = matchList[1]/firstsum
            matchList[2] = matchList[2]/firstsum
            matchList[3] = matchList[3]/secondsum
            matchList[4] = matchList[4]/secondsum
            matchList[5] = matchList[5]/secondsum            
            out+= myquery.upper() + ":\t" + str(matchList) + "<br>"
            OutputStr.append(out)            
        except:
            print "third"
            OutputStr.append(out + "Stock not found in system")


        body = ''
        for eachItem in OutputStr:
            body+=eachItem 

        # print "OutputStr:\n%s" % OutputStr
        # print "Body:\n%s" % body
        self.write(body)
        

class docSearchHandler(tornado.web.RequestHandler):
    @gen.coroutine            
    def get(self):
        global IndustryCorrelation, tokenizer
        myquery = urllib.unquote(self.request.uri)
        (docid, query) = myquery.replace('/doc?id=','\t').split("&q=")        
        query=query.split()
        
        self.write(json.dumps({'result':[{ 'url':IndustryCorrelation[int(docid)]['url'],
            'snippet': Tosnippet(IndustryCorrelation[int(docid)]['text'], query, 150),
            'docID': docid,
            'title': IndustryCorrelation[int(docid)]['title']
            }]}))
        
    
        


        


count=0
class HomeHandler(tornado.web.RequestHandler):
    @gen.coroutine     
    def get(self):      
        global count
        self.write("Reflesh Count:" + str(count))
        count=count+1


class BackEndApp(object):
    def __init__(self, serverType, serverNum, port):
        global IndustryCorrelation, tokenizer, price_correlation, NEWSCorrelation, P_2015revenue, classification
        if (serverType=='indexServer'):
            path = os.path.dirname(__file__) + '/../category_correlation/output/correlation_output_Final.txt'
            # path = '../out/correlation_output_Final.txt'
        else:
            raise NameError('path error')
        
        #load pickle the proper pickle file
        print bcolors.OKGREEN + "Loading IndustryCorrelation" + bcolors.ENDC
        path = os.path.dirname(__file__) + '/../category_correlation/output/correlation_output_Final'
        IndustryCorrelation = pickle.loads(open(path).read())        
        
        print bcolors.OKGREEN + "Loading price_correlation" + bcolors.ENDC
        path = os.path.dirname(__file__) + '/../price_correlation/output/price_correlation_top_worst20'                
        price_correlation = pickle.loads(open(path).read())

        print bcolors.OKGREEN + "Loading NEWSCorrelation" + bcolors.ENDC
        path = os.path.dirname(__file__) + '/../Vincent_NEWSCorrelation/output/NEWSCorrelation'
        NEWSCorrelation = pickle.loads(open(path).read())

        print bcolors.OKGREEN + "Loading P_2015revenue" + bcolors.ENDC
        path = os.path.dirname(__file__) + '/../Vincent_PredictModel/P_2015revenue'
        P_2015revenue = pickle.loads(open(path).read())

        print bcolors.OKGREEN + "Loading classification" + bcolors.ENDC
        path = os.path.dirname(__file__) + '/../Vincent_Classification/macro_classification/output2/classification'
        classification = pickle.loads(open(path).read())
        
        # path = os.path.dirname(__file__) + '/../Vincent_PredictModel/output'
        # with open(path,'r') as f:
        #     for line in f:
        #         (stock1, val) = line.split("\t")                                
        #         P_2015revenue[stock1] = float(val)
        #         # print P_2015revenue[stock1]
        #         # try:
        #         #     NEWSCorrelation[stock1].append( (stock2, int(count)))
        #         #     # print NEWSCorrelation[stock1]
        #         # except:
        #         #     NEWSCorrelation[stock1] = [(stock2, int(count))]
        #         #     # print NEWSCorrelation[stock1]
        
        # path = os.path.dirname(__file__) + '/../Vincent_PredictModel/P_2015revenue'
        # fileObj = open (path, 'w')
        # pickle.dump(P_2015revenue,fileObj)
        # fileObj.close()
        
        # path = os.path.dirname(__file__) + '/../Vincent_Classification/macro_classification/output2/part-r-00000'
        # with open(path,'r') as f:
        #     for line in f:
        #         arr = line.split("\t")                                                
        #         stock = arr.pop(0)                
        #         classification[stock] = arr
        
        
        
        self.app = tornado.httpserver.HTTPServer(Application(serverType) )        
