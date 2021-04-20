import requests
from bs4 import BeautifulSoup
import json,time

domain = 'http://oa.chinasoftinc.com:8888/'

jessionId = ''
headers = {
    'Cookie': 'JSESSIONID={};ROLTPAToken={}'
}
print('输入用户名:')
# login_user = input()
login_user = '109645'
print('输入密码:')
# login_passw = input()
login_passw = 'Luoxiaolu0317'
url = 'http://ics.chinasoftinc.com/login'
parmas = {
    'linkpage': '',
    'userid': login_user,
    'userName': login_user,
    'password': login_passw,
    'j_username': login_user,
    'j_password': login_passw
}
#登陆
if jessionId == '':
    r = requests.get(url, headers=headers, params=parmas)
    ROLTPAToken = r.history[0].cookies['ROLTPAToken']
    JSESSIONID = r.history[0].cookies['JSESSIONID']
headers = {
    'Cookie': 'JSESSIONID={};ROLTPAToken={}'.format(JSESSIONID, ROLTPAToken)
}
data={
    'empCode':'5VNmTd8d3HHW6IN/xp7LDQ=='
}
r=requests.get('http://ics.chinasoftinc.com:8010/sso/toLoginYellow',headers=headers,allow_redirects=True)
print(r.headers)
r1=requests.get(r.history[0].headers["location"],headers=headers,allow_redirects=True)
print(r1.status_code)
r2 = requests.get('http://ics.chinasoftinc.com:8010/ehr_saas/web/user/loginByEmpCode.jhtml',data=data,headers=headers)
print(r2.status_code)
print(r2.text)
r3 = requests.get('http://ics.chinasoftinc.com:8010/ehr_saas/web/attExamStep/getAttExamStepSer.empweb?',headers=headers)
print(r3.status_code)
print(r3.text)