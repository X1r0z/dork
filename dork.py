#!/usr/bin/python3

from random import choice
from urllib import parse
from queue import Queue
import threading
import argparse
import requests
import random
import signal
import time
import sys

user_agent = 'Dork v1.4#stable (https://github.com/X1r0z/dork)'
user_ip = '127.0.0.1'
cookie = 'hello=world'
referer = 'https://www.baidu.com/'
prefix = 'http://'
code = [200, 301, 302, 403, 500]

mutex  =  threading.RLock()
sig = threading.Event()
flag = False

class MultiThread(threading.Thread):
    def __init__(self, queue, urls, method, keyword, delay, timeout, headers):
        threading.Thread.__init__(self)
        self.queue = queue
        self.urls = urls
        self.method = method
        self.keyword = keyword
        self.delay = delay
        self.timeout = timeout
        self.headers = headers

    def run(self):
        while not self.queue.empty():
            if flag:
                print_text('Recevied a Exit Signal!', 'warning')
                sys.exit()
            path = self.queue.get()
            for url in self.urls:
                murl = join_url(url) + path
                url = parse_url(url)
                self.headers.update(random_ua())
                self.headers.update(random_ip())
                startscan(murl, url, self.method, self.keyword, self.timeout, self.headers)
                delay(self.delay)

def startscan(murl, url, method, keyword, timeout, headers):
    if method.lower() == 'head':
        headscan(murl, url, timeout, headers)
    elif method.lower() == 'get':
        getscan(murl, url, keyword, timeout, headers)
    elif method.lower() == 'post':
        postscan(murl, url, keyword, timeout, headers)
    else:
        print_text('Wrong Method! Please Check it!', 'info')
        sys.exit()

def headscan(murl, url, timeout, headers):
    try:
        response = requests.head(murl, headers=headers, timeout=timeout)
        status_code = response.status_code
    except:
        status_code = 'Connect Error'
    if mutex.acquire(1):
         if status_code in code:
            existsurl[url].append(str(status_code) + '\t' + murl)
            print_text(str(status_code) + '\t' + ' -> ' + murl, 'success')
         else:
             print_text(str(status_code) + '\t' + ' -> ' + murl, 'error')
         mutex.release()

def getscan(murl, url, keyword, timeout, headers):
    try:
        response = requests.get(murl, headers=headers, timeout=timeout)
        status_code = response.status_code
        if keyword is not None:
            if response.text.find(keyword) != -1:
                status_code = 404
    except:
        status_code = 'Connect Error'

    if mutex.acquire(1):
         if status_code in code:
            existsurl[url].append(str(status_code) + '\t' + murl)
            print_text(str(status_code) + '\t'  + ' -> ' + murl, 'success')
         else:
             print_text(str(status_code) + '\t' + ' -> ' + murl, 'error')
         mutex.release()

def postscan(murl, url, keyword, timeout, headers):
    try:
        response = requests.post(murl, headers=headers, timeout=timeout)
        status_code = response.status_code
        if keyword is not None:
            if response.text.find(keyword) != -1:
                status_code = 404
    except:
        status_code = 'Connect Error'

    if mutex.acquire(1):
         if status_code in code:
            existsurl[url].append(str(status_code) + '\t' + murl)
            print_text(str(status_code) + '\t' + ' -> ' + murl, 'success')
         else:
             print_text(str(status_code) + '\t' + ' -> ' + murl, 'error')
         mutex.release()

def sigquit(a, b):
    global flag
    flag = True
    sys.exit()

def readdic(filename):
    dics = list()
    for line in open(filename,'r', encoding='utf-8'):
        line = line.strip()
        if line[0] != '/':
            line = '/' + line
        dics.append(line)
    return list(set(dics))

def delay(sec):
    time.sleep(sec)

