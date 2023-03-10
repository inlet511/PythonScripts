import json
import logging

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from yt_dlp import YoutubeDL
import time

class DownloaderThread(QThread):
    # 信号****************
    # 进度改变, 第一个值是进度，第二个值是url
    progressChanged = pyqtSignal(float,str)


    def __init__(self, urls, save_path, cores):
        super().__init__()
        self.urls = urls
        self.save_path = save_path
        self.cores = cores

    def run(self):
        try:
            ydl_opts = {
                'outtmpl': self.save_path + '/%(title)s.%(ext)s',
                'progress_hooks': [self.progress_hook],
                'concurrent-fragments': self.cores
            }
            with YoutubeDL(ydl_opts) as ydl:
                print("downloading urls:{}".format(self.urls))
                ydl.download(self.urls)
        except Exception as e:
            logging.WARNING("下载时出现错误", e)

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            progress = d['_percent_str']
            self.progressChanged.emit(float(progress[:-1]), d['info_dict']['original_url'])
        elif d['status'] == 'finished':
            # 一个任务可能多次出发finished, 这里传出事件无意义
            pass

class RequestInfoThread(QThread):

    # 信号第一个参数是字典类型，第二个参数是整型，表示行数
    receivedInfo = pyqtSignal(dict, int)

    def __init__(self, in_buffer):
        super().__init__()
        self.buffer = in_buffer
        self.shouldExit = False

    def stop(self):
        self.shouldExit = True

    def run(self):
        ydl_opts = {}
        try:
            with YoutubeDL(ydl_opts) as ydl:
                while not self.shouldExit: # 始终循环
                    # 下面这个get()可能因为队列为空而阻塞，这是设计目的
                    item_info = self.buffer.get()
                    info = ydl.extract_info(item_info.get('url'), download=False)
                    info = ydl.sanitize_info(info)
                    if info is None:
                        print("获取信息失败")
                    else:
                        size_mb = info.get('filesize_approx')/1048576
                        size_str = '{:.2f} MB'.format(size_mb)
                        info_dict = {'title': info.get("title"),'filesize': size_str}

                        self.receivedInfo.emit(info_dict, item_info.get('row'))
        except Exception as ex:
            print('获取视频信息时发生错误. {}'.format(ex))

