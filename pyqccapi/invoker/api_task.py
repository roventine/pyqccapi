from pyqccapi.base.api_config import config_instance


class Task:
    def __init__(self, method, params):
        self.method = method
        self.params = params
        self.success = False
        self.code = ''
        self.message = ''
        self.data = None

    def to_method_detail(self):
        return config_instance.to_method_detail(self.method)

    def to_request_url(self):
        return self.to_method_detail()['Titles']['paramList']['apiUrl']


