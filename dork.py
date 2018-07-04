#!/usr/bin/python3

from urllib import parse
from queue import Queue
import threading
import argparse
import requests
import signal
import time
import sys
import re

mutex  =  threading.RLock()
sig = threading.Event()

existsurl = []
is_exit = False

MAXSIZE = 1000000

baiduUserAgent = 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)'
googleUserAgent = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
browserUserAgent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'
bingUserAgent = 'Mozilla/5.0 (compatible;+bingbot/2.0;++http://www.bing.com/bingbot.htm)'

def parse_url(url):
    return url.replace('http://','') + '/'

def print_info_text(print_text):
    print('\033[1;34m[*]\033[0m ' + print_text)

def print_success_text(print_text):
    print('\033[1;32m[+]\033[0m ' + print_text)

def print_error_text(print_text):
    print('\033[1;31m[-]\033[1;0m ' + print_text)

def print_other_text(print_text):
    print('\033[1;33m[!]\033[0m ' + print_text)

class MultiThread(threading.Thread):
    global is_exit
    def __init__(self, url, queue, method, keyword, cookie, spider):
        threading.Thread.__init__(self)
        self.sharedata = queue
        self.url = url
        self.method = method
        self.keyword = keyword
        self.cookie = cookie
        self.spider = spider

    def run(self):
        T1 = time.time()
        while self.sharedata.qsize() > 0:
            if is_exit:
                print_other_text(self.getName() + ' Received a Exit Signal!')
                sys.exit()
            else:
                murl = self.url + self.sharedata.get()
                while murl.find('//') != -1:
                    murl = murl.replace('//','/')
                murl = 'http://' + murl
                startscan(murl, self.getName(), self.method, self.keyword, self.cookie, self.spider)

def sigquit(a, b):
    global is_exit
    is_exit = True
    sys.exit()

def startscan(url, ThreadName, method, keyword, cookie, spider):
    if method.lower() == 'head':
        headscan(url, ThreadName, cookie, spider)
    elif method.lower() == 'get':
        getscan(url, ThreadName, keyword, cookie, spider)
    else:
        print_info_text('Wrong Method! Please Check it! [Only Get Or Head] ')
        sys.exit()

def defineUserAgent(spider):
        if spider == 'browser':
            StrUserAgent = browserUserAgent
        elif spider == 'google':
            StrUserAgent = googleUserAgent
        elif spider == 'baidu':
            StrUserAgent = baiduUserAgent
        elif spider == 'bing':
            StrUserAgent = bingUserAgent
        else:
            StrUserAgent = browserUserAgent

        return StrUserAgent

def headscan(url, ThreadName, cookie, spider):
        StrUserAgent = defineUserAgent(spider)
        reg  =  {
	        'User-Agent':StrUserAgent,
	        'Accept':'text/html,application/xhtml+xml,application/xml;q = 0.9,*/*;q = 0.8',
	        'Accept-Language':'zh-cn,zh;q = 0.5',
	        'Referer':url,
	        'Cookie':cookie,
	        'Accept-Encoding':'gzip, deflate'
	    }
        try:
            response = requests.head(url, headers=reg)

        except requests.exceptions.InvalidSchema as e:
            RtnCode = 'URL Error'
        except requests.exceptions.ConnectTimeout as e:
            RtnCode = 'Time Out'
        except requests.exceptions.ConnectionError as e:
            RtnCode = 'Connect Error'
        else:
            RtnCode = response.status_code

        if mutex.acquire(1):

             if RtnCode == 200 or RtnCode == 403  or RtnCode == 301 or RtnCode == 302 or RtnCode == 500 or RtnCode == 400  or RtnCode == 401:
                existsurl.append(str(RtnCode) + '\t' + url)
                print_success_text(str(RtnCode) + '\t' + ThreadName + ' -> ' + url)
             else:
                 print_error_text(str(RtnCode) + '\t' + ThreadName + ' -> ' + url)
             mutex.release()

