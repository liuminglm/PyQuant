# -*- coding: utf-8 -*-
"""
Created on Sat May 07 12:58:55 2016

@author: ming
"""

import numpy as np
import pandas as pd
import time,os,requests
import datetime
from gmsdk import md


def DaimaAll():
    url = 'http://hqdigi2.eastmoney.com/EM_Quote2010NumericApplication/index.aspx?type=s&sortType=C&sortRule=-1&pageSize=100&page=1&jsName=quote_123&style=33&token=&_g='
    r = requests.get(url)
    num = int(r.text[14:].split('k:')[1].split(',p')[1].split(':')[1][:-1])+1
    daima=[]
    for n in range(1,num):
        url1 = 'http://hqdigi2.eastmoney.com/EM_Quote2010NumericApplication/index.aspx?type=s&sortType=C&sortRule=-1&pageSize=100&page='+str(n)+'&jsName=quote_123&style=33&token=&_g='
        condition = True
        while condition:
            try:
                r = requests.get(url1,timeout = 10)   
                condition = False
            except:
                pass
        for n2 in range(100):
            try:
                r.text[14:].split('k:')[1].split(',p')[0].split('","')[n2].split(',')[1]
                daima.append(r.text[14:].split('k:')[1].split(',p')[0].split('","')[n2].split(',')[1])
            except:
                pass   
    return daima
    
def DaimaInDeal():
    ret = md.init("yourname", "password")
    daima_set = []
    for b1 in md.get_instruments('SHSE', 1, 1):
        if b1.symbol[5:7]=='60':
            daima_set.append(b1.symbol[5:])
        else:
            pass

    for c1 in md.get_instruments('SZSE', 1, 1):
        if c1.symbol[5:7]=='60':
            pass
            
        else:
            daima_set.append(c1.symbol[5:])
    daima_set_end = []
    for ck in daima_set:
        if ck[0:2]=='20':
            pass
        else:
            daima_set_end.append(ck)
    return daima_set_end


def TransactionTime():
    def time_transfer_timeStamp(time_str):
        timeArray = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        return str(timeStamp)

    def time_transfer_string(time_str):
        timesplit = time_str.split(' ')
        time_str_new = timesplit[0]+' '+timesplit[1]+' '+timesplit[2]+' '+timesplit[3]+' '+timesplit[5]
        data = time.mktime(time.strptime(time_str_new,"%a %b %d %H:%M:%S %Y"))
        return str(datetime.datetime.fromtimestamp(data))[0:10]

    def get_xueqiu():
        header = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Encoding':'gzip, deflate, sdch',
                    'Accept-Language':'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,ja;q=0.2',
                    'Cache-Control':'max-age=0',
                    'Connection':'keep-alive',
                    'DNT':'1',
                    'Host':'xueqiu.com',
                    'Referer':'https://www.baidu.com/link?url=CQu5rGbzI_vt0fSj3b12LTyZgWvzjrK9f3L_GLIBqum&wd=&eqid=88e8a3ca0001535b00000005572edf29',
                    'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'}

        s = requests.session()
        t = s.get('https://xueqiu.com/',headers = header)
        endtime = time_transfer_timeStamp(str(datetime.datetime.now())[0:19])+'000'
        url = 'https://xueqiu.com/stock/forchartk/stocklist.json?symbol=SH000001&period=1day&type=normal&begin=0&end='+endtime+'&_='+endtime
        r = s.get(url,headers = header)

        data = r.content.split('[{')[1][0:-3].split('},{')
        timep = []
        for a in data:
            shijian_xueqiu = a.split(',')[-1].split('":"')[1][0:-1]
            time_tmp = time_transfer_string(shijian_xueqiu)
            timep.append(time_tmp)
        return timep

    return get_xueqiu()
