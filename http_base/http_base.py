import requests
from bs4 import BeautifulSoup
import json,time


def saveQueRen(workFlow, saveFlowRunData, headers):
    requests.post(domain+'flowRun/updateRunLevel.action', data={'runId': workFlow['runId'], 'level': '1'}, headers=headers)
    requests.post(domain+'flowRun/saveFlowRunData.action', data=saveFlowRunData, headers=headers)

def rejectQingJia(form, j_resp, workFlow, message):
    saveFlowRunData = {}
    saveFlowRunData['SYS_DOC_DEPT_NAMES'] = ''
    saveFlowRunData['SYS_DOC_DEPT_IDS'] = ''
    if form.find('input',attrs={'id': 'DATA_5'})['value'] == 'PM/代PM':
        saveFlowRunData['DATA_50'] = form.find('input',attrs={'id': 'DATA_50'})['value']
        saveFlowRunData['EXTRA_50'] = form.find('input',attrs={'id': 'EXTRA_50'})['value']
        saveFlowRunData['DATA_62'] = form.find('input',attrs={'id': 'DATA_62'})['value']
        saveFlowRunData['EXTRA_62'] = form.find('input',attrs={'id': 'EXTRA_62'})['value']
        saveFlowRunData['DATA_48'] = message
        saveFlowRunData['DATA_44'] = '不同意'
    else:
        if j_resp['rtData']['flowPrcs']['sid'] == 587:
            saveFlowRunData['DATA_50'] = form.find('input',attrs={'id': 'DATA_50'})['value']
            saveFlowRunData['EXTRA_50'] = form.find('input',attrs={'id': 'EXTRA_50'})['value']
            saveFlowRunData['DATA_62'] = form.find('input',attrs={'id': 'DATA_62'})['value']
            saveFlowRunData['EXTRA_62'] = form.find('input',attrs={'id': 'EXTRA_62'})['value']
            saveFlowRunData['DATA_48'] = message
            saveFlowRunData['DATA_44'] = '不同意'
        else:
            saveFlowRunData['DATA_49'] = form.find('input',attrs={'id': 'DATA_49'})['value']
            saveFlowRunData['EXTRA_49'] = form.find('input',attrs={'id': 'EXTRA_49'})['value']
            saveFlowRunData['DATA_61'] = form.find('input',attrs={'id': 'DATA_61'})['value']
            saveFlowRunData['EXTRA_61'] = form.find('input',attrs={'id': 'EXTRA_61'})['value']
            saveFlowRunData['DATA_30'] = message
            saveFlowRunData['DATA_43'] = '不同意'
    saveFlowRunData['runId'] = workFlow['runId']
    saveFlowRunData['frpSid'] = workFlow['frpSid']
    saveFlowRunData['flowId'] = workFlow['flowId']
    saveQueRen(workFlow, saveFlowRunData, headers)
    preprcsList = requests.post(domain+'flowRun/getPrePrcsList.action', data={'flowId': workFlow['flowId'], 'frpSid': workFlow['frpSid']}, headers=headers)
    preprcsList_j=json.loads(preprcsList.text)
    print('reject 请假 runId:{}'.format(workFlow['runId']))
    requests.post(domain+'flowRun/backToOther.action', data={'flowId': workFlow['flowId'],'runId': workFlow['runId'], 'frpSid': workFlow['frpSid'], 'prcsTo': preprcsList_j['rtData'][0]['frpSid'],'isPhoneRemind':0}, headers=headers)

