# -*- coding: utf-8 -*-
#---------------------------------------
#   程序：智联招聘爬虫
#   版本：2.1
#   作者：andrew9tech
#   日期：2015-1-12
#   语言：Python 2.7
#   操作：
#   功能：
#---------------------------------------
import os
import sys
import time
import urllib
import urllib2
import Verification_Code
import ResumeContentDownloadThread

reload(sys)   
sys.setdefaultencoding('utf8')


#---------------------------------------
#获取验证码及Cookie
#---------------------------------------
Url = 'http://rd2.zhaopin.com/s/loginmgr/picturetimestamp.asp'
ZhaoPin_Ver_Code = Verification_Code.Verification_Code_Pro()
ZhaoPin_Ver_Code.Install_Opener()
text = ZhaoPin_Ver_Code.Verification_Code_Input(Url)


time1 = time.time()
#---------------------------------------

#---------------------------------------
#需要POST的数据#
postdata=urllib.urlencode({
    'username':'zhang_shengjie',
    'password':'wwwhuihui',
    'Validate':text,
    'Submit':''
})
#伪装成浏览器，加入headers
headers = {
    'Content-Type':'application/x-www-form-urlencoded',
    'Origin':'http://rd2.zhaopin.com',
    'Referer':'http://rd2.zhaopin.com/portal/myrd/regnew.asp?za=2',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36'
    }
#自定义一个请求
req = urllib2.Request(
    url = 'http://rd2.zhaopin.com/loginmgr/loginproc.asp?DYWE=Date.parse(new%20Date())',
    data = postdata,
    headers = headers
)
#访问该链接#
response = urllib2.urlopen(req)
#输出当前url
cur_url =  response.geturl()
FinalPage = urllib2.urlopen(cur_url)


#简历搜索页面
SearchUrl = 'http://rdsearch.zhaopin.com'
response = urllib2.urlopen(SearchUrl)



#-------------------------------------
#
#
#
#-----------------------------------
School = [['%E8%A5%BF%E5%AE%89%E4%BA%A4%E9%80%9A%E5%A4%A7%E5%AD%A6','西安交通大学'],
          ['%E8%A5%BF%E5%8C%97%E5%B7%A5%E4%B8%9A%E5%A4%A7%E5%AD%A6','西北工业大学'],
          ['%E8%A5%BF%E5%8C%97%E5%86%9C%E6%9E%97%E7%A7%91%E6%8A%80%E5%A4%A7%E5%AD%A6','西北农林科技大学'],
          ['%E8%A5%BF%E5%8C%97%E5%A4%A7%E5%AD%A6','西北大学'],
          ['%E8%A5%BF%E5%AE%89%E7%94%B5%E5%AD%90%E7%A7%91%E6%8A%80%E5%A4%A7%E5%AD%A6','西安电子科技大学'],
          ['%E9%99%95%E8%A5%BF%E5%B8%88%E8%8C%83%E5%A4%A7%E5%AD%A6','陕西师范大学'],
          ['%E9%95%BF%E5%AE%89%E5%A4%A7%E5%AD%A6','长安大学'],
          ['%E8%A5%BF%E5%AE%89%E5%BB%BA%E7%AD%91%E7%A7%91%E6%8A%80%E5%A4%A7%E5%AD%A6','西安建筑科技大学'],
          ['%E9%99%95%E8%A5%BF%E7%A7%91%E6%8A%80%E5%A4%A7%E5%AD%A6','陕西科技大学'],
          #西安外国语学院加入西安外国语大学
          ['%E8%A5%BF%E5%AE%89%E5%A4%96%E5%9B%BD%E8%AF%AD%E5%A4%A7%E5%AD%A6','西安外国语大学'],
          ['%E8%A5%BF%E5%AE%89%E5%A4%96%E5%9B%BD%E8%AF%AD%E5%AD%A6%E9%99%A2','西安外国语学院']]
