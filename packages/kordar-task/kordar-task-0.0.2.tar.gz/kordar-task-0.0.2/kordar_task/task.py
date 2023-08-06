from abc import ABCMeta, abstractmethod
from kordar_task import write_logger


class ibody(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def task_id(self):
        """
        设置body对应的taskId，程序根据该id获取task处理器
        :return:
        """
        return "0"


class itask(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def id(self):
        """
        taskId
        :return:
        """
        return "0"

    @abstractmethod
    def execute(self, body):
        """
        执行task任务逻辑
        :param body: ibody
        :return:
        """
        pass


class DefaultBody(ibody):
    def task_id(self):
        return "default-kordar_task"


class DefaultTask(itask):
    def id(self):
        return "default-kordar_task"

    def execute(self, body):
        write_logger("defaultTask, name = %s" % body.task_id())
