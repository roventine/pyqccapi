import hashlib
import time

import requests

from pyqccapi.constant import error_code
from pyqccapi.invoker.api_task import *
from pyqccapi.util.yamls import *

encode = 'utf-8'
url_base = 'http://api.qichacha.com/'


class ApiInvoker:
    def __init__(self,
                 config_path: str,
                 task: Task):
        self.config = of_yaml(config_path)
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
        url_req = self.task.to_request_url()
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


