# -*- coding:utf-8 -*-

# 爬取百度贴吧的数据
# 思路：见XMind
# Author: Blue
# Date: 2017/01/12

import urllib2
import re
import sys
import datetime
import os

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

    # re.sub()方法： 用一个string代替匹配的模式
    def replace(self ,x):
        x = re.sub(self.removeImg , "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLineFeed ,"\n",x)
        x = re.sub(self.replaceTR ,"\t",x)
        x = re.sub(self.replaceSpace ,"\n  ",x)
        x = re.sub(self.replaceBR ,"\n",x)
        x = re.sub(self.removeExtraTag ,"",x)
        # strip()函数把前后多余内容删除
        return x.strip()

# 爬虫类：
class BDTB:
    # 初始化数据
    def __init__(self ,baseUrl,seeLZ,floorTag):
        # 设置默认编码为utf-8 否则会出现写入错误
        reload(sys)
        sys.setdefaultencoding('utf-8')
        # baseURL
        self.baseURL = baseUrl
        # 是否只看楼主
        self.seeLZ = '?see_lz=' + str(seeLZ)
        # 工具类
        self.tool = Tool()
        # 写入文件
        self.file = None
        # 当前时间
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 默认文件名
        self.default = "百度贴吧"+self.date
        # 存储路径(自行更改)
        self.path = '//SomeCodes//PythonData'
        # 楼层数
        self.floor = 1
        # 楼层分隔标识
        self.floorTag = floorTag

    # 传入页码，获取该页帖子的代码
    def getPage(self,pageNum):
        try:
            url = self.baseURL + self.seeLZ + '&pn=' + str(pageNum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            return  response.read().decode(u'utf-8')   # 必须加decode否则报错
        except urllib2.URLError,e:
            if hasattr(e , "reason"):
                print u"连接百度贴吧失败，错误原因",e.reason
                return None

    # 获取标题
    def getTitle(self,page):
        pattern = re.compile(ur'<h3 class="core_title_txt.*?">(.*?)</h3>')
        result = re.search(pattern,page)
        if result:
            print "标题：",result.group(1)   # 输出标题
            return result.group(1)
        else:
            print "Error"
            return None

    # 获取当前帖子一共有多少页
    def getPageNum(self,page):
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
        contents = []
        for item in result:
            content = "\n" + self.tool.replace(item) + "\n"
            contents.append(content.encode('utf-8'))
        return contents

    # 为文件设置名称
    def setFileName(self,title):
        if title is not None:
            os.chdir(self.path)  # 更换文件存放路径
            self.file = open(title + u".txt", u"w+")  # w+是先清空再写入，防止爬取数据重复
        else:
            self.file = open(self.default +u".txt",u"w+")

    # 写入文件
    def writeFile(self,contents):
        # 在文件开头写入链接和时间
        self.file.write("该贴子的链接为：http://tieba.baidu.com/p/"+code+"\n"+ "爬取日期："+ self.date + "\n")
        for item in contents:
            if self.floorTag == "1":
                # 楼层之间的分隔线
                floorLine = "\n" + str(self.floor) + u"楼-----------------------------------------------------\n"
                self.file.write(floorLine)
            self.file.write(item)
            self.floor += 1

    # 关闭文件
    def closeFile(self):
        self.file.close()

    # 开始爬虫
    def start(self):
        pageIndex = self.getPage(1)
        pageNum = self.getPageNum(pageIndex)
        title = bdtb.getTitle(pageIndex)
        self.setFileName(title)
        if(pageNum == None):
            print "URL已经失效，请重试"
            return
        try:
            print "该贴共有" +str(pageNum) + "页"
            for i in range(1,int(pageNum)+1):
                print "正在写入"+ str(i) + "页的数据"
                page = self.getPage(i)
                contents = self.getContent(page)
                self.writeFile(contents)
            print "写入完成"
        except IOError,e:
            print "发生错误"+e.message
        finally:
            self.closeFile()

print u'请输入贴子代号'
code = str(raw_input(u'http://tieba.baidu.com/p/'))  # 贴子代号
baseURL = 'http://tieba.baidu.com/p/'+code  # 爬取的链接
seeLZ = raw_input("是否只获取楼主的发言 1:是 其他:否\n")
floorTag = raw_input("是否打印楼层 1:是 其他:否\n")
bdtb = BDTB(baseURL,seeLZ,floorTag)
bdtb.start()