SchoolName = [['西安交通大学','陕西西安交通大学','西安交通大学兴庆校区','西安交通大学雁塔校区'],
              ['西北工业大学','陕西西北工业大学','西北工业大学友谊校区','西北工业大学长安校区'],
              ['西北农林科技大学','陕西西北农林科技大学','陕西省西北农林科技大学'],
              ['西北大学','陕西西北大学','陕西省西北大学','西安西北大学','西北大学太白校区','西北大学桃园校区','西北大学长安校区'],
              ['西安电子科技大学','陕西西安电子科技大学','陕西省西安电子科技大学'],
              ['陕西师范大学','陕西师范大学雁塔校区','陕西师范大学长安校区'],
              ['长安大学','陕西长安大学','陕西省长安大学','西安长安大学','西安市长安大学'],
              ['西安建筑科技大学','陕西西安建筑科技大学','陕西省西安建筑科技大学'],
              ['陕西科技大学'],
              #西安外国语学院加入西安外国语大学
              ['西安外国语大学','陕西西安外国语大学','陕西省西安外国语大学'],
              ['西安外国语学院','陕西西安外国语学院']]
ProvCity = ['548%3B530%3B556%3B552%3B535%3B536%3B539%3B544%3B540%3B549',
            '541%3B532%3B539%3B537%3B542%3B543%3B545%3B547%3B550%3B553',
            '554%3B557%3B558%3B551%3B561%3B562%3B534%3B559%3B538%3B531',
            '533%3B560%3B563%3B555']


Edu = [7, 9, 11, 13, 15, 16]
Age = range(16,36)
Industry=[['210500'],['160400'],['160000'],['160500'],
          ['160200'],['300100'],['160100'],['160600'],
          ['180000'],['180100'],['300500'],['300900'],['140000'],
          ['140100'],['140200'],['200300'],['200302'],
          ['201400'],['201300'],['300300'],['120400'],
          ['120200'],['170500'],['170000'],['300700'],
          ['201100'],['120800'],['121000'],['129900'],
          ['121100'],['121200'],['210600'],['120700'],
          ['121300'],['121500'],['300000'],['150000'],['301100'],
          ['121400'],['200600'],['200800'],['210300'],
          ['200700'],['130000'],['120500'],['130100'],['201200'],
          ['200100'],['120600'],['100000'],['100100'],['990000']]

Gender = [0, 1, 2]
#-----------------------------------
#异常恢复记录文件读取
#------------------------------------
if(os.path.isfile("Breakpoints_log.txt")):
    f = open("Breakpoints_log.txt", 'r')
    ReadLogData = []
    for line in f.readlines():
        ReadLogData.append(line.strip('\n'))
    print ReadLogData
else:
    ReadLogData = [0, 0, 0, 0, 0]

