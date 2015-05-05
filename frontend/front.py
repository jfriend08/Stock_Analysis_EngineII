import tornado.httpserver
import tornado.ioloop
import tornado.web
import hashlib
import socket
import getpass

import json

from tornado.httpclient import AsyncHTTPClient
from tornado import gen
from tornado.options import define, options
import tornado.web as web
from tornado.template import Loader

from constants import color
bcolors = color.bcolors()

# ## collecting four available ports
ports=[]
ports_index = []
ports_Doc = []

# base = str("<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1"><!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags --><title>Bootstrap 101 Template</title><!-- Bootstrap --><link href="web_beautify/css/bootstrap.min.css" rel="stylesheet"><link href="web_beautify/css/customized.css" rel="stylesheet"><script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script><script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script><script type="text/javascript"></script></head><body>%s</body></html>")

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),            
            (r"/search", SearchHandler),
            (r'/(.*)', web.StaticFileHandler, {'path': "web_beautify/js/2c.js"}),
            (r'/(\d{4})/(\d{2})/(\d{2})/([a-zA-Z\-0-9\.:,_]+)/?', DetailHandler)            
        ]        
        tornado.web.Application.__init__(self, handlers)

class SearchHandler(tornado.web.RequestHandler):
    @gen.coroutine            
    def get(self):
        
        K=10
        myquery = self.request.uri        
        print "\n" + bcolors.HEADER + '====== OPERATION RECORD ======'+ bcolors.ENDC    
        print bcolors.LIGHTBLUE + "Searching query: " + myquery + bcolors.ENDC
        # fetching index server
        doc_list=[]
        for i in range(len(ports_index)):            
            toFetch=str(ports_index[i]) + str(myquery.replace('/search?', '/index?'))
            # toFetch="http://linserv2.cims.nyu.edu:" + str(ports_index[i]) + str(myquery.replace('search', 'index'))
            print bcolors.LIGHTBLUE + "Fetching index server " + toFetch + bcolors.ENDC
            http_client = AsyncHTTPClient()                                
            tmp_response = yield http_client.fetch(toFetch)                        


        # self.write("Hi")
        self.write(tmp_response.body)        
        # self.write(loader.load("myindex.html"))
        # self.render("../web_beautify/myindex.html")
            # self.render("../web_beautify/demo1.html")
            
            # self.render("../web_beautify/demo1.html" )
            # report = base % tmp_response.body
            # self.write(report)

            # n=json.loads(tmp_response.body)                        
            # doc_list.extend(n[n.keys()[0]])            

        
        # doc_list.sort(key=lambda x: x[1], reverse=True)
        # print bcolors.LIGHTBLUE + "Top" + str(K) + " doc_list after sorting: " + str(doc_list[0:10]) + bcolors.ENDC

        # # find the min number
        # minN= min(K,len(doc_list))

        # # fetching document server
        # report=[]
        # for i in range(min(K,len(doc_list))):                                                            
        #     toFetch=str(ports_Doc[doc_list[i][0] %3]) + "/doc?id=" + str(doc_list[i][0]) + "&" + str(myquery.replace('/search?', ''))
        #     # toFetch="http://linserv2.cims.nyu.edu:" + str(ports_Doc[doc_list[i][0] %3]) + "/doc?id=" + str(doc_list[i][0]) + "&" + str(myquery.replace('/search?', ''))
        #     print bcolors.LIGHTBLUE + "Fetching document server " + toFetch + bcolors.ENDC
        #     http_client = AsyncHTTPClient()                                
        #     tmp_response = yield http_client.fetch(toFetch)
        #     n=json.loads(tmp_response.body)                        
        #     report.extend(n[n.keys()[0]])

        # # make the final report
        # final = {"numResults":minN, "results":report}
        # self.write(json.dumps(final))

count=0
class HomeHandler(tornado.web.RequestHandler):
    @gen.coroutine     
    def get(self):    	
    	global count        
        self.render("../web_beautify/demo1.html")
        # self.write("Reflesh Count:" + str(count))
        count=count+1

class DetailHandler(tornado.web.RequestHandler):
    def get(self, year, month, day, slug):
        self.write("DetailHandler:" + str(slug))

class FrontEndApp(object):
    def __init__(self, Idxservers, Docservers):
        global ports_index, ports_Doc
        ports_index = Idxservers
        ports_Doc = Docservers
        self.app = tornado.httpserver.HTTPServer(Application() )        



# def main():
# 	global ports
# 	tornado.options.parse_command_line()
# 	http_server = tornado.httpserver.HTTPServer(Application() )
# 	http_server.listen(ports[0])
# 	tornado.ioloop.IOLoop.instance().start()

# if __name__ == "__main__":        
# 	main()




