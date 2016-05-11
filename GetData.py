# -*- coding: utf-8 -*-
"""
Created on Tue May 03 12:49:48 2016

@author: ming
"""


import numpy as np
import pandas as pd
import time,os,requests
import datetime
import shutil
from StringIO import StringIO


    
def day_data(daima,start_date,end_date,fuquan):
    def time_transfer_timeStamp(time_str):
        timeArray = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        return str(timeStamp)

    def time_transfer_string(time_str):
        data = time.mktime(time.strptime(time_str,"%a %b %d %H:%M:%S +0800 %Y"))
        return str(datetime.fromtimestamp(data))[0:10]

    def get_xueqiu(daima,start_date,end_date,fuquan):
        header = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Encoding':'gzip, deflate, sdch',
                    'Accept-Language':'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,ja;q=0.2',
                    'Cache-Control':'max-age=0',
                    'Connection':'keep-alive',
                    'DNT':'1',
                    'Host':'xueqiu.com',
                    'Referer':'https://www.baidu.com/link?url=CQu5rGbzI_vt0fSj3b12LTyZgWvzjrK9f3L_GLIBqum&wd=&eqid=88e8a3ca0001535b00000005572edf29',
                    'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'}

        
        start_time_tmp =start_date[0:4]+'-'+start_date[4:6]+'-'+start_date[6:]+' 00:00:00'
        end_time_tmp =end_date[0:4]+'-'+end_date[4:6]+'-'+end_date[6:]+' 15:30:00'
        
        if daima[0:2]=='60':
            daima_new = 'SH'+daima
        else:
            daima_new = 'SZ'+daima
        s = requests.session()
        t = s.get('https://xueqiu.com/',headers = header)

        start_time = time_transfer_timeStamp(start_time_tmp)
        end_time = time_transfer_timeStamp(end_time_tmp)+'000'

        r = s.get('https://xueqiu.com/stock/forchartk/stocklist.json?symbol='+daima_new+'&period=1day&type='+fuquan+'&begin='+start_time+'&end='+end_time+'&_='+end_time,headers = header)

        data = r.content.split('[{')[1][0:-3].split('},{')
        openp = []
        closep = []
        highp = []
        lowp = []
        timep = []
        volume = []
        turnrate = []
        dif = []
        dea = []
        macd = []

        for a in data:
            openp.append(float(a.split(',')[1].split(':')[1]))
            closep.append(float(a.split(',')[3].split(':')[1]))
            highp.append(float(a.split(',')[2].split(':')[1]))
            lowp.append(float(a.split(',')[4].split(':')[1]))
            volume.append(float(a.split(',')[0].split(':')[1]))
            turnrate.append(float(a.split(',')[7].split(':')[1]))
            dif.append(float(a.split(',')[12].split(':')[1]))
            dea.append(float(a.split(',')[13].split(':')[1]))
            macd.append(float(a.split(',')[14].split(':')[1]))

            shijian_xueqiu = a.split(',')[-1].split('":"')[1][0:-1]
            c = time.mktime(time.strptime(shijian_xueqiu,"%a %b %d %H:%M:%S +0800 %Y"))
            time_tmp = datetime.datetime.fromtimestamp(c)
            timep.append(time_tmp)

        df = pd.DataFrame({'time':timep,
                           'open':openp,
                           'close':closep,
                           'high':highp,
                           'low':lowp,
                           'volume':volume,
                           'turnrate':turnrate,
                           'dif':dif,
                           'dea':dea,
                           'macd':macd})
        return df


                    



    def get_wangyi(daima,start_date,end_date):
    
        if daima[0:2]=='60':
            a = '0'+daima
        else:
            a = '1'+daima
                
        url='http://quotes.money.163.com/service/chddata.html?code='+a+'&start='+start_date+'&end='+end_date+'&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
        condition = True
        while condition:
            try:
                r = requests.get(url,timeout = 10)
                condition = False
            except:
                pass
        
        a1=pd.read_csv(StringIO(r.content),skiprows=[0],names=['shijian','daima','name','closep','haighp','lowp','openp','preclosep','CHG','PCHG','TURNOVER','volume','amount','zongshizhi','liutongshizhi'])
        if a1.empty:
            return None
        else:
            a2 = a1[a1['volume']<>0].sort_index(axis = 0,ascending=False)
            a3 = a2[['shijian','openp','haighp','lowp','closep','volume','amount','liutongshizhi','zongshizhi']]
            return a3


    def get_tenxun(daima):
        if daima[0:2]=='60':
            daima_new = 'sh'+daima
        else:
            daima_new = 'sz'+daima
        url = 'http://qt.gtimg.cn/q='+daima_new
        r = requests.get(url).content
        data = r.split('~')
        liutongzhishi = float(data[44])
        zongshizhi = float(data[45])
        return [liutongzhishi,zongshizhi]

    def zuhe():
        df_xueqiu = get_xueqiu(daima,start_date,end_date,fuquan)
        df_wangyi = get_wangyi(daima,start_date,end_date)
        tx_liutongshizhi = get_tenxun(daima)[0]
        tx_zongshizhi = get_tenxun(daima)[1]
        
        df_new = pd.DataFrame({'time':np.array(df_xueqiu['time']),
                               'open':np.array(df_xueqiu['open']),
                               'close':np.array(df_xueqiu['close']),
                               'high':np.array(df_xueqiu['high']),
                               'low':np.array(df_xueqiu['low']),
                               'volume':np.array(df_xueqiu['volume']),
                               'turnrate':np.array(df_xueqiu['turnrate']),
                               'dif':np.array(df_xueqiu['dif']),
                               'dea':np.array(df_xueqiu['dea']),
                               'macd':np.array(df_xueqiu['macd']),
                               'liutongshizhi':np.append(np.array(df_wangyi['liutongshizhi']),tx_liutongshizhi),
                               'zongshizhi':np.append(np.array(df_wangyi['zongshizhi']),tx_zongshizhi)})
        return df_new
        

    return zuhe()
        


