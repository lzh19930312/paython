import requests
from bs4 import BeautifulSoup
import json,time

domain = 'http://ics.chinasoftinc.com:8010/'
jessionId=''
userToken='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjdXN0SWQiOiJCY0hWYXJMR3Z0VW15RHIxWXZHUUtaQlRxZnNOdlRMazZpcENlSEdnZnFzbWI5UkJ4d29IOGljVjdnYmF0aWlWT0JQM0w4RUdKaXRiaEhBMjNibHRvZm52MmxIc2tzYjdPV0hiRGdYZ0hnMm05MXRZMXNuVHdkV0hRYVlDZVlCbWtLN010azhWUXB2bUVvRDZOTnJDSnl5b3U0YkM3ZXdTb0FnV3VzczJ4dGs9IiwidXNlcklkIjoiaVJ6UC9haXJnUStTQlNoeTZXUnpCcVlLWno0allKWEprZGJpaE9QM0lQOUlITW1Od2dpMkRQYXd5Wml5SE9weWJhUUxsMlU1d0RZVmoycEtNNmVDdnhtck9VSlg3bEFzb0ZrM0k5RFgvTlZKQTlqZFVEd29Oem0yeE5lajNhbHR4S3M3alphTmJxUjlIdjFYQVNya2VyeTBWWE9MaXpERjQ0bDVZZDU4TmY4PSIsImVtcElkIjoiZVZMdHBLTWRXd3JqcmZCSDBIUGJnYVJFTmpMaDl6NGRVVG51czZJQ3gyWVlmR0wxQWI1dzg5REtNMmlMU1RJc1FRVnFhVC9NcnZkZkJLdmdIdDdGNGM2TnBybm9jalloeEpSb0svYUd0YXBEanNCNXkrNFcraWJ4MC9oek9PQ1daL0Q1SzIvMDZGVDhYYkdPcTR6RUVXR01iZ0F4a0NyTm1QdEJyQ1BoemRrPSIsInRva2VuVHlwZSI6ImVtcFdlYiIsInRpbWVzdGFtcCI6MTYxODg0NDY2OTMwOH0.TyklPil-i38q0l7b95yd08V1JF5PsJi_MU7480Emz78'
headers = {
    #'Cookie': 'JSESSIONID={};UserToken={};'.format(jessionId),
    'token': userToken
}
data={
    'pageIndex':1,
    'pageSize':999
}
r = requests.post(domain+'ehr_saas/web/attExamStep/getAttExamStepMyselfPage.empweb?',data=data, headers=headers)
respJson = json.loads(r.text)
spList = respJson['result']['data']['page']['items']
print(len(spList))
for shenpi in spList:
    # if shenpi['applyContent'].find('2021-04-') > -1:
    #     print("4月份: {} {}".format(shenpi['empName'],shenpi['applyContent']))
    #     continue
    if shenpi['examSource'] == 19 or shenpi['examSource'] == 3 or shenpi['examSource'] == 1:
        detailRequest = {
            'applyId': shenpi['applyId'],
            'edition': 2,
            'examId': shenpi['examId'],
            'examSource': shenpi['examSource']
        }
        headers['content-type']='application/json;charset=UTF-8'
        detailResponse = requests.post(domain+'ehr_saas/web/attExamStep/getAttExamStepDetail.empweb?',data=json.dumps(detailRequest), headers=headers)
        detailResponseJson = json.loads(detailResponse.text)
        examStep4MobileRequest = {
            'applyId': shenpi['applyId'],
            'examId': shenpi['examId'],
            'examSource': shenpi['examSource'],
            'isOver': shenpi['isOver'],
            'remark': shenpi['remark'],
            'state': 1
        }
        examMan={}
        stepList=detailResponseJson['result']['data']['stepList']
        if len(stepList) > 0:
            deptList=stepList[0]['deptList']
            if len(deptList) > 0:
                examManList=deptList[0]['examManList']
                if len(examManList) == 1:
                    examMan = examManList[0]
                elif len(examManList) == 2:
                    #审批通过  0 罗璐 1 邓辉
                    examMan = examManList[1]
        if len(examMan) > 1:
            if examMan['examManName'] == '邓辉':
                examStep4MobileRequest['examMans'] = json.dumps([examMan])
            else:
                print("下级审批不匹配 {} {}".format(shenpi['empName'],shenpi['applyContent']))
                continue
        requests.post(domain+'ehr_saas/web/attExamStep/examStep4Mobile.empweb?',data=json.dumps(examStep4MobileRequest), headers=headers)
        print('{}电子流审批结束 姓名 {} {}'.format(shenpi['examSourceXq'],shenpi['empName'],shenpi['applyContent']))
