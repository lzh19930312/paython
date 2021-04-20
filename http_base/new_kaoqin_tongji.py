import requests, json, time, math
from bs4 import BeautifulSoup
from data_utils import dataUtils

domain = 'http://ics.chinasoftinc.com:8010/'
jessionId=''
userToken='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjdXN0SWQiOiJQLzVEa3RqTENkSVM5SnI0MW83ZGF5QVFsakluQ3RsN3RzeStxQUtNdno0VmJLdENKU3J2blVreVljMTVJcmtVODNzQzUzRXBDN0YvQVZjRGUvRGJTbTFoWjU4Tnl1MUhpRnRydkhvQXRodktEZTdXUjB2OEJGSDZYNXgxSzhoWWtHbFJMaVd5c29WV281NWxWMWpNNStPN05wTWpKbitpTkhEZFVPQXlCLzQ9IiwidXNlcklkIjoiVVZLME1WTHE1N3ovN2lVbUNmblN4RktuUCtDakZOaSs3K3FwT1M1bUg3Z09yWXFXQTMvUVVtUFMyM1ZCcHppbjBrOUdSRjJ6U0xDMEVVMVBDRkl5MjJsamFoYzdvVXBvOFhoWGZzcjMydmZsNDlNNzM0TXI0U3NmMzBsbVM1NEtBSTJCNlhLWHpNUUh4alpnakpTZHlsdThDSWsyT0R2eVlOWE0rRW1EV2FVPSIsImVtcElkIjoiV2ZZMXU4QnlrMVE1RFNzOFZVVzdlYytkcjdrRkFJcXZDTHBQOEkwMDNYaTRIKzFKN1JSZGxXKzhmSzdPQzlWTmIxLzBnR3pCeERTWjhJbHNwK1JpYVk4YkxKeE5Ua1AxNlR3SWFUSFV6QmdCaUMwNjBzczF3R002L2pjUDRhMGVtbFMvcUlHTGZyRjRUNkpGc2ZDczZjYlU1U2lSUk1KQXZ3T25ZRDUzY3JFPSIsInRva2VuVHlwZSI6ImVtcFdlYiIsInRpbWVzdGFtcCI6MTYxNzE5OTI3ODIwN30.A7VIjgPDJCcsU3aMaSZ0OQK2MaWVwL4EUOId8qdE9cU'
headers = {
    #'Cookie': 'JSESSIONID={};UserToken={};'.format(jessionId),
    'token': userToken
}
pageIndex=1
while True:
    data={
        'deptId':'101472',
        'pageIndex':pageIndex,
        'pageSize':999,
        'search': '{"approvalStartTime":"2021-03-30","approvalEndTime":"2021-03-30 23:59:59"}'
        
    }
    r = requests.post(domain+'ehr_saas/web/attExamStep/getAttExamStepHistoryMyselfPage.empweb?',data=data, headers=headers)
    respJson = json.loads(r.text)
    spList = respJson['result']['data']['page']['items']
    pageTotal = respJson['result']['data']['page']['pageTotal']
    for shenpi in spList:
        #if shenpi['state'] == 3:
        #    break
        applyContent = shenpi['applyContent']
        if (shenpi['examSourceXq'].find('假') > -1 or shenpi['examSourceXq'].find('休') > -1) and applyContent.find('2021-03') > -1:
            sj = applyContent.split('<br/>')
            sjkssj = (sj[0].split('：'))[1]
            sjjssj = (sj[1].split('：'))[1]
            sjts = (sj[2].split('：'))[1]
            result = dataUtils.getOneDayHours(sjkssj, sjjssj)
            if result == '':
                result = sjts
            statusStr = '通过'
            print('{}*{}*{}*{}*{}*{}'.format(shenpi['examSourceXq'],shenpi['empName'],sjkssj, sjjssj,result,statusStr))
    if pageIndex == pageTotal:
        print('last page End')
        break
    if pageTotal > 1:
        pageIndex = pageIndex + 1
    else:
        print('only 1 page End')
        break
