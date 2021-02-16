from multiprocessing import Process, Queue, cpu_count

from pyqccapi.task.task_invoker import *

task_queue = Queue()
result_queue = Queue()


def task_producer_proxy(task: AsyncTask):
    task_queue.put(task)


def task_consumer():
    while True:
        task = task_queue.get()
        result_queue.put(ApiInvoker(task).invoke().to_task())


if __name__ == '__main__':
    process_list = []
    for i in range(cpu_count()):
        process_list.append(Process(target=task_consumer, args=()))

    for process in process_list:
        process.start()

    for process in process_list:
        process.join()