#a=b=c=1
for s in range(int(ReadLogData[0]), len(School)):
    time1 = time.time()
    for l in range(int(ReadLogData[1]), 3):
        print "l:",l
        for m in range(int(ReadLogData[2]), len(Age)):
            print "m", m
            for n in range(int(ReadLogData[3]), len(ProvCity)):
                print "n", n
                for g in range(0, 3):
                    print "g", g
                    #本代码任务属于IO密集型，应避免频繁访问网络，特做一下if处理
                    #本科生处理
                    if(l == 0):
                        if (m == 0):
                            if (n == 0) and (g == 0):
                                SearchEdu = "&SF_1_1_5=7%2C7"
                                SearchAge = "&SF_1_1_8=16%2C21"
                                SearchProvCity = ""
                                SearchGender = ""
                            elif (n != 0) or (g != 0):
                                continue
                        elif (0 < m < 6):
                            continue
                        elif (m > 5) and (g != 0):
                            SearchEdu = "&SF_1_1_5=7%2C7"
                            SearchAge = "&SF_1_1_8=" + str(Age[m]) + "%2C" + str(Age[m])
                            SearchProvCity ="&SF_1_1_6=" + str(ProvCity[n])
                            SearchGender = "&SF_1_1_9=" + str(Gender[g])
                        else:
                            continue

                    #研究生处理
                    if (l == 1):
                        if (m == 0):
                            if (n == 0) and (g == 0):
                                SearchEdu = "&SF_1_1_5=9%2C9"
                                SearchAge = "&SF_1_1_8=16%2C24"
                                SearchProvCity = ""
                                SearchIndustry = ""
                                SearchGender = ""
                            elif (n != 0) or (g != 0):
                                continue
                        elif (0 < m < 9):
                            continue
                        elif (m > 8) and (n == 0) and (g == 0):
                            SearchEdu = "&SF_1_1_5=9%2C9"
                            SearchAge = "&SF_1_1_8=" + str(Age[m]) + "%2C" + str(Age[m])
                            SearchProvCity = ""
                            SearchGender = ""
                        else:
                            continue

                    #MBA及其以上处理
                    if (l == 2):
                        if (m == 0) and (n == 0) and (g == 0):
                            SearchEdu = "&SF_1_1_5=11%2C16"
                            SearchAge = ""
                            SearchProvCity = ""
                            SearchGender = ""
                        else:
                            continue


                    SearchUrl2 = 'http://rdsearch.zhaopin.com/Home/ResultForCustom?'\
                                + "SF_1_1_11=" + str(School[s][0])\
                                + SearchEdu\
                                + SearchAge\
                                + SearchProvCity\
                                + SearchGender\
                                + '&orderBy=DATE_MODIFIED%2C1&exclude=1'
                    print "SearchUrl2:", SearchUrl2

                    #-----------------------------------
                    #写入Log日志
                    #-----------------------------------
                    WriteLogData = []
                    WriteLogData.append(s)
                    WriteLogData.append(l)
                    WriteLogData.append(m)
                    WriteLogData.append(n)
                    WriteLogData.append(g)
                    f = open("Breakpoints_log.txt",'w+')
                    for data in WriteLogData:
                        f.write("%s\n"%data)
                    f.close()

                    #循环记录文件创建
                    recordpath = u"h:\\Resume_ID_storage\\陕西\\" 
                    Recordpath = recordpath.strip().rstrip("\\")
                    if not os.path.exists(Recordpath):
                        os.makedirs(Recordpath)
                    else:
                        print Recordpath+ u"目录已存在"
                    f = open(recordpath + School[s][1].decode("utf-8") + "Loop_record.txt",'a+')
                    for data in WriteLogData:
                        f.write("%s\t"%data)
                    f.write("\n")
                    f.close()

                    #-----------------------------------
                    #定义搜索请求，发出搜索请求
                    #-----------------------------------
                    headers2 = {
                        'Referer':'http://rdsearch.zhaopin.com/'
                        }
                    #自定义一个请求2
                    try:
                        req2 = urllib2.Request(url = SearchUrl2, headers = headers2)
                        FinalPage2 = urllib2.urlopen(req2)
                        PrintOut2 = FinalPage2.read().decode('utf-8')
                        #print PrintOut2
                        cur_url =  FinalPage2.geturl()
                        print "cur_url:",cur_url
                    except Exception as e:
                        print e
                        pass
                        continue

                    #---------------------------------------
                    #输出搜索结果页面数，预测有多少份简历
                    #---------------------------------------
                    PageNumDownloader= ResumeContentDownloadThread.Get_Search_info()
                    try:
                        PageNum, SumResumeNum = PageNumDownloader.Resume_Num(PrintOut2)
                        print "SumResumeNum:", SumResumeNum
                        print "PageNum:", PageNum
                        print type(PageNum)
                    except Exception as e:
                        print e
                        pass
                        continue


                    #存储简历编号

                    BaseUrl = SearchUrl2 + '&pageIndex='
                    #开启5个线程
                    ThreadingNum = 5;Numdownloadthreads = []
                    for i in range(ThreadingNum):
                        begin = ((int(PageNum) + (ThreadingNum-1))/ThreadingNum) * i + 1
                        end = (((int(PageNum) + (ThreadingNum-1))/ThreadingNum) * (i+1) + 1)
                        t = ResumeContentDownloadThread.Download_Number_Thread(BaseUrl, begin, end, SchoolName[s], i)
                        Numdownloadthreads.append(t)

                    for i in range(len(Numdownloadthreads)):
                        Numdownloadthreads[i].start()

                    for i in range(len(Numdownloadthreads)):
                        Numdownloadthreads[i].join()


    ################################
    #测试单次循环耗费时间
    ###############################
    time2 = time.time()
    Loadtimecost = time2 - time1
    print "Loadtimecost:", Loadtimecost
