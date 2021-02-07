import hashlib
import time
from enum import Enum

import requests

from pyqccapi import api_config
from pyqccapi.constant import error_code

encode = 'utf-8'
url_base = 'http://api.qichacha.com/'

dict_method_url = api_config.to_method_url_dict()


class TaskType(Enum):
    BASE = 0
    NEWS = 1


class Task:
    def __init__(self, method, params):
        self.method = method
        self.params = params
        self.success = False
        self.code = ''
        self.message = ''
        self.data = None
        self.type = TaskType.BASE


class ApiInvoker:
    def __init__(self,
                 config_path: str,
                 task: Task):
        self.config = api_config.to_config(config_path)
        self.task = task

    def to_token(self, timespan):
        token = self.config['appkey'] + timespan + self.config['seckey']
        md5 = hashlib.md5()
        md5.update(token.encode(encoding=encode))
        return md5.hexdigest().upper()

    def to_header(self):
        timespan = str(int(time.time()))
        return {'Token': self.to_token(timespan), 'Timespan': timespan}

    def invoke(self):
        url_req = dict_method_url[self.task.method]
        params = self.task.params
        params['key'] = self.config['appkey']

        r = requests.get(url=url_req,
                         headers=self.to_header(),
                         params=params)

        if r.status_code == 200:
            code = int(r.json()['Status'])
            self.task.code = code
            if code == 200:
                # self.task.data = json.dumps(str(r.content, encoding=encode))\
                #     .encode(encode)\
                #     .decode("unicode-escape")
                self.task.data = r.json()
                self.task.success = True
            else:
                self.task.message = error_code.get(str(code), '')
        else:
            self.task.code = r.status_code
            # self.task.message = error_code[r.status_code]
        return self

    def to_task(self):
        return self.task




