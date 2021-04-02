import os
from multiprocessing.pool import Pool

from pyqccapi.scenario.base_scenario import *

"""
股权穿透，用于获取客户股权关系图谱
"""


def to_equity_through_by_id(uni_id: str) -> dict:
    """
    根据统一社会信用代码列表，返回股权穿透信息
    :param uni_id:
    :return:
    """
    method_id = 'c2e25afe-65eb-4990-a609-110ffdf5963e'
    params = {
        'keyWord': uni_id
    }
    task = Task(method_id, params)
    return to_task_invoker(task) \
        .invoke() \
        .to_task()


def to_equity_through_list(uni_id_list: list) -> list:
    """
    根据统一社会信用代码列表，返回股权穿透列表，使用串行
    :param uni_id_list:
    :return:
    """
    equity_through_list = []
    for uni_id in uni_id_list:
        equity_through_list.append(to_equity_through_by_id(uni_id))
    return equity_through_list


def to_equity_through_list_parallel(uni_id_list: list) -> list:
    """
    根据统一社会信用代码列表，返回股权穿透列表，使用并行
    :param uni_id_list:
    :return:
    """
    futures = []
    equity_through_list = []

    pool = Pool(os.cpu_count())

    for i, uni_id in enumerate(uni_id_list):
        futures.append(pool.apply_async(func=to_equity_through_by_id, args=(uni_id,)))

    pool.close()
    pool.join()

    for future in futures:
        equity_through_list.append(future.get())

    return equity_through_list


# if __name__ == '__main__':
    # result_list = to_equity_through_list_parallel(['91460000MA5T1CK245','91310000054572362X'])
    # json.dumps(result_list, ensure_ascii=False, indent=4, cls=TaskEncoder)
    # pass
