import requests
from bs4 import BeautifulSoup
import json,time

domain = 'http://ics.chinasoftinc.com:8010/'
jessionId=''
userToken='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjdXN0SWQiOiJleE5ReTY2MERla2VQcEVDZG82bk9VdUVuTDY3bjRJTksxdmRPalNnTjJFQlNTNzltaEFhQ29RWUkwSWFUNmptczVnaVBQTnlXbkJ5WW1GTGl6NzFlWUJmRkdnQlZRbXVQRXZaenNFb2VFbTlnWEYvQzd2YStINUdLbTN2UGFnMEl6dmRsWTF6L1BNTm4xK0tjS0FYYjFQNVEvaC95T0xBY29JOWhERmFrL2M9IiwidXNlcklkIjoiRXlubi9ialJVcXNaN1Z5MlBIckVYSDI2djRhSHQxNHhNaS81cC8vczltKzZzZEtqVHVPKzJzeEdmNjBqMlUrdGZhTWI0ZjBNb24zYldHRmlVTWtIaldoYitOZGtOcHVOYlhmbjcwNDA5aitvRHVFL0Z1aENWRlNNMUFqcDZDd25jRlVtdGU5WHJseWF1RTFVOUxNRGpMQVRJRExGSmMwck1HVjF2QzZFZWQ0PSIsImVtcElkIjoiTGMyWjNLeEtDb2FEK1dvZnVNTm94czcvSFN1TzVSOGMzN3UrNkdacFJoaFVRMnNDVjAxUWl5U1lzWHNKTU1LK1Q3TXV1ZUdrdnpRL0dha1dhSnJ3SURCZVdENDN1RWJVU1RvelB5L0VKTGRSNHZGcUNWZ1BLY2xPWCtFUkZlT1dHZEdsc2FPQkM0c3JaaVpNZ25qYmFqdEFlU3RSZkJsQ0c0c3JGczRKQmhvPSIsInRva2VuVHlwZSI6ImVtcFdlYiIsInRpbWVzdGFtcCI6MTYwOTczNDg5Mjk1Nn0.ecxO6Gh11u5p1Z7DTcwdk_IukfCivKmffQrhl79l7vw'
headers = {
    #'Cookie': 'JSESSIONID={};UserToken={};'.format(jessionId),
    'token': userToken,
    'content-type': 'application/json;charset=UTF-8'
}
data={
    'pageIndex':1,
    'pageSize':50,
    'search': '{"warnType":"999"}'
}
for i in range(1,50):
    r = requests.post(domain+'ehr_saas/web/syswarning/querySysWarningPages.empweb',data=data, headers=headers)
    respJson = json.loads(r.text)
    messageIds = []
    for item in respJson['result']['data']['page']['items']:
        messageIds.append(item['wId'])
    deleteSysMessageUnreadReq = {
        'messageIds': messageIds
    }
    print(json.dumps(deleteSysMessageUnreadReq))
    dr = requests.post(domain+'ehr_saas/web/syswarning/deleteSysMessageUnread.empweb?',data=json.dumps(deleteSysMessageUnreadReq), headers=headers)
    print(dr.text)
    print('{}-{} done'.format(50 * (i-1),50 * i))