def getscan(url, ThreadName, keyword, cookie, spider):
        global setcolor
        StrUserAgent = defineUserAgent(spider)
        reg  =  {
	        'User-Agent':StrUserAgent,
	        'Accept':'text/html,application/xhtml+xml,application/xml;q = 0.9,*/*;q = 0.8',
	        'Accept-Language':'zh-cn,zh;q = 0.5',
	        'Referer':url,
	        'Cookie':cookie,
	        'Accept-Encoding':'gzip, deflate'
	    }

        try:
	        response = requests.get(url, headers=reg)

        except requests.exceptions.InvalidSchema as e:
            RtnCode = 'URL Error'
        except requests.exceptions.ConnectTimeout as e:
            RtnCode = 'Time Out'
        except requests.exceptions.ConnectionError as e:
            RtnCode = 'Connect Error'
        else:
            RtnCode = response.status_code

            if keyword is not None:
                page_content = response.text
                if  page_content.find(keyword) != -1:
                    RtnCode = 404

        if mutex.acquire(1):

             if RtnCode == 200 or RtnCode == 403  or RtnCode == 301 or RtnCode == 302 or RtnCode == 500  or RtnCode == 400  or RtnCode == 401:
                existsurl.append(str(RtnCode) + '\t' + url)
                print_success_text(str(RtnCode) + '\t' + ThreadName + ' -> ' + url)
             else:
                 print_error_text(str(RtnCode) + '\t' + ThreadName + ' -> ' + url)
             mutex.release()

def readdic(path):
    codes = list()
    fp = open(path,'r', encoding='utf-8')
    testcodes = fp.readlines()
    for testcode in testcodes[0:MAXSIZE]:
        testcode = testcode.replace('\r','')
        testcode = testcode.replace('\n','')
        testcode.strip()
        codes.append(testcode)

    fp.close()
    return list(set(codes))

def social(url):
    Surl = []
    Sext = ['.rar','.zip','.tar','.gz','.tar.gz','.tgz','.tar.Z','.bz','.bz2','.7z']
    Suname = ['www','wwwroot','root','html','data','db','site','web','back','databack','backup','databackup',
            'webroot','bak','beifen','database','wangzhan''upload','file']
    while url.find('/') != -1:
        url = url.replace('/','')
    Purl = url.split('.')
    length = len(Purl)
    for uinfo in Purl:
        Suname.append(uinfo)
    url3 = ''
    for i in range(length):
        url3 += Purl[i]
    Suname.append(url3)
    if length == 3:
        Suname.append(Purl[0] + Purl[1])
        Suname.append(Purl[1] + Purl[2])

    Suname = list(set(Suname))
    for uname in Suname:
            for ext in Sext :
                    Surl.append(uname + ext)
    return Surl

def banner():
    print('''\033[1;93m
              ___   
 ____        __H__
|    \ ___ ___|\033[41m.\033[0m\033[1;93m|__  \033[1;97m{\033[90m1.0#stable\033[1;97m}\033[1;93m
|  |  | . |  _|\033[41m.\033[0m\033[1;93m|_/
|____/|___|_| |\033[41m.\033[0m\033[1;93m|_\\
               V     \033[0m\033[4;37mexp10it.cn\033[0m
      
        ''')

if __name__ == '__main__':
    parser  =  argparse.ArgumentParser(usage=banner())
    parser.add_argument('-u', help='Target URL', dest='url', metavar='<URL>', required=True)
    parser.add_argument('-m', help='Use method', dest='method', metavar='GET HEAD', default='HEAD')
    parser.add_argument('-f', help='Dictionary file', dest='file', metavar='<PATH>', required=True)
    parser.add_argument('-t', help='Threads number', dest='threads', metavar='THREADS', type=int, default=5)
    parser.add_argument('-k', help='Custom Not Found keyword', dest='keyword', metavar='keyword')
    parser.add_argument('-c', help='Custom cookie', dest='cookie', metavar='cookie', default='hello_the_world')
    parser.add_argument('-s', help='Use spider\'s User-Agent', dest='spider', metavar='spider', default='browser')
    args = parser.parse_args()

    url = parse_url(args.url)
    THS = []
    Surl = social(url)
    pathqueue = Queue(MAXSIZE + len(Surl))

    dics = readdic(args.file)
    if len(dics) < 1 :
        print_info_text('The dic file is empty,check your dic!')
        sys.exit()
    print_info_text('Loading dic successfully')
    time.sleep(1)
    for uinfo in Surl:
        dics.append(uinfo)
    dics = list(set(dics))
    print_info_text('Cutting off the same rows')
    time.sleep(1)
    for info in dics :
         pathqueue.put(parse.quote(info))

    print_info_text('There are %s links will be scanned' % str(pathqueue.qsize()))
    time.sleep(1)
    signal.signal(signal.SIGINT,sigquit)
    signal.signal(signal.SIGTERM,sigquit)
    for i in range(args.threads):
        Th = MultiThread(url,pathqueue,args.method,args.keyword,args.cookie,args.spider)
        THS.append(Th)
        Th.start()

    while  threading.active_count() > 1:
        time.sleep(3)
    if len(existsurl) > 0:
        print_info_text('Scan Result')
        for urls in existsurl:
            print_success_text(urls)
    else:
        print_info_text('Oops,No Result!')
    print_info_text('ALL Threads have done! Main Thread exit!')
    print_info_text('Scan over!')