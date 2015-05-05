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
import tornado.web as web

from operator import mul


IndustryCorrelation = {}
tokenizer = None
price_correlation ={}
NEWSCorrelation = {}
P_2015revenue = {}
classification = {}


from constants import color
bcolors = color.bcolors()


def plot(superList):
    finalOut=""
    for i in range(len(superList)):
        elmList = []
        valList = []
        myreturn="<script type=%s>$(function () {$('#container%s').highcharts({chart: {type: 'column'},"%("\"text/javascript\"", i)
        myreturn+="title: {text: 'Related Industries Ranking'},subtitle: {text: 'Source: stock engine'},"
        print "============ %s ============" % i
        for (elm,val) in superList[i]:
            elmList.append(str(elm))
            valList.append("{name: '%s',data: [%s]}"%(elm,val))
            print "elm:\t%s\tval:%s\tType(elm):%s"%(elm,val,type(elm))
        print "+++++ elmList +++++\n%s"%elmList
        myreturn+="xAxis: {categories: %s,crosshair: true}," % str(elmList)
        myreturn+="yAxis: {min: 0,title: {text: 'correlation count'}},"
        myreturn+="tooltip: {headerFormat: '<span style=%s>{point.key}</span><table>',pointFormat: '<tr><td style=%s>{series.name}: </td>' +'<td style=%s><b>{point.y:.1f} mm</b></td></tr>',footerFormat: '</table>',shared: true,useHTML: true},"%("\"font-size:10px\"", "\"color:{series.color};padding:0\"", "\"padding:0\"")
        myreturn+="plotOptions: {column: {pointPadding: 0.2,borderWidth: 0}},series: [%s]});});</script>"%(",".join(valList))
        
        finalOut+=myreturn
    # myreturn= ""
    # myreturn+="<script type=%s>$(function () {$('#container').highcharts({chart: {type: 'column'},"%("\"text/javascript\"")
    # myreturn+="title: {text: 'Related Industries Ranking'},subtitle: {text: 'Source: stock engine'},"
    # myreturn+="xAxis: {categories: ['Computer Communications Equipment','Electronic Components','Computer Software: Prepackaged Software','Semiconductors','Packaged Foods','Telecommunications Equipment','EDP Services',],crosshair: true},"
    # myreturn+="yAxis: {min: 0,title: {text: 'correlation rate'}},"
    # myreturn+="tooltip: {headerFormat: '<span style=%s>{point.key}</span><table>',pointFormat: '<tr><td style=%s>{series.name}: </td>' +'<td style=%s><b>{point.y:.1f} mm</b></td></tr>',footerFormat: '</table>',shared: true,useHTML: true},"%("\"font-size:10px\"", "\"color:{series.color};padding:0\"", "\"padding:0\"")
    # myreturn+="plotOptions: {column: {pointPadding: 0.2,borderWidth: 0}},series: [{name: 'self',data: [49.9]}, {name: 'avg',data: [78.8]}, {name: 'max',data: [39.3]}, {name: 'min',data: [57.4]        }]});});    </script>"
    return finalOut


def plot1():
    myreturn= ""
    myreturn+="<script type=%s>$(function () {$('#container1').highcharts({chart: {type: 'column'},"%("\"text/javascript\"")
    myreturn+="title: {text: 'Related Industries Ranking'},subtitle: {text: 'Source: stock engine'},"
    myreturn+="xAxis: {categories: ['Computer Communications Equipment','Electronic Components','Computer Software: Prepackaged Software','Semiconductors','Packaged Foods','Telecommunications Equipment','EDP Services',],crosshair: true},"
    myreturn+="yAxis: {min: 0,title: {text: 'correlation rate'}},"
    myreturn+="tooltip: {headerFormat: '<span style=%s>{point.key}</span><table>',pointFormat: '<tr><td style=%s>{series.name}: </td>' +'<td style=%s><b>{point.y:.1f} mm</b></td></tr>',footerFormat: '</table>',shared: true,useHTML: true},"%("\"font-size:10px\"", "\"color:{series.color};padding:0\"", "\"padding:0\"")
    myreturn+="plotOptions: {column: {pointPadding: 0.2,borderWidth: 0}},series: [{name: 'self',data: [100]}, {name: 'avg',data: [78.8]}, {name: 'max',data: [39.3]}, {name: 'min',data: [57.4]        }]});});    </script>"
    return myreturn


