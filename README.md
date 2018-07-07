# dork everything

dork 是一款 Web 目录爆破工具.

```
              ___   
 ____        __H__
|    \ ___ ___|.|__  {1.2#stable}
|  |  | . |  _|.|_/
|____/|___|_| |.|_\
               V     exp10it.cn
```


## feature

支持 GET/POST/HEAD 三种请求方式

自定义 Cookie, Referer, 404 keyword

根据域名组合字典 (备份)

随机 IP, User-Agent

延时时间 (bypass)

## usage

```
usage: dork.py [-h] -u <URL> [-m HEAD GET POST] -f <PATH> [-t THREADS]
               [-k keyword] [-c cookie] [-r referer] [-d second] [-s] [-a]
               [-i]

optional arguments:
  -h, --help        show this help message and exit
  -u <URL>          Target URL
  -m HEAD GET POST  Use method
  -f <PATH>         Dictionary file
  -t THREADS        Threads number
  -k keyword        Not Found keyword
  -c cookie         Custom Cookie
  -r referer        Custom Referer
  -d second         Delay Time (second)
  -s                Use Social Engineering Mode
  -a                Use Random User-Agent
  -i                Use Random IP

```

## Example

```
./dork.py -u www.test.com -f dict/DIR.txt
./dork.py -u url.txt -f dict/DIR.txt -t 5
./dork.py -u www.test.com -m GET -k '404' -f dict/DIR.txt
./dork.py -u www.test.com -m POST -d 1 -t 1 -s -a -i -f dict/DIR.txt
./dork.py -u www.test.com -m HEAD -c 'isLogin=1' -r 'https://www.google.com/' -f dict/DIR.txt
```

## Other

程序代码开头定义了默认的 user-agent, ip, cookie, referer, prefix, code

```
user_agent = 'Dork v1.2#stable (https://github.com/X1r0z/dork)'
user_ip = '127.0.0.1'
cookie = 'hello=world'
referer = 'https://www.baidu.com/'
prefix = 'http://'
code = [200, 301, 302, 403, 500]
```

程序默认支持 `-u www.test.com` 和 `-u http://www.test.com` 两种方式.

如果使用第一种方式, 则 url 为 `http://www.test.com` (`prefix + url`)

*建议扫描 https 站点时使用第二种方式, 或更改 prefix*