def social(url):
    sname = ('bak', 'backup', 'www', 'web', 'wwwroot', 'webroot', 'root', 'html', 'site', 'beifen', 'ftp', 'website', 'back', 'databack', 'backupdata', 'databackup', 'temp', 'htdocs', 'database', 'data', 'user', 'admin', 'test', 'conf', 'config', 'db', 'wangzhan', 'upload', 'file', 'sql', 'install')
    surl = (url, url.replace('.', ''), url.split('.', 1)[1], url.split('.', 1)[1].replace('.', ''), url.split('.', 1)[0], url.split('.')[1], '.'.join(url.split('.')[:-1]), ''.join(url.split('.')[:-1]), url.split('.')[-1])
    ext = ('.rar', '.zip', '.tar', '.tar.gz', '.tar.bz2', '.tar.xz', '.gz', '.bz2', '.xz', '.tgz', '.7z', '.z')
    dic = []
    for e in ext:
        for s in surl:
            dic.append('/' + s + e)
        for n in sname:
            dic.append('/' + n + e)
    dic = list(set(dic))
    return dic

def random_ua():
    uas = [
    'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html）',
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html) ',
    'Googlebot/2.1 (+http://www.googlebot.com/bot.html)',
    'Googlebot/2.1 (+http://www.google.com/bot.html)',
    'Mozilla/5.0 (compatible; Yahoo! Slurp China; http://misc.yahoo.com.cn/help.html”)',
    'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp”)',
    'iaskspider/2.0(+http://iask.com/help/help_index.html”)',
    'Mozilla/5.0 (compatible; iaskspider/1.0; MSIE 6.0)',
    'Sogou web spider/3.0(+http://www.sogou.com/docs/help/webmasters.htm#07″)',
    'Sogou Push Spider/3.0(+http://www.sogou.com/docs/help/webmasters.htm#07″)',
    'Mozilla/5.0 (compatible; YodaoBot/1.0; http://www.yodao.com/help/webmaster/spider/”; )',
    'msnbot/1.0 (+http://search.msn.com/msnbot.htm”)',
    'Mozilla/5.0 (Linux;u;Android 4.2.2;zh-cn;)',
    'AppleWebKit/534.46 (KHTML,like Gecko) Version/5.1 Mobile Safari/10600.6.3',
    '(compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html）',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36 OPR/37.0.2178.32',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 BIDUBrowser/8.3 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.9.2.1000 Chrome/39.0.2146.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36 Core/1.47.277.400 QQBrowser/9.4.7658.400',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 UBrowser/5.6.12150.8 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.154 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36 TheWorld 7'
    ]
    if args.ua:
        ua = choice(uas)
    else:
        ua = user_agent

    headers = {
            'User-Agent': ua
    }
    return headers

def random_ip():
    if args.ip:
        ip = '%s.%s.%s.%s' % (
        choice(range(255)),
        choice(range(255)),
        choice(range(255)),
        choice(range(255))
    )
    else:
        ip = user_ip
    headers = {
    'Client-IP': ip,
    'X-Client-IP': ip,
    'X-Real-IP': ip,
    'True-Client-IP': ip,
    'X-Originating-IP': ip,
    'X-Forwarded-For': ip,
    'X-Remote-IP': ip,
    'X-Remote-Addr': ip,
    'X-Forwarded-Host': ip
    }
    return headers

def parse_url(url):
    url = url.replace('http://', '').replace('https://', '')
    return url.split('/')[0]

def join_url(url):
    if url.find('://') == -1:
        return prefix + url
    else:
        return url

def print_text(text,level):
    if level == 'info':
        print('\033[1;34m[*]\033[0m ' + text)
    elif level == 'success':
        print('\033[1;32m[+]\033[0m ' + text)
    elif level == 'error':
        print('\033[1;31m[-]\033[1;0m ' + text)
    elif level == 'warning':
        print('\033[1;33m[!]\033[0m ' + text)
    else:
        raise Exception('Level Error')

