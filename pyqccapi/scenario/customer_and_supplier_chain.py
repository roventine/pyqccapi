import os
from multiprocessing.pool import Pool

from pyqccapi.scenario.base_scenario import *
from pyqccapi.util.encoders import *

"""
获取企业的客户及供应商信息，构建供应链图谱
"""


def to_customer_by_id(uni_id: str) -> Task:
    """
    根据统一社会信用代码，获取该企业的客户信息
    :param uni_id:
    :return:
    """
    method_id = '5a836c40-0888-40ad-99bc-5cf181f6a1f7'
    params = {
        'searchKey': uni_id
    }
    task = Task(method_id, params)
    return to_task_invoker(task) \
        .invoke() \
        .to_task()


def to_customer_list(uni_id_list: list) -> list:
    """
    根据统一社会信用代码列表，获取客户信息列表，串行执行
    :param uni_id_list:
    :return:
    """
    customer_list = []
    for uni_id in uni_id_list:
        customer_list.append(to_supplier_by_id(uni_id))
    return customer_list


def to_customer_list_parallel(uni_id_list: list) -> list:
    """
    根据统一社会信用代码列表，获取客户信息列表，并行执行
    :param uni_id_list:
    :return:
    """
    futures = []
    customer_list = []

    pool = Pool(os.cpu_count())

    for i, uni_id in enumerate(uni_id_list):
        futures.append(pool.apply_async(func=to_customer_by_id, args=(uni_id,)))

    pool.close()
    pool.join()

    for future in futures:
        customer_list.append(future.get())

    return customer_list


def to_supplier_by_id(uni_id: str) -> Task:
    """
    根据统一社会信用代码，获取该企业的供应商信息
    :param uni_id:
    :return:
    """
    method_id = 'cd046310-373d-4d40-9707-6cac199372a2'
    params = {
        'searchKey': uni_id
    }
    task = Task(method_id, params)
    return to_task_invoker(task) \
        .invoke() \
        .to_task()


def to_supplier_list(uni_id_list: list) -> list:
    """
    根据统一社会信用代码列表，获取供应商信息列表，串行执行
    :param uni_id_list:
    :return:
    """
    supplier_list = []
    for uni_id in uni_id_list:
        supplier_list.append(to_supplier_by_id(uni_id))
    return supplier_list


def to_supplier_list_parallel(uni_id_list: list) -> list:
    """
    根据统一社会信用代码列表，获取供应商信息列表，串行执行
    :param uni_id_list:
    :return:
    """
    futures = []
    supplier_list = []

    pool = Pool(os.cpu_count())

    for i, uni_id in enumerate(uni_id_list):
        futures.append(pool.apply_async(func=to_supplier_by_id, args=(uni_id,)))

    pool.close()
    pool.join()

    for future in futures:
        supplier_list.append(future.get())

    return supplier_list
