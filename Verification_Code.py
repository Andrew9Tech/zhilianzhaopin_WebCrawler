#!/usr/bin/env python
# -*- coding: utf-8 -*-
#---------------------------------------
#   程序：验证码处理模块
#   作者：andrew9tech
#   日期：2014-12-31
#   语言：Python 2.7
#   功能：获取验证码及自动管理cookie
#---------------------------------------

#import re
import urllib2
import cookielib
#from pytesser import *
#import cStringIO
#from PIL import Image


class Verification_Code_Pro:

    #安装cookiesJar，不多说    
    def Install_Opener(self):
        cookiejar = cookielib.MozillaCookieJar()
        cookieSupport= urllib2.HTTPCookieProcessor(cookiejar)
        opener = urllib2.build_opener(cookieSupport)
        urllib2.install_opener(opener)

    #手动输入验证码，调试阶段使用
    def Verification_Code_Input(self, url):
        #下载验证码图片，手动输入
        f = open('img.gif', 'wb')
        stream = urllib2.urlopen(url).read()
        f.write(stream)
        f.close()
        #验证码破解代码，调试阶段，此处未用
        # img = Image.open(file)
        # text = image_to_string(img)
        # print text
        #手动输入验证码
        text = raw_input('input yan zheng ma:：')
        return text
"""
    #自动破解验证码，
    def Verification_Code_Auto_Ident(self, url):
        #访问验证码URL，存储为文件格式
        file = cStringIO.StringIO(urllib2.urlopen('http://rd2.zhaopin.com/s/loginmgr/picturetimestamp.asp').read())
        #以图片形式打开
        img = Image.open(file)
        #调用pytesser库，做图片识别
        text1 = image_to_string(img)
        #识别出来的字符串包含空格斜划线等无效字符，匹配出数字及字母
        text2 = re.findall(r'\w', str(text1), re.S)
        #列表转化为字符串，因为findall输出为列表
        text = ''.join(list(text2))
"""

