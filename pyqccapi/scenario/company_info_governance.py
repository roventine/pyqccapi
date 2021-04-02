import os
from multiprocessing.pool import Pool

from pyqccapi.scenario.base_scenario import *

"""
企业客户信息治理
根据企业名称等线索获取统一社会信用代码
"""


def to_uni_id_by_name(company_name: str) -> str:
    """

    :param company_name:
    :return:
    """
    method_id = '8a577c55-6fa9-430a-ab71-d54630713244'
    params = {
        'searchKey': company_name
    }
    task = Task(method_id, params)
    task = to_task_invoker(task).invoke().to_task()
    if task.success:
        uni_id = task.data['Result']['CreditCode']
    return uni_id


def to_corp_info(company: dict) -> dict:
    company['id_uni'] = to_uni_id_by_name(company['name'])
    return company


def to_corp_list_parallel(company_list: list) -> dict:
    """

    :param company_list:
    :return:
    """

    futures = []
    corp_list = []

    pool = Pool(os.cpu_count())

    for i, company in enumerate(company_list):
        futures.append(pool.apply_async(func=to_corp_info, args=(company,)))

    pool.close()
    pool.join()

    for future in futures:
        corp_list.append(future.get())

    return corp_list


def purify(corp_name:str)->str:
    corp_name = corp_name.strip()
    if corp_name.endswith(")") or corp_name.endswith("）"):
        start_pos = corp_name.index("(")



if __name__ == '__main__':
    corp_list = []
    with open('d:/tmp/ABCSH_CUST_ORG_GOV_FAIL.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            cols = line.split('|!')
            id = cols[0]
            corp_name = purify(cols[1])
            corp_list.append({
                'id': id,
                'name':corp_name
             })

