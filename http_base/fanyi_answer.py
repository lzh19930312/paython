import requests
import json,time
import hashlib
import random

def getFanYi(context):
    domain = 'http://fanyi.youdao.com'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'Host': 'fanyi.youdao.com',
        'Origin': 'http://fanyi.youdao.com',
        'Referer': 'http://fanyi.youdao.com/',
    }
    data = {
        'i': "You need to reduce the number of unplanned rollbacks of erroneous production deployments in your company's web hosting platform. Improvement to the QA/Test processes accomplished an 80% reduction.Which additional two approaches can you take to further reduce the rollbacks? Choose 2 answers",
        'from': 'AUTO',
        'to': 'AUTO',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_CLICKBUTTION'
    }
    data['i'] = context
    r = requests.post(domain+'/translate?smartresult=dict&smartresult=rule',data=data, headers=headers)
    result = json.loads(r.text)
    tgt_r=''
    for tgts in result['translateResult'][0]:
        tgt_r = tgt_r + tgts['tgt']
    return tgt_r

file = open("F:/Workspaces/anwer_2.json","r")
answers = json.loads(file.read())

for answer in answers:
    answer['question_zh'] = getFanYi(answer['question'])
    if isinstance(answer['answer'], list):
        answer_zh = []
        for x in answer['answer']:
            answer_zh.append(getFanYi(x))
        answer['answer_zh'] = answer_zh
    else:
        answer['answer_zh'] = getFanYi(answer['answer'])
file = open("F:/Workspaces/anwer_zh_2.json","w+",encoding='utf-8')
file.write(str(answers))
file.close()