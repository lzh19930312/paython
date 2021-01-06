from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header
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
    'rows': '300'
}
#获取所有电子流
r = requests.post(domain+'workflow/getHandledWorks.action?flowSortId=0',data=data, headers=headers)
respJson = json.loads(r.text)
workFlows = respJson['rows']
print(len(workFlows))
msgs = []
for workFlow in workFlows:
    endTime = time.strptime(workFlow['endTime'], '%Y-%m-%d %H:%M:%S')
    if workFlow['flowName'] == '请假申请' and endTime.tm_mon == 11 and endTime.tm_mday >= 1:
        request_data = {
            'runId': workFlow['runId'],
            'frpSid': workFlow['frpSid'],
            'view':'1'
        }
        #print(workFlow['beginPerson'])
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
        msg = '请假申请 {} 审批时间 {} {} {} {} {}天 {}时 {} {}'
        msg = msg.format(qjleixing,workFlow['endTime'],workFlow['beginPerson'],qjkssj,qjjssj,qjtj,qjxss,jieguo,spyj)
        msgs.append(msg)
        print(msg)

mail_host = "smtp.qq.com"  #设置服务器
mail_user = "1451445318@qq.com"    #用户名
mail_pass = "zbrfviwwpbvrjaej"   #口令
sender = '1451445318@qq.com'
receivers = ['luolu@chinasofti.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

message = MIMEText("\r\n".join(msgs) + " ", 'plain', 'utf-8')
message['From'] = Header("1451445318@qq.com", 'utf-8')   # 发送者
message['To'] =  Header("luolu@chinasofti.com", 'utf-8')        # 接收者

subject = '电子流审批列表'
message['Subject'] = Header(subject, 'utf-8')

try:
    smtp_obj = SMTP_SSL(mail_host)
    smtp_obj.set_debuglevel(1)    # 25 为 SMTP 端口号
    smtp_obj.ehlo(mail_host)
    smtp_obj.login(mail_user, mail_pass)
    smtp_obj.sendmail(sender, receivers, message.as_string())
    smtp_obj.quit()
    print("邮件发送成功")
except SMTP_SSL.SMTPException:
    print("Error: 无法发送邮件")