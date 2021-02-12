import json
from pyqccapi.invoker.api_invoker import Task


class TaskEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Task):
            return {
                'method': obj.method,
                'params': obj.params,
                'success': obj.success,
                'code': obj.code,
                'message': obj.message,
                'data': obj.data
            }
        return json.JSONEncoder.default(self, obj)
