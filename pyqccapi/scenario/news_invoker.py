from multiprocessing import Pool, cpu_count

from pyqccapi.invoker.api_invoker import ApiInvoker, Task, TaskType
from pyqccapi.constant import news_category


class NewsTask(Task):
    def __init__(self, method, params):
        Task.__init__(self, method, params)
        self.type = TaskType.NEWS


class NewsInvoker:

    def __init__(self,
                 config_path: str,
                 news_task: NewsTask):
        self.config_path = config_path
        self.news_task = news_task
        self.id_uni = news_task.params['id_uni']
        self.dt = news_task.params['dt']

    def to_api_invoker(self, task):
        return ApiInvoker(self.config_path, task)

    def invoke(self):
        return self.to_news_detail_list()

    def to_news_detail(self, id_news: str):
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
        return self.to_api_invoker(task).invoke().to_task()

    def to_news_detail_by_summary(self, news: dict):
        """
        根据新闻摘要，填充新闻内容
        :param news:新闻摘要字典
        :return:填充内容后的完整新闻内容，如果调用失败则不填充
        """
        t = self.to_news_detail(news['NewsId'])
        if t.success:
            news['Content'] = t.data['Result']['Content']
        return news

    def to_news_summary_list(self):
        method_id = '3a5dd06b-aec5-445d-9b91-82be4d5b884b'
        page_size = 50
        summary_list = []

        params = {
            'searchKey': self.id_uni,
            'startDate': self.dt,
            'endDate': self.dt,
            'pageSize': page_size,
            'pageIndex': 1
        }
        task = Task(method_id, params)
        t = self.to_api_invoker(task).invoke().to_task()

        if t.success:
            total = t.data['Paging']['TotalRecords']
        else:
            self.news_task.code = t.code
            self.news_task.message = t.message
            return summary_list

        page_count = total // page_size + 1

        for i in range(page_count + 1)[1:]:
            params['pageIndex'] = i
            task = Task(method_id, params)
            t = self.to_api_invoker(task).invoke().to_task()
            if t.success:
                for summary in t.data['Result']:
                    category_names = []
                    category_list = str(summary['Category']).split(',')
                    for category in category_list:
                        category_names.append(news_category.get(category, ''))
                    summary['CategoryName'] = ','.join(category_names)
                    summary_list.append(summary)

        return summary_list

    def to_news_detail_list_parallel(self):
        """
        一个容忍失败的版本，适合调用且只调用一次的场景
        :return:
        """
        try:
            future_list = []
            news_list = []
            pool_size = cpu_count()
            pool = Pool(pool_size)

            summary_list = self.to_news_summary_list()
            for summary in summary_list:
                future_list.append(pool.apply_async(func=self.to_news_detail_by_summary, args=(summary,)))
            pool.close()
            pool.join()

            for future in future_list:
                news_list.append(future.get())

            self.news_task.data = news_list
            self.news_task.success = True


        except Exception as ignored:
            print(str(ignored))

        return self

    def to_news_detail_list(self):
        """
        一个容忍失败的版本，适合调用且只调用一次的场景
        :return:
        """
        try:
            news_list = []

            summary_list = self.to_news_summary_list()
            if len(summary_list) == 0:
                return self
            for summary in summary_list:
                news_list.append(self.to_news_detail_by_summary(summary))

            self.news_task.data = news_list
            self.news_task.success = True
            self.news_task.code = 200

        except Exception as ignored:
            print(str(ignored))

        return self

    def to_task(self):
        return self.news_task
