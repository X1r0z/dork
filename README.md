# dork everything

```
              ___   
 ____        __H__
|    \ ___ ___|.|__  {1.0#stable}
|  |  | . |  _|.|_/
|____/|___|_| |.|_\
               V     exp10it.cn
```

## usage

```
usage: dork.py [-h] -u <URL> [-m GET HEAD] -f <PATH> [-t THREADS] [-k keyword]
               [-c cookie] [-s spider]

optional arguments:
  -h, --help   show this help message and exit
  -u <URL>     Target URL
  -m GET HEAD  Use method
  -f <PATH>    Dictionary file
  -t THREADS   Threads number
  -k keyword   Custom Not Found keyword
  -c cookie    Custom cookie
  -s spider    Use spider's User-Agent
```

## Example

```
./dork.py -u www.test.com -f dict/DIR.txt
./dork.py -u www.test.com -m GET -k '404' -f dict/DIR.txt
./dork.py -u www.test.com -m HEAD -c 'isLogin=1' -s baidu -f dict/DIR.txt
```
