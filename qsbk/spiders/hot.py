# -*- coding: utf-8 -*-
import scrapy
import time
import os
import urllib2
import re
import platform
from qsbk.items import QsbkItem

class HotSpider(scrapy.Spider):
    name = "hot"
    allowed_domains = ["qiushibaike.com"]
    start_urls = (
        'http://www.qiushibaike.com/hot/1',
    )
    max_page=1                # hot最多35页
    curr_page=0
    show_user_pic = False     # 头像大小调整需要emacs支持imagemagick，如果不支持，建议不显示头像
    story_img_file=''
    user_img_file=''
    date = time.localtime()
    org_file=r'./%d-%d.org' % (date.tm_mon,date.tm_mday)
    if platform.system() == 'Windows':
        newline='\r\n'
    elif platform.system() == 'Linux':
        newline='\n'
    else:
        newline='\r'
    if os.path.exists(org_file):
        os.remove(org_file)
    if not os.path.exists('./user_pic'):
        os.mkdir(r'./user_pic')
    if not os.path.exists('./story_pic'):
        os.mkdir(r'./story_pic')

    with open(org_file,'a+') as of:
        of.write(r'#+OPTIONS: ^:nil \n:t author:nil timestamp:nil creator:nil'+newline)
        of.write(r'#+TITLE: 糗事百科24小时热门'+newline)

    def down_pic(self,story):
        if story['img']:
            self.story_img_file = re.search(r'http.*/(.*[jpg|jpeg|png])',story['img'][0].lower()).group(1).lower()
            self.story_img_file = r'./story_pic/'+self.story_img_file
            if not os.path.exists(self.story_img_file):
                picsrc = urllib2.urlopen(story['img'][0]).read()
                open(self.story_img_file,"wb").write(picsrc)

        if self.show_user_pic and story['author_img']:
            self.user_img_file = re.search(r'http.*/(.*[jpg|jpeg|png])',story['author_img'][0].lower()).group(1)
            self.user_img_file = r'./user_pic/'+self.user_img_file
            if not os.path.exists(self.user_img_file):
                picsrc = urllib2.urlopen(story['author_img'][0]).read()
                open(self.user_img_file,"wb").write(picsrc)

    def write_org(self,story,page):
        with open(self.org_file,'a+') as of:
            storyid=re.search(r'tag_(\d*)',story['id'][0]).group(1)
            if self.curr_page != page:
                self.curr_page=page
                of.write(r'* page '+ str(page)+':'+ self.newline)
            of.write(r'- '+r'[[http://www.qiushibaike.com/article/'+str(storyid)+'][糗事'+str(storyid)+']]'+self.newline)
            if self.show_user_pic and story['author_img']:
                of.write(r'#+ATTR_HTML: :width 50px'+self.newline)
                of.write(r'[['+self.user_img_file+r']]   ')
            of.write(r'[[http://www.qiushibaike.com'+story['userlink'][0].encode('utf-8')+']['+story['author'][0].encode('utf-8').strip()+']]'+self.newline)
            of.write(story['text'][0].encode('utf-8').strip()+self.newline)
            if story['img']:
                of.write(r'#+ATTR_HTML: :width 300px'+self.newline)
                of.write(r'[['+self.story_img_file+r']]'+self.newline)
            of.write(2*self.newline)
    def parse(self, response):
        page_url=response.xpath("//li/span[@class='current']/text()").extract()
        page=int(page_url[0])
        for item in response.xpath("//div[@id='content-left']/div[@class='article block untagged mb15']"):
            story = QsbkItem()
            story['id']=item.xpath("./@id").extract()
            story['url'] = item.xpath("./@id").extract()
            story['author'] = item.xpath("./div[@class='author clearfix']//h2/text()").extract()
            story['userlink']=item.xpath("./div[@class='author clearfix']/a[@rel='nofollow']/@href").extract()
            if not story['userlink']:
                story['userlink']=['']
            if not story['author']:
                story['author']=['']
                story['author_img']=['']
            else:
                story['author_img'] = item.xpath("./div[@class='author clearfix']/a[1]/img/@src").extract()
            tmptext=item.xpath("./div[@class='content']")
            story['text']=tmptext.xpath('string(.)').extract()
            story['img']=item.xpath("./div[@class='thumb']/a/img/@src").extract()
            yield story
            self.down_pic(story)
            self.write_org(story,page)

        if(page < self.max_page):
            next_url=response.xpath("//span[@class='next']/../@href").extract()
            next_url='http://www.qiushibaike.com'+next_url[0].strip()
            yield scrapy.Request(next_url, callback=self.parse)
