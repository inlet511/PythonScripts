from PyQt5.QtCore import QMutex, QWaitCondition


class RequestInfoBuffer:
    def __init__(self):
        self.request_info_queue=[]
        self.mutex = QMutex()
        self.notEmpty = QWaitCondition()

    def put(self, item):
        self.mutex.lock()
        self.request_info_queue.insert(0, item)
        self.notEmpty.wakeOne()
        self.mutex.unlock()

    def get(self):
        self.mutex.lock()
        while len(self.request_info_queue) == 0:
            self.notEmpty.wait(self.mutex)
        item = self.request_info_queue.pop()
        self.mutex.unlock()
        return item