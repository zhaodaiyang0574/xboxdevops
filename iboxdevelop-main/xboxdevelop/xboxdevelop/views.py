from django.http import HttpResponse
import grequests
import requests
import json
import re

def appname(request):
    if request.method == 'POST':
        json_str = request.body
        data_str = json.loads(json_str)
        token = data_str.get("token", "")
        point = data_str.get("linkage_params", "").get("point")
        if token == "xxxxxxxxxxxxxxxxx":
            # session = requests.Session()
            json_headers = {'Content-Type': 'application/json'}
            # Create the play
            payload = {"username": "xxx", "password": "xxx", "type": "default"}
            # get access_token
            login_url = requests.post("https://spug.xxx.com/api/account/login/", data=json.dumps(payload),headers=json_headers)
            data = json.loads(login_url.text)
            access_toke = data.get('data').get('access_token')
            token_headers = {'X-Token': access_toke}
            app_url = requests.get("https://spug.xxx.com/api/app/", headers=token_headers)
            app_data = json.loads(app_url.text)

            #thread
            app_key = []
            for data in app_data.get('data'):
                app_key.append(data.get('key'))
            req_list = [grequests.get('https://spug.xxx.com/api/apis/config/?apiKey=xxxxxxxxxxxxxxxx=' + u + '&env=prod&noPrefix=1&format=json') for u in app_key]
            reps_list = grequests.map(req_list)

            options = []
            texts_zh_cn = {}
            texts_en_us = {}
            i = 0
            for j in reps_list:
                data = json.loads(j.text)
                if data:
                    if data.get('type') == point:
                        i = i + 1
                        appname = '-'.join(re.findall(r'(\w+)_(\w+)_(\w+)_(\w+)', j.url)[0])
                        if i == 1:
                            options.append({
                                "id": "%s" % str(i),
                                "value": appname,
                                "isDefault": True
                            })
                        else:
                            options.append({
                                "id": "%s" % str(i),
                                "value": appname,
                            })
                        texts_zh_cn[appname] = appname
                        texts_en_us[appname] = appname
            ret = {
                        "code": 0,
                        "msg": "success!",
                        "data": {
                            "result": {
                                "options": options,
                                "i18nResources": [
                                    {
                                        "locale": "zh_cn",
                                        "isDefault": True,
                                        "texts": texts_zh_cn
                                    },
                                    {
                                        "locale": "en_us",
                                        "isDefault": False,
                                        "texts": texts_en_us
                                    }
                                ]
                            }
                        }
                    }
            return HttpResponse(json.dumps(ret))

