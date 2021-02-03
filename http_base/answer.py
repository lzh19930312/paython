import requests
import json,time

def getAnswer(item):
    if item['type'] == 1:
        return item['attr{}'.format(answerMap[item['qanswer']])]
    elif item['type'] == 2:
        qanswer = item['qanswer']
        answers = qanswer.split('|')
        result = []
        for answer in answers:
            key = 'attr{}'.format(answerMap[answer])
            result.append(item[key])
        return result

domain = 'http://xa.chinasoftinc.com'

jessionId = '3E5B30EE4D37E0F9AEC7E3BA0465CA85'
headers = {
    'Cookie': 'JSESSIONID={};'.format(jessionId)
}
#examid mtBD6AwXHsFx0sG
#uniqId nR8egd1416Q8nw0

#OFMHSzeAjsxhJE4
#JD9mGuGAY8EKN0U

#daxr4A0ygpXETL4
#qpg5uBlDarq0WTf

data = {
    'action': 'queryResult',
    'examid': 'OFMHSzeAjsxhJE4',
    'uniqId': 'JD9mGuGAY8EKN0U',
    'userid':'XHY1bTOujJMKGCv'
}
answerMap = {'A':'1','B':'2','C':'3','D':'4','E':'5','F':'6','G':'7'}
r = requests.post(domain+'/lms/Binput.do',data=data, headers=headers)
respJson = json.loads(r.text)
result = []
for item in respJson['root']:
    newItem = {}
    newItem['question'] = item['question']
    newItem['qanswer'] = item['qanswer']
    newItem['answer'] = getAnswer(item)
    result.append(newItem)
file = open("F:/Workspaces/anwer_2.json","w+")
file.write(json.dumps(result))
file.close()
