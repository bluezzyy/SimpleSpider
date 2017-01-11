# -*- coding: utf-8 -*-
# Date：2017/01/09
# Version:1.0
# 执行顺序: __init__ -> start() -> getOneStory/loadPage() -> getPageItem() -> getOnePage()
# 执行顺序：初始化数据 -> 开始程序 -> 输出一个段子/获取一页数据 -> 正则判断，爬取单条段子 -> 爬虫程序(request,headers,stories)


import urllib2
import re
class QSBK:
    # 初始化变量
    def __init__(self):
        self.pageIndex = 1
        # 必须加入headers 否则无法访问
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.3 Safari/537.36'
        self.headers = {'User-Agent':self.user_agent}
        self.stories = []
        self.enables = False   # 判断能否继续运行

    # 获取一页数据
    def getOnePage(self,pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            content = response.read().decode('utf-8')
            return content
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason

    # 获取段子数据
    def getPageItem(self,pageIndex):
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
                pageStories.append([item[0].strip(),item[1].strip(),item[2].strip()])

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

    # 调用该方法，每敲一次回车输出一个段子
    def getOneStory(self,pageStories,page):
        for story in pageStories:
            input = raw_input()
            # 每输入一次回车，判断是否加载新页面
            self.loadPage()
            if input == "Q":
                self.enables = False
                print u'退出糗事百科！'
                return
            # 输出爬取到的单个段子数据
            print u"爬到的数据为：第%d页\t %s \t %s\t %s\t" %(page,story[0],story[1],story[2])

    # 开始方法
    def start(self):
        print u"正在读取糗事百科，按回车查看新段子，Q退出"
        # 使变量变为True,程序可以正常运行
        self.enables = True
        # 获取单页段子数据
        self.loadPage()
        # 局部变量，控制当前读到第几页
        nowPage = 0
        while self.enables:
            if(self.stories)>0:
                # 从全局list中获取一页的段子
                pageStories = self.stories[0]
                # 当前读到的页数加一
                nowPage +=1
                #将全局list中第一个元素删除，因为已经取出
                del self.stories[0]
                # 输出该页的段子
                self.getOneStory(pageStories,nowPage)

spider = QSBK()
spider.start()



