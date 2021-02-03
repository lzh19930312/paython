import time, math

def getDateFromStr(strDate):
    return time.strptime(strDate, '%Y-%m-%d %H:%M:%S')

def splitYMD(strDate):
    return strDate.split('-')

def splitSpace(strDate):
    return strDate.split(' ')

def diffOneDayHours(eDate, sDate, xxsDate, xxeDate):
    diffH = eDate.tm_hour - sDate.tm_hour
    diffM = eDate.tm_min - sDate.tm_min
    diff = time.mktime(eDate) - time.mktime(sDate)
    if sDate < xxsDate and xxeDate < eDate:
        diff = diff - 5400
    diffH = math.ceil(diff/1800) * 0.5
    if diffH > 8:
        diffH = 8
    return diffH

def getDays( year, month ):
    day = 31                #定义每月最多的天数
    while day:
        try:
            time.strptime( '%s-%s-%d'%( year, month, day ), '%Y-%m-%d' )      #尝试将这个月最大的天数的字符串进行转化
            return day      #成功时返回得就是这个月的天数
        except:
            day -= 1        #否则将天数减1继续尝试转化, 直到成功为止

def getOneDayHours(startTime, endTime):
    startTime1 = splitSpace(startTime)
    endTime1 = splitSpace(endTime)

    startYMD = splitYMD(startTime1[0])
    endYMD = splitYMD(endTime1[0])
    if len(startTime) == 10:
        return ''
    sDate = getDateFromStr(startTime)
    eDate =  getDateFromStr(endTime)
    #休息开始时间
    xxsDate = getDateFromStr(endTime1[0] + ' 12:30:00')
    #休息结束时间
    xxeDate = getDateFromStr(endTime1[0] + ' 14:00:00')
    #上班时间
    sbDate = getDateFromStr(endTime1[0] + ' 9:00:00')
    #下班时间
    xbDate = getDateFromStr(endTime1[0] + ' 19:30:00')

    if eDate > xbDate:
        eDate = xbDate

    if startYMD[0] == endYMD[0] and startYMD[1] == endYMD[1] and startYMD[2] == endYMD[2]:
        if sDate < sbDate:
            sDate = sbDate
        return (str(diffOneDayHours(eDate, sDate, xxsDate, xxeDate)) + '小时')
    elif startYMD[0] == endYMD[0]  and startYMD[2] < endYMD[2]:
        diffD = (eDate.tm_yday - sDate.tm_yday) * 8
        if sDate < sbDate:
            sDate = sbDate
        return (str(diffOneDayHours(eDate, sDate, xxsDate, xxeDate) + diffD) + '小时')
    elif startYMD[0] == endYMD[0] and startYMD[1] < endYMD[1]:
        #同年不同月, 取指定月
        return ''
    elif startYMD[0] < endYMD[0]:
        diffD = ((getDays(startYMD[0], startYMD[1]) - sDate.tm_mday) + eDate.tm_yday) * 8
        #不同年
        if sDate < sbDate:
            sDate = sbDate
        return (str(diffOneDayHours(eDate, sDate, xxsDate, xxeDate) + diffD) + '小时')
    else:
        return ''
        