def min_data(daima,start_date,end_date,n):

    def count_split_days(start_date,end_date):
        if datetime.datetime(int(start_date[0:4]),int(start_date[4:6]),int(start_date[6:]))<datetime.datetime(2015,1,5):
            num = (datetime.datetime(int(end_date[0:4]),int(end_date[4:6]),int(end_date[6:]))-datetime.datetime(2015,1,5)).days
        else:
            num = (datetime.datetime(int(end_date[0:4]),int(end_date[4:6]),int(end_date[6:]))-datetime.datetime(int(start_date[0:4]),int(start_date[4:6]),int(start_date[6:]))).days
        return num
        
        
    from gmsdk import md
    ret = md.init("yourname", "password")
    if daima[0:2]=='60':
        daima_new = str('SHSE.')+str(daima)
    else:
        daima_new = str('SZSE.')+str(daima)
    mins = n*60
    strtime = []
    openp = []
    high = []
    low = []
    close = []
    volume = []
    amount = []

    days_internal = 120

    LoopNum = divmod(count_split_days(start_date,end_date),days_internal)[0]+1
    left = divmod(count_split_days(start_date,end_date),days_internal)[1]
    bars_set = []
    n = 0
    for ln in range(0,LoopNum):
        if n == 0:
            bars = md.get_bars(daima_new,mins,str(datetime.datetime(int(start_date[0:4]),int(start_date[4:6]),int(start_date[6:]))+datetime.timedelta(days=days_internal*(ln)))[0:10]+' 09:00:00',str(datetime.datetime(int(start_date[0:4]),int(start_date[4:6]),int(start_date[6:]))+datetime.timedelta(days=days_internal*(ln+1)))[0:10]+' 15:30:00')
            n = n+1
        else:
            if ln == LoopNum-1:
                bars = md.get_bars(daima_new,mins,str(datetime.datetime(int(start_date[0:4]),int(start_date[4:6]),int(start_date[6:]))+datetime.timedelta(days=days_internal*(ln)+1))[0:10]+' 09:00:00',end_date[0:4]+'-'+end_date[4:6]+'-'+end_date[6:]+' 15:30:00')
                n = n+1
            else:
                bars = md.get_bars(daima_new,mins,str(datetime.datetime(int(start_date[0:4]),int(start_date[4:6]),int(start_date[6:]))+datetime.timedelta(days=days_internal*(ln)+1))[0:10]+' 09:00:00',str(datetime.datetime(int(start_date[0:4]),int(start_date[4:6]),int(start_date[6:]))+datetime.timedelta(days=days_internal*(ln+1)))[0:10]+' 15:30:00')
                n = n+1
                
            

        bars_set.append(bars)

    
    for SignalBars in bars_set:
        for b in SignalBars:
            strtime.append(b.strtime)
            openp.append(b.open)
            high.append(b.high)
            low.append(b.low)
            close.append(b.close)
            volume.append(b.volume)
            amount.append(b.amount)

    mins = pd.DataFrame({'strtime':strtime,
                        'open':openp,
                        'close':close,
                        'high':high,
                        'low':low,
                        'volume':volume,
                        'amount':amount})
    return mins
