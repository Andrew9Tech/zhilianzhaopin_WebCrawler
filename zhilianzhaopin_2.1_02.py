#coding=utf-8
#   程序：智联招聘爬虫
#   版本：2.1
#   作者：andrew9tech
#   日期：2015-2-15
#   语言：Python 2.7
#   操作：改写！
#        启用requests模块，弃用urllib\urllib2\cookielib
#        以后优选requests模块
#   功能：
#---------------------------------------
import re
import os
import random
import time
import requests

s = requests.Session()

YanZhengMaUrl = 'http://rd2.zhaopin.com/s/loginmgr/picturetimestamp.asp'
f = open('img1.gif', 'wb')
stream = s.get(YanZhengMaUrl).content
f.write(stream)
f.close()
text = raw_input('input yan zheng ma:')
print text

time1 = time.time()
#需要POST的数据#
postdata= {'username':'zhang_huaxiu','password':'wwwhuihui','Validate':text,'Submit':''}
#伪装成浏览器，加入headers
headers = {
    'Accept-Encoding':'gzip,deflate',
    'Content-Type':'application/x-www-form-urlencoded',
    'Origin':'http://rd2.zhaopin.com',
    'Referer':'http://rd2.zhaopin.com/portal/myrd/regnew.asp?za=2',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36'
    }
#自定义一个请求
url = 'http://rd2.zhaopin.com/loginmgr/loginproc.asp?DYWE=Date.parse(new%20Date())'
#访问该链接#
response = s.post(url, data=postdata, headers=headers)
#判断头文件信息，包含数据是否用gzip传输,
#print response.headers

#简历搜索页面
#ResumeUrlBase = 'http://rd.zhaopin.com/resumepreview/resume/viewone/2/JM252345566R90250000000_1_1?searchresume=1'
#response = s.get(ResumeUrlBase, hesders=headers)
#判断头文件信息，包含数据是否用gzip传输
#print response.headers
  


School = u"南京大学"
ResumeSerNum = []
f = open(u"H:\\Resume_ID_storage\\江苏\\" + School + "_Deduplication.txt", "r+")
for line in f.readlines():
    ResumeSerNum.append(line.strip('\n'))
print len(ResumeSerNum)
f.close()
#-----------------------------------
#异常恢复记录文件读取
#------------------------------------
if(os.path.isfile("Breakpoints_log.txt")):
    f = open("Breakpoints_log.txt", 'r')
    line = f.readlines()
    ReadLogData = line[0].strip('\n')
    print ReadLogData
else:
    ReadLogData = 0

Logerror =0; Neterror = 0;Counter = 0;NoneTypeNum = 0;
ResumeUrlBase = 'http://rd.zhaopin.com/resumepreview/resume/viewone/2/'

for i in range(int(ReadLogData),len(ResumeSerNum)):
    FinaResumeUrl = ResumeUrlBase + str(ResumeSerNum[i]) + '_1?searchresume=1'
    try:
        #易网络访问出错行
        second = random.uniform(0, 0.99)
        time.sleep(second)
        if Counter == 10:
            time.sleep(0.8); Counter = 0
        Page = s.get(FinaResumeUrl, headers=headers).content
    except Exception as e1:
        try:
            second = random.uniform(0, 0.8)
            time.sleep(second)
            if Counter == 10:
                time.sleep(0.8); Counter = 0
            Page = s.get(FinaResumeUrl,  headers=headers).content
        except Exception as e2:
            print ResumeSerNum[i] + u"Download failed，save in _UnDownload.txt"
            print e2
            Neterror = Neterror + 1
            f = open(School + "_UnDownload.txt",'a+')
            f.write("%s\n" %ResumeSerNum[i])
            f.close()
            if (Neterror == 10):
                print "Network Error!"
                break

    Counter = Counter + 1

    flag = u"个人信息"
    try:
        data = str(re.search('<body>(.*?)</body>',Page,re.S).group(0))
    except Exception as e3:
        print u"AttributeError: 'NoneType' object has no attribute 'group'"
        NoneTypeNum = NoneTypeNum + 1
        continue
    if flag.encode("utf-8") in data:
        path = u"H:\\Detail_Resume\\江苏\\" + School +"\\"+ str(ResumeSerNum[i][0:2]) + "\\" + str(ResumeSerNum[i][0:5]) + "\\" + str(ResumeSerNum[i][0:8]) + "\\" + str(ResumeSerNum[i][0:11])

        # 去除首位空格、尾部 \ 符号
        path=path.strip().rstrip("\\")
        # 判断路径是否存在
        isExists=os.path.exists(path)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            print path+ " Creat Successfully!!"
            # 创建目录操作函数
            os.makedirs(path)
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print path+ u" Directory already exists!"

        f = open(path + "\\" + ResumeSerNum[i] + '.html', 'w+')
        f.writelines(data)
        f.close()
        print 'Report：File has been downloaded and stored into a local html file!!'
        print '\n'
    elif u"该简历已被求职者删除，无法查看!".encode("utf") in data:
        continue
    elif(Logerror == 10):
        print "It has been reached today's download limitation"
        break
    else:
        Logerror = Logerror + 1

print "Download failed breakpoint：",(i)
f = open("Breakpoints_log.txt",'w+')
f.write("%s\n"%str(i-10))
f.close()

time2 = time.time()
timecost = time2 - time1
print "timecost:", timecost


    
