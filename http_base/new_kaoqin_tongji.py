import requests, json, time, math
from bs4 import BeautifulSoup
from data_utils import dataUtils

domain = 'http://ics.chinasoftinc.com:8010/'
jessionId=''
userToken='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjdXN0SWQiOiJRcnAzVkFodFFMaSs5dnZPYXoySzc2SUpuNlZhRDhGU29qTnFURnNxelZxY25EVTZlSkxVd0VmbDhJVjg4cHBYTCt3d1BHVkxISlhvRWh0Wm1VTE9nUUZvRFFpaXMwMWI4amVKZHNFTUlmc1JVejJQOFFoY0RnbVdNMUZGSEg0MlQyVjhOdDR6OCsyY0k0ZzRtZ2FxU3F2UlBNS2pkT0I4YTV5YWIwK1JVVXM9IiwidXNlcklkIjoiZ3pDUFExRVF0UGZpbnhXNDdhN0czL2sxNHpLeTI4VDdyb28vOFZ1cDJpbFEwSXN5eWZnbmZ3N2JZR3lsK0ZoQ04rV3NBNE41YnJHdXVlSWtXdXNUSkYzOE83S0JUdEJ2ZU4raHBhd2FudFl6WlUyMVhIOGQvTUpsSWg0S2I4MmxxSDNPRXlZd3ZvK0YrM0taZGFpQ3Qrb3hoSk15cEllQ3doTjVQY3RiY2JZPSIsImVtcElkIjoiUmJaS1hJdGpib0Y1ZldUalFBajNIOE10ZnlWbU9Mc1hHWXNOMnFQREdGQWdsVk9tNzFjOHBzTUlraWRiRzJ3L2pWZjZmYlNHNlhQb3piakJPRVVML20xT2FzRzlMMldQdEtiTVpseDEyRzZ2VDlreXZXNlNFN0grQlB4MFk3RUp1Nk04ckJCVlpNZTZiTk43SGtjUGxia1VnZ0xCNkVXNW1EVjQzeGlSZXBJPSIsInRva2VuVHlwZSI6ImVtcFdlYiIsInRpbWVzdGFtcCI6MTYxMDM3NjAxODg3Nn0.d2eBUdIu1i59QbECFDyMC6b-yt3MN_xQPPWvZokvUhA'
headers = {
    #'Cookie': 'JSESSIONID={};UserToken={};'.format(jessionId),
    'token': userToken
}
pageIndex=1
while True:
    data={
        'deptId':'101472',
        'pageIndex':pageIndex,
        'pageSize':999
    }
    r = requests.post(domain+'ehr_saas/web/attExamStep/getAttExamStepHistoryMyselfPage.empweb?',data=data, headers=headers)
    respJson = json.loads(r.text)
    spList = respJson['result']['data']['page']['items']
    pageTotal = respJson['result']['data']['page']['pageTotal']
    for shenpi in spList:
        #if shenpi['state'] == 3:
        #    break
        applyContent = shenpi['applyContent']
        if (shenpi['examSourceXq'].find('假') > -1 or shenpi['examSourceXq'].find('休') > -1) and applyContent.find('2020-12') > -1:
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
