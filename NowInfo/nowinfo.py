#!/bin/env python
# encoding: utf-8

import sys
import json
from workflow import Workflow3, web
from workflow.notify import notify

#ts api
TS_API="http://quan.suning.com/getSysTime.do"

#full info api
FULLINFO_API="https://tool.bitefu.net/jiari/?d={date}&info=1"

def GetTs(api):
    r = web.get(api)
    r.raise_for_status()
    result = r.json()
    return result["sysTime2"]

def GetFullInfo(api):
    r = web.get(api)
    r.raise_for_status()
    return r.json()

def GetNongli(info):
    return u"{yearname}年 {date}".format(yearname=info["yearname"], date=info["nonglicn"])

def GetWeek(info):
    return u"星期{week_cn} {week_en}".format(week_cn=info["weekcn"], week_en=info["week3"])

def GetWork(info):
    return info["typename"]

def main(wf):

    query_api = FULLINFO_API.format(date="20190908")
    fullinfo = GetFullInfo(query_api)

    #work
    wf.add_item(u"今天是%s"%(GetWork(fullinfo)), "")

    #time
    ts = GetTs(TS_API)
    wf.add_item(u'北京时间', ts, arg=ts, valid=True)
    notify(u"当前时间", ts)
    
    #nongli
    
    wf.add_item(u'农历', GetNongli(fullinfo), arg=GetNongli(fullinfo), valid=True)

    #week
    wf.add_item(u'星期', GetWeek(fullinfo), arg=GetWeek(fullinfo), valid=True)

    #suit
    wf.add_item(u'宜', fullinfo["suit"], arg=fullinfo["suit"], valid=True)

    #avoid
    wf.add_item(u'忌', fullinfo["avoid"], arg=fullinfo["avoid"], valid=True)

    wf.send_feedback()

if __name__ == "__main__":
    wf = Workflow3()
    sys.exit(wf.run(main))

