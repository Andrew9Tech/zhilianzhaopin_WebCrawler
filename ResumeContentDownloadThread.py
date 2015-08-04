# -*- coding: utf-8 -*-

import re
import os
import sys
import urllib2
import threading

reload(sys)   
sys.setdefaultencoding('utf8')

class Get_Search_info:
    def Resume_Num(self, myPage):
        #匹配共有多少份简历
        #<span class="resumelist-num-icon manner-border number-current current-icon-default">30</span>
        try:
            PageNum = re.search(r'id="rd-resumelist-pageNum">1/(.*?)</span>', myPage, re.S).group(1)
            #print int(PageNum)
            PerNum = re.search(r'<span class="resumelist-num-icon manner-border">(.*?)</span>', myPage, re.S).group(1)
            #print int(PerNum)
            SumResumeNum = int(PageNum) * int(PerNum)
        except Exception as e:
            print "Exception:",e
            pass
        return PageNum, SumResumeNum

class Download_Number_Thread(threading.Thread):
    def __init__(self, BaseUrl, begin, end, school, num):
        threading.Thread.__init__(self)
        self.BaseUrl = BaseUrl
        self.begin = int(begin)
        self.end = int(end)
        self.school = str(school[0])
        self.schoolname = school
        self.num = int(num)

    def Download_ResNum(self):
        #自定义
        header = {'Referer':'http://rdsearch.zhaopin.com/'}
        ResumeSerNum = []
        TargetSerNum = []
        #print self.num
        #简历索引是从pageIndex=1开始，结束于pageIndex=PageNum
        for pagenum in range(self.begin, (self.end)):
            PageUrl = self.BaseUrl + str(pagenum)
            request = urllib2.Request(url = PageUrl,headers = header)

            try:
                pagecont = urllib2.urlopen(request).read().decode("utf-8")

                SerNum = re.findall(r'<tr class="info" style="display: none" tag="(.*?)">.*?(&nbsp;){4,}(.*?)(&nbsp;){4,}(.*?)(&nbsp;){4,}(.*?)<br/', pagecont, re.S)
                #print len(SerNum)
            except Exception as e:
                continue
                pass
            
            ResumeSerNum = ResumeSerNum + SerNum

        #print "self.schoolname:",self.schoolname
        #print "self.school:",self.school

        for i in range(len(ResumeSerNum)):
            if ResumeSerNum[i][2] in self.schoolname:
                TargetSerNum = TargetSerNum + [ResumeSerNum[i][0]]

        f = open(u"h:\\Resume_ID_storage\\陕西\\" + self.school.decode("utf-8")+ ".txt",'a+')
        for ID in TargetSerNum:
            f.write("%s\n"%ID)
        f.close()

        f = open(u"h:\\Resume_ID_storage\\陕西\\" + self.school.decode("utf-8") + "_NPure.txt",'a+')
        for j in range(len(ResumeSerNum)):
            f.write("%s\t"%ResumeSerNum[j][0])
            f.write("%s\n"%ResumeSerNum[j][2])
        f.close()

    def run(self):
        self.Download_ResNum()
