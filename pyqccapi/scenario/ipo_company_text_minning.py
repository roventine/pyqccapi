import csv

from pyqccapi.constant import *
from pyqccapi.environment import *
from pyqccapi.task.task_invoker import ApiInvoker
from pyqccapi.util import jsons
from pyqccapi.util import texts
from pyqccapi.util.dates import *
from pyqccapi.util.encoders import *
from pyqccapi.util.logger import logger

Environment('../config.yaml')

ipo_company_list = {
    '上海之江生物科技股份有限公司',
    '上海艾为电子技术股份有限公司',
    '上海丛麟环保科技股份有限公司',
    '上海禾赛科技股份有限公司',
    '上海微创电生理医疗科技股份有限公司',
    '上海复旦微电子集团股份有限公司',
    '上海国缆检测股份有限公司',
    '上海毕得医药科技股份有限公司',
    '南侨食品集团（上海）股份有限公司',
    '上海能辉科技股份有限公司',
    '上海奥普生物医药股份有限公司',
    '上海霍普建筑设计事务所股份有限公司',
    '上海皓元医药股份有限公司',
    '天士力生物医药股份有限公司',
    '上海翼捷工业安全设备股份有限公司',
    '上海海优威新材料股份有限公司',
    '上海微创医疗机器人（集团）股份有限公司',
    '上海盟科药业股份有限公司',
    '上海芯龙半导体技术股份有限公司',
    '上海行动教育科技股份有限公司',
    '读客文化股份有限公司',
    '超捷紧固系统（上海）股份有限公司',
    '上海中洲特种合金材料股份有限公司',
    '上海盛剑环境系统科技股份有限公司',
    '上海睿昂基因科技股份有限公司',
    '上海保立佳化工股份有限公司',
    '上海艾录包装股份有限公司',
    '上海肇民新材料科技股份有限公司',
    '上海凯淳实业股份有限公司',
    '上海永茂泰汽车科技股份有限公司',
    '上海尤安建筑设计股份有限公司',
    '上海罗曼照明科技股份有限公司',
    '上海太和水环境科技发展股份有限公司',
    '南侨食品集团（上海）股份有限公司',
    '上海新炬网络信息技术股份有限公司',
    '上海德必文化创意产业发展（集团）股份有限公司',
    '上海霍普建筑设计事务所股份有限公司',
    '上海电气风电集团股份有限公司',
    '上海皓元医药股份有限公司',
    '上海翼捷工业安全设备股份有限公司',
    '上海华依科技集团股份有限公司',
    '上海霍莱沃电子系统技术股份有限公司',
    '格科微有限公司',
    '盛美半导体设备（上海）股份有限公司'
}


def to_uni_id_map():
    uni_id_map = {}
    for company in ipo_company_list:
        task = Task(method='a038dd89-121d-4830-9993-b9c429ee01e0',
                    params={
                        'keyword': company
                    })
        task = ApiInvoker(config_path='../config.yaml', task=task).invoke().to_task()
        if task.success:
            uni_id_map[company] = task.data['Result']['CreditCode']
    return uni_id_map


uni_id_map = {
    '上海睿昂基因科技股份有限公司': '91310120590029056K',
    '上海罗曼照明科技股份有限公司': '913100006314149553',
    '上海华依科技集团股份有限公司': '91310000631238592E',
    '上海永茂泰汽车科技股份有限公司': '91310118742121602R',
    '上海尤安建筑设计股份有限公司': '91310110757926286X',
    '上海微创电生理医疗科技股份有限公司': '913101155618553243',
    '上海艾为电子技术股份有限公司': '91310000676257316N',
    '上海禾赛科技股份有限公司': '91310114320742767K',
    '上海奥普生物医药股份有限公司': '91310115133295009P',
    '上海毕得医药科技股份有限公司': '91310110660715642B',
    '上海微创医疗机器人（集团）股份有限公司': '91310115329558376Y',
    '上海丛麟环保科技股份有限公司': '91310112MA1GBNPD17',
    '超捷紧固系统（上海）股份有限公司': '91310000729528125L',
    '上海国缆检测股份有限公司': '91310113759006977Q',
    '上海凯淳实业股份有限公司': '91310118682255907X',
    '上海中洲特种合金材料股份有限公司': '91310000740597762W',
    '上海皓元医药股份有限公司': '91310000794467963L',
    '南侨食品集团（上海）股份有限公司': '91310000558792983B',
    '读客文化股份有限公司': '91310116690106151R',
    '上海太和水环境科技发展股份有限公司': '91310116566529966T',
    '上海能辉科技股份有限公司': '91310000685457643J',
    '上海霍普建筑设计事务所股份有限公司': '913100006762867235',
    '上海海优威新材料股份有限公司': '913100007811009510',
    '上海盛剑环境系统科技股份有限公司': '9131011459814645XR',
    '上海德必文化创意产业发展（集团）股份有限公司': '91310000572698184Q',
    '上海新炬网络信息技术股份有限公司': '91310118320863016N',
    '上海霍莱沃电子系统技术股份有限公司': '91310000664324630E',
    '上海翼捷工业安全设备股份有限公司': '91310000682266227Y',
    '天士力生物医药股份有限公司': '91310000733341187M',
    '上海行动教育科技股份有限公司': '91310000787230976G',
    '上海复旦微电子集团股份有限公司': '91310000631137409B',
    '上海艾录包装股份有限公司': '913100007927010822',
    '上海盟科药业股份有限公司': '91310115599770596C',
    '盛美半导体设备（上海）股份有限公司': '91310000774331663A',
    '上海肇民新材料科技股份有限公司': '91310116585243154G',
    '上海电气风电集团股份有限公司': '91310112792759719A',
    '上海之江生物科技股份有限公司': '913100007743014560',
    '上海保立佳化工股份有限公司': '91310000729349653F',
    '上海芯龙半导体技术股份有限公司': '913100005964495291'
}

