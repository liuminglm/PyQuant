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
