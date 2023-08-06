from multiprocessing import Queue, Process
import os
import signal
from kordar_task import write_logger


class TaskHandler:

    def __init__(self, work_size=5, queue_buff_len=20):
        # 存放每个MsgId 所对应的处理方法的map属性
        cpu_count = os.cpu_count()
        if work_size > cpu_count:
            work_size = cpu_count

        if cpu_count == 1:
            work_size = 1

        self.__container = {}
        self.__worker_pool_size = work_size
        self.__task_queue_buff_len = queue_buff_len
        self.__task_queue = [Queue(work_size) for _ in range(work_size)]
        self.__pids = []
        self.__msg_id = 0

    def __do_msg_handler(self, body):
        """
        获取处理器，并执行
        :param body:
        :return:
        """
        handler = self.__container.get(body.task_id())
        if handler:
            handler.execute(body)
        else:
            write_logger('kordar_task[%s] is not FOUND!' % body.task_id(), t="warning")

    def start_one_worker(self, q):
        """
        启动一个Worker工作流
        :return:
        """
        while True:
            try:
                # 有消息则取出队列的Request，并执行绑定的业务方法
                body = q.get(True)
                self.__do_msg_handler(body)
            except Exception as e:
                write_logger('except: %s' % e, t="error")

    def start_work_pool(self):
        """
        启动worker工作池
        :return:
        """
        for index in range(self.__worker_pool_size):
            write_logger("Worker ID = %s is started." % index)
            q = self.__task_queue[index]
            p = Process(target=self.start_one_worker, args=(q,))
            p.daemon = True
            p.start()
            self.__pids.append(p.pid)

    def close(self):
        # TODO 直接kill存在风险，后期改动
        print("close processing!!!")
        for pid in self.__pids:
            try:
                os.kill(pid, signal.SIGKILL)
                print('已杀死pid为%s的进程' % pid)
            except OSError as e:
                print('没有如此进程!!!')

    def send(self, body):
        # 得到需要处理此条连接的workerID
        work_id = self.__msg_id % self.__worker_pool_size
        self.__task_queue[work_id].put(body)
        if self.__msg_id > 1000000:
            self.__msg_id = 0
        else:
            self.__msg_id += 1

    def add_task(self, task):
        task_id = task.id()
        if task_id in self.__container:
            raise ValueError('repeated func , taskId =  %s' % task_id)
        # 添加msg与api的绑定关系
        self.__container[task_id] = task
        write_logger("Add func taskId = %s" % task_id)

