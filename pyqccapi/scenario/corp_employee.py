from multiprocessing.pool import Pool

from pyqccapi.constant import *
from pyqccapi.scenario.base_scenario import *


"""
企业主要人员，用于打通对公到对私的主要场景
"""


def to_employee_list_by_id(uni_id: str) -> dict:
    """
    根据统一社会信用代码，获取一个企业的员工列表
    :param uni_id:
    :return:
    """

    method_id = 'f46916ef-5910-4c2f-8216-f9cd708d5d36'
    page_size = 50
    employees = []
    params = {
        'searchKey': uni_id,
        'pageSize': page_size,
        'pageIndex': 1
    }

    task = to_task_invoker(Task(method_id, params)).invoke().to_task()

    if task.success:
        for employee in task.data['Result']:
            employee['uni_id'] = uni_id
            employees.append(employee)
        if task.data['Paging'] is not None:
            total = task.data['Paging']['TotalRecords']
        else:
            return employees
    else:
        return employees

    page_count = total // page_size + 1
    if page_count > 1:
        for i in range(page_count + 1)[2:]:
            params['pageIndex'] = i
            task = to_task_invoker(Task(method_id, params)).invoke().to_task()
            if task.success:
                for employee in task.data['Result']:
                    employee['uni_id'] = uni_id
                    employees.append(employee)

    return employees


def to_employee_list(uni_id_list: list) -> list:
    """
    根据统一社会信用代码列表，获取企业的员工列表，使用串行
    :param uni_id_list:
    :return:
    """
    employee_list = []
    for uni_id in uni_id_list:
        employee_list += to_employee_list_by_id(uni_id)
    return employee_list


def to_employee_list_parallel(uni_id_list: list) -> list:
    """
    根据统一社会信用代码列表，获取企业的员工列表，使用并行
    :param uni_id_list:
    :return:
    """
    futures = []
    employee_list = []

    pool = Pool(os.cpu_count())

    for i, uni_id in enumerate(uni_id_list):
        futures.append(pool.apply_async(func=to_employee_list_by_id, args=(uni_id,)))

    pool.close()
    pool.join()

    for future in futures:
        employee_list += future.get()

    return employee_list