def rejectwaichu(form, j_resp, workFlow, message):
    saveFlowRunData = {}
    saveFlowRunData['SYS_DOC_DEPT_NAMES'] = ''
    saveFlowRunData['SYS_DOC_DEPT_IDS'] = ''
    if j_resp['rtData']['flowPrcs']['prcsName'] == '直接主管审批':
            saveFlowRunData['DATA_17'] = form.find('input',attrs={'id': 'DATA_17'})['value']
            saveFlowRunData['EXTRA_17'] = form.find('input',attrs={'id': 'EXTRA_17'})['value']
            saveFlowRunData['DATA_18'] = form.find('input',attrs={'id': 'DATA_18'})['value']
            saveFlowRunData['EXTRA_18'] = form.find('input',attrs={'id': 'EXTRA_18'})['value']
            saveFlowRunData['DATA_16'] = message
            saveFlowRunData['DATA_19'] = "不确认"
    elif j_resp['rtData']['flowPrcs']['prcsName'] == '交付经理/总监':
        saveFlowRunData['DATA_25'] = form.find('input',attrs={'id': 'DATA_25'})['value']
        saveFlowRunData['EXTRA_25'] = form.find('input',attrs={'id': 'EXTRA_25'})['value']
        saveFlowRunData['DATA_26'] = form.find('input',attrs={'id': 'DATA_26'})['value']
        saveFlowRunData['EXTRA_26'] = form.find('input',attrs={'id': 'EXTRA_26'})['value']
        saveFlowRunData['DATA_24'] = message
        saveFlowRunData['DATA_27'] = "不确认"
    saveFlowRunData['runId'] = workFlow['runId']
    saveFlowRunData['frpSid'] = workFlow['frpSid']
    saveFlowRunData['flowId'] = workFlow['flowId']
    saveQueRen(workFlow, saveFlowRunData, headers)
    preprcsList = requests.post(domain+'flowRun/getPrePrcsList.action', data={'flowId': workFlow['flowId'], 'frpSid': workFlow['frpSid']}, headers=headers)
    preprcsList_j=json.loads(preprcsList.text)
    print('reject 外出 runId:{}'.format(workFlow['runId']))
    requests.post(domain+'flowRun/backToOther.action', data={'flowId': workFlow['flowId'],'runId': workFlow['runId'], 'frpSid': workFlow['frpSid'], 'prcsTo': preprcsList_j['rtData'][0]['frpSid'],'isPhoneRemind':0}, headers=headers)


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
    'rows': '300'
}
#获取所有电子流
r = requests.post(domain+'workflow/getReceivedWorks.action?flowSortId=0',data=data, headers=headers)
respJson = json.loads(r.text)
turnModel = ''
redirectToTimData = {
    "runId": "",
    "flowId": "",
    "frpSid": "",
    "nextPrcsAlert": "0",
    "beginUserAlert": "0",
    "allPrcsUserAlert": "0",
    "viewPerson": "",
    "prcsEvent": "",
    "turnModel": '',
    "childFlowTurnModel": '[]'
}