def warning_message():
    print_text('Current status code: '+ ' '.join([str(c) for c in code]), 'warning')
    print_text('Time out: ' + str(args.timeout), 'warning')
    print_text('Delay Time: ' + str(args.delay), 'warning')
    print_text('Cookie: ' + cookie, 'warning')
    print_text('Referer: ' + referer, 'warning')
    if args.ua:
        print_text('Using Random User-Agent', 'warning')
    else:
        print_text('User-Agent: ' + user_agent, 'warning')
    if args.ip:
        print_text('Using Random IP', 'warning')
    else:
        print_text('IP: ' + user_ip, 'warning')
    if args.social:
        print_text('Using Social Engineering Mode', 'warning')

def banner():
    print('''\033[1;93m
              ___   
 ____        __H__
|    \ ___ ___|\033[41m.\033[0m\033[1;93m|__  \033[1;97m{\033[90m1.2#stable\033[1;97m}\033[1;93m
|  |  | . |  _|\033[41m.\033[0m\033[1;93m|_/
|____/|___|_| |\033[41m.\033[0m\033[1;93m|_\\
               V     \033[0m\033[4;37mexp10it.cn\033[0m
      
        ''')

if __name__ == '__main__':
    parser  =  argparse.ArgumentParser(usage=banner())
    parser.add_argument('-u', help='Target URL', dest='url', metavar='<URL>', required=True)
    parser.add_argument('-m', help='Use method', dest='method', metavar='HEAD GET POST', default='HEAD')
    parser.add_argument('-f', help='Dictionary file', dest='filename', metavar='<PATH>', required=True)
    parser.add_argument('-t', help='Threads number', dest='threads', metavar='THREADS', type=int, default=5)
    parser.add_argument('-k', help='Not Found keyword', dest='keyword', metavar='keyword', default='None')
    parser.add_argument('-c', help='Custom Cookie', dest='cookie', metavar='cookie', default=cookie)
    parser.add_argument('-r', help='Custom Referer', dest='referer', metavar='referer', default=referer)
    parser.add_argument('--delay', help='Delay Time', dest='delay', metavar='second', type=int, default=0)
    parser.add_argument('--timeout', help='Request Timeout', dest='timeout',metavar='second', type=int, default=3)
    parser.add_argument('--random-agent', help='Use Random User-Agent', dest='ua', action='store_true')
    parser.add_argument('--random-ip', help='Use Random IP', dest='ip', action='store_true')
    parser.add_argument('--social', help='Use Social Engineering Mode', dest='social', action='store_true')
    args = parser.parse_args()
    
    signal.signal(signal.SIGINT, sigquit)
    signal.signal(signal.SIGTERM, sigquit)

    queue = Queue()
    dics = readdic(args.filename)
    urls, existsurl = [], {}

    try:
        for line in open(args.url):
            url = line.strip()
            urls.append(url)
    except:
        urls.append(args.url)

    for url in urls:
        url = parse_url(url)
        if args.social:
            dics += social(url)
        existsurl[url] = []

    for path in dics:
         queue.put(parse.quote(path))

    headers = {
        'Cookie': args.cookie,
        'Referer': args.referer
    }

    print_text('Loading dic successfully', 'info')
    time.sleep(1)
    print_text('There are %s urls will be scanned' % str(len(urls)), 'info')
    print_text('There are %s paths will be scanned' % str(queue.qsize()), 'info')
    print()
    warning_message()
    print()
    time.sleep(1)

    for i in range(args.threads):
        t = MultiThread(queue, urls, args.method, args.keyword, args.delay, args.timeout, headers)
        t.start()

    while threading.active_count() > 1:
        time.sleep(1)

    for url in list(existsurl.keys()):
        print()
        if existsurl[url]:
            print_text('Scan Result for ' + url, 'info')
            for urls in existsurl[url]:
                print_text(urls, 'success')
        else:
            print_text('No Result for ' + url, 'info')
    
    print()
    print_text('Done!', 'info')