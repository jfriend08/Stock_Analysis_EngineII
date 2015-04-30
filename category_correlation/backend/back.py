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

invertedIndex = {}
tokenizer = None


from constants import color
bcolors = color.bcolors()

def top10String(sorted_List):
    outputStr = "<h1>Top10 related industry to your stock</h1>"
    for (industry, count) in sorted_List[1:10]:
        outputStr+= industry + " " + str(count) + "<br>"
    

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
        global invertedIndex, tokenizer
        myquery = self.request.uri
        myquery = urllib.unquote(myquery.split('?q=')[-1])                
        mydict= {}
        try:
            mydict = eval(invertedIndex[myquery.upper()])                
            sorted_List = sorted(mydict.items(), key=operator.itemgetter(1), reverse=True)        
            OutputStr = top10String(sorted_List)
        except:
            OutputStr = "Stock not found in system"            
                
        self.write(OutputStr)
        

class docSearchHandler(tornado.web.RequestHandler):
    @gen.coroutine            
    def get(self):
        global invertedIndex, tokenizer
        myquery = urllib.unquote(self.request.uri)
        (docid, query) = myquery.replace('/doc?id=','\t').split("&q=")        
        query=query.split()
        
        self.write(json.dumps({'result':[{ 'url':invertedIndex[int(docid)]['url'],
            'snippet': Tosnippet(invertedIndex[int(docid)]['text'], query, 150),
            'docID': docid,
            'title': invertedIndex[int(docid)]['title']
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
        global invertedIndex, tokenizer
        if (serverType=='indexServer'):
            path = os.path.dirname(__file__) + '/../pickle/correlation_output_Final.txt'
        else:
            raise NameError('path error')
        
        # load pickle the proper pickle file
        print bcolors.OKGREEN + str(serverType) + ":" + str(port) + " loading: " + str(path) + bcolors.ENDC
        with open(path,'r') as f:
            for line in f:
                (key, val) = line.split("\t")                
                invertedIndex[key] = val

        self.app = tornado.httpserver.HTTPServer(Application(serverType) )        
