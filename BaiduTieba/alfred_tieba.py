#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division, absolute_import

import alp
import re
import urllib
import urllib2
import ast
import json

real_query='{query}'

#判断是否有中文 
def CheckContainChinese(check_str):
    for ch in check_str.decode('utf-8'):
    	if u'\u4e00' <= ch <= u'\u9fff':
        	return True
    return False

#获得搜索引擎推荐的中文
def GetSuggestWord(in_word):
    #如果非中文才去检索
    if CheckContainChinese(in_word):
    	return in_word

    if in_word[0] == '@' :
	return in_word[1:]
    suggest_url="http://api.bing.com/osjson.aspx?query=" + urllib.quote(in_word)
    result = urllib2.urlopen(suggest_url)
    #result_list = ast.literal_eval(unicode(result.read(), "utf-8"))
    result_list = json.loads(urllib.unquote(result.read()))
    return result_list[1][0]

result_list = None

target_word=GetSuggestWord(real_query)
url = "http://wapp.baidu.com/f?kw=" + target_word
r = alp.Request(url, payload=None, post=False).souper()


result = [u'<?xml version="1.0"?>', u'<items>']

i = 0
for link in r.find_all("div", "i"):
    title = link.find("a").string.encode('utf-8')
    title = re.sub(r"^\d*\. *", "", title)

    id_ = re.search("kz\=(\d*)\&", link.find("a")["href"]).group(1)
    click_num = re.search("点(\d*)", link.find("p").string.encode('utf-8')).group(1)
    reply_num = re.search("回(\d*)", link.find("p").string.encode('utf-8')).group(1)
    aurl = u"http://tieba.baidu.com/p/" + id_
    result.append(u'<item uid="baidusearch' + str(i) + u'" arg="' + aurl + u'">')
    result.append(u'<title>' + title.decode("utf8") + u'</title>')
    result.append(u'<subtitle> 点击' + click_num + u' 回复' + reply_num + u'</subtitle>')
    result.append(u'<icon>icon.png</icon>')
    result.append(u'</item>')
    i += 1


result.append(u'</items>')
xml = ''.join(result)

print xml.encode("utf8")
print url
