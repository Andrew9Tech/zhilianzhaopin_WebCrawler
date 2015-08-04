# zhilianzhaopin_WebCrawler
爬取智联招聘简历

简历爬取主要分两步
第一步，抓取简历编号，使用的文件有zhilianzhaopin_2.1_01.py、Verification_Code.py、ResumeContentDownloadThread.py
zhilianzhaopin_2.1_01.py是主文件，调用Verification_Code.py(模拟登陆部分)，ResumeContentDownloadThread.py(多线程下载部分)

第二步，根据前期获取的简历编号抓取简历html，文件是zhilianzhaopin_2.1_02.py，这里面也涉及到模拟登陆，需要调用Verification_Code.py。


注：原始版本，加的有代理，但访问速度很慢。经过多次测试，在增加每次访问间的等待时间可以避开服务器对爬虫的限制，这个等待时间是在某一个范围随机的。