def addHead():
    myreturn = ""
    myreturn += "<html lang=%s><head><meta charset=%s><meta http-equiv=%s content=%s>"%("\"en\"", "\"utf-8\"", "\"X-UA-Compatible\"", "\"IE=edge\"")
    myreturn += "<meta name=%s content=%s><title>Stock Analysis</title>"%("\"viewport\"", "\"width=device-width, initial-scale=1\"")
    myreturn += "<link href=%s rel=%s><link href=%s rel=%s>"%("\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css\"", "\"stylesheet\"", "\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap-theme.min.css\"", "\"stylesheet\"")
    # myreturn += "<link href=%s rel=%s><link href=%s rel=%s>"%("../web_beautify/css/bootstrap.min.css", "stylesheet", "../web_beautify/css/customized.css", "stylesheet")
    myreturn += "<script src=%s></script><script src=%s></script>"%("\"https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js\"", "\"https://oss.maxcdn.com/respond/1.4.2/respond.min.js\"")
    myreturn += "<script type=%s></script></head>"%("text/javascript")

    return myreturn
def addTail(superList):
    global static_path
    # print "superList:\n%s"%superList
    myreturn = ""
    myreturn += "<script src=%s></script>"%("\"https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js\"")
    myreturn += "<script src=%s></script>"%("\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js\"")
    myreturn += "<script src=%s></script>"%("//code.jquery.com/jquery-1.11.2.min.js")
    myreturn += "<script src=%s></script>"%("\"http://code.highcharts.com/highcharts.js\"")
    myreturn += plot(superList)
    # myreturn += "<script src=%s></script>" %("./js/2c.js")
    # %("//web_beautify/js/2c.js")
    return myreturn

def top10String(sorted_List, title, addlink):        
    outputStr = "<div><h1>%s</h1><table>" % title
    # outputStr = "<th>Correlation Score</th>"+outputStr
    for (industry, count) in sorted_List[:10]:
        if addlink:
            url = "http://finance.yahoo.com/q?s=%s&fr=uh3_finance_web&uhb=uhb2" % industry
            outputStr+="<tr><td><a href=%s>%s:</a></td><td>%s</td></tr>" %(url,industry, count)
            # outputStr += '<a href=%s>%s</a>: %s<br>' % (url, industry, str(count))
        else:
            outputStr+="<tr><td>%s:</td><td>%s</td></tr>" %(industry, count)
            
            # outputStr+= industry + ":\t" + str(count) + "<br>"
    

    outputStr += "</table></div>"
    # outputStr += "<div id=%s style=%s></div>"%("\"container1\"", "\"width:70%; height:300px;\"")
    
    return outputStr




class Application(tornado.web.Application):
    def __init__(self, server):
        global static_path
        if(server == 'indexServer'):            
            handlers = [
                (r"/", HomeHandler),            
                (r"/index", idxSearchHandler),
                (r'/(.*)', web.StaticFileHandler, {'path': "web_beautify/js/2c.js"})
            ]        
        elif (server == 'docServer'):            
            handlers = [
                (r"/", HomeHandler),            
                (r"/doc", docSearchHandler),
                (r'/(.*)', web.StaticFileHandler, {'path': "web_beautify/js/2c.js"})
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
        superList = []
        
        #IndustryCorrelation            
        try:
            mydict = eval(IndustryCorrelation[myquery.upper()])
            sorted_List = sorted(mydict.items(), key=operator.itemgetter(1), reverse=True)        
            superList.append(sorted_List[:10])
            OutputStr.append(top10String(sorted_List, "Top10 related industry to your stock", False))
            
            OutputStr.append("<div id=%s style=%s></div>"%("\"container0\"", "\"width:70%; height:300px;\""))
        except:
            print "first"
            OutputStr.append("Stock not found in system"  )
            
        #price_correlation            
        try:
            mydict = price_correlation[myquery.upper()]
            superList.append(mydict['top20'][:10])
            superList.append(mydict['worst20'][:10])
            
            OutputStr.append(top10String(mydict['top20'], "Top10 related stocks to your stock", True))
            OutputStr.append("<div id=%s style=%s></div>"%("\"container1\"", "\"width:70%; height:300px;\""))
            
            OutputStr.append(top10String(mydict['worst20'], "Worst10 related stocks to your stock", True))            
            OutputStr.append("<div id=%s style=%s></div>"%("\"container2\"", "\"width:70%; height:300px;\""))

        except:
            print "second"
            OutputStr.append("Stock not found in system"  )

        #NEWSCorrelation
        try:
            match = NEWSCorrelation[myquery.upper()]
            sorted_List = sorted(match, key=lambda tup: tup[1], reverse=True)
            superList.append(sorted_List[:10])
            OutputStr.append(top10String(sorted_List, "Top10 related NEWScorrelation to your stock",True))            
            OutputStr.append("<div id=%s style=%s></div>"%("\"container3\"", "\"width:70%; height:300px;\""))
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


        body = '<body>'
        for eachItem in OutputStr:
            body+=eachItem 
        result=addHead()+body+addTail(superList)+'</body></html>'        
        print result
        fo = open("./web_beautify/myindex.html", "wb")
        fo.write(result);
        fo.close()
        self.write(result)
        

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
        
        
        
        
        self.app = tornado.httpserver.HTTPServer(Application(serverType) )        
