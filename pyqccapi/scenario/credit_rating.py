from multiprocessing.pool import Pool

from pyqccapi.scenario.base_scenario import *

"""
信用评级，用于构建外部信用指标
"""


def to_credit_rating(uni_id: str) -> list:
    """

    """

    method_id = 'adaf6ffb-3293-40e1-8715-ec6571f047d7'
    credit_rating = []
    params = {
        'searchKey': uni_id
    }

    task = to_task_invoker(Task(method_id, params)).invoke().to_task()

    if task.success:
        for rating in task.data['Result']:
            rating['uni_id'] = uni_id
            credit_rating.append(rating)

    return credit_rating


def to_credit_rating_list(uni_id_list: list) -> list:
    """

    """

    credit_rating_list = []
    for uni_id in uni_id_list:
        credit_rating_list += to_credit_rating(uni_id)

    return credit_rating_list


def to_credit_rating_list_parallel(uni_id_list: list) -> list:
    """

    """
    futures = []
    credit_rating_list = []

    pool = Pool(os.cpu_count())

    for i, uni_id in enumerate(uni_id_list):
        futures.append(pool.apply_async(func=to_credit_rating, args=(uni_id,)))

    pool.close()
    pool.join()

    for future in futures:
        credit_rating_list += future.get()

    return credit_rating_list
