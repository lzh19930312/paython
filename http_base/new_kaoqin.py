import requests
from bs4 import BeautifulSoup
import json,time

domain = 'http://ics.chinasoftinc.com:8010/'
jessionId=''
userToken='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjdXN0SWQiOiJZQitoWFhUNVhYYWJsYlkzckJQWjZlczFsb25xR05iUWxqeVg0YkFnMzdFV2tDcGYrZFh0ejh4WUR0Tk8vWTlRRWdxT1Vselg1d29VNkFOV2oxT1h3bDA3Ui93Z3ZMd3RKVncxckF4aE9xbW9pMVNRVDFXMVVxN3I5cU9lZEw3NUp5VGVpcGsrWVJKRU1yTEQxNndlRFJGd0FYVWlTQVpjMnVITW5WYmZYQ0E9IiwidXNlcklkIjoiWHpmb0FNYmFNNy9vK1VZcURNbWh2b0k0RUlLVXo2RkVFeXNRM3djd0x6T0JRdHduMFdzcmF2VWRzT1JFUzBibUs4bTVUL01wK2lsN29ybEhyK2xNalFPeHAzMDlWNUg5ZE5La0JtM1g1VzhsT0pJTVI5c3NFZEkvNmV5MkZBanlYTEVkZzlnL1dVZGFlSHI3TlhEL0s2eUgwYkkyTlpub3dkUU1TVXFpaVY0PSIsImVtcElkIjoiYXdUV0VTOGV2SkVVRHB6Z1NGdkp5eHA1QU5GTmVZZTM3NmdjRCtPb0RveDJaSmRKMWJseDVHYWZXWWM5bE5UQkxuVGtuMzlyeDZndHhaQmE0M09Jdmh2a1hiaWY4WEFrWTl5WkxGOEFWMDN6Umpua2ZSckN2N0syNmMraW9WUTBubnE1cVpNS014cGVqUnJwSUsrcXVHditpNkcxUUhhTjdKNW1ZTmpCRzNrPSIsInRva2VuVHlwZSI6ImVtcFdlYiIsInRpbWVzdGFtcCI6MTYxMjI3MjQ3OTY1N30.6EVuUiYBsBnUMkRd2FmfTkG1UpSABFHg1_ChoPBUlX0'
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
    if shenpi['applyContent'].find('2021-02-') > -1:
        continue
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
        # 判断是否有下一级审批
        if len(detailResponseJson['result']['data']['stepList']) > 0:
            #审批通过  0 罗璐 1 邓辉
            examMan = detailResponseJson['result']['data']['stepList'][0]['deptList'][0]['examManList'][1]
            if examMan['examManName'] == '邓辉' or examMan['examManName'] == '罗璐':
                examStep4MobileRequest['examMans'] = json.dumps([examMan])
            else:
                break
        requests.post(domain+'ehr_saas/web/attExamStep/examStep4Mobile.empweb?',data=json.dumps(examStep4MobileRequest), headers=headers)
        print('{}电子流审批结束, 姓名{} {}'.format(shenpi['examSourceXq'],shenpi['empName'],shenpi['applyContent']))
