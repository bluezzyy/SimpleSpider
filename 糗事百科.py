# -*- coding: utf-8 -*-
# Date：2017/01/09
# Version:1.0
# 执行顺序: __init__ -> start() -> getOneStory/loadPage() -> getPageItem() -> getOnePage()
# 执行顺序：初始化数据 -> 开始程序 -> 输出一个段子/获取一页数据 -> 正则判断，爬取单条段子 -> 爬虫程序(request,headers,stories)


import urllib2
import re
import datetime
import os
import sys

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
        x = re.sub(self.removeImg ,"", x)
        x = re.sub(self.removeAddr,"", x)
        x = re.sub(self.replaceLineFeed ,"\n",x)
        x = re.sub(self.replaceTR ,"\t",x)
        x = re.sub(self.replaceSpace ,"\n  ",x)
        x = re.sub(self.replaceBR ,"\n",x)
        x = re.sub(self.removeExtraTag ,"",x)
        # strip()函数把前后多余内容删除
        return x.strip()

class QSBK:
    # 初始化变量
    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.pageIndex = 1
        # 必须加入headers 否则无法访问
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.3 Safari/537.36'
        self.headers = {'User-Agent':self.user_agent}
        self.stories = []
        self.enables = False   # 判断能否继续运行
        # 工具类
        self.tool = Tool()
        # 写入文件
        self.file = None
        # 当前时间
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 默认文件名
        self.default = "糗事百科"+self.date
        # 存储路径(自行更改)
        self.path = '//SomeCodes//PythonData'

    # 获取一页数据
    def getOnePage(self,pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            content = response.read().decode('utf-8')
            return content
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                print "错误原因:" , e.reason

    # 获取段子数据
    def getPageItem(self,pageIndex):
        global pageStories
        pageCode = self.getOnePage(pageIndex)
        if pageCode:
            pattern = re.compile('<div class="author clearfix">.*?href.*?<img src.*?title=.*?<h2>(.*?)</h2>.*?'+
              '<div class="content">(.*?)</div>.*?<i class="number">(.*?)</i>',re.S)
            items = re.findall(pattern,pageCode) # 返回一个list 其中(.*?)为一个元素。
            pageStories = []  #用于存放一个段子的数据
            for item in items:
                # @param: 作者
                # @param: 内容
                # @param：评论
                pageStory = self.tool.replace(item[0])
                pageStory1 = self.tool.replace(item[1])
                pageStory2 = self.tool.replace(item[2])
                pageStories.append([pageStory.encode("utf-8"),pageStory1.encode("utf-8"),pageStory2.encode("utf-8")])

        return pageStories

    # 加载一页数据，并且添加到列表中
    def loadPage(self):
        # 如果当前未看的页数少于2页，则加载新一页
        if self.enables == True:
            if len(self.stories) < 2:
                # 获取新一页
                pageStories = self.getPageItem(self.pageIndex)
                # 将该页的段子存放到全局list中
                if pageStories:
                    self.stories.append(pageStories)
                    # 获取完之后页码索引加一，表示下次读取下一页
                    self.pageIndex += 1

    # 为文件设置名称
    def setFileName(self):
        os.chdir(self.path)  # 更换文件存放路径
        self.file = open(self.default + u".txt", u"w+")  # w+是先清空再写入，防止爬取数据重复


    # 调用该方法，把数据存放到文件中
    def getOneStory(self,pageStories,page):
        for story in pageStories:
            self.loadPage()
            if input == "Q":
                self.enables = False
                print u'退出糗事百科！'
                return
            # 爬取到的单个段子数据
            item = u"第%d页\n 作者:%s \n %s\n 评论数:%s\n" % (page, story[0], story[1], story[2])
            # 写入文件
            self.file.write("\n----------------------我是分割线------------------------------\n")
            self.file.write(item)

    # 开始方法
    def start(self):
        print u"正在读取糗事百科，按回车查看新段子，Q退出"
        # 使变量变为True,程序可以正常运行
        self.enables = True
        # 开始爬虫
        print u'输入Blue开始爬虫:'
        self.begin = raw_input()
        # 获取单页段子数据
        self.loadPage()
        # 局部变量，控制当前读到第几页
        nowPage = 0
        # 设置文件名
        self.setFileName()
        if self.begin == "Blue":
            if(self.stories)>0:
                # 从全局list中获取一页的段子
                pageStories = self.stories[0]
                print "正在写入第" + str(nowPage) + "页数据 command+F2暂停"
                # 当前读到的页数加一
                nowPage +=1
                #将全局list中第一个元素删除，因为已经取出
                del self.stories[0]
                # 存储该页的段子
                self.getOneStory(pageStories,nowPage)
        else:
            print "输入错误，请重试"
            exit()

spider = QSBK()
spider.start()



