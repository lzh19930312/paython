import requests
from bs4 import BeautifulSoup
import json,time

domain = 'http://oa.chinasoftinc.com:8888/'

jessionId = ''
headers = {
    'Cookie': 'JSESSIONID={};'.format(jessionId)
}
print('输入用户名:')
# login_user = input()
login_user = '109645'
print('输入密码:')
# login_passw = input()
login_passw = 'Luoxiaolu0317'
url = 'http://ics.chinasoftinc.com/login'
parmas = {
    'linkpage': 'http://oa.chinasoftinc.com:8888/sso.route?target=L3N5c3RlbS9mcmFtZS80L2luZGV4LmpzcA==',
    'loginFailurePage': 'http://oa.chinasoftinc.com:8888/',
    'userid': login_user,
    'password': login_passw,
    'verifyCode': '',
    'submit': ''
}
#登陆
if jessionId == '':
    r = requests.get(url, headers=headers, params=parmas)
    jessionId = r.history[1].cookies['JSESSIONID']
    print(jessionId)
headers = {
    'Cookie': 'JSESSIONID={};'.format(jessionId)
}
data = {
    'page': '1',
    'rows': '999',
    'flowId':'72'
}
#获取所有电子流
r = requests.post(domain+'workflow/getHandledWorks.action?flowSortId=0',data=data, headers=headers)
respJson = json.loads(r.text)
workFlows = respJson['rows']
print(len(workFlows))
for workFlow in workFlows:
    endTime = time.strptime(workFlow['endTime'], '%Y-%m-%d %H:%M:%S')
    if endTime.tm_year == 2020 and workFlow['flowName'] == '请假申请' and ((endTime.tm_mon == 11 and endTime.tm_mday > 4) or (endTime.tm_mon == 12 and endTime.tm_mday == 1)):
        request_data = {
            'runId': workFlow['runId'],
            'frpSid': workFlow['frpSid'],
            'view':'1'
        }
        #print(workFlow['runId'])
        resp = requests.post(domain+'flowRun/getFormPrintData.action',data=request_data,headers=headers)
        j_resp = json.loads(resp.text)
        form = BeautifulSoup(j_resp['rtData']['form'], "lxml")
        #角色
        juese = form.find('input',attrs={'title': '角色'})['value']
        #请假类型
        qjleixing = form.find('input',attrs={'title': '请假类别'})['value']
        #请假开始时间
        qjkssj = form.find('input',attrs={'title': '请假起始时间'})['value']
        #请假结束时间
        qjjssj = form.find('input',attrs={'title': '请假截止时间'})['value']
        #请假天数
        qjtj = form.find('input',attrs={'title': '天数'})['value']
        #请假小时数
        qjxss = form.find('input',attrs={'title': '小时'})['value']
        #是否同意
        jieguo = ''
        spyj = ''
        if juese == '员工':
            jieguo = form.find('input',attrs={'title': '直接主管是否同意'})['value']
            spyj = form.find('input',attrs={'title': '直接主管审批意见'})['value']
        else:
            jieguo = form.find('input',attrs={'title': '交付部经理或经理审批'})['value']
            spyj = form.find('input',attrs={'title': '交付部经理或经理审批意见'})['value']
        #审批意见
        
        print('请假申请 {} {} 审批时间 {} {} {} {} {}天 {}时 {} {}'.format(qjleixing,workFlow['runId'],workFlow['endTime'],workFlow['beginPerson'],qjkssj,qjjssj,qjtj,qjxss,jieguo,spyj))