# -*- coding:utf-8 -*-

# 爬取百度贴吧的数据
# 爬取顺序：__init__  -> getPage()
# 爬取顺序： 初始化 ->  获取传入页码的数据(整个页面的数据)

import urllib2
import re

class BDTB:
    def __init__(self,baseUrl,seeLZ):
        self.baseURL = baseUrl
        self.seeLZ = '?see_lz=' + str(seeLZ)

    # 传入页码，获取该页帖子的代码
    def getPage(self,pageNum):
        try:
            url = self.baseURL + self.seeLZ + '&pn=' + str(pageNum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            # print response.read()
            return  response.read().decode(u'utf-8')  # 必须加decode否则报错
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                print u"连接百度贴吧失败，错误原因",e.reason
                return None

    # 获取标题
    def getTitle(self):
        page = self.getPage(1)
        pattern = re.compile('<h3 class="core_title_text.*?">(.*?)</h3>',re.S)
        pattern1 = re.compile(ur'<h(\d)(\W)+class="core_title_txt.*>(.*)</h\1>')
        result = re.search(pattern1,page)
        if result:
            print "OK"
            print result.group(0) # 测试输出
            return result.group(0)
        else:
            print "Error"
            return None

baseURL = 'http://tieba.baidu.com/p/3138733512'
bdtb = BDTB(baseURL,1)
bdtb.getTitle()
