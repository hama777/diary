#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import urllib.parse
import codecs
import os.path
import datetime

#from dt import datetime

version = "0.00"
out =  ""
logf = ""
appdir = os.path.dirname(os.path.abspath(__file__))
logfile = appdir + "\\dconv.log"

outputdir = "D:\\misc\\Dropbox\\doc\\diary\\"
youbi = ["月","火","水","木","金","土","日"]
teble_line = "<tr><td %s >%d</td><td %s>%s</td><td>%s</td></tr>"
#teble_line = "<tr bgcolor=""#ffffff""><td %s >%d</td><td %s>%s</td><td>%s</td></tr>"
template = appdir + "\\diaryconv.htm"
inputdir = "d:\\ols\diary\\"
holifile = inputdir + "holiday.txt"
holidata = []

def main_proc() :
    global out,logf,infofile
    logf = codecs.open(logfile, 'a', 'utf-8')
    logf.write("=== start %s === \n" % datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

    read_holiday()
    startyy = 2010
    startmm = 1
    endyy = 0
    endmm = 0
    if endyy == 0 :    # 終了年月が指定されていない場合は、今月まで
        wtoday = datetime.date.today()
        endyy = wtoday.year
        endmm = wtoday.month

    yy = startyy
    mm = startmm
    while True :
        monthly(yy,mm)
        if yy == endyy and mm == endmm :
            break 
        mm = mm + 1 
        if mm > 12 :
          yy = yy + 1 
          mm = 1 

def read_holiday() :
    holif = open(holifile, 'r')

    for line in holif :
        dt = line.split(";")
#        print(dt[0])
        holidata.append(dt[0])

    holif.close()

def monthly(yy,mm) :
    global out

    yydir = "%s%s\\" % (outputdir,yy)
    if not os.path.isdir(yydir) :
        os.mkdir(yydir)

    outputfile = '{0}{1}{2:02d}.htm'.format(yydir,yy, mm)
    out = open(outputfile,'w')
    f = open(template,'r')
    for line in f :
        if "%body" in line :
             body(yy,mm)
             continue
        if "%titledate" in line :
             out.write("%d 年 %d月" % (yy,mm))
             continue
        out.write(line)
    out.close()
    f.close()

def holicheck(yy,mm,dd) :
    for holi  in holidata :
        holidate  = holi.split("/")
        if holidate[0] == "*" : 
            hyy = -1
        else :
            hyy = int(holidate[0]) + 2000
        hmm = int(holidate[1])
        hdd = int(holidate[2])
        if hyy == -1 :
            if mm == hmm and dd == hdd :
                return True
        else :
            if yy == hyy and mm == hmm and dd == hdd :
                return True
    
    return False

def body(yy,mm) :
    inputfile = '{0}NIK{1}{2:02d}.txt'.format(inputdir,yy,mm)
    inf = open(inputfile,'r')
    day = 0 
    for line in inf :
        dt = line.split("\t")
        day = day + 1 
        holicolor = ""
        dateform = '{0}/{1:02d}/{2:02d}'.format(yy,mm,day)
        # NIKファイルは常に31日分の行数があるので、30日の月は例外になるため。
        try:
            week = youbi[datetime.datetime.strptime(dateform,'%Y/%m/%d').weekday()]
        except(ValueError) : 
            break 
        if week == "土" or week == "日" or holicheck(yy,mm,day)  :
            holicolor = "bgcolor=#ffd8dd"
        
        out.write(teble_line % (holicolor,day,holicolor,week,dt[1]))

    inf.close()

# -------------------------------------------------------------
main_proc()