workFlows = respJson['rows']
print(len(workFlows))
for workFlow in workFlows:
    if workFlow['flowName'] == '外出申请':
        #continue
        request_data = {
            'runId': workFlow['runId'],
            'frpSid': workFlow['frpSid']
        }
        resp = requests.post(domain+'flowRun/getHandlerData.action',data=request_data,headers=headers)
        j_resp = json.loads(resp.text)
        form = BeautifulSoup(j_resp['rtData']['form'], "lxml")
        #外出天数
        wcts = form.find('input',attrs={'id': 'DATA_8'})['value']
        #外出小时数
        wcsj = form.find('input',attrs={'id': 'DATA_9'})['value']
        wckssj = form.find('input',attrs={'id': 'DATA_6'})['value']
        wcjssj = form.find('input',attrs={'id': 'DATA_7'})['value']
        twckssj = time.strptime(wckssj, '%Y-%m-%d %H:%M:%S')
        twcjssj = time.strptime(wcjssj, '%Y-%m-%d %H:%M:%S')
        rejectwaichu(form, j_resp, workFlow, "作废")
        continue
        if twckssj.tm_mon != twcjssj.tm_mon:
            rejectwaichu(form, j_resp, workFlow, "不能跨月")
            continue
        if float(wcsj) == 8 or float(wcts) == 1 :
            if twckssj.tm_mday != twcjssj.tm_mday :
                print('外出申请 {} exception, 流水号 {}'.format(workFlow['beginPerson'], workFlow['runId']))
                continue
        elif float(wcts) > 1:
            if twcjssj.tm_mday - twckssj.tm_mday != (int(wcts)-1):
                print('外出申请 {} exception, 流水号 {}'.format(workFlow['beginPerson'], workFlow['runId']))
                continue
            
        saveFlowRunData = {}
        saveFlowRunData['SYS_DOC_DEPT_NAMES'] = ''
        saveFlowRunData['SYS_DOC_DEPT_IDS'] = ''
        saveFlowRunData['runId'] = workFlow['runId']
        saveFlowRunData['frpSid'] = workFlow['frpSid']
        saveFlowRunData['flowId'] = workFlow['flowId']
        if j_resp['rtData']['flowPrcs']['prcsName'] == '直接主管审批':
            saveFlowRunData['DATA_17'] = form.find('input',attrs={'id': 'DATA_17'})['value']
            saveFlowRunData['EXTRA_17'] = form.find('input',attrs={'id': 'EXTRA_17'})['value']
            saveFlowRunData['DATA_18'] = form.find('input',attrs={'id': 'DATA_18'})['value']
            saveFlowRunData['EXTRA_18'] = form.find('input',attrs={'id': 'EXTRA_18'})['value']
            saveFlowRunData['DATA_16'] = form.find('textarea',attrs={'id': 'DATA_16'}).get_text()
            saveFlowRunData['DATA_19'] = form.find('select', attrs={'id': 'DATA_19'}).find('option', attrs={'selected': 'selected'})['value']
        elif j_resp['rtData']['flowPrcs']['prcsName'] == '交付经理/总监':
            saveFlowRunData['DATA_25'] = form.find('input',attrs={'id': 'DATA_25'})['value']
            saveFlowRunData['EXTRA_25'] = form.find('input',attrs={'id': 'EXTRA_25'})['value']
            saveFlowRunData['DATA_26'] = form.find('input',attrs={'id': 'DATA_26'})['value']
            saveFlowRunData['EXTRA_26'] = form.find('input',attrs={'id': 'EXTRA_26'})['value']
            saveFlowRunData['DATA_24'] = form.find('textarea',attrs={'id': 'DATA_24'}).get_text()
            saveFlowRunData['DATA_27'] = "同意"
        saveQueRen(workFlow, saveFlowRunData, headers)
        #获取是否下一步转交
        redirect_json = json.loads(requests.post(domain+'flowRun/getTurnHandlerData.action', data={'runId': workFlow['runId'], 'flowId': workFlow['flowId'], 'frpSid': workFlow['frpSid'], 'prcsEvent': ''}, headers=headers).text)
        select_type = {}
        for sle in redirect_json['rtData']['prcsNodeInfos']:
            if 'autoSelect' in sle:
                select_type = sle
                break
        if select_type['prcsId'] == 1673:
            #137127 luolu
            #95227 tim
            turnModel = '[{"prcsId": "1673","opFlag": 1,"prcsUser": {},"opUser": "137127","timeout": {}}]'
        elif select_type['prcsId'] == 817:
            turnModel = '[{"prcsId":817,"opFlag":1}]'
        elif select_type['prcsId'] == 1674:
            turnModel = '[{"prcsId": "1673","opFlag": 1,"prcsUser": {},"opUser": "95227","timeout": {}}]'
        else:
            break
        redirectToTimData['runId'] = workFlow['runId']
        redirectToTimData['flowId'] = workFlow['flowId']
        redirectToTimData['frpSid'] = workFlow['frpSid']
        redirectToTimData['turnModel'] = turnModel
        #requests.post(domain+'flowRun/turnNextHandler.action',data=redirectToTimData,headers=headers)
        print('外出申请 {} done'.format(workFlow['beginPerson']))
    elif workFlow['flowName'] == '忘打卡申请':
        #continue
        request_data = {
            'runId': workFlow['runId'],
            'frpSid': workFlow['frpSid']
        }
        resp = requests.post(domain+'flowRun/getHandlerData.action',data=request_data,headers=headers)
        j_resp = json.loads(resp.text)
        form = BeautifulSoup(j_resp['rtData']['form'], "lxml")
        sbsj = form.find('input',attrs={'id': 'DATA_5'})['value']
        xbsj = form.find('input',attrs={'id': 'DATA_6'})['value']
        if sbsj != '':
            if int(sbsj.split(':')[0]) > 10:
                print('忘打卡申请 {} exception'.format(workFlow['beginPerson']))
                continue
        if xbsj != '':
            if int(xbsj.split(':')[0]) < 18:
                print('忘打卡申请 {} exception'.format(workFlow['beginPerson']))
                continue
        saveFlowRunData = {}
        saveFlowRunData['SYS_DOC_DEPT_NAMES'] = ''
        saveFlowRunData['SYS_DOC_DEPT_IDS'] = ''
        saveFlowRunData['DATA_55'] = form.find('input',attrs={'id': 'DATA_55'})['value']
        saveFlowRunData['EXTRA_55'] = form.find('input',attrs={'id': 'EXTRA_55'})['value']
        saveFlowRunData['DATA_75'] = form.find('input',attrs={'id': 'DATA_75'})['value']
        saveFlowRunData['EXTRA_75'] = form.find('input',attrs={'id': 'EXTRA_75'})['value']
        saveFlowRunData['DATA_70'] = form.find('input',attrs={'id': 'DATA_70'})['value']
        saveFlowRunData['DATA_74'] = form.find('textarea',attrs={'id': 'DATA_74'}).get_text()
        saveFlowRunData['DATA_53'] = '确认属实'
        saveFlowRunData['runId'] = workFlow['runId']
        saveFlowRunData['frpSid'] = workFlow['frpSid']
        saveFlowRunData['flowId'] = workFlow['flowId']
        #saveQueRen(workFlow, saveFlowRunData, headers)
        turnModel = '[{"prcsId":711,"opFlag":1}]'
        redirectToTimData['runId'] = workFlow['runId']
        redirectToTimData['flowId'] = workFlow['flowId']
        redirectToTimData['frpSid'] = workFlow['frpSid']
        redirectToTimData['turnModel'] = turnModel
        #requests.post(domain+'flowRun/turnNextHandler.action', data=redirectToTimData, headers=headers)
        # print(redirectToTimData)
        preprcsList = requests.post(domain+'flowRun/getPrePrcsList.action', data={'flowId': workFlow['flowId'], 'frpSid': workFlow['frpSid']}, headers=headers)
        preprcsList_j=json.loads(preprcsList.text)
        print('reject 忘打卡申请 runId:{}'.format(workFlow['runId']))
        requests.post(domain+'flowRun/backToOther.action', data={'flowId': workFlow['flowId'],'runId': workFlow['runId'], 'frpSid': workFlow['frpSid'], 'prcsTo': preprcsList_j['rtData'][0]['frpSid'],'isPhoneRemind':0}, headers=headers)
        #print('忘打卡申请 {} done'.format(workFlow['beginPerson']))
    elif workFlow['flowName'] == '请假申请':
        request_data = {
            'runId': workFlow['runId'],
            'frpSid': workFlow['frpSid']
        }
        #print(workFlow['beginPerson'])
        resp = requests.post(domain+'flowRun/getHandlerData.action',data=request_data,headers=headers)
        j_resp = json.loads(resp.text)
        form = BeautifulSoup(j_resp['rtData']['form'], "lxml")
        #请假类型
        qjleixing = form.find('input',attrs={'id': 'DATA_11'})['value']
        #请假开始时间
        qjkssj = form.find('input',attrs={'id': 'DATA_13'})['value']
        #请假结束时间
        qjjssj = form.find('input',attrs={'id': 'DATA_14'})['value']
        #请假天数
        qjtj = form.find('input',attrs={'id': 'DATA_60'})['value']
        #请假小时数
        qjxss = form.find('input',attrs={'id': 'DATA_16'})['value']
        tqjkssj = time.strptime(qjkssj, '%Y-%m-%d %H:%M:%S')
        tqjjssj = time.strptime(qjjssj, '%Y-%m-%d %H:%M:%S')
        rejectQingJia(form, j_resp, workFlow,"作废")
        continue
        if float(qjxss) == 1:
            if not(time.mktime(tqjjssj) - time.mktime(tqjkssj) == 3600):
                continue
        elif 1 < float(qjxss) < 8:
            if tqjkssj.tm_mday != tqjjssj.tm_mday:
                continue
            elif not('18:30:00' in qjjssj):
                rejectQingJia(form, j_resp, workFlow,"请以18:30为结束时间")
                continue
            elif not((time.mktime(tqjjssj) - time.mktime(tqjkssj))/3600 == float(qjxss)):
                rejectQingJia(form, j_resp, workFlow,"请假小时数不对")
                continue
        elif qjtj == '1' or qjxss == '8':
            if not (tqjkssj.tm_mday == tqjjssj.tm_mday and tqjkssj.tm_hour == 9 and tqjjssj.tm_hour == 18 and tqjkssj.tm_min==0 and tqjjssj.tm_min == 30):
                rejectQingJia(form, j_resp, workFlow,"请以09:00为开始时间以18:30为结束时间")
                continue
        elif int(qjtj) > 1:
            if not('18:30:00' in qjjssj):
                rejectQingJia(form, j_resp, workFlow,"请以09:00为开始时间以18:30为结束时间")
                continue
            elif tqjjssj.tm_mday - tqjkssj.tm_mday != (int(qjtj)-1):
                continue
        saveFlowRunData = {}
        saveFlowRunData['SYS_DOC_DEPT_NAMES'] = ''
        saveFlowRunData['SYS_DOC_DEPT_IDS'] = ''
        if form.find('input',attrs={'id': 'DATA_5'})['value'] == 'PM/代PM':
            saveFlowRunData['DATA_50'] = form.find('input',attrs={'id': 'DATA_50'})['value']
            saveFlowRunData['EXTRA_50'] = form.find('input',attrs={'id': 'EXTRA_50'})['value']
            saveFlowRunData['DATA_62'] = form.find('input',attrs={'id': 'DATA_62'})['value']
            saveFlowRunData['EXTRA_62'] = form.find('input',attrs={'id': 'EXTRA_62'})['value']
            saveFlowRunData['DATA_48'] = form.find('textarea',attrs={'id': 'DATA_48'}).get_text()
            saveFlowRunData['DATA_44'] = '同意'
        else:
            if j_resp['rtData']['flowPrcs']['sid'] == 587:
                saveFlowRunData['DATA_50'] = form.find('input',attrs={'id': 'DATA_50'})['value']
                saveFlowRunData['EXTRA_50'] = form.find('input',attrs={'id': 'EXTRA_50'})['value']
                saveFlowRunData['DATA_62'] = form.find('input',attrs={'id': 'DATA_62'})['value']
                saveFlowRunData['EXTRA_62'] = form.find('input',attrs={'id': 'EXTRA_62'})['value']
                saveFlowRunData['DATA_48'] = form.find('textarea',attrs={'id': 'DATA_48'}).get_text()
                saveFlowRunData['DATA_44'] = '同意'
            else:
                saveFlowRunData['DATA_49'] = form.find('input',attrs={'id': 'DATA_49'})['value']
                saveFlowRunData['EXTRA_49'] = form.find('input',attrs={'id': 'EXTRA_49'})['value']
                saveFlowRunData['DATA_61'] = form.find('input',attrs={'id': 'DATA_61'})['value']
                saveFlowRunData['EXTRA_61'] = form.find('input',attrs={'id': 'EXTRA_61'})['value']
                saveFlowRunData['DATA_30'] = form.find('textarea',attrs={'id': 'DATA_30'}).get_text()
                saveFlowRunData['DATA_43'] = '同意'
        saveFlowRunData['runId'] = workFlow['runId']
        saveFlowRunData['frpSid'] = workFlow['frpSid']
        saveFlowRunData['flowId'] = workFlow['flowId']
        saveQueRen(workFlow, saveFlowRunData, headers)
        #获取是否下一步转交
        redirect_json = json.loads(requests.post(domain+'flowRun/getTurnHandlerData.action', data={'runId': workFlow['runId'], 'flowId': workFlow['flowId'], 'frpSid': workFlow['frpSid'], 'prcsEvent': ''}, headers=headers).text)
        select_type = {}
        for sle in redirect_json['rtData']['prcsNodeInfos']:
            if 'autoSelect' in sle:
                select_type = sle
                break
        if select_type['prcsId'] == 1673:
            turnModel = '[{"prcsId": "1673","opFlag": 1,"prcsUser": {},"opUser": "95227","timeout": {}}]'
        elif select_type['prcsId'] == 817:
            turnModel = '[{"prcsId":817,"opFlag":1}]'
        elif select_type['prcsId'] == 585:
            turnModel = '[{"prcsId": "585","opFlag": 1,"prcsUser": {},"opUser": "243779","timeout": {}}]'
        elif select_type['prcsId'] == 587:
            turnModel = '[{"prcsId": "587","opFlag": 1,"prcsUser": {},"opUser": "137127","timeout": {}}]'
        elif select_type['prcsId'] == 588:
            turnModel = '[{"prcsId": "588","opFlag": 1,"prcsUser": {},"opUser": "95227","timeout": {}}]'
        else:
            continue
        redirectToTimData['runId'] = workFlow['runId']
        redirectToTimData['flowId'] = workFlow['flowId']
        redirectToTimData['frpSid'] = workFlow['frpSid']
        redirectToTimData['turnModel'] = turnModel
        #requests.post(domain+'flowRun/turnNextHandler.action',data=redirectToTimData,headers=headers)
        print('请假申请 请假类型 {} {} done {} {} {}天 {}时'.format(qjleixing,workFlow['beginPerson'],qjkssj,qjjssj,qjtj,qjxss))






# headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
