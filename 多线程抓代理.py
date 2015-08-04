#coding:utf-8

import urllib2
import re
import threading
import time
import random

rawProxyList = []
checkedProxyList = []
imgurl_list = []



#抓取代理网站
#高匿代理：http://proxy.com.ru/gaoni/list_%d.html
#http://proxy.com.ru/gaoni/list_2.html
#
targets = []
for i in xrange(1, 4):
    target = r"http://www.xici.net.co/nn/%d" % i
    targets.append(target)
print targets



#获取代理的类
#子类化Thread类，定制线程对象
class ProxyGet(threading.Thread):
    def __init__(self,target):
        threading.Thread.__init__(self)
        self.target = target

    def getProxy(self):
        print u"代理服务器目标网站： " + self.target + '\n'
        req = urllib2.urlopen(self.target, timeout = 20)
        result = req.read().decode("utf-8")
        #print result
	    #匹配IP，端口，地址     .*?<td>(\d{1,5})</td>.*?<td>高匿</td>.*?<td>HTTP</td>    <td>8123</td>     .*?<td>HTTP</td>
        matchs  = re.findall(r'<tr class="\w{0,3}">(.*?)</tr>', result,re.S)
        for string in matchs:
            string = string.replace(' ', '').replace('\n', '').replace('</td>', '|')
            string = re.sub(r'</?[^>]+>', '', string)[2:].split('|')
            if string[4] == 'HTTP': 
                proxy = [string[0], string[1]]
                print proxy
                rawProxyList.append(proxy)

    def run(self):
        self.getProxy()

#检验代理的类
class ProxyCheck(threading.Thread):
    def __init__(self,proxyList):
        threading.Thread.__init__(self)
        self.proxyList = proxyList
        self.timeout = 5
	#测试段，testStr是成功打开testUrl后网页内容的一部分
        self.testUrl = "http://t.dianping.com/shanghai/"
        self.testStr = "31202063"

    def checkProxy(self):
        cookies = urllib2.HTTPCookieProcessor()
        for proxy in self.proxyList:
            proxyHandler = urllib2.ProxyHandler({"http" : r'http://%s:%s' %(proxy[0],proxy[1])})
            print r'http://%s:%s' %(proxy[0],proxy[1])
            opener = urllib2.build_opener(cookies,proxyHandler)
            opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0')] 
            #urllib2.install_opener(opener)
            t1 = time.time()

            try:
                #req = urllib2.urlopen("http://www.baidu.com", timeout=self.timeout)
                req = opener.open(self.testUrl, timeout=self.timeout)
                print "urlopen is ok...."
                result = req.read()
                print "read html...."
                timeused = time.time() - t1
                pos = result.find(self.testStr)
                print "pos is %s" %pos

                if pos > 1:
                    checkedProxyList.append((proxy[0],proxy[1],proxy[2],timeused))
                    #print "ok ip: %s %s %s %s" %(proxy[0],proxy[1],proxy[2],timeused)
                else:
                     continue
            except Exception,e:
                #print e.message
                continue

    def run(self):
        self.checkProxy()





if __name__ == "__main__":
    getThreads = []
    checkThreads = []
    #imgurlList('http://www.ivsky.com')
    #getPicThreads = []

#对每个目标网站开启一个线程负责抓取代理
for i in range(len(targets)):
    t = ProxyGet(targets[i])
    getThreads.append(t)

for i in range(len(getThreads)):
    getThreads[i].start()

for i in range(len(getThreads)):
    getThreads[i].join()

print '.'*10+"总共抓取了%s个代理" %len(rawProxyList) +'.'*10


#开启20个线程负责校验，将抓取到的代理分成20份，每个线程校验一份
for i in range(5):
    t = ProxyCheck(rawProxyList[((len(rawProxyList)+4)/5) * i:((len(rawProxyList)+4)/5) * (i+1)])
    checkThreads.append(t)

for i in range(len(checkThreads)):
    checkThreads[i].start()

for i in range(len(checkThreads)):
    checkThreads[i].join()

print '.'*10+"总共有%s个代理通过校验" %len(checkedProxyList) +'.'*10

#代理持久化，写入txt
f = open("proxy_list.txt",'w+')
for proxy in checkedProxyList:
    f.write("%s:%s\n"%(proxy[0],proxy[1]))
f.close()

#测试写入是否成功
list1 = []
f = open("proxy_list.txt", "r")
for line in f.readlines():
    list1.append(line.strip('\n'))
print list1