# 从全局变量中获取比较合适
path_config = ''


def to_task_invoker(task: Task):
    return ApiInvoker(task)


def to_news_detail(id_news: str) -> Task:
    """
    根据新闻id获取新闻内容
    :param id_news:
    :return:一个字典，包含调用结果
    """
    method_id = '7501bee3-4242-4e72-aec3-4ed756c8e6a0'
    params = {
        'id': id_news
    }
    task = Task(method_id, params)
    return to_task_invoker(task) \
        .invoke() \
        .to_task()


def to_news_summary_list(id_uni: str, dt: str):
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
                category_names = []
                category_list = str(summary['Category']).split(',')
                for category in category_list:
                    category_names.append(news_category.get(category, ''))
                summary['CategoryName'] = ','.join(category_names)
                summary_list.append(summary)

    return summary_list


def to_news_detail(id_news: str):
    """
    根据新闻id获取新闻内容
    :param id_news:
    :return:一个字典，包含调用结果
    """
    method_id = '7501bee3-4242-4e72-aec3-4ed756c8e6a0'
    params = {
        'id': id_news
    }
    task = Task(method_id, params)
    return to_task_invoker(task).invoke().to_task()


def to_news_detail_by_summary(news: dict):
    """
    根据新闻摘要，填充新闻内容
    :param news:新闻摘要字典
    :return:填充内容后的完整新闻内容，如果调用失败则不填充
    """
    t = to_news_detail(news['NewsId'])
    if t.success:
        news['Content'] = t.data['Result']['Content']
    return news


def to_news_detail_list(id_uni: str, dt: str):
    """
    一个容忍失败的版本，适合调用且只调用一次的场景
    :return:
    """
    try:
        news_list = []

        summary_list = to_news_summary_list(id_uni, dt)
        if len(summary_list) == 0:
            return news_list
        for summary in summary_list:
            news_list.append(to_news_detail_by_summary(summary))

    except Exception as e:
        logger.error(e)

    return news_list


def to_news_collection_by_date(d):
    daily_news = {}
    for k, v in uni_id_map.items():
        daily_news[v] = to_news_detail_list(v, d)
    return daily_news


def to_news_collection_by_period(start, end):
    period_news = {}
    days_diff = to_days_diff(start, end)
    for i in range(days_diff):
        date_after = to_date_after(start, i)
        period_news[date_after] = to_news_collection_by_date(date_after)
    return period_news


def to_news_category_for_human(news_categories: str):
    l = []
    if news_categories.find(',') >= 0:
        for category in news_categories.split(','):
            l.append(news_category.get(category))
    else:
        if len(news_categories)>0:
            l.append(news_category.get(news_categories))
    return ','.join(l)


def to_news_record(id_uni, news):
    return [id_uni, news['EmotionType'],
         to_news_category_for_human(news['Category']),
         news['NewsTags'],
         text,
         news['Url'],
         news['Source']];


# s = to_news_collection_by_period('20210101', '20210331')
# with open('news_collection_20210101_20210331.json', 'w', encoding='utf-8') as f:
#     json.dump(s, f, ensure_ascii=False, indent=4, cls=TaskEncoder)

news_result = []
news_collection = jsons.of_json_file('news_collection_20210101_20210331.json')
for daily_news_dict in news_collection:
    for (id_uni, daily_news) in news_collection[daily_news_dict].items():
        if len(daily_news) > 0:
            for news in daily_news:
                content = news['Content']
                if not content == '':
                    text = texts.to_text(content)
                    news_result.append(to_news_record(id_uni, news))
print(news_result)
json.dumps(news_result, ensure_ascii=False, indent=4)
# with open('test.csv', 'w',encoding='utf-8',newline='') as f:
#     f_csv = csv.writer(f)
#     f_csv.writerows(news_result)
