import requests
from bs4 import BeautifulSoup
import json,time

domain = 'http://ics.chinasoftinc.com:8010/'
jessionId=''
userToken='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjdXN0SWQiOiJSeGpyN0I2RTRqd3grek43MHJOb3dhTmJRMi9nZ3VwcktPaTAvNi9FUTcycVY4WjlrNnRxTnJjeUFNTGFFMXo2a2xPKzV1ZlRXNkIvZkhVeVcxd3hkdVlieWpFZXMvbFByaERad2ZzVWJ3ZjBPV0E3ZGtDdEhlblFxcDNjaklLMHByZlFwTnVuaENUNjdRZEdWa3lwNWhJWFUxNmtXZWVPdy9HN0tyYWhTb1E9IiwidXNlcklkIjoiSU13NVVxakErS1RNL1d3bUlTWmZ3OVkrRHVRcWFNUDg5UVR3Qm0rWUE4UXNwak5WWWpYZ0U1TndnbnJweTNiL3JGcnYrWG8rdEF1cXBrUENtWTB5S3k1QWhWSEZQUWQvY3pJU1cyTitoTk1FTWhmZC9pWGdRSTJkcFpreHNzT0p0eDFHdnpNczhpMDd6ZGI2VTBrVkgxdThZQ1JIL0EzM3F2L1dVYnR1MjdrPSIsImVtcElkIjoiYjRvT0NPQVlYVVIwREVyeXpDYmNncS9SMEoyMVlXVWQ5L2tlM0NWUWova2VXL25USFJHWnZIYU15NllkU1hQL0g4YmRzSUFORlVBRjhZRGxjMlpONWswVUczQUNSQTVGUFhkMTVmRVBjSmVlVnNqL1cvellMbS80dHdDRDMyTk4ybDFqL3l3b1dVVDBOU1VDUnRNekVES2xVZjc1Qk5HZE1IYmt2dHNXSWU0PSIsInRva2VuVHlwZSI6ImVtcFdlYiIsInRpbWVzdGFtcCI6MTYwOTkwNDA5MjgyNX0.Wx8IztUvkAuot6WxB2YwP09K7FZqZhvoJlLzUh57iqg'
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
    detailRequest = {
        'applyId': shenpi['applyId'],
        'edition': 2,
        'examId': shenpi['examId'],
        'examSource': shenpi['examSource']
    }
    headers['content-type']='application/json;charset=UTF-8'
    detailResponse = requests.post(domain+'ehr_saas/web/attExamStep/getAttExamStepDetail.empweb?',data=json.dumps(detailRequest), headers=headers)
    detailResponseJson = json.loads(detailResponse.text)
    #获得流程校验后的节点成功
    checkExamRequest = {
        'applyId': shenpi['applyId'],
        'examId': shenpi['examId']
    }
    checkExamResponse = requests.post(domain+'ehr_saas/web/attExamStep/checkExamManSelfSelectLogic.empweb?',data=json.dumps(checkExamRequest), headers=headers)
    checkExamResponseJson = json.loads(checkExamResponse.text)
    examStepIds = checkExamResponseJson['result']['data']['examStepIds']
    #公出 转tim
    if shenpi['examSource'] == 19:
        sj = shenpi['applyContent'].split('<br/>')
        # 申请开始时间 申请结束时间 天数
        sjkssj = (sj[0].split('：'))[1]
        sjjssj = (sj[1].split('：'))[1]
        sjts = (sj[2].split('：'))[1]
        # examStepId 2055639759114256
        if examStepIds[0] == '2055639759114256':
            #审批通过
            examMan = detailResponseJson['result']['data']['stepList'][0]['deptList'][0]['examManList'][1]
            if examMan['examManName'] == '邓辉':
                examStep4MobileRequest = {
                    'applyId': shenpi['applyId'],
                    'examId': shenpi['examId'],
                    'examSource': shenpi['examSource'],
                    'isOver': shenpi['isOver'],
                    'remark': shenpi['remark'],
                    'state': 1,
                    'examMans': json.dumps([examMan])
                }
                requests.post(domain+'ehr_saas/web/attExamStep/examStep4Mobile.empweb?',data=json.dumps(examStep4MobileRequest), headers=headers)
                print('{}电子流审批结束, 姓名{} {}'.format(shenpi['examSourceXq'],shenpi['empName'],shenpi['applyContent']))
    #补签 年假
    elif shenpi['examSource'] == 3 or shenpi['examSource'] == 1:
        if detailResponseJson['result']['data']['currentExamManName'] == '罗璐-0000109645':
            examStep4MobileRequest = {
                    'applyId': shenpi['applyId'],
                    'examId': shenpi['examId'],
                    'examSource': shenpi['examSource'],
                    'isOver': shenpi['isOver'],
                    'remark': shenpi['remark'],
                    'state': 1
                }
            requests.post(domain+'ehr_saas/web/attExamStep/examStep4Mobile.empweb?',data=json.dumps(examStep4MobileRequest), headers=headers)
            print('{}电子流审批结束, 姓名{} {}'.format(shenpi['examSourceXq'],shenpi['empName'],shenpi['applyContent']))
