from pyqccapi.constant import *
from pyqccapi.scenario.base_scenario import *
from pyqccapi.util.dates import *


def to_news_detail_by_id(id_news: str) -> Task:
    """
    根据新闻id，获取新闻详情
    :param id_news:
    :return:
    """
    method_id = '7501bee3-4242-4e72-aec3-4ed756c8e6a0'
    params = {
        'id': id_news
    }
    task = Task(method_id, params)
    return to_task_invoker(task) \
        .invoke() \
        .to_task()


def to_news_summary_list_at_date(id_uni: str, dt: str) -> list:
    """
    根据统一社会信用代码，获取一个企业在给定日期的新闻概要列表
    :param id_uni:
    :param dt:
    :return:
    """
    method_id = '3a5dd06b-aec5-445d-9b91-82be4d5b884b'
    page_size = 50
    summary_list = []

    params = {
        'searchKey': id_uni,
        'startDate': dt,
        'endDate': dt,
        'pageSize': page_size,
        'pageIndex': 1
    }
    task = Task(method_id, params)
    t = to_task_invoker(task).invoke().to_task()

    if t.success:
        total = t.data['Paging']['TotalRecords']
    else:
        task.code = t.code
        task.message = t.message
        return summary_list

    page_count = total // page_size + 1

    for i in range(page_count + 1)[1:]:
        params['pageIndex'] = i
        task = Task(method_id, params)
        task = to_task_invoker(task).invoke().to_task()
        if task.success:
            for summary in task.data['Result']:
                summary['CategoryName'] = to_news_category_for_human(summary['Category'])
                summary_list.append(summary)

    return summary_list


def to_news_detail_by_summary(news: dict) -> dict:
    """
    根据新闻摘要，填充新闻具体内容，返回填充后的新闻对象
    :param news:
    :return:
    """
    t = to_news_detail_by_id(news['NewsId'])
    if t.success:
        news['Content'] = t.data['Result']['Content']
    return news


def to_news_detail_list_at_date(id_uni: str, dt: str) -> list:
    """
    根据统一社会信用代码，获取一个企业在给定日期的新闻详情列表
    :param id_uni:
    :param dt:
    :return:
    """
    detail_list = []

    for summary in to_news_summary_list_at_date(id_uni, dt):
        detail_list.append(to_news_detail_by_summary(summary))

    return detail_list


def to_news_detail_list_by_period(id_uni: str, start: str, end: str) -> list:
    """
    根据统一社会信用代码，获取一个企业在给定日期范围内的新闻详情列表
    :param id_uni:
    :param start:
    :param end:
    :return:
    """
    period_list = []

    days_diff = to_days_diff(start, end)
    for i in range(days_diff):
        date_after = to_date_after(start, i)
        period_list += to_news_detail_list_at_date(id_uni, date_after)
    return period_list


# def to_news_dict_by_date(dt: str) -> dict:
#     news_dict = {}
#     for k, v in uni_id_map.items():
#         news_dict[v] = to_news_detail_list(v, dt)
#     return news_dict


# def to_news_dict_by_period(start, end):
#     period_news_dict = {}
#     days_diff = to_days_diff(start, end)
#     for i in range(days_diff):
#         date_after = to_date_after(start, i)
#         period_news_dict[date_after] = to_news_collection_by_date(date_after)
#     return period_news


def to_news_category_for_human(news_categories: str) -> str:
    """
    将新闻类别翻译为人类能看懂的中文
    :param news_categories:
    :return:
    """
    l = []
    if news_categories.find(',') >= 0:
        for category in news_categories.split(','):
            l.append(news_category.get(category))
    else:
        if len(news_categories) > 0:
            l.append(news_category.get(news_categories))
    return ','.join(l)

# def to_news_record(id_uni: str, news: dict):
#     return [id_uni, news['EmotionType'],
#             to_news_category_for_human(news['Category']),
#             news['NewsTags'],
#             text,
#             news['Url'],
#             news['Source']];


# s = to_news_collection_by_period('20210101', '20210331')
# with open('news_collection_20210101_20210331.json', 'w', encoding='utf-8') as f:
#     json.dump(s, f, ensure_ascii=False, indent=4, cls=TaskEncoder)

# news_result = []
# news_collection = jsons.of_json_file('news_collection_20210101_20210331.json')
# for daily_news_dict in news_collection:
#     for (id_uni, daily_news) in news_collection[daily_news_dict].items():
#         if len(daily_news) > 0:
#             for news in daily_news:
#                 content = news['Content']
#                 if not content == '':
#                     text = texts.to_text(content)
#                     news_result.append(to_news_record(id_uni, news))
# print(news_result)
# json.dumps(news_result, ensure_ascii=False, indent=4)


# with open('test.csv', 'w',encoding='utf-8',newline='') as f:
#     f_csv = csv.writer(f)
#     f_csv.writerows(news_result)
