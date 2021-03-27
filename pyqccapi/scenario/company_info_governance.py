from pyqccapi.task.task_invoker import ApiInvoker, Task

"""
企业客户信息治理
根据企业名称等线索得到统一社会信用代码
"""


def to_uni_code_by_name(company_name):
    uni_code = ''
    task = Task(method='8a577c55-6fa9-430a-ab71-d54630713244',
                params={
                    'keyword': company_name
                })
    task = ApiInvoker(config_path='../config.yaml', task=task).invoke().to_task()
    if task.success:
        uni_code = task.data['Result']['CreditCode']
    return uni_code


def to_uni_code_by_list(companies):
    uni_code_list = []
    for company in companies:
        uni_code_list.append(to_uni_code_by_name(company))
    return uni_code_list




