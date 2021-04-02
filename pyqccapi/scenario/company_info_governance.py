from pyqccapi.scenario.base_scenario import *

"""
企业客户信息治理
根据企业名称等线索获取统一社会信用代码
"""


def to_uni_id_by_name(company_name: str) -> str:
    method_id = '8a577c55-6fa9-430a-ab71-d54630713244'
    params = {
        'searchKey': company_name
    }
    task = Task(method_id, params)
    return to_task_invoker(task) \
        .invoke() \
        .to_task()
    if task.success:
        uni_id = task.data['Result']['CreditCode']
    return uni_id


def to_uni_id_dict(companies):
    uni_id_dict = {}
    for company in companies:
        uni_id_dict[company] = to_uni_id_by_name(company)
    return uni_id_dict



