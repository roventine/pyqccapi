import json

from pyqccapi.api_invoker import ApiInvoker, Task
from pyqccapi.news_invoker import NewsInvoker, NewsTask
import datetime

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


def to_daily_news_collection(d):
    daily_news = []
    for k, v in uni_id_map.items():
        news_task = NewsTask(method='',
                             params={
                                 'id_uni': v,
                                 'dt': d
                             })
        news_task = NewsInvoker(config_path='../config.yaml',
                                news_task=news_task).invoke().to_task()
        if news_task.code == 200:
            daily_news.append(news_task)
    return daily_news


def to_days_diff(start, end):
    dt_start = datetime.datetime.strptime(start, '%Y%m%d')
    dt_end = datetime.datetime.strptime(end, '%Y%m%d')
    diff = dt_end - dt_start
    return diff.days


def to_date_after(base, days):
    dt_base = datetime.datetime.strptime(base, '%Y%m%d')
    dt_after = dt_base + datetime.timedelta(days=days)
    return dt_after.strftime('%Y%m%d')


def to_period_news_collection(start, end):
    period_news = {}
    days_diff = to_days_diff(start, end)
    for i in range(days_diff):
        date_after = to_date_after(start, i)
        period_news[date_after] = to_daily_news_collection(date_after)
    return period_news


class NewsTaskEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, NewsTask):
            return {
                'method': obj.method,
                'params': obj.params,
                'success': obj.success,
                'code': obj.code,
                'message': obj.message,
                'data': obj.data,
                'type': obj.type.value
            }
        return json.JSONEncoder.default(self, obj)


s = to_period_news_collection('20200101', '20201231')
with open('news_collection_20200101_20201231.json', 'w', encoding='utf-8') as f:
    json.dump(s, f, ensure_ascii=False, indent=4, cls=NewsTaskEncoder)
