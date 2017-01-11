# -*- coding:utf-8 -*-

# 爬取百度贴吧的数据
# 爬取顺序：__init__  -> getPage()
# 爬取顺序： 初始化 ->  获取传入页码的数据(整个页面的数据)

import urllib2
import re

baseURL = 'http://tieba.baidu.com/p/3138733512'  # 爬取的链接

# 处理页面标签类
class Tool:
    # 去除图片标签还有7位空格
    removeImg = re.compile('<img.*?>| {7}|')
    # 去除超链接标签
    removeAddr = re.compile('<a.*?></a>')
    # 把换行的标签换成\n
    replaceLineFeed = re.compile('<tr><div></div></p>')
    # 把表格制表td标签换成\t
    replaceTR = re.compile('<td>')
    # 把段落开头换成\n加两空格
    replaceSpace = re.compile('<p.*?>')
    # 把换行符或双换行符\n
    replaceBR = re.compile('<br><br>|<br>')
    # 把其余标签删除
    removeExtraTag = re.compile('<.*?>')

    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLineFeed,"\n",x)
        x = re.sub(self.replaceTR,"\t",x)
        x = re.sub(self.replaceSpace,"\n  ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        # strip()函数把前后多余内容删除
        return x.strip()



# 爬虫类：
class BDTB:
    def __init__(self,baseUrl,seeLZ):
        self.baseURL = baseUrl
        self.seeLZ = '?see_lz=' + str(seeLZ)
        self.tool = Tool()

    # 传入页码，获取该页帖子的代码
    def getPage(self,pageNum):
        try:
            url = self.baseURL + self.seeLZ + '&pn=' + str(pageNum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            # print response.read()
            return  response.read().decode(u'utf-8')   # 必须加decode否则报错
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                print u"连接百度贴吧失败，错误原因",e.reason
                return None

    # 获取标题
    def getTitle(self):
        page = self.getPage(1)
        pattern = re.compile(ur'<h3 class="core_title_txt.*?">(.*?)</h3>')
        # pattern1 = re.compile(ur'<h(\d)(\W)+class="core_title_txt.*>(.*)</h\1>')    # 参考
        result = re.search(pattern,page)
        if result:
            print "标题：",result.group(1)   # 输出标题
            return result.group(1)
        else:
            print "Error"
            return None

    # 获取当前帖子一共有多少页
    def getPageNum(self):
        page = self.getPage(1)
        pattern = re.compile(ur'<li class="l_reply_num".*?<span.*?>.*?</span>.*?<span.*?>(.*?)</span>',re.S)
        result = re.search(pattern,page)
        if result:
            print "总页数:", result.group(1)   # 输出总页数
            return result.group(1)
        else:
            print "Error"
            return None

    # 获取正文内容
    def getContent(self,page):
        pattern = re.compile('<div id="post_content.*?" class="d_post_content.*?">(.*?)</div>',re.S)
        result = re.findall(pattern,page)
        print self.tool.replace(result[1])

bdtb = BDTB(baseURL,1)
page = bdtb.getPage(1)  # 获取当前页所有内容
bdtb.getTitle()
bdtb.getPageNum()
bdtb.getContent